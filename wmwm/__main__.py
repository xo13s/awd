#!/usr/bin/python

'''
A wacky manager of window manager.
'''

import argparse
import sys

from traceback import print_exc

from wmwm.api import get_active_window
from wmwm.api import get_current_desktop
from wmwm.api import get_desktop_viewport
from wmwm.api import get_windows
from wmwm.api import get_wm_desktop
from wmwm.api import get_wm_name
from wmwm.api import set_active_window
from wmwm.layout import LAYOUT_HANDLERZ
from wmwm.logger import LOGLEVELZ
from wmwm.logger import logger
from wmwm.util import is_window_in_viewport
from wmwm.util import printerr

DESCRIPTION = '''\
A wacky manager of window manager.
'''

USAGE = '''\
%(prog)s [options] <args>
'''

EPILOG = '''\
available layouts:
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

def parse_args():
    '''
    Parse arguments.

    Returns
    -------
    argparse.Namespace
        An object holding options and arguments as attributes.
    '''
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        usage=USAGE,
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('--loglevel',
                        choices=LOGLEVELZ.values(),
                        default='info',
                        metavar='<loglevel>',
                        help='log level')
    parser.add_argument('--exclude',
                        action='append',
                        default=[],
                        metavar='<exclude>',
                        help='exclude window names matching pattern')
    parser.add_argument('layout',
                        choices=LAYOUT_HANDLERZ.keys(),
                        metavar='<layout>',
                        help='layout name')
    args = parser.parse_args()
    return args

def filter_windows(windows, desktop, viewport, excludes):
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
    excludes : list
        A list of window name exclude patterns.

    Returns
    -------
    list
        A list of windows that pass the filter.
    '''
    ans = []
    for window in windows:

        # Filter by desktop.
        if get_wm_desktop(window) != desktop:
            continue

        # Filter by viewport.
        if not is_window_in_viewport(window, viewport):
            continue

        # Filter by window name.
        wm_name = get_wm_name(window)
        if any([x in wm_name for x in excludes]):
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

def _main():
    '''
    Actual main function.
    '''
    # Parse args.
    args = parse_args()
    loglevel = args.loglevel
    layout = args.layout
    exclude = args.exclude

    # Set log level.
    logger.setLevel({v: k for k, v in LOGLEVELZ.items()}[loglevel])

    # Get all windows managed by WM.
    windows = get_windows()
    logger.d('all windows %s', windows)

    # Get current active window.
    active_window = get_active_window()
    logger.d('active_window %s', active_window)

    # Get current desktop.
    desktop = get_current_desktop()
    logger.d('current desktop %s', desktop)

    # Get current viewport.
    viewport = get_desktop_viewport()
    logger.d('current viewport %s', viewport)

    # Filter windows by desktop and viewport.
    windows = filter_windows(windows, desktop, viewport, exclude)
    logger.d('filtered windows %s', windows)

    # Layout windows.
    layout_windows(windows, layout, active_window)

    # Activate the original active window.
    set_active_window(active_window)

def main():
    '''
    Main function wrapper.
    '''
    try:
        _main()
    except Exception as e:
        print_exc(e)
        sys.exit(1)

if __name__ == '__main__':
    main()
