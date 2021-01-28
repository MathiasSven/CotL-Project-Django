import configparser
import gspread
from pathlib import Path

import requests
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timezone, timedelta
from celery import shared_task

from .serializer import call_api
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

    def create_activity_instance(minutessinceactive):
        active_datetime = data_get_datetime - timedelta(minutes=minutessinceactive)
        Activity.objects.create(active_datetime=active_datetime)

    for nation in data['nations']:
        nation.pop('alliance', None)
        nation_object, _ = Nation.objects.get_or_create(nationid=nation['nationid'])

        if nation_object.minutessinceactive is None:
            create_activity_instance(nation['minutessinceactive'])
        elif nation_object.minutessinceactive > nation['minutessinceactive']:
            create_activity_instance(nation['minutessinceactive'])

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
    # Deletes ex-members
    AllianceMember.objects.exclude(nation_id__in=[nation['nationid'] for nation in data['nations']]).delete()


@shared_task()
def push_to_sheets():
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(f"{BASE_DIR}/credentials.json", scope)
    client = gspread.authorize(credentials)

    sheet = client.open_by_key(config.get("googlesheets", "SHEET_KEY"))
    data_dump_worksheet_name = config.get("googlesheets", "DATA_DUMP_NAME")
    data_dump_worksheet = sheet.worksheet(data_dump_worksheet_name)

    sheet.values_clear(f"{data_dump_worksheet_name}!A2:{gspread.utils.rowcol_to_a1(100, 29)}")

    members = []
    for alliance_member_object in AllianceMember.objects.all():
        members.append([
            alliance_member_object.nation.nation,
            f"https://politicsandwar.com/nation/id={alliance_member_object.nation.nationid}",
            alliance_member_object.nation.nationid,
            alliance_member_object.nation.leader,
            alliance_member_object.nation.cities,
            alliance_member_object.nation.score,
            alliance_member_object.nation.minutessinceactive,
            alliance_member_object.cityprojecttimerturns,
            alliance_member_object.nation.infrastructure,
            alliance_member_object.nation.nationmilitary.soldiers,
            alliance_member_object.nation.nationmilitary.tanks,
            alliance_member_object.nation.nationmilitary.aircraft,
            alliance_member_object.nation.nationmilitary.ships,
            alliance_member_object.nation.nationmilitary.missiles,
            alliance_member_object.nation.nationmilitary.nukes,
        ])
    update_range = f"A2:{gspread.utils.rowcol_to_a1(len(members) + 1, 18)}"
    print(len(members))
    data_dump_worksheet.batch_update([{
        'range': update_range,
        'values': members,
    }])


@shared_task()
def changeup():
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(f"{BASE_DIR}/credentials.json", scope)
    client = gspread.authorize(credentials)

    sheet = client.open_by_key('1mZuzUY6A5Day38gkTbuxeGiNyRf3v3eFJvX0fmSFBvQ')
    data_dump_worksheet_name = 'Data Dump'
    data_dump_worksheet = sheet.worksheet(data_dump_worksheet_name)

    sheet.values_clear(f"{data_dump_worksheet_name}!A2:{gspread.utils.rowcol_to_a1(100, 29)}")

    members = []
    for alliance_member_object in AllianceMember.objects.all():
        members.append([
            alliance_member_object.nation.nation,
            f"https://politicsandwar.com/nation/id={alliance_member_object.nation.nationid}",
            alliance_member_object.nation.nationid,
            alliance_member_object.nation.leader,
            alliance_member_object.nation.cities,
            alliance_member_object.nation.score,
            alliance_member_object.nation.minutessinceactive,
            alliance_member_object.cityprojecttimerturns,
            alliance_member_object.nation.infrastructure,
            alliance_member_object.nation.nationmilitary.soldiers,
            alliance_member_object.nation.nationmilitary.tanks,
            alliance_member_object.nation.nationmilitary.aircraft,
            alliance_member_object.nation.nationmilitary.ships,
            alliance_member_object.nation.nationmilitary.missiles,
            alliance_member_object.nation.nationmilitary.nukes,
        ])
    update_range = f"A2:{gspread.utils.rowcol_to_a1(len(members) + 1, 18)}"
    print(len(members))
    data_dump_worksheet.batch_update([{
        'range': update_range,
        'values': members,
    }])
