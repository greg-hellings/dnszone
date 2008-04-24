# encoding: utf-8

'''zone_reload

A wrapper around 'rndc' for requesting zone reloads from named.

Example::

    >>> from easyzone.zone_reload import ZoneReload
    >>> r = ZoneReload()
    >>> r.reload('example.com')
    zone reload up-to-date
    >>> r.reload('foo.com')
    rndc: 'reload' failed: not found
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "easyzone/zone_reload.py", line 51, in reload
        raise ZoneReloadError("rndc failed with return code %d" % r)
    easyzone.zone_reload.ZoneReloadError: rndc failed with return code 1
    >>> 
    >>> r = ZoneReload(rndc='/usr/sbin/rndc')
    >>> r.reload('example.com')
    zone reload up-to-date
    >>>
'''

__author__ = 'Chris Miles'
__copyright__ = '(c) Chris Miles 2007'
__id__ = '$Id$'
__url__ = '$URL$'
__version__ = '1.0'


# ---- Imports ----

# - Python Modules -
import subprocess


# ---- Exceptions ----

class ZoneReloadError(Exception):
    '''An error occurred within ZoneReload.
    '''


# ---- Classes ----

class ZoneReload(object):
    '''A wrapper around bind's rndc utility, used for reloading a modified
    DNS zone.
    
    `rndc` : string containing path to rndc binary.  Or leave as "rndc"
    to search with default PATH.
    '''
    def __init__(self, rndc='rndc'):
        self.rndc = rndc
    
    def reload(self, zone):
        '''Ask named to perform a zone reload by calling the
        rndc commmand.
        '''
        cmd = [
            self.rndc,
            'reload',
            zone
        ]
        
        r = subprocess.call(cmd)
        
        if r != 0:
            raise ZoneReloadError("rndc failed with return code %d" % r)
    

