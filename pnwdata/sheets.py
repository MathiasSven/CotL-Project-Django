from oauth2client.service_account import ServiceAccountCredentials
from celery import shared_task

import configparser
import gspread
from pathlib import Path

from .models import AllianceMember

BASE_DIR = Path(__file__).resolve().parent.parent
config = configparser.ConfigParser()
config.read(f"{BASE_DIR}/config.ini")


# noinspection DuplicatedCode
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


# noinspection DuplicatedCode
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
