# Hi there, this is <a href="https://querystar.io/" style="color: #AF3BEA;"><img src="./assets/logo.png" height="28"> QueryStar</a> 👋

### QueryStar is the easiest way for data and Python developers to ship AI-powered bots.

![How does QueryStar work?](./assets/diagram.png)

## Install

```
pip install querystar
```

## Get your access token : app.querystar.io

## Add access token to environment variable

## Sample app

```py
# app.py
import querystar as qs

message_info = qs.triggers.slack.new_message()
print(message_info)
```

## Run using

```bash
querystar run app.py
```
