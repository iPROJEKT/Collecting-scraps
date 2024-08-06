import os
import asyncio
import copy
from datetime import datetime, timedelta

from aiogoogle import Aiogoogle
from aiohttp import web

from bot.core import const
from bot.crud.crud import get_all_incident, create_url, get_all_observations, get_user_by_id, get_all_maintenance
from bot.google_sheets.google_client import get_service


async def get_spreadsheet_body(
        locale: str = const.LOCALE,
        sheet_type: str = const.SHEERTYPE,
        sheet_id: int = const.SHEERTID,
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
    for sheet in body['sheets']:
        sheet['properties']['sheetType'] = sheet_type
        sheet['properties']['sheetId'] = sheet_id
        sheet['properties']['gridProperties']['rowCount'] = row_count
        sheet['properties']['gridProperties']['columnCount'] = column_count
    return body


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    service = await wrapper_services.discover('sheets', 'v4')
    body = await get_spreadsheet_body()
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=body)
    )
    spreadsheet_id = response['spreadsheetId']
    await create_url(str(spreadsheet_id))
    return spreadsheet_id


async def set_user_permissions(spreadsheet_id: str, wrapper_services: Aiogoogle) -> None:
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
        data: list,
        wrapper_services: Aiogoogle,
        sheet_title: str,
) -> None:
    table = [[const.A1, datetime.now().strftime(const.FORMAT)]]
    service = await wrapper_services.discover('sheets', 'v4')

    if sheet_title == "Дефекты":
        for item in data:
            new_row = [
                str(item.number_robot),
                str(item.incident),
                str(item.name_user),
                str(item.comment),
                str(item.name_main_programm),
                str(item.coord),
                str(item.datatime),
            ]
            table.append(new_row)

    elif sheet_title == "Наблюдения":
        for item in data:
            user = await get_user_by_id(item.user_id)
            new_row = [
                str(item.id_robot),
                str(user.name),
                str(user.surname),
                str(item.comment),
            ]
            table.append(new_row)

    elif sheet_title == "Обслуживаниие":
        for item in data:
            new_row = [
                str(item.datatime),
                str(item.last_updata_men),
                str(item.last_updata_men_sur),
                str(item.whot_swap),
                str(item.wire_mark),
                str(item.wire_diameter),
                str(item.name_gaz),
                str(item.robot_id),
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
            range=f"{sheet_title}!{const.RANGE}",
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )


async def create_sheets(spreadsheet_id: str, wrapper_services: Aiogoogle) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    requests = [
        {
            "addSheet": {
                "properties": {
                    "title": "Дефекты",
                    "sheetType": const.SHEERTYPE,
                    "gridProperties": {
                        "rowCount": const.ROW_COUNT,
                        "columnCount": const.COLUMN_COUNT
                    }
                }
            }
        },
        {
            "addSheet": {
                "properties": {
                    "title": "Наблюдения",
                    "sheetType": const.SHEERTYPE,
                    "gridProperties": {
                        "rowCount": const.ROW_COUNT,
                        "columnCount": const.COLUMN_COUNT
                    }
                }
            }
        },
        {
            "addSheet": {
                "properties": {
                    "title": "Обслуживаниие",
                    "sheetType": const.SHEERTYPE,
                    "gridProperties": {
                        "rowCount": const.ROW_COUNT,
                        "columnCount": const.COLUMN_COUNT
                    }
                }
            }
        },
        {
            "deleteSheet": {
                "sheetId": 0
            }
        }
    ]
    batch_update_request_body = {
        'requests': requests
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.batchUpdate(
            spreadsheetId=spreadsheet_id,
            json=batch_update_request_body
        )
    )


async def scheduled_update(wrapper_services: Aiogoogle, last_run_date: datetime):
    while True:
        today = datetime.now().date()
        if today > last_run_date:
            print(f"Creating a new spreadsheet for {today}")
            last_run_date = today
            spreadsheet_id = await spreadsheets_create(wrapper_services)
            await create_sheets(spreadsheet_id, wrapper_services)
            await set_user_permissions(spreadsheet_id, wrapper_services)

        incidents = await get_all_incident()
        all_observations = await get_all_observations()
        maintenance = await get_all_maintenance()

        if not incidents:
            print("No Дефекты found.")
        else:
            print(f"Updating Incidents sheet with {len(incidents)} Дефекты.")
        await spreadsheets_update_value(spreadsheet_id, incidents, wrapper_services, "Дефекты")

        if not all_observations:
            print("No Наблюдения found.")
        else:
            print(f"Updating Наблюдения sheet with {len(all_observations)} Наблюдения.")
        await spreadsheets_update_value(spreadsheet_id, all_observations, wrapper_services, "Наблюдения")

        if not maintenance:
            print("No Обслуживание found.")
        else:
            print(f"Updating Обслуживание sheet with {len(maintenance)} Обслуживаниие.")
        await spreadsheets_update_value(spreadsheet_id, maintenance, wrapper_services, "Обслуживаниие")

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