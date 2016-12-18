#!/usr/bin/python

'''Utility module.'''

import sys

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
    window : dict
        A window object having fields: x, y, w, h.
    viewport : dict
        A viewport object having fields: x, y, w, h.

    Returns
    -------
    bool
        True iff window is in viewport.
    '''
    wl = window['x']
    wt = window['y']
    wr = window['x'] + window['w']
    wb = window['y'] + window['h']

    vl = viewport['x']
    vt = viewport['y']
    vr = viewport['x'] + viewport['w']
    vb = viewport['y'] + viewport['h']

    return not (wl > vr or wt > vb or wr < vl or wb < vt)

