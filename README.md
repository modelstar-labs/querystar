# QueryStar

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
