#!/usr/bin/python

'''
A wacky manager of window manager.
'''

import argparse
import subprocess
import sys

from wmwm.api import *
from wmwm.layout import LAYOUT_HANDLERZ
from wmwm.logger import logger
from wmwm.util import is_window_in_viewport
from wmwm.util import printerr
from wmwm.util import printout

USAGE_TEXT = '''
Usage: wmwm [options] <layout>

Available layouts:
    cascade             Cascade windows
    hstack              Stack windows horizontally
    vstack              Stack windows vertically
    bmain               Main window on the bottom
    lmain               Main window on the left
    rmain               Main window on the right
    tmain               Main window on the top
    rowgrid[x][y]       Row-major grid layout (2 <= x, y <= 4)
    colgrid[x][y]       Col-major grid layout (2 <= x, y <= 4)
'''

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

def filter_windows(windows, desktop, viewport):
    '''
    Filter out windows which are not in the desktop or not in the viewport.

    Parameters
    ----------
    windows : list
        A list of windows.
    desktop : int
        A desktop number.
    viewport : list
        A viewport.

    Returns
    -------
    list
        A list of windows that pass the filter.
    '''
    ans = []
    for window in windows:
        if get_wm_desktop(window) != desktop:
            continue
        if not is_window_in_viewport(window, viewport):
            continue
        ans.append(window)
    return ans

def layout_windows(windows, layout, active_window):
    '''
    Layout windows.

    Parameters
    ----------
    windows : list
        A list of windows.
    layout : str
        Layout name.
    active_window : object
        The active window object.
    '''
    LAYOUT_HANDLERZ[layout](windows, active_window)

def run():
    '''
    Run function.
    '''
    # Parse args.
    layout = parse_args()

    # Get all windows managed by WM.
    windows = get_windows()
    logger.d('all windows', windows)

    # Get current active window.
    active_window = get_active_window()
    logger.d('active_window', active_window)

    # Get current desktop.
    desktop = get_current_desktop()
    logger.d('current desktop', desktop)

    # Get current viewport.
    viewport = get_desktop_viewport()
    logger.d('current viewport', viewport)

    # Filter windows by desktop and viewport.
    windows = filter_windows(windows, desktop, viewport)
    logger.d('filtered windows', windows)

    # Layout windows.
    layout_windows(windows, layout, active_window)

    # Activate the original active window.
    set_active_window(active_window)

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
