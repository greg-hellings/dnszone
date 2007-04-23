easyzone
========

Overview
--------

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

  $ easy_install dnspython
  $ easy_install easyzone


Example
-------

>>> from easyzone import easyzone
>>> z = easyzone.zone_from_file('example.com', '/var/namedb/example.com')
>>> z.domain
'example.com.'
>>> z.root.soa.serial
2007012902L
>>> z.root.records
{'NS' : ['ns1.example.com.', 'ns2.example.com.'], 'MX' : [(10, 'mail.example.com.'), (20, 'mail2.example.com.')]}
>>> z.names['foo'].records
{'A' : ['10.0.0.1'], 'MX' : [(10, 'mail.example.com.')]}

>>> ns = z.root.records('NS')
>>> ns.add('ns3.example.com.')
>>> [r for r in z.root.records('NS')]
['ns1.example.com.', 'ns2.example.com.', 'ns3.example.com.']
>>> ns.delete('ns2.example.com')
>>> [r for r in z.root.records('NS')]
['ns1.example.com.', 'ns3.example.com.']
