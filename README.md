# zart-bot
Bot that will run IPL systems and run ZART profiles

To start the bot run `./rollout.sh` after adding execute permissions or `bash rollout.sh`

pylon_factory.py is the bot main function
rollout.sh is the startup and health monitor script for the bot

Return codes:
  RC=0 , bot exited normally and should not be restarted
  RC=1 , bot exited normally and will restart after updating
  RC>1 , bot exited abnormally and will attempt to restart
