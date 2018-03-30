import datetime

SHRUG_MAN = "¯\_(ツ)_/¯"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

DEFAULT_RESPONSE = "You are a goober."
DEFAULT_FN = "log.txt"

# Logger class
# Handles buffering logs messages and writing them to the file
class Logger:

    def __init__(self, fn = DEFAULT_FN):
        self.fn = fn
        self.LOG_STREAM = []

    def buffer(self, text):
        self.LOG_STREAM.append(text)

    def write(self, text = ""):
        with open(self.fn,'a') as logfile:
            if text:
                logfile.write(text + "\n")
            else:
                for x in self.LOG_STREAM:
                    try:
                        logfile.write(str(datetime.datetime.now()) +": "+x)
                    except TypeError:
                        logfile.write(str(datetime.datetime.now()) +": LOG ERR")
                    except UnicodeEncodeError:
                        logfile.write(str(datetime.datetime.now()) +": "+\
                                      str(x.encode("utf-8","replace")))
                    logfile.write("\n")
                del self.LOG_STREAM[:]


def send_message(message, channel, sc):
    sc.api_call(
            "chat.postMessage",
            channel=channel,
            text = message or DEFAULT_RESPONSE
            )
    return

