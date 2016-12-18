#!/usr/bin/python

'''
Layout module.

This module contains layout handlers which lay windows into different layout
patterns.

To implement a new layout, define a new layout handler and add it to
`LAYOUT_HANDLERZ`.
'''

import subprocess

from wmwm.api import activate_window
from wmwm.api import get_display_geometry
from wmwm.api import hide_desktop
from wmwm.util import printerr

def set_window(id_, x, y, w, h):
    '''
    Set window position and size.

    Parameters
    ----------
    id_
        Window ID.
    x
        x coord.
    y
        y coord.
    w
        Width.
    h
        Height.

    Returns
    -------
    None
        None.
    '''
    # Handle window decoration offsets.
    l, r, t, b = 0, 0, 0, 0
    line = subprocess.check_output([
        'xprop', '-id', str(id_), '_NET_FRAME_EXTENTS',
    ]).decode()
    line = line.strip()
    if line.startswith('_NET_FRAME_EXTENTS'):
        l, r, t, b = [int(x) for x in line.split('=')[1].split(',')]

    # Move and resize window.
    subprocess.check_call([
        'wmctrl',
        '-ir', str(id_),
        '-e', '0,{},{},{},{}'.format(x, y, w - l - r, h - t - b),
    ])

    # Activate window.
    activate_window(id_)

def _order_windows(windows, active_window):
    '''
    Order windows. Active window comes last.

    Parameters
    ----------
    windows
        A dict of windows keyed by ID.
    active_window
        Active window ID.

    Returns
    -------
    list
        A list of windows.
    '''
    ans = []
    tmp = None
    for _, window in windows.items():
        if window['id'] != active_window:
            ans.append(window)
        else:
            tmp = window
    if tmp is not None:
        ans.append(tmp)
    return ans

def cascade(desktop, active_window):
    '''
    Cascade windows.

    Parameters
    ----------
    desktop : dict
        A desktop object.
    active_window : int
        Active window ID.

    Returns
    -------
    None
        None.
    '''
    ngrid = 16  # Magic: Number of grids on each axis.
    nwin = 10   # Magic: Number of grids a window occupies on each axis.

    dp_w, dp_h = get_display_geometry()
    xstep, ystep = dp_w // ngrid, dp_h // ngrid

    windows = desktop['windows']
    if len(windows) == 0:
        return
    x, y, w, h = xstep, ystep, nwin * xstep, nwin * ystep
    for window in _order_windows(windows, active_window):
        set_window(window['id'], x, y, w, h)
        if len(windows) == 1:
            break
        x += (ngrid - 2 - nwin) * xstep // (len(windows) - 1)
        y += (ngrid - 2 - nwin) * ystep // (len(windows) - 1)
    hide_desktop()

def hstack(desktop, active_window):
    '''
    Stack windows horizontally.

    Parameters
    ----------
    desktop : dict
        A desktop object.
    active_window : int
        Active window ID.

    Returns
    -------
    None
        None.
    '''
    windows = desktop['windows']
    if len(windows) == 0:
        return
    x, y, w, h = 0, 0, desktop['wa_w'] // len(windows), desktop['wa_h']
    for window in _order_windows(windows, active_window):
        set_window(window['id'], x, y, w, h)
        x += w
    hide_desktop()

def vstack(desktop, active_window):
    '''
    Stack windows vertically.

    Parameters
    ----------
    desktop : dict
        A desktop object.
    active_window : int
        Active window ID.

    Returns
    -------
    None
        None.
    '''
    windows = desktop['windows']
    if len(windows) == 0:
        return
    x, y, w, h = 0, 0, desktop['wa_w'], desktop['wa_h'] // len(windows)
    for window in _order_windows(windows, active_window):
        set_window(window['id'], x, y, w, h)
        y += h
    hide_desktop()

def tmain(desktop, active_window):
    '''
    Two-row layout, top row is main row.

    Parameters
    ----------
    desktop : dict
        A desktop object.
    active_window : int
        Active window ID.

    Returns
    -------
    None
        None.
    '''
    windows = desktop['windows']
    if len(windows) == 0:
        return

    # Process the active window.
    width = desktop['wa_w']
    height = desktop['wa_h'] // 2
    set_window(active_window, 0, 0, width, height)

    # Process the rest.
    if len(windows) > 1:
        x, y, w, h = 0, height, width // (len(windows) - 1), height
        for i, window in enumerate(_order_windows(windows, active_window)):
            if i == len(windows) - 1:
                break
            set_window(window['id'], x, y, w, h)
            x += w

    hide_desktop()

def bmain(desktop, active_window):
    '''
    Two-row layout, bottom row is main row.

    Parameters
    ----------
    desktop : dict
        A desktop object.
    active_window : int
        Active window ID.

    Returns
    -------
    None
        None.
    '''
    windows = desktop['windows']
    if len(windows) == 0:
        return

    # Process the active window.
    width = desktop['wa_w']
    height = desktop['wa_h'] // 2
    set_window(active_window, 0, height, width, height)

    # Process the rest.
    if len(windows) > 1:
        x, y, w, h = 0, 0, width // (len(windows) - 1), height
        for i, window in enumerate(_order_windows(windows, active_window)):
            if i == len(windows) - 1:
                break
            set_window(window['id'], x, y, w, h)
            x += w

    hide_desktop()
