#!/bin/bash

# Display startup script.
# If the monitor is connected via HDMI, display only that.
# If the monitor is disconnected, display from laptop screen only.

# Use LVDS1 (laptop screen) by default:
MONITOR=eDP1

function ActivateHDMI {
  # External montior only by default:
  #xrandr --output HDMI2 --auto --output eDP1 --off
  # Dual monitors by default (with laptop on the right-hand-side):
  xrandr --auto
  xrandr --output HDMI2 --primary --left-of eDP1 --output eDP1 --mode 1920x1080
  MONITOR=HDMI1
}

function DeactivateHDMI {
  xrandr --auto
  xrandr --output HDMI2 --off --output eDP1 --auto
  MONITOR=LVDS1
}

# Functions to check if HDMI is connected and in use
function HDMIActive {
  [ $MONITOR = "HDMI2" ]
}

function HDMIConnected {
  ! xrandr | grep "^HDMI2" | grep disconnected
}


if ! HDMIActive && HDMIConnected
  then
  ActivateHDMI
fi

if HDMIActive && ! HDMIConnected
then
  DeactivateHDMI
fi

bash ~/.i3/change-background-every-ten-minutes.bash
