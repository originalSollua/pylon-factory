#!/bin/bash

msg_headers=("MONITOR" "UPDATE" "ERROR")
retry_count=0
return_code=0
bot_status=""

# Messaging function
function post_msg {
  printf "%-8s" $1
  echo ": $2"
}

# Bot startup function
function start_bot {
  retry_count=0
  return_code=0
  while [ $retry_count -lt 5 ]; do
    python pylon_factory.py "$bot_status" & pylon_pid=$!
    sleep 2
    if kill -0 "$pylon_pid"; then
      break
    else
      retry_count=$((++retry_count))
    fi
  done
  if [ $retry_count -ge 5 ]; then
    post_msg ${msg_headers[2]} "Process failed to start, possibly broken build"
    post_msg ${msg_headers[1]} "Backing up to previous commit"
    git revert --no-commit HEAD~1..HEAD
    git commit -m "AUTO: Reverting to previous commit"; return_code=$?
    if [ $return_code -eq 0 ]; then
      git push; return_code=$?
      if [ $return_code -eq 0 ]; then
        post_msg ${msg_headers[1]} "Sucessfully reverted, restarting bot"
        return_code=1
      else
        post_msg ${msg_headers[2]} "Unable to push reversion, hep"
        exit 1
      fi
    else
      post_msg ${msg_headers[2]} "Unable to revert or commit change, hep"
      exit 1
    fi
  fi
}


# Mainline
while sleep 1; do

    # Attempt to start bot
    start_bot

    if [ $return_code -eq 0 ]; then
      # Wait for finish and grab return code
      post_msg ${msg_headers[0]} "pylon_factory.py started with pid: $pylon_pid"
      wait "$pylon_pid"; pylon_exit=$?

      # Check return code
      # RC=0 , clean exit
      if [ $pylon_exit -eq 0 ]; then
        post_msg ${msg_headers[0]} "pylon_factory.py exited with RC=$pylon_exit"
        post_msg ${msg_headers[0]} "Script terminating"
        exit 0

      # RC=1 , clean exit and update
      elif [ $pylon_exit -eq 1 ]; then
        post_msg ${msg_headers[0]} "pylon_factory.py exited with RC=$pylon_exit"
        post_msg ${msg_headers[1]} "Beginning update"
        git pull; return_code=$?

        if [ $return_code -eq 0 ]; then
          post_msg ${msg_headers[1]} "Pull successful, restarting bot with new code"
          bot_status=""
        else
          post_msg ${msg_headers[2]} "Pull unsuccessful, restarting bot with old code"
          bot_status="`git log --name-status HEAD^..HEAD`"
        fi

      # RC=? , unknown return code from bot, attempt to restart
      else
        post_msg ${msg_headers[2]} "Unrecognized return code, attempting restart"
        bot_status=""
      fi
    fi
done
