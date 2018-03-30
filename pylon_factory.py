import re
import util
import commandHandlers
import eventHandlers

GPIO_on = True
try:
    import pylonGPIO
except ImportError as importError:
    GPIO_on = False


class PylonFactory:

    def __init__(self, sc, bot_id, logger):
        self.slack_client = sc
        self.bot_id = bot_id
        self.logger = logger
        self.con_t = 0
        if GPIO_on:
            pylonGPIO.initPylonIO()
        else:
            self.logger.buffer('GPIO library not imported: no temp data')
        util.send_message("I'm back", 'general', self.slack_client)

    def process(self, event_list, t_tick, r_tick):
        return_code = 0
        if event_list:
            return self.react(event_list)
        else:
            return self.act(t_tick, r_tick)

    def act(self, t_tick, r_tick):
        return_code = 0
        if GPIO_on:
            pylonGPIO.lcdTick()
        if t_tick >= 10:
            return_code += 1
            try:
                self.slack_client.server.ping()
            except:
                self.logger.buffer("Why would ping fail?")
            if GPIO_on:
                temp = pylonGPIO.readCoreTemp()
                if int(temp) >= 48000:
                    util.send_message('*WARNING THERMAL OVERLOAD IN PROGRESS!*',
                            'bot_spam', self.slack_client)
                    util.send_message('CORE TEMPERATURE IS: ' + str(temp),
                            'bot_spam', self.slack_client)
                    if not pylonGPIO.fanOn:
                        pylonGPIO.activateFan()
                elif int(temp) < 45000 and pylonGPIO.fanOn:
                    util.send_message('Thermal crisis averted.',
                            'bot_spam', self.slack_client)
                    pylonGPIO.deactivateFan()
                else:
                    self.logger.buffer('nothing to report')
        if r_tick >= 100:
            return_code += 10
            chance = commandHandlers.roll("roll 1d99")
            if (chance == "You rolled: 99"):
                util.send_message(commandHandlers.iWannaKnow(),
                        channel, self.slack_client)
        return return_code

    def react(self, event_list):
        return_code = 0
        command, channel = self.parse_bot_commands(event_list)
        if command:
            self.logger.buffer(command)
            response, return_code = eventHandlers.handle_command(command, channel)
            self.logger.buffer(response)
            if response:
                util.send_message(response, channel, self.slack_client)
        return return_code

    def parse_bot_commands(self, slack_events):
        for event in slack_events:
            if event["type"] == "message" and not "subtype" in event:
                user_id, message = self.parse_dm(event["text"], event["channel"])
                if user_id == self.bot_id:
                    self.logger.buffer(message)
                    return message, event["channel"]
        return None, None

    def parse_dm(self, message_text, channel):
        self.logger.buffer(message_text)
        if GPIO_on:
            pylonGPIO.lcdLog(message_text)
        self.con_t = self.con_t+1
        if self.con_t >= 10:
            util.send_message(commandHandlers.iWannaKnow(),"general",self.slack_client)
            self.con_t = 0
        if util.SHRUG_MAN in message_text:
            util.send_message(util.SHRUG_MAN, channel,self.slack_client)
        matches = re.search(util.MENTION_REGEX, message_text)
        return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

