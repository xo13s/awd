#!/usr/bin/python

'''
A wacky manager of window manager.

Desktop object definition
================================================

::

    {
        'num': int,
        'is_current': bool,
        'dg_w': int,
        'dg_h': int,
        'vp_x': int,
        'vp_y': int,
        'wa_x': int,
        'wa_y': int,
        'wa_w': int,
        'wa_h': int,
        'windows': dict,
    }

Window object definition
================================================

::

    {
        'id': int,
        'desktop_num': int,
        'x': int,
        'y': int,
        'w': int,
        'h': int,
    }

'''

import argparse
import json
import re
import subprocess
import sys

from wmwm.api import activate_window
from wmwm.api import get_active_window
from wmwm.api import get_display_geometry
from wmwm.api import set_fullscreen
from wmwm.api import set_maximized
from wmwm.api import set_window_size
from wmwm.layout import LAYOUT_HANDLERZ
from wmwm.util import is_window_in_viewport
from wmwm.util import printerr
from wmwm.util import printout

USAGE_TEXT = '''
Usage: wmwm [options] <layout>

Available layouts:
    cascade     Cascade windows.
    htile       Tile windows horizontally.
    vtile       Tile windows vertically.
'''

# Desktop regex.
RE_DESKTOP = re.compile(
    r'(\d+)\s+([*-])\s+'
    r'DG:\s+(\d+)x(\d+)\s+'
    r'VP:\s+(\d+),(\d+)\s+'
    r'WA:\s+(\d+),(\d+)\s+(\d+)x(\d+)\s+'
    r'.*'
)

# Window regex.
RE_WINDOW = re.compile(
    r'(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+.*'
)

def usage():
    '''
    Usage function.
    '''
    printerr(USAGE_TEXT)

def parse_args():
    '''
    Parse arguments.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('layout',
                        choices=LAYOUT_HANDLERZ.keys(),
                        help='layout')
    args = parser.parse_args()
    return args.layout

def downsize():
    '''
    Downsize all windows on the current desktop.
    '''
    # Get desktops.
    lines = subprocess.check_output([
        'wmctrl', '-d'
    ]).decode().split('\n')
    desktopz = {}
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if '*' in line:
            m = RE_DESKTOP.match(line)
            desktop = {
                'num': int(m.group(1)),
                'is_current': m.group(2) == '*',
                'dg_w': int(m.group(3)),
                'dg_h': int(m.group(4)),
                'vp_x': int(m.group(5)),
                'vp_y': int(m.group(6)),
                'wa_x': int(m.group(7)),
                'wa_y': int(m.group(8)),
                'wa_w': int(m.group(9)),
                'wa_h': int(m.group(10)),
                'windows': {},
            }
        else:
            desktop = {
                'num': int(line.split()[0]),
                'is_current': False,
                'windows': {},
            }
        desktopz[desktop['num']] = desktop

    # Get windows.
    lines = subprocess.check_output([
        'wmctrl', '-lG'
    ]).decode().split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        m = RE_WINDOW.match(line)
        window = {
            'id': int(m.group(1), 16),
            'desktop_num': int(m.group(2)),
            'x': int(m.group(3)),
            'y': int(m.group(4)),
            'w': int(m.group(5)),
            'h': int(m.group(6)),
        }

        # Bypass sticky windows.
        if window['desktop_num'] == -1:
            continue

        # Bypass windows not on the current desktop.
        desktop = desktopz[window['desktop_num']]
        if not desktop['is_current']:
            continue

        # Bypass windows that are not in the current viewport.
        dp_w, dp_h = get_display_geometry()
        viewport = {
            'x': 0,
            'y': 0,
            'w': dp_w,
            'h': dp_h,
        }
        if not is_window_in_viewport(window, viewport):
            continue

        # Remove fullscreen property.
        set_fullscreen(window['id'], 'off')

        # Remove maximized property.
        set_maximized(window['id'], 'off')

        # Downsize to 1x1.
        set_window_size(window['id'], 1, 1)

def get_desktops():
    '''
    Get all desktops and windows.

    Returns
    -------
    dict
        A dict of desktops keyed by number.
    '''
    # Get desktops.
    lines = subprocess.check_output([
        'wmctrl', '-d'
    ]).decode().split('\n')
    desktopz = {}
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if '*' in line:
            m = RE_DESKTOP.match(line)
            desktop = {
                'num': int(m.group(1)),
                'is_current': m.group(2) == '*',
                'dg_w': int(m.group(3)),
                'dg_h': int(m.group(4)),
                'vp_x': int(m.group(5)),
                'vp_y': int(m.group(6)),
                'wa_x': int(m.group(7)),
                'wa_y': int(m.group(8)),
                'wa_w': int(m.group(9)),
                'wa_h': int(m.group(10)),
                'windows': {},
            }
        else:
            desktop = {
                'num': int(line.split()[0]),
                'is_current': False,
                'windows': {},
            }
        desktopz[desktop['num']] = desktop

    # Get windows.
    lines = subprocess.check_output([
        'wmctrl', '-lG'
    ]).decode().split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        m = RE_WINDOW.match(line)
        window = {
            'id': int(m.group(1), 16),
            'desktop_num': int(m.group(2)),
            'x': int(m.group(3)),
            'y': int(m.group(4)),
            'w': int(m.group(5)),
            'h': int(m.group(6)),
        }

        # Bypass sticky windows.
        if window['desktop_num'] == -1:
            continue

        # Bypass windows not on the current desktop.
        desktop = desktopz[window['desktop_num']]
        if not desktop['is_current']:
            continue

        # Bypass windows that are not in the current viewport.
        dp_w, dp_h = get_display_geometry()
        viewport = {
            'x': 0,
            'y': 0,
            'w': dp_w,
            'h': dp_h,
        }
        if not is_window_in_viewport(window, viewport):
            continue

        # Bypass a window if its size is the same as the display geometry. It
        # must be the root window because we have tried to downsize all windows
        # (and the root window cannot be downsized).
        if window['w'] == dp_w and window['h'] == dp_h:
            continue

        # Add window to desktop.
        desktopz[window['desktop_num']]['windows'][window['id']] = window

    # Return desktops.
    return desktopz

def set_desktops(desktopz, layout, active_window):
    '''
    Set desktops layout.

    Parameters
    ----------
    desktopz
        A dict of desktops keyed by number.
    layout
        A layout.
    active_window
        Active window ID.

    Returns
    -------
    None
        None.
    '''
    for _, desktop in desktopz.items():
        LAYOUT_HANDLERZ[layout](desktop, active_window)

def run():
    '''
    Run function.
    '''
    # Parse args.
    layout = parse_args()
    # Save the original active window.
    active_window = get_active_window()
    # Downsize all windows.
    downsize()
    # Get desktops.
    desktopz = get_desktops()
    # Set desktops.
    set_desktops(desktopz, layout, active_window)
    # Activate the original active window.
    activate_window(active_window)

def main():
    '''
    Main function.
    '''
    try:
        run()
    except Exception as e:
        raise e
        usage()
        sys.exit(1)

if __name__ == '__main__':
    main()
