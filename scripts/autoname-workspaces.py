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
MDI_CHROME = ''
MDI_CODE = ''
MDI_RSTUDIO = 'R>'
MDI_FILE_PDF_O = ''
MDI_FILE_TEXT_O = ''
MDI_FILES_O = ''
MDI_FIREFOX = ''
MDI_MUSIC = ''
MDI_PICTURE_O = ''
MDI_SPOTIFY = ''
MDI_TERMINAL = ''
MDI_VIM = ''
MDI_QGIS = ''
MDI_HANGOUTS = ''
MDI_APPFINDER = ''
MDI_BOOK = ''
MDI_R_PLOT = 'R'
MDI_TRANSMISSION = ''
MDI_PRINTER = ''
MDI_ENPASS = ''
MDI_VOLUME = ''
MDI_VLC = ''
MDI_EMAIL = ''
MDI_SETTINGS = ''
MDI_WIFI = ''
MDI_GIMP = ''
MDI_GNOME = ''
MDI_GPIO = ''
MDI_SKYPE = ''
MDI_XSTATA = 'Stata'
MDI_STEAM = ''
MDI_SPREADSHEET = ''
MDI_PLAY = ''
MDI_WEB = ''
MDI_GPM = ''
MDI_CALENDAR = ''
MDI_CONKY = ''
MDI_DARKTABLE = ''
MDI_WINE = ''
MDI_KEEP = ''
MDI_CALENDAR = ''
MDI_SLACK = ''

WINDOW_ICONS = {
    'urxvt': MDI_TERMINAL,
    'xfce4-terminal': MDI_TERMINAL,
    'google-chrome': MDI_CHROME,
    'chromium': MDI_CHROME,
    'chromium-browser': MDI_CHROME,
    'subl': MDI_CODE,
    'subl3': MDI_CODE,
    'gedit': MDI_CODE,
    'spotify': MDI_SPOTIFY,
    'Spotify': MDI_SPOTIFY,
    'Firefox': MDI_FIREFOX,
    'Firefox-esr': MDI_FIREFOX,
    'Iceweasel': MDI_FIREFOX,
    'LibreOffice' : MDI_FILE_TEXT_O,
    'libreoffice-calc': MDI_SPREADSHEET,
    'gnumeric': MDI_SPREADSHEET,
    'libreoffice-writer': MDI_FILE_TEXT_O,
    'soffice': MDI_FILE_TEXT_O,
    'feh': MDI_PICTURE_O,
    'mupdf': MDI_FILE_PDF_O,
    'evince': MDI_FILE_PDF_O,
    'okular': MDI_FILE_PDF_O,
    'nautilus': MDI_FILES_O,
    'thunar': MDI_FILES_O,
    'rstudio': MDI_RSTUDIO,
    'vim': MDI_VIM,
    'gvim': MDI_VIM,
    'qgis.bin': MDI_QGIS,
    'hangouts': MDI_HANGOUTS,
    'hangups' : MDI_HANGOUTS,
    'xfce4-appfinder': MDI_APPFINDER,
    'kbibtex': MDI_BOOK,
    'calibre': MDI_BOOK,
    'r_x11': MDI_R_PLOT,
    'R_x11': MDI_R_PLOT,
    'transmission-gtk' : MDI_TRANSMISSION,
    'Transmission' : MDI_TRANSMISSION,
    'system-config-printer.py' : MDI_PRINTER,
    'Enpass' : MDI_ENPASS,
    'Rhythmbox' : MDI_MUSIC,
    'Pavucontrol' : MDI_VOLUME,
    'vlc' : MDI_VLC,
    'eog' : MDI_PICTURE_O,
    'geary' : MDI_EMAIL,
    'gnome-control-center' : MDI_SETTINGS,
    'unity-control-center' : MDI_SETTINGS,
    'Wicd Network Manager' : MDI_WIFI,
    'wicd-client.py' : MDI_WIFI,
    'gimp' : MDI_GIMP,
    'oregano' : MDI_GPIO,
    'Fritzing' : MDI_GPIO,
    'Ghetto Skype' : MDI_SKYPE,
    'Skype' : MDI_SKYPE,
    'skypeforlinux' : MDI_SKYPE,
    'referencer' : MDI_BOOK,
    'xstata' : MDI_XSTATA,
    'xstata-se' : MDI_XSTATA,
    'StataSE-64.exe' : MDI_XSTATA,
    'Steam' : MDI_STEAM,
    'gPodder' : MDI_PLAY,
    'vivaldi-stable' : MDI_WEB,
    'crx_knipolnnllmklapflnccelgolnpehhpl' : MDI_HANGOUTS,
    'crx_hmjkmjkepdijhoojdojkdfohbdgmmhki' : MDI_KEEP,
    'evolution' : MDI_CALENDAR,
    'libreoffice-startcenter' : MDI_FILE_TEXT_O,
    'acroread' : MDI_FILE_PDF_O,
    'conky' : MDI_CONKY,
    'Conky' : MDI_CONKY,
    'google play music desktop player' : MDI_GPM,
    'darktable' : MDI_DARKTABLE,
    'PlayOnLinux' : MDI_WINE,
    'Thunderbird' : MDI_EMAIL,
    'Mail' : MDI_EMAIL,
    'Inbox - Mozilla Thunderbird' : MDI_EMAIL,
    'minetime' : MDI_CALENDAR,
    'california' : MDI_CALENDAR,
    'slack' : MDI_SLACK
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
