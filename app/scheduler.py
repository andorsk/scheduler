#!/usr/bin/env python3
import os
import schedule
import time
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests
import json

logging.basicConfig(level=logging.INFO)

def sendMessage(slack_client, msg, channel):
  try:
    slack_client.chat_postMessage(
      channel=channel,
      blocks=msg
    )
  except SlackApiError as e:
    logging.error('Request to Slack API Failed: {}.'.format(e.response.status_code))
    logging.error(e.response)

def sendDailyWisdom(slack_client):
  resp = requests.post("http://daily_wisdom.kesselmanrao.com/slack/tao")
  sendMessage(slack_client, resp.json()["blocks"], channel="#tao")

if __name__ == "__main__":
  SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
  slack_client = WebClient(SLACK_BOT_TOKEN)
  logging.debug("authorized slack client")
  resp = requests.post("http://daily_wisdom.kesselmanrao.com/slack/tao")
  schedule.every().day.at("10:30").do(sendDailyWisdom, slack_client=slack_client)
#  schedule.every(5).seconds.do(sendDailyWisdom, slack_client=slack_client)

  while True:
    schedule.run_pending()
    time.sleep(5) # sleep for 5 seconds between checks on the scheduler

