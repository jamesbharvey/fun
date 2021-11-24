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
