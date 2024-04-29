from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

TIME_FORMAT = '%Y/%m/%d %H:%M:%S'

SPREADSHEET_TEMPLATE = {
    'properties': {'title': None,
                   'locale': 'ru_RU'},
    'sheets': [{'properties': {'sheetType': 'GRID',
                               'sheetId': 0,
                               'title': 'Лист1',
                               'gridProperties': {'rowCount': 100,
                                                  'columnCount': 11}}}]
}

HEADER_TABLE_VALUE = [
    ['Отчёт от', None],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]


async def spreadsheets_create(wrapper_services: Aiogoogle,
                              title_date: str = None) -> str:
    now = title_date or datetime.now().strftime(TIME_FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')

    spreadsheet_body = SPREADSHEET_TEMPLATE.copy()
    spreadsheet_body['properties']['title'] = f'Отчёт от {now}'

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}

    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    now = datetime.now().strftime(TIME_FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')

    header_table = HEADER_TABLE_VALUE.copy()
    header_table[0] = ['Отчёт от', now]
    table_values = [
        *header_table,
        *[list(map(str, [project['name'],
                         str(project['close_date'] - project['create_date']),
                         project['description']])) for project in
          projects[::-1]]
    ]

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }

    num_rows = len(table_values)
    num_cols = len(table_values[0]) if table_values else 0
    end_cell = chr(ord('A') + num_cols - 1) + str(num_rows)

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'A1:{end_cell}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
