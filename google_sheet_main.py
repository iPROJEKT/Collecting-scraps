import os
import asyncio
import copy
from datetime import datetime, timedelta

from aiogoogle import Aiogoogle
from aiohttp import web

from bot.core import const
from bot.google_sheets.google_client import get_service
from bot.crud.crud import get_all_incident, create_url


async def get_spreadsheet_body(
        locale: str = const.LOCALE,
        sheet_type: str = const.SHEERTYPE,
        sheet_id: int = const.SHEERTID,
        title: str = const.SHEET_TITLE,
        row_count: int = const.ROW_COUNT,
        column_count: int = const.COLUMN_COUNT,
        body: dict = const.SPREADSHEET_BODY
) -> dict:
    body['properties']['title'] = const.SPREADSHEET_TITLE.format(
        datetime.now().strftime(
            const.FORMAT
        )
    )
    body['properties']['locale'] = locale
    body['sheets'][0]['properties']['sheetType'] = sheet_type
    body['sheets'][0]['properties']['sheetId'] = sheet_id
    body['sheets'][0]['properties']['title'] = title.format(
        datetime.now().strftime(
            const.FORMAT
        )
    )
    body['sheets'][0]['properties']['gridProperties']['rowCount'] = row_count
    body['sheets'][0]['properties']['gridProperties']['columnCount'] = column_count
    return body


async def spreadsheets_create(
        wrapper_services: Aiogoogle
) -> str:
    service = await wrapper_services.discover('sheets', 'v4')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=await get_spreadsheet_body())
    )
    spreadsheet_id = response['spreadsheetId']
    await create_url(str(spreadsheet_id))
    return spreadsheet_id


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {
        'type': const.TYPE,
        'role': const.ROLE,
    }
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields=const.FILDS_FOR_SERVIS_ACCOUNT
        )
    )


async def spreadsheets_update_value(
        spreadsheet_id: str,
        ins: list,
        wrapper_services: Aiogoogle
) -> None:
    table = copy.deepcopy(const.TABLE_VALUES)
    table[0] = [const.A1, datetime.now().strftime(const.FORMAT)]
    service = await wrapper_services.discover('sheets', 'v4')
    for inst in ins:
        new_row = [
            str(inst.number_robot),
            str(inst.incident),
            str(inst.name_user),
            str(inst.comment),
            str(inst.name_main_programm),
            str(inst.coord),
            str(inst.datatime),
        ]
        table.append(new_row)
    update_body = {
        'majorDimension': const.TABLE_UPDATA,
        'values': table
    }
    if len(table) > const.ROW_COUNT:
        raise ValueError(const.ROW_COUNT_ERROR)
    if len(table[0]) > const.COLUMN_COUNT:
        raise ValueError(const.COLUMN_COUNT_ERROR)
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=const.RANGE,
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )


async def read_values(service, spreadsheet_id):
    response = await service.spreadsheets.values.get(
        spreadsheetId=spreadsheet_id,
        range=const.RANGE
    )
    return response['values']


async def spreadsheet_update_values(service, spreadsheet_id, data):
    table_values = await read_values(service, spreadsheet_id)
    table_values.append(list(map(str.strip, data.split(','))))
    request_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    request = service.spreadsheets.values.update(
        spreadsheetId=spreadsheet_id,
        range=const.RANGE,
        valueInputOption="USER_ENTERED",
        json=request_body
    )
    await request.execute()


async def scheduled_update(wrapper_services: Aiogoogle, last_run_date: datetime):
    while True:
        today = datetime.now().date()
        if today > last_run_date:
            print(f"Creating a new spreadsheet for {today}")
            last_run_date = today
            spreadsheet_id = await spreadsheets_create(wrapper_services)
            await set_user_permissions(spreadsheet_id, wrapper_services)

        incidents = await get_all_incident()
        if not incidents:
            print("No incidents found.")
        else:
            print(f"Updating spreadsheet with {len(incidents)} incidents.")
        await spreadsheets_update_value(spreadsheet_id, incidents, wrapper_services)
        await asyncio.sleep(20)
        os.system('cls' if os.name == 'nt' else 'clear')


async def init_app():
    app = web.Application()
    service = get_service()
    async with Aiogoogle(service_account_creds=service) as wrapper_services:
        last_run_date = datetime.now().date() - timedelta(days=1)
        await asyncio.create_task(scheduled_update(wrapper_services, last_run_date))

    return app


if __name__ == '__main__':
    web.run_app(init_app())
