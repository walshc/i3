#!/bin/bash

# Display the volume in i3bar and enable changing of volume with two-finger
# scrolling over the symbol and toggle mute with right click.

# Get the volume percentage:
VOLUME=$(amixer sget Master | egrep -o -m 1 "[0-9]+%")

# Check if muted:
STATE=`amixer sget Master | egrep -m 1 'Playback.*?\[o' | egrep -o '\[o.+\]'`
# Use mouse to change volume and toggle mute in i3bar:
case $BLOCK_BUTTON in
  1) pavucontrol ;; #urxvt -title "float" -e alsamixer --view all ;;
  # Right click to toggle mute
  3) amixer -q sset Master toggle & ~/.i3/vol-notify ;;
  # Scroll up to increase volume
  4) amixer -q sset Master 5%+ & ~/.i3/vol-notify ;;
  # Scroll down to decrease volume
  5) amixer -q sset Master 5%- & bash ~/.i3/vol-notify ;;
esac

# # What to display in i3bar:
if [[ $STATE == '[off]' ]]; then
        echo ""
        exit 0
else
        VOLNUM=$(echo -e $VOLUME | egrep -o "[0-9]+")
        if [ $VOLNUM -lt "33" ]; then
                echo ""$VOLUME
                exit 0
        elif [ $VOLNUM -lt "66" ]; then
                echo ""$VOLUME
                exit 0
        else
                echo ""$VOLUME
                exit 0
        fi
fi
