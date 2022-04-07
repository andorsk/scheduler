#!/usr/bin/env python3
import os
import json
import logging

from flask import Flask, request, make_response, Response
from fastapi import FastAPI, HTTPException, Request

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.signature import SignatureVerifier

from slashCommand import Slash

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

@app.post("/slack/test")
def command():
  if not verifier.is_valid_request(request.get_data(), request.headers):
    return make_response("invalid request", 403)
  info = request.form

  try:
    response = slack_client.chat_postMessage(
      channel='#{}'.format(info["channel_name"]),
      text=commander.getMessage()
    )#.get()
  except SlackApiError as e:
    logging.error('Request to Slack API Failed: {}.'.format(e.response.status_code))
    logging.error(e.response)
    return make_response("", e.response.status_code)

  return make_response("", response.status_code)

# Start the Flask server
if __name__ == "__main__":
  SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
  SLACK_SIGNATURE = os.environ['SLACK_SIGNATURE']
  slack_client = WebClient(SLACK_BOT_TOKEN)
  verifier = SignatureVerifier(SLACK_SIGNATURE)

  commander = Slash("Hey there! It works.")

  app.run()
