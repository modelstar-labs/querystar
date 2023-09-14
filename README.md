# 👋 Hi there, this is <a href="https://querystar.io/" style="color: #AF3BEA;"><img src="./assets/logo.png" height="28"> QueryStar</a> 

### Python-First Solution to Develop Bots

QueryStar lets you easily set up triggers and actions to automate workflows.

<img src="https://raw.githubusercontent.com/modelstar-labs/querystar/main/assets/diagram.png" alt="Slack-GSheets Automation" width=500 href="none"></img>

Something like 

> Saving Slack new messages that must contain 'hello' to a Google sheet

can be easily done:
```python
# bot.py
import querystar as qs

data = qs.triggers.slack.new_message(channel_id='MyChannelID',
                                     trigger_string='hello')

qs.actions.slack.new_message(
    spreadsheet_id='MySheetID',
    worksheet_id='Sheet1',
    data=[[data['user'], data['text']]])
```

QueryStar can help you:
- automate workflows
- develop Slack bots
- integrate SaaS data to your own apps
- run background jobs
- schedule tasks
- ...

<img src="https://raw.githubusercontent.com/modelstar-labs/querystar/readme/assets/readme-demo-short.gif" alt="Slack-GSheets Automation" width=500 href="none"></img>

## Get Started

### Installation

```
pip install querystar
```

### Setup Slack (or other apps) Connection 

This step takes 3-5 mins:
- Crete a free account at [querystar.io](https://querystar.io)
- Add any SaaS tools that you want to automate in your QueryStar workspace. (Head over to [quickstart](https://querystar.io/docs/quickstart/token/#step-2-connect-to-slack) in our docs for instructions.)
- Get a QueryStar token. ([Instruction](https://querystar.io/docs/quickstart/token/#step-3-get-querystar-token))
- Add the token as an environment variable on your dev machine.

> [!IMPORTANT]
> Your Data is Safe on QueryStar backend:
> QueryStar takes care of 3rd party API integration. It only monitors trigger events and passes action data back to the apps of your choice. Your data is **NOT** stored or logged in any form or capacity. Please see [Privacy Policy](https://querystar.io/Privacy) for more details.


### Build and Run a Bot

- Create a new file `app.py` and add this code:
  ```py
  # app.py
  import querystar as qs
  
  message = qs.triggers.slack.new_message(channel_id='MyChannelID')
  print(message)
  ```

- Add QueryStar app to your Slack channel, and copy the channel ID ([Instruction](https://querystar.io/docs/quickstart/coding/#step-2-add-querystar-app-to-the-channel))
- Replace `MyChannelID` with the channel id. 
- Run the bot:
  
  ```bash
  $ querystar run app.py
  ```

## Get Inspired

Because you use Python, there's much more you can build.

- A LLM-powered (Large Language Model) Slack bot: [tutorial](https://querystar.io/docs/tutorials/llamaindex-doc-bot/).

