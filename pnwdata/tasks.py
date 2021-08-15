from django.core.exceptions import ValidationError

from oauth2client.service_account import ServiceAccountCredentials

import configparser
import gspread
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
from celery import shared_task
from pathlib import Path

from typing import Literal, overload

from .caller import call_api
from .models import *

BASE_DIR = Path(__file__).resolve().parent.parent
config = configparser.ConfigParser()
config.read(f"{BASE_DIR}/config.ini")


def endpoint_url(endpoint, args=''):
    return f"http://politicsandwar.com/api/{endpoint}/{args}{'&' if args else '?'}key={config.get('pnw', 'API_KEY')}"


@shared_task()
def get_nation(nation_id: int) -> object:
    url = endpoint_url('nation', f'id={nation_id}')
    data = call_api(url)
    return data


@shared_task()
def send_message(nation_id: int, subject: str, message: str):
    url = 'https://politicsandwar.com/api/send-message/'
    response = requests.post(url, {'key': str(config.get('pnw', 'API_KEY')), 'to': nation_id, 'subject': subject, 'message': message})
    return response.text


@shared_task()
def get_transaction(nation_id: int, min_lookup_date: datetime.date, identifier_type: Literal['NOTE', 'TX_ID'], identifier: int) -> dict:
    import re
    min_date = min_lookup_date.strftime(format='%Y%m%d')
    url = f"https://politicsandwar.com/api/v2/nation-bank-recs/{config.get('pnw', 'API_KEY')}/&nation_id={nation_id}&min_tx_date={min_date}&format=1"
    data = call_api(url)
    if not data['data']:
        return None
    else:
        regex = re.compile(r'[A-Z]+ (?P<identifier>\d{4,})')
        for transaction in data['data']:
            if identifier_type == 'NOTE':
                match = regex.match(transaction['note'])
                if match:
                    if match['identifier'] == str(identifier):
                        return transaction
            elif identifier_type == 'TX_ID':
                if transaction['tx_id'] == identifier:
                    return transaction
            else:
                return
    return


