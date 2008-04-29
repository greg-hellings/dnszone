easyzone
========

Overview
--------

Easyzone is a package to manage the common record types of a
zone file, including SOA records.  This module sits on top of
the dnspython package and provides a higher level abstraction
for common zone file manipulation use cases.

Main features:

* A high-level abstraction on top of dnspython.
* Load a zone file into objects.
* Modify/add/delete zone/record objects.
* Save back to zone file.
* Auto-update serial (if necessary).


Requirements
------------

  * dnspython - http://www.dnspython.org/


Build/Test/Install
------------------

Build::

  $ python setup.py build

Test::

  $ python setup.py test

Install::

  $ python setup.py install


OR with setuptools::

  $ easy_install easyzone


Examples
--------

easyzone::

  >>> from easyzone import easyzone
  >>> z = easyzone.zone_from_file('example.com', '/var/namedb/example.com')
  >>> z.domain
  'example.com.'
  >>> z.root.soa.serial
  2007012902L
  >>> z.root.records('NS').items
  ['ns1.example.com.', 'ns2.example.com.']
  >>> z.root.records('MX').items
  [(10, 'mail.example.com.'), (20, 'mail2.example.com.')]
  >>> z.names['foo.example.com.'].records('A').items
  ['10.0.0.1']

  >>> ns = z.root.records('NS')
  >>> ns.add('ns3.example.com.')
  >>> ns.items
  ['ns1.example.com.', 'ns2.example.com.', 'ns3.example.com.']
  >>> ns.delete('ns2.example.com')
  >>> ns.items
  ['ns1.example.com.', 'ns3.example.com.']

  >>> z.save(autoserial=True)

ZoneCheck::

  >>> from easyzone.zone_check import ZoneCheck
  >>> c = ZoneCheck()
  >>> c.isValid('example.com', '/var/named/zones/example.com')
  True
  >>> c.isValid('foo.com', '/var/named/zones/example.com')
  False
  >>> c.error
  'Bad syntax'
  >>> 
  >>> c = ZoneCheck(checkzone='/usr/sbin/named-checkzone')
  >>> c.isValid('example.com', '/var/named/zones/example.com')
  True
  >>>

ZoneReload::

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
