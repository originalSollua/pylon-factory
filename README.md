# zart-bot
Bot that will run IPL systems and run ZART profiles

To start the bot run `./rollout.sh` after adding execute permissions or `bash rollout.sh`

pylon_factory.py is the bot main function</br>
rollout.sh is the startup and health monitor script for the bot

Bot return codes:
  </br>&nbsp;&nbsp;&nbsp;&nbsp;RC=0 , bot exited normally and should not be restarted
  </br>&nbsp;&nbsp;&nbsp;&nbsp;RC=1 , Python encountered an error, likely broken build
  </br>&nbsp;&nbsp;&nbsp;&nbsp;RC=2 , bot exited normally and should update
  </br>&nbsp;&nbsp;&nbsp;&nbsp;RC>2 , bot exited abnormally and will attempt to restart
