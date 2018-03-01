import os
import time
import re
from slackclient import SlackClient

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
        response = "My nanme is Rick"
    slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response or default_response
    )

if __name__ == "__main__":
    print("in the main probabpl")
    if slack_client.rtm_connect(with_team_state=False):
        print("Pylon factory is up and running")
        botid = slack_client.api_call("auth.test")["user_id"]
        slack_client.api_call(
                "chat.postMessage",
                channel='general',
                text="I'm back"
        )
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection Failed, see traceback")


