#!/bin/bash

IMAGE=~/.blur.png
LEFT=~/.blur-0.png
RIGHT=~/.blur-1.png
ICON=~/.i3/lock-icon.png
scrot $IMAGE
convert $IMAGE -scale 5% -scale 2000% $IMAGE

function HDMIConnected {
  ! xrandr | grep "^HDMI2" | grep disconnected
  }

if HDMIConnected
        then
        mogrify -crop 50%x100% $IMAGE
        convert $LEFT $ICON -gravity center -composite -matte $LEFT
        convert $RIGHT $ICON -gravity center -composite -matte $RIGHT
        convert $LEFT $RIGHT +append $IMAGE
        else
        convert $IMAGE $ICON -gravity center -composite -matte $IMAGE
fi

i3lock -u -i $IMAGE
killall ~/.i3/change-background-every-ten-minutes.bash
sudo pm-suspend
bash ~/.i3/change-background-every-ten-minutes.bash
