from querystar.client import _client_connection
import logging

logger = logging.getLogger("querystar")


def add_row(spreadsheet_id: str,
            worksheet_id: int,
            data: list):
    """
    spreadsheet_id: spreadsheet_id
    worksheet_id: worksheet_id
    data: a list of data to append to the worksheet. 
          Multi data type support. E.g. ["Data", 123.45, true, "=MAX(D2:D4)", "10"]


    Google API reference: https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/append
    Request: 
        POST https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}/values/{range}:append

    Path parameters:
        spreadsheetId = spreadsheet_id
        range = worksheet_id (in A1 notation: https://developers.google.com/sheets/api/guides/concepts#expandable-1)

    Default query parameters:
        valueInputOption="RAW"
        InsertDataOption="INSERT_ROWS"
        includeValuesInResponse=True

    scope: https://www.googleapis.com/auth/spreadsheets

    Return example:
        {
                "spreadsheetId": string,
                "tableRange": string,
                "updates": {
                object (UpdateValuesResponse)
                }
        }
    """
    logger.info('Started ACTION - google_sheets.add_row')
    payload = {'spreadsheet_id': spreadsheet_id,
               'worksheet_id': worksheet_id,
               'data': data}

    data = _client_connection.fire(integration='sheets',
                                   event='add_row',
                                   payload=payload)

    logger.info('Finished ACTION - google_sheets.add_row')
    return data
