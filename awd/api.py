#!/usr/bin/env python3

'''
ewmh api module;
'''

from ewmh_ext import EWMH
import logging_ext as logging

##  ewmh object;
ewmh = None

def _get_ewmh():

    '''
    get the ewmh object;
    '''

    global ewmh
    if ewmh is None:
        ewmh = EWMH()
    return ewmh

#def get_desktop_geometry():
#    '''
#    Get the common size of all desktops.
#
#    Returns
#    -------
#    list
#        The common size of all desktops.
#    '''
#    ewmh = _get_ewmh()
#    return list(ewmh.getDesktopGeometry())
#
#def get_desktop_viewport():
#    '''
#    Get the top left corner of each desktop's viewport.
#
#    Returns
#    -------
#    list
#        The [top, left] corner of each desktop's viewport.
#    '''
#    ewmh = _get_ewmh()
#    return list(ewmh.getDesktopViewPort())
#
#def get_current_desktop():
#    '''
#    Get the index of the current desktop.
#
#    Returns
#    -------
#    int
#        The index of the current desktop.
#    '''
#    ewmh = _get_ewmh()
#    return ewmh.getCurrentDesktop()
#
#def get_active_window():
#    '''
#    Get the active window.
#
#    Returns
#    -------
#    object
#        The active window object.
#    '''
#    ewmh = _get_ewmh()
#    return ewmh.getActiveWindow()
#
#def get_workarea():
#    '''
#    Get the work area.
#
#    Returns
#    -------
#    list
#        The work area [x, y, w, h].
#    '''
#    ewmh = _get_ewmh()
#    return list(ewmh.getWorkArea())
#
#def get_wm_name(window):
#    '''
#    Get name of the window.
#
#    Parameters
#    ----------
#    window : object
#        A window object.
#
#    Returns
#    -------
#    str
#        Name of the window.
#    '''
#    ewmh = _get_ewmh()
#    return ewmh.getWmName(window).decode()
#
#def get_wm_desktop(window):
#    '''
#    Get the desktop the window is in.
#
#    Parameters
#    ----------
#    window : object
#        A window object.
#
#    Returns
#    -------
#    int
#        A desktop number.
#    '''
#    ewmh = _get_ewmh()
#    return ewmh.getWmDesktop(window)
#
#def set_active_window(window):
#    '''
#    Set the active window.
#
#    Parameters
#    ----------
#    window : object
#        A window object.
#
#    Returns
#    -------
#    None
#        None.
#    '''
#    ewmh = _get_ewmh()
#    ewmh.setActiveWindow(window)
#    ewmh.display.flush()
#
#def move_resize_window(window, x, y, w, h):
#    '''
#    Changes the size and location of the specified window.
#
#    Parameters
#    ----------
#    window
#        A window object.
#    x
#        X coord.
#    y
#        Y coord.
#    w
#        Width.
#    h
#        Height.
#
#    Returns
#    -------
#    None
#        None.
#    '''
#    ewmh = _get_ewmh()
#    window.configure(x=x, y=y, width=w, height=h)
#    ewmh.display.flush()

def get_windows(excludes=None):

    '''
    get windows in current desktop;

    ## params

    excludes:list
    :   window name exclude pattern;

    ## return

    :list
    :   a list of windows;
    '''

    ewmh = _get_ewmh()
    desktop = ewmh.getCurrentDesktop()

    windows = []
    for w in ewmh.getClientList():
        w_type = ewmh.getWmWindowType(w, True)
        w_state = ewmh.getWmState(w, True)
        w_desktop = ewmh.getWmDesktop(w)
        w_name = ewmh.getWmName(w)

        if '_NET_WM_WINDOW_TYPE_DESKTOP' in w_type:
            continue
        elif '_NET_WM_WINDOW_TYPE_DOCK' in w_type:
            continue

        if '_NET_WM_STATE_STICKY' in w_state:
            continue

        if desktop != w_desktop:
            continue

        if excludes is not None:
            if any((e in w_name for e in excludes)):
                continue

        windows.append(w)
    return windows

def place_window(window, x, y, w, h):

    '''
    place a window; coords include borders;
    '''

    ewmh = _get_ewmh()
    ewmh.setWmState(window, 0, '_NET_WM_STATE_MAXIMIZED_HORZ')
    ewmh.setWmState(window, 0, '_NET_WM_STATE_MAXIMIZED_VERT')
    ewmh.setWmState(window, 0, '_NET_WM_STATE_FULLSCREEN')
    l, r, t, b = ewmh.getFrameExtents(window) or (0, 0, 0, 0)
    ewmh.setMoveResizeWindow(window, 0, x + l, y + t, w - l - r, h - t - b)
    ewmh.display.flush()

def _layout_cascade(windows):

    '''
    layout: cascade;
    '''

    ewmh = _get_ewmh()
    desktop = ewmh.getCurrentDesktop()
    x, y, w, h = ewmh.getWorkArea()[4 * desktop:4 * (desktop + 1)]
    n = len(windows)

    for window in windows:
        place_window(window, x, y, w // 2, h // 2)
        x, y = x + w // 2 // (n - 1), y + h // 2 // (n - 1)

def _layout_horizontal(windows):

    '''
    layout: horizontal;
    '''

    ewmh = _get_ewmh()
    desktop = ewmh.getCurrentDesktop()
    x, y, w, h = ewmh.getWorkArea()[4 * desktop:4 * (desktop + 1)]
    n = len(windows)

    for window in windows:
        place_window(window, x, y, w // n, h // 1)
        x, y = x + w // (n - 1), y + h // (n - 1)

def _layout_vertical(windows):
    pass

def _layout_left(windows):
    pass

def _layout_right(windows):
    pass

def _layout_top(windows):
    pass

def _layout_bottom(windows):
    pass

def _layout_grid(windows):
    pass

def layout_windows(windows, layout):

    '''
    layout windows;
    '''

    handlers = {
        'cascade'   : _layout_cascade,
        'horizontal': _layout_horizontal,
        'vertical'  : _layout_vertical,
        'left'      : _layout_left,
        'right'     : _layout_right,
        'top'       : _layout_top,
        'bottom'    : _layout_bottom,
        'grid'      : _layout_grid,
    }

    handler = handlers.get(layout)

    if handler is None:
        die('invalid layout: {}'.format(layout))

    handler(windows)

