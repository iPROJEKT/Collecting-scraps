import copy
from datetime import datetime, timedelta
import asyncio
from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds
from aiohttp import web

from bot.core.config import settings
from bot.crud.crud import get_all_incident, create_url
from bot.core import const


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
        'emailAddress': settings.email
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


async def read_values(service, spreadsheetId):
    response = await service.spreadsheets.values.get(
        spreadsheetId=spreadsheetId,
        range=const.RANGE
    )
    return response['values']


async def spreadsheet_update_values(service, spreadsheetId, data):
    table_values = await read_values(service, spreadsheetId)
    table_values.append(list(map(str.strip, data.split(','))))
    request_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    request = service.spreadsheets.values.update(
        spreadsheetId=spreadsheetId,
        range="A1:E30",
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

        incidents = await get_all_incident()  # Получаем все инциденты
        if not incidents:
            print("No incidents found.")
        else:
            print(f"Updating spreadsheet with {len(incidents)} incidents.")
        await spreadsheets_update_value(spreadsheet_id, incidents, wrapper_services)
        await asyncio.sleep(6)  # Спать 24 часа


async def init_app():
    app = web.Application()

    # Создаем экземпляр Aiogoogle и используем его
    service = get_service()
    async with Aiogoogle(service_account_creds=service) as wrapper_services:
        # Начальная дата - вчера, чтобы сразу создать новый файл
        last_run_date = datetime.now().date() - timedelta(days=1)
        await asyncio.create_task(scheduled_update(wrapper_services, last_run_date))

    return app


def get_service():
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    INFO = {
        'type': settings.type,
        'project_id': settings.project_id,
        'private_key_id': settings.private_key_id,
        'private_key': settings.private_key.replace('\\n', '\n'),
        'client_email': settings.client_email,
        'client_id': settings.client_id,
        'auth_uri': settings.auth_uri,
        'token_uri': settings.token_uri,
        'auth_provider_x509_cert_url': settings.auth_provider_x509_cert_url,
        'client_x509_cert_url': settings.client_x509_cert_url
    }

    return ServiceAccountCreds(scopes=SCOPES, **INFO)


if __name__ == '__main__':
    web.run_app(init_app())
