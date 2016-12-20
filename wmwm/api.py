#!/usr/bin/python

'''Low-level API module.'''

import subprocess

from Xlib import Xatom
from Xlib.display import Display
from ewmh import EWMH

# Maximum property value length (in bytes).
MAX_PROPERTY_VALUE_LEN = 4096

# Display object.
disp = None

# EWMH object.
ewmh = None

def _get_display():
    '''
    Get the display object.

    Returns
    -------
    object
        The display object.
    '''
    global disp
    if disp is None:
        disp = Display()
    return disp

def _get_ewmh():
    '''
    Get the EWMH object.

    Returns
    -------
    object
        The EWMH object.
    '''
    global ewmh
    if ewmh is None:
        ewmh = EWMH()
    return ewmh

def get_windows():
    '''
    Get all X Windows managed by the Window Manager.

    Sticky windows are excluded.

    Returns
    -------
    list
        A list of windows managed by the Window Manager.
    '''
    ewmh = _get_ewmh()
    windows = []
    for w in ewmh.getClientList():
        wm_state = ewmh.getWmState(w, True)
        if '_NET_WM_STATE_STICKY' not in wm_state:
            windows.append(w)
    return windows

def get_desktop_geometry():
    '''
    Get the common size of all desktops.

    Returns
    -------
    list
        The common size of all desktops.
    '''
    ewmh = _get_ewmh()
    return list(ewmh.getDesktopGeometry())

def get_desktop_viewport():
    '''
    Get the top left corner of each desktop's viewport.

    Returns
    -------
    list
        The [top, left] corner of each desktop's viewport.
    '''
    ewmh = _get_ewmh()
    return list(ewmh.getDesktopViewPort())

def get_current_desktop():
    '''
    Get the index of the current desktop.

    Returns
    -------
    int
        The index of the current desktop.
    '''
    ewmh = _get_ewmh()
    return ewmh.getCurrentDesktop()

def get_active_window():
    '''
    Get the active window.

    Returns
    -------
    object
        The active window object.
    '''
    ewmh = _get_ewmh()
    return ewmh.getActiveWindow()

def get_wm_desktop(window):
    '''
    Get the desktop the window is in.

    Parameters
    ----------
    object
        A window object.

    Returns
    -------
    int
        A desktop number.
    '''
    ewmh = _get_ewmh()
    return ewmh.getWmDesktop(window)

def set_active_window(window):
    '''
    Set the active window.

    Parameters
    ----------
    window : object
        A window object.

    Returns
    -------
    None
        None.
    '''
    ewmh = _get_ewmh()
    ewmh.setActiveWindow(window)
    ewmh.display.flush()

############################

def activate_window(id_):
    '''
    Activate window.

    Parameters
    ----------
    id_
        Window ID.
    '''
    subprocess.check_call([
        'xdotool', 'windowactivate', str(id_),
    ])

def get_display_geometry():
    '''
    Get display geometry.

    Returns
    -------
    list
        Display geometry '[w, h]'.
    '''
    line = subprocess.check_output([
        'xdotool', 'getdisplaygeometry',
    ]).decode().strip()
    return [int(x) for x in line.split()]

def hide_desktop():
    '''
    Turn off *show desktop*.

    Hiding desktop actually means showing windows.
    '''
    subprocess.check_call([
        'wmctrl', '-k', 'off',
    ])

def set_fullscreen(id_, op):
    '''
    Add/Remove/Toggle fullscreen property of a window.

    Parameters
    ----------
    id_ : int
        Window ID.
    op : str
        Operation: 'on', 'off' or 'toggle'.
    '''
    if op == 'on':
        op = 'add'
    elif op == 'off':
        op = 'remove'
    elif op == 'toggle':
        op = 'toggle'
    else:
        raise Exception('invalid operation {}'.format(op))

    subprocess.check_call([
        'wmctrl',
        '-ir', str(id_),
        '-b', '{},fullscreen'.format(op),
    ])

def set_maximized(id_, op):
    '''
    Add/Remove/Toggle maximized property of a window.

    Parameters
    ----------
    id_ : int
        Window ID.
    op : str
        Operation: 'on', 'off' or 'toggle'.
    '''
    if op == 'on':
        op = 'add'
    elif op == 'off':
        op = 'remove'
    elif op == 'toggle':
        op = 'toggle'
    else:
        raise Exception('invalid operation {}'.format(op))

    subprocess.check_call([
        'wmctrl',
        '-ir', str(id_),
        '-b', '{},maximized_horz,maximized_vert'.format(op),
    ])

def get_window_size(id_):
    '''
    Get window width and height.
    '''
    pass

def set_window_size(id_, w, h):
    '''
    Set window size.

    Parameters
    ----------
    id_ : int
        Window ID.
    w : int
        Window width.
    h : int
        Window height.
    '''
    subprocess.check_call([
        'xdotool', 'windowsize', str(id_), str(w), str(h),
    ])
