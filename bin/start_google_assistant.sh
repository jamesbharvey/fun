#!/bin/bash

source /home/pi/env/bin/activate

google-assistant-demo \
    --project-id pi-my-life--assistant-acc3e \
    --device-model-id pi-my-life--assistant-acc3e-pi-google-assistant-dpuhov


exit

##
## re-run this if there is an auth error.
##

google-oauthlib-tool --client-secrets ~/googleassistant/credentials.json \
		     --scope https://www.googleapis.com/auth/assistant-sdk-prototype \
		     --scope https://www.googleapis.com/auth/gcm \
		     --save --headless


https://pimylifeup.com/raspberry-pi-google-assistant/

##
## record and play to test mike and speaker
##

arecord --format=S16_LE --duration=5 --rate=16000 --file-type=raw out.raw
aplay --format=S16_LE --rate=16000 out.raw