def lmain(desktop, active_window):
    '''
    Two-column layout, left column is main column.

    Parameters
    ----------
    desktop : dict
        A desktop object.
    active_window : int
        Active window ID.

    Returns
    -------
    None
        None.
    '''
    windows = desktop['windows']
    if len(windows) == 0:
        return

    # Process the active window.
    width = desktop['wa_w'] // 2
    height = desktop['wa_h']
    set_window(active_window, 0, 0, width, height)

    # Process the rest.
    if len(windows) > 1:
        x, y, w, h = width, 0, width, height // (len(windows) - 1)
        for i, window in enumerate(_order_windows(windows, active_window)):
            if i == len(windows) - 1:
                break
            set_window(window['id'], x, y, w, h)
            y += h

    hide_desktop()

def rmain(desktop, active_window):
    '''
    Two-column layout, right column is main column.

    Parameters
    ----------
    desktop : dict
        A desktop object.
    active_window : int
        Active window ID.

    Returns
    -------
    None
        None.
    '''
    windows = desktop['windows']
    if len(windows) == 0:
        return

    # Process the active window.
    width = desktop['wa_w'] // 2
    height = desktop['wa_h']
    set_window(active_window, width, 0, width, height)

    # Process the rest.
    if len(windows) > 1:
        x, y, w, h = 0, 0, width, height // (len(windows) - 1)
        for i, window in enumerate(_order_windows(windows, active_window)):
            if i == len(windows) - 1:
                break
            set_window(window['id'], x, y, w, h)
            y += h

    hide_desktop()

def _rowgrid(desktop, active_window, nrows, ncols):
    '''
    Grid layout, row-major.

    Parameters
    ----------
    desktop : dict
        A desktop object.
    active_window : int
        Active window ID.
    nrows:
        Number of rows.
    ncols:
        Number of cols.

    Returns
    -------
    None
        None.
    '''
    windows = desktop['windows']
    if len(windows) == 0:
        return

    if nrows * ncols < len(windows):
        printerr('Warning: Not enough space. Windows may overlap.')

    width = desktop['wa_w'] // ncols
    height = desktop['wa_h'] // nrows
    x, y, w, h = 0, 0, width, height
    for i, window in enumerate(_order_windows(windows, active_window)):
        y, x = divmod(i % (nrows * ncols), ncols)
        x *= width
        y *= height
        set_window(window['id'], x, y, w, h)
    hide_desktop()

def rowgrid22(desktop, active_window):
    return _rowgrid(desktop, active_window, 2, 2)
def rowgrid23(desktop, active_window):
    return _rowgrid(desktop, active_window, 2, 3)
def rowgrid24(desktop, active_window):
    return _rowgrid(desktop, active_window, 2, 4)
def rowgrid32(desktop, active_window):
    return _rowgrid(desktop, active_window, 3, 2)
def rowgrid33(desktop, active_window):
    return _rowgrid(desktop, active_window, 3, 3)
def rowgrid34(desktop, active_window):
    return _rowgrid(desktop, active_window, 3, 4)
def rowgrid42(desktop, active_window):
    return _rowgrid(desktop, active_window, 4, 2)
def rowgrid43(desktop, active_window):
    return _rowgrid(desktop, active_window, 4, 3)
def rowgrid44(desktop, active_window):
    return _rowgrid(desktop, active_window, 4, 4)

def _colgrid(desktop, active_window, nrows, ncols):
    '''
    Grid layout, col-major.

    Parameters
    ----------
    desktop : dict
        A desktop object.
    active_window : int
        Active window ID.
    nrows:
        Number of rows.
    ncols:
        Number of cols.

    Returns
    -------
    None
        None.
    '''
    windows = desktop['windows']
    if len(windows) == 0:
        return

    if nrows * ncols < len(windows):
        printerr('Warning: Not enough space. Windows may overlap.')

    width = desktop['wa_w'] // ncols
    height = desktop['wa_h'] // nrows
    x, y, w, h = 0, 0, width, height
    for i, window in enumerate(_order_windows(windows, active_window)):
        x, y = divmod(i % (nrows * ncols), nrows)
        x *= width
        y *= height
        set_window(window['id'], x, y, w, h)
    hide_desktop()

def colgrid22(desktop, active_window):
    return _colgrid(desktop, active_window, 2, 2)
def colgrid23(desktop, active_window):
    return _colgrid(desktop, active_window, 2, 3)
def colgrid24(desktop, active_window):
    return _colgrid(desktop, active_window, 2, 4)
def colgrid32(desktop, active_window):
    return _colgrid(desktop, active_window, 3, 2)
def colgrid33(desktop, active_window):
    return _colgrid(desktop, active_window, 3, 3)
def colgrid34(desktop, active_window):
    return _colgrid(desktop, active_window, 3, 4)
def colgrid42(desktop, active_window):
    return _colgrid(desktop, active_window, 4, 2)
def colgrid43(desktop, active_window):
    return _colgrid(desktop, active_window, 4, 3)
def colgrid44(desktop, active_window):
    return _colgrid(desktop, active_window, 4, 4)

# Layout handlers.
LAYOUT_HANDLERZ = {
    'cascade': cascade,
    'hstack': hstack,
    'vstack': vstack,
    'bmain': bmain,
    'lmain': lmain,
    'rmain': rmain,
    'tmain': tmain,
    'rowgrid22': rowgrid22,
    'rowgrid23': rowgrid23,
    'rowgrid24': rowgrid24,
    'rowgrid32': rowgrid32,
    'rowgrid33': rowgrid33,
    'rowgrid34': rowgrid34,
    'rowgrid42': rowgrid42,
    'rowgrid43': rowgrid43,
    'rowgrid44': rowgrid44,
    'colgrid22': colgrid22,
    'colgrid23': colgrid23,
    'colgrid24': colgrid24,
    'colgrid32': colgrid32,
    'colgrid33': colgrid33,
    'colgrid34': colgrid34,
    'colgrid42': colgrid42,
    'colgrid43': colgrid43,
    'colgrid44': colgrid44,
}
