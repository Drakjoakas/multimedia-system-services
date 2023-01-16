#!/bin/bash

# Start USB program
python /home/joaquin/Documentos/automatic_detect_USB.py &

# Start local service
su joaquin -c "python /home/joaquin/Documentos/webserver.py &"

# Change directory
cd /home/joaquin/Documentos/multimedia-system

# Start ps4 controller program
antimicrox --hidden --profile ../ps4Profile.gamecontroller.amgp &


# Start node server with react app
serve -s build &
webapp=""

while [ "$webapp" = "" ];
do
	webapp=`sudo lsof -i -P -n | grep :3000`
done

#Open Browser
chromium-browser --noerrdialog --start-fullscreen http://localhost:3000 &

