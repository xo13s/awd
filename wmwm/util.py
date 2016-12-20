#!/usr/bin/python

'''Utility module.'''

import sys

from wmwm.api import get_desktop_geometry
from wmwm.logger import logger

def printout(s):
    '''
    Print to stdout and flush.
    '''
    print(s, file=sys.stdout, flush=True)

def printerr(s):
    '''
    Print to stderr and flush.
    '''
    print(s, file=sys.stderr, flush=True)

def is_window_in_viewport(window, viewport):
    '''
    Check whether window is in viewport.

    Parameters
    ----------
    window : object
        A window object.
    viewport : list
        A viewport.

    Returns
    -------
    bool
        True iff window is in viewport.
    '''
    # Get window geometry.
    win_geo = window.get_geometry()
    # Get root window.
    root = win_geo.root
    # Translate coords (window -> root).
    win_in_root_geo = root.translate_coords(window, win_geo.x, win_geo.y)

    wl = win_in_root_geo.x
    wt = win_in_root_geo.y
    wr = win_in_root_geo.x + win_geo.width
    wb = win_in_root_geo.y + win_geo.height
    logger.d([wl, wt, wr - wl, wb - wt])

    # Get root geometry.
    root_geo = root.get_geometry()

    vl = viewport[0]
    vt = viewport[1]
    vr = viewport[0] + root_geo.width
    vb = viewport[1] + root_geo.height
    logger.d([vl, vt, vr - vl, vb - vt])

    return not (wl > vr or wt > vb or wr < vl or wb < vt)