@shared_task()
def update_alliances():
    url = endpoint_url('alliances')
    data = call_api(url)
    for alliance in data['alliances']:
        alliance['founddate'] = datetime.strptime(alliance.pop('founddate'), '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
        alliance_object, _ = Alliance.objects.update_or_create(
            id=alliance['id'], defaults=filter_kwargs(Alliance, alliance)
        )


@shared_task()
def update_nations():
    url = endpoint_url('nations')
    data = call_api(url)
    for nation in data['nations']:
        alliance_object, _ = Alliance.objects.get_or_create(id=nation['allianceid'])
        nation['alliance'] = alliance_object
        nation_object, _ = Nation.objects.update_or_create(
            nationid=nation['nationid'], defaults=filter_kwargs(Nation, nation)
        )


@shared_task()
def update_banks():
    banks_to_update = {'alliance': {'id': config.get('pnw', 'ALLIANCE_ID'), 'key': config.get('pnw', 'API_KEY')},
                       'offshore': {'id': config.get('pnw', 'OFFSHORE_ID'), 'key': config.get('pnw', 'OFFSHORE_KEY')}}
    for bank in banks_to_update.values():
        url = f"http://politicsandwar.com/api/alliance-bank/?allianceid={bank['id']}&key={bank['key']}"
        data = call_api(url)
        contents = data["alliance_bank_contents"][0]
        alliance_object, _ = Alliance.objects.get_or_create(id=contents['alliance_id'])
        bank_object, _ = Bank.objects.update_or_create(
            alliance=alliance_object, defaults=filter_kwargs(Bank, contents)
        )


@shared_task()
def update_alliance_members():
    url = endpoint_url('alliance-members', f"?allianceid={config.get('pnw', 'ALLIANCE_ID')}")
    data = call_api(url)

    data_get_datetime = datetime.now(timezone.utc)

    def create_activity_instance(minutessinceactive, _alliance_member_object):
        active_datetime = data_get_datetime - timedelta(minutes=minutessinceactive)
        Activity.objects.create(nation=_alliance_member_object, active_datetime=active_datetime)

    for nation in data['nations']:
        nation.pop('alliance', None)
        nation_object, _ = Nation.objects.get_or_create(nationid=nation['nationid'])

        previous_minutessinceactive = nation_object.minutessinceactive

        nation_object.__dict__.update(filter_kwargs(Nation, nation))
        alliance, _ = Alliance.objects.get_or_create(id=nation['allianceid'])
        nation_object.alliance = alliance
        nation_object.save()

        nation.pop('nation', None)

        alliance_member_object, _ = AllianceMember.objects.update_or_create(
            nation=nation_object, defaults=filter_kwargs(AllianceMember, nation)
        )
        projects_object, _ = Projects.objects.update_or_create(
            nation=nation_object, defaults=filter_kwargs(Projects, nation)
        )
        military_object, _ = NationMilitary.objects.update_or_create(
            nation=nation_object, defaults=filter_kwargs(NationMilitary, nation)
        )

        if previous_minutessinceactive is None:
            create_activity_instance(nation['minutessinceactive'], alliance_member_object)
        elif previous_minutessinceactive > nation['minutessinceactive']:
            create_activity_instance(nation['minutessinceactive'], alliance_member_object)

    # Deletes ex-members
    AllianceMember.objects.exclude(nation_id__in=[nation['nationid'] for nation in data['nations']]).delete()


@shared_task()
def update_tax_records(records=500):
    login_payload = {
        'email': config.get('pnw', 'EMAIL'),
        'password': config.get('pnw', 'PASSWORD'),
        'loginform': 'login'
    }
    with requests.Session() as s:
        s.post('https://politicsandwar.com/login/', data=login_payload, headers={'User-Agent': 'Mozilla/5.0'})
        for page in range((records + 100) // 100):
            bank_taxes_page = BeautifulSoup(s.post('https://politicsandwar.com/alliance/id=7452&display=banktaxes', data={'maximum': page * 100 + 100, 'minimum': page * 100, 'search': 'Go'}).text, 'html.parser')
            table = bank_taxes_page.find('table', {"class": "nationtable"})
            rows = table.find_all('tr')

            for row in rows[1:-1]:
                cols = row.find_all('td')
                nationid = cols[2].a['href'].split('id=')[1]

                nation_object, _ = Nation.objects.get_or_create(nationid=nationid)
                date = datetime.strptime(cols[1].text.strip(), '%m/%d/%Y %I:%M %p').replace(tzinfo=timezone.utc)

                tax_record_object = TaxRecord(nation=nation_object, date=date, note=cols[1].img['title'], tax_id=cols[16].text.strip(),
                                              money=cols[4].text.strip().replace(',', '')[1:],
                                              food=cols[5].text.strip().replace(',', ''),
                                              coal=cols[6].text.strip().replace(',', ''),
                                              oil=cols[7].text.strip().replace(',', ''),
                                              uranium=cols[8].text.strip().replace(',', ''),
                                              lead=cols[9].text.strip().replace(',', ''),
                                              iron=cols[10].text.strip().replace(',', ''),
                                              bauxite=cols[11].text.strip().replace(',', ''),
                                              gasoline=cols[12].text.strip().replace(',', ''),
                                              munitions=cols[13].text.strip().replace(',', ''),
                                              steel=cols[14].text.strip().replace(',', ''),
                                              aluminum=cols[15].text.strip().replace(',', ''),
                                              )
                try:
                    tax_record_object.validate_unique()
                except ValidationError:
                    break
                else:
                    tax_record_object.save()


@shared_task()
def update_trade_records(records=5000):
    url = endpoint_url('trade-history', f"?records={records}")
    data = call_api(url)

    resource_market = {f"{resource[0]}": Market.objects.get(pk=resource[0]) for resource in Market.RESOURCE_TYPE}

    repeated_records = 0
    existing_trade_records = Trade.objects.all().order_by('-trade_id').values_list('trade_id', flat=True)
    for trade in data['trades']:
        if int(trade['trade_id']) in existing_trade_records:
            repeated_records += 1
            continue
        offerer_nation_object, _ = Nation.objects.get_or_create(nationid=trade.pop('offerer_nation_id'))
        accepter_nation_object, _ = Nation.objects.get_or_create(nationid=trade.pop('accepter_nation_id'))

        Trade.objects.create(date=datetime.strptime(trade.pop('date'), '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc),
                             offerer_nation=offerer_nation_object, accepter_nation=accepter_nation_object,
                             market=resource_market[trade.pop('resource')], **trade)

    return repeated_records


@shared_task()
def update_market():
    for resource in Market.RESOURCE_TYPE:
        resource = resource[0]
        url = endpoint_url('tradeprice', f"?resource={resource}")
        data = call_api(url)

        Market.objects.filter(resource=resource).update(avgprice=data['avgprice'], marketindex=data['marketindex'].replace(",", ""))


@shared_task()
def alliance_member_to_sheets(sheet_id: str, worksheet_name: str, fields: list):
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(f"{BASE_DIR}/credentials.json", scope)
    client = gspread.authorize(credentials)

    sheet = client.open_by_key(sheet_id)
    data_dump_worksheet_name = worksheet_name
    data_dump_worksheet = sheet.worksheet(data_dump_worksheet_name)

    from django.db.models import Model
    alliance_members = AllianceMember.objects.all()

    members = [fields]
    for alliance_member_object in alliance_members:
        row_list = []
        for field in fields:
            field_lookup = field.split(".")
            instance_lookup = alliance_member_object
            attribute = None
            for lookup in field_lookup:
                attribute = getattr(instance_lookup, lookup)
                if isinstance(attribute, Model):
                    instance_lookup = attribute
            row_list.append(attribute)
        members.append(row_list)

    sheet.values_clear(f"{data_dump_worksheet_name}!A1:{gspread.utils.rowcol_to_a1(150, 30)}")

    update_range = f"A1:{gspread.utils.rowcol_to_a1(len(members) + 2, len(fields))}"
    data_dump_worksheet.batch_update([{
        'range': update_range,
        'values': members,
    }])
