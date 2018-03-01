#!/usr/bin/bash

retries=0

while sleep 1; do
  # Start up bot and grab pid (assuming command is just python, update as needed)
  python pylon_factory.py & pylon_pid=$!
  sleep 2

  # See if it started
  if kill -0 "$pylon_pid"; then
    # Wait for finish and grab return code
    echo "MONITOR: pylon_factory.py started with pid: $pylon_pid"
    wait "$pylon_pid"; pylon_exit=$?

    # Check return code
    if [ $pylon_exit -gt 0 ]; then
      echo "MONITOR: pylon_factory failed with exit code: $pylon_exit"

      # restart if we haven't retried too many times
      if [ $retries -lt 5 ]; then
        echo "MONITOR: restarting..."
        retries=$retries+1
      else
        echo "MONITOR: Too many retries, giving up"
        exit 1
      fi

    else
      echo "MONITOR: pylon_factory exited cleanly"
      exit
    fi

  else
    echo "MONITOR: pylon_factory.py failed to start"
    exit
  fi
done
