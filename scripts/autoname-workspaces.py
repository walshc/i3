# -*- coding: utf-8 -*-

# This script listens for i3 events and updates workspace names to show icons
# for running programs.  It contains icons for a few programs, but more can
# easily be added by inserting them into WINDOW_ICONS below.
#
# Dependencies
# * xorg-xprop - install through system package manager
# * i3ipc - install with pip


import i3ipc
import subprocess as proc
import re
import signal
import sys


# Add icons here for common programs you use.  The keys are the X window class
# (WM_CLASS) names and the icons can be any text you want to display. However
# most of these are character codes for font awesome:
#   http://fortawesome.github.io/Font-Awesome/icons/
FA_CHROME = ''
FA_CODE = ''
FA_RSTUDIO = 'R>'
FA_FILE_PDF_O = ''
FA_FILE_TEXT_O = ''
FA_FILES_O = ''
FA_FIREFOX = ''
FA_MUSIC = ''
FA_PICTURE_O = ''
FA_SPOTIFY = ''
FA_TERMINAL = ''
FA_VIM = ''
FA_QGIS = ''
FA_HANGOUTS = ''
FA_APPFINDER = ''
FA_BOOK = ''
FA_R_PLOT = 'R'
FA_TRANSMISSION = ''
FA_PRINTER = ''
FA_ENPASS = ''
FA_VOLUME = ''
FA_VLC = ''
FA_EMAIL = ''
FA_SETTINGS = ''
FA_WIFI = ''
FA_GIMP = ''
FA_GNOME = ''
FA_GPIO = ''
FA_SKYPE = ''
FA_XSTATA = 'Stata'

WINDOW_ICONS = {
    'urxvt': FA_TERMINAL,
    'xfce4-terminal': FA_TERMINAL,
    'google-chrome': FA_CHROME,
    'chromium': FA_CHROME,
    'chromium-browser': FA_CHROME,
    'subl': FA_CODE,
    'subl3': FA_CODE,
    'gedit': FA_CODE,
    'spotify': FA_SPOTIFY,
    'Spotify': FA_SPOTIFY,
    'Firefox': FA_FIREFOX,
    'Iceweasel': FA_FIREFOX,
    'libreoffice': FA_FILE_TEXT_O,
    'soffice': FA_FILE_TEXT_O,
    'feh': FA_PICTURE_O,
    'mupdf': FA_FILE_PDF_O,
    'evince': FA_FILE_PDF_O,
    'okular': FA_FILE_PDF_O,
    'nautilus': FA_FILES_O,
    'thunar': FA_FILES_O,
    'rstudio': FA_RSTUDIO,
    'vim': FA_VIM,
    'gvim': FA_VIM,
    'qgis.bin': FA_QGIS,
    'hangouts': FA_HANGOUTS,
    'xfce4-appfinder': FA_APPFINDER,
    'kbibtex': FA_BOOK,
    'calibre': FA_BOOK,
    'r_x11': FA_R_PLOT,
    'R_x11': FA_R_PLOT,
    'transmission-gtk' : FA_TRANSMISSION,
    'Transmission' : FA_TRANSMISSION,
    'system-config-printer.py' : FA_PRINTER,
    'Enpass' : FA_ENPASS,
    'Rhythmbox' : FA_MUSIC,
    'Pavucontrol' : FA_VOLUME,
    'vlc' : FA_VLC,
    'eog' : FA_PICTURE_O,
    'geary' : FA_EMAIL,
    'gnome-control-center' : FA_SETTINGS,
    'Wicd Network Manager' : FA_WIFI,
    'wicd-client.py' : FA_WIFI,
    'gimp' : FA_GIMP,
    'oregano' : FA_GPIO,
    'Fritzing' : FA_GPIO,
    'Ghetto Skype' : FA_SKYPE,
    'Skype' : FA_SKYPE,
    'skypeforlinux' : FA_SKYPE,
    'pokemon-go-map' : FA_QGIS,
    'referencer' : FA_BOOK,
    'xstata' : FA_XSTATA,
    'StataSE-64.exe' : FA_XSTATA
}


i3 = i3ipc.Connection()

# Returns an array of the values for the given property from xprop.  This
# requires xorg-xprop to be installed.
def xprop(win_id, property):
    try:
        prop = proc.check_output(['xprop', '-id', str(win_id), property], stderr=proc.DEVNULL)
        prop = prop.decode('utf-8')
        return re.findall('"([^"]+)"', prop)
    except proc.CalledProcessError as e:
        print("Unable to get property for window '%s'" % str(win_id))
        return None

def icon_for_window(window):
    classes = xprop(window.window, 'WM_CLASS')
    if classes != None and len(classes) > 0:
        for cls in classes:
            if cls in WINDOW_ICONS:
                return WINDOW_ICONS[cls]
        print('No icon available for window with classes: %s' % str(classes))
    return '*'

# renames all workspaces based on the windows present
def rename():
    for workspace in i3.get_tree().workspaces():
        icons = [icon_for_window(w) for w in workspace.leaves()]
        icon_str = ' ' + ''.join(set(icons)) if len(icons) else ''
        new_name = str(workspace.num) + icon_str
        i3.command('rename workspace "%s" to "%s"' % (workspace.name, new_name))

rename()

# exit gracefully when ctrl+c is pressed
def signal_handler(signal, frame):
    # rename workspaces to just numbers on exit to indicate that this script is
    # no longer running
    for workspace in i3.get_tree().workspaces():
        i3.command('rename workspace "%s" to "%d"' % (workspace.name, workspace.num))
    i3.main_quit()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# call rename() for relevant window events
def on_change(i3, e):
    if e.change in ['new', 'close', 'move']:
        rename()
i3.on('window', on_change)
i3.main()
