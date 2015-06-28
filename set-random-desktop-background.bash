#!/bin/bash

# Directory of wallpapers:
DIR="$HOME/Pictures/2560x1440/"

# Choose a random wallpaper from files in that directory:
FILES=($DIR/*)
WALLPAPER=`printf "%s\n" "${FILES[RANDOM % ${#FILES[@]}]}"`

# Set as desktop background:
feh --bg-scale $WALLPAPER
