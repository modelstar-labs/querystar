import querystar as qs

channel_id = "..."  # add your own Slack channel ID

data = qs.triggers.slack.new_message(channel_id=channel_id,
                                     trigger_string='kudos')

qs.actions.slack.add_message(channel_id=channel_id,
                             text="Thanks for sending the kudo")

qs.actions.google_sheets.add_row(
    spreadsheet_id='...',   # add your own Google spreadsheet_ID
    worksheet_id='Sheet1',
    data=[[data['user'], data['text']]]
)