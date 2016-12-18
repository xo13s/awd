#!/usr/bin/python

'''Low-level API module.'''

import subprocess

def get_active_window():
    '''
    Get active window ID.

    Returns
    -------
    int
        Active window ID.
    '''
    line = subprocess.check_output([
        'xdotool', 'getactivewindow',
    ]).decode().strip()
    return int(line)

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
