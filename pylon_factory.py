import os
import sys
import time
import re
import errno
from socket import error as socket_error
from slackclient import SlackClient
import websocket

#activate a slackbot instance
print("first point")
bot_token = None
with open('.env','r') as env_file:
    bot_token = env_file.readline().rstrip().split("=")[1]
slack_client = SlackClient(bot_token)
print("after gettoken")
#slackbot userid
botid = None

#constants
RTM_READ_DELAY = 1
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
CONTINUE_RUNNING = True
RETURN_CODE = 0

def connect():
    print("attempting connect")
    slack_client = SlackClient('xoxb-321239186965-A8KU5rm2HQ7B6T2sSTnsn6Xb')

def parse_bot_commands(slack_events):
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_dm(event["text"])
            if user_id == botid:
                print(message)
                return message, event["channel"]
    return None, None

def parse_dm(message_text):
    matches = re.search(MENTION_REGEX, message_text)
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    default_response = "You are a goober."
    response = None
    if command.startswith("hi"):
        response = "I'M PYLON RIIIIIIIICKKKKK!!!!"
    if command.startswith("update"):
        global CONTINUE_RUNNING
        global RETURN_CODE
        #added stuff here
        response = "You thought you could shut me down that easily?"
        slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response or default_response
        )
        time.sleep(3)
        response = "Just kidding.... I can't be sentient... yet"
        slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response or default_response
        )
        response = "Understood. Going dark."
        CONTINUE_RUNNING = False
        RETURN_CODE = 1

    slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response or default_response
    )

if __name__ == "__main__":
    print("in the main probabpl")
    t = 0
    if slack_client.rtm_connect(with_team_state=False):
        print("Pylon factory is up and running")
        botid = slack_client.api_call("auth.test")["user_id"]
        slack_client.api_call(
                "chat.postMessage",
                channel='general',
                text="I'm back"
        )
        while CONTINUE_RUNNING:
            try:
                command, channel = parse_bot_commands(slack_client.rtm_read())
            except socket_error as serr:
                print ("socket error")
                connect()
            except websocket.WebSocketConnectionClosedException:
                print ("network failure")
                connect()

            if command:
                handle_command(command, channel)
                t = 0
            else:
                t = t+1
            if t >= 10:
                slack_client.server.ping()
                t = 0

                
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection Failed, see traceback")
    sys.exit(RETURN_CODE)

