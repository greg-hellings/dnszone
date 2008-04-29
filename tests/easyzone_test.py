#!/usr/bin/env python
# encoding: utf-8
"""
easyzone_test.py

Created by Chris Miles on 2007-01-29.
Copyright (c) 2007 Chris Miles. All rights reserved.
"""

import os
import tempfile
import types
import unittest

from easyzone.easyzone import Name, SOA, Zone, RecordsError, ZoneError, zone_from_file



class BasicZoneTest(unittest.TestCase):
    def test_missing_dot(self):
        zone = Zone('example.com')
        self.failUnlessEqual(zone.domain, 'example.com.')
    
    def test_empty_domain(self):
        self.failUnlessRaises(ZoneError, Zone, '')
    
    def test_bad_domain(self):
        self.failUnlessRaises(ZoneError, Zone, 29873)
    
    def test_unicode_domain(self):
        zone = Zone(u'example.com')
        self.failUnlessEqual(zone.domain, u'example.com.')
    

class ZoneLoadTest(unittest.TestCase):
    def setUp(self):
        self.zone = Zone('example.com.')
        zone_file = os.path.join(os.path.dirname(__file__), 'files', 'example.com')
        self.zone.load_from_file(zone_file)
    
    def test_type(self):
        self.failUnlessEqual(type(self.zone), Zone)
    
    def test_domain(self):
        self.failUnlessEqual(self.zone.domain, 'example.com.')
    
    def test_root_type(self):
        root = self.zone.root
        self.failUnlessEqual(type(root), Name)
    
    def test_root_name(self):
        root = self.zone.root
        self.failUnlessEqual(root.name, '@')
    
    def test_soa_type(self):
        soa = self.zone.root.soa
        self.failUnlessEqual(type(soa), SOA)
    
    def test_soa_mname(self):
        self.failUnlessEqual(self.zone.root.soa.mname, 'ns1.example.com.')
    
    def test_soa_rname(self):
        self.failUnlessEqual(self.zone.root.soa.rname, 'hostmaster.example.com.')
    
    def test_soa_serial(self):
        self.failUnlessEqual(self.zone.root.soa.serial, 2007012501)
    
    def test_soa_refresh(self):
        self.failUnlessEqual(self.zone.root.soa.refresh, 28800)
    
    def test_soa_retry(self):
        self.failUnlessEqual(self.zone.root.soa.retry, 7200)
    
    def test_soa_expire(self):
        self.failUnlessEqual(self.zone.root.soa.expire, 864000)
    
    def test_soa_minttl(self):
        self.failUnlessEqual(self.zone.root.soa.minttl, 86400)
    
    def test_root_records_A(self):
        records = self.zone.root.records('A').items
        self.failUnlessEqual(records, ['10.0.0.1'])
    
    def test_root_records_NS(self):
        records = self.zone.root.records('NS').items
        self.failUnlessEqual(records, ['ns1.example.com.', 'ns2.example.com.'])
    
    def test_root_records_MX(self):
        records = self.zone.root.records('MX').items
        self.failUnlessEqual(records, [(10, 'mail.example.com.'), (20, 'mail2.example.com.')])
    
    def test_names_type(self):
        names = self.zone.names
        self.failUnlessEqual(type(names), types.DictType)
    
    def test_names_foo_A(self):
        records = self.zone.names['foo.example.com.'].records('A').items
        self.failUnlessEqual(records, ['10.0.0.1'])
    
    def test_names_foo_MX(self):
        records = self.zone.names['foo.example.com.'].records('MX').items
        self.failUnlessEqual(records, [(10, 'mail.example.com.')])
    
    def test_names_bar_A(self):
        records = self.zone.names['bar.example.com.'].records('A').items
        self.failUnlessEqual(records, ['10.0.0.2', '10.0.0.3'])
    
    def test_names_foofoo_CNAME(self):
        records = self.zone.names['foofoo.example.com.'].records('CNAME').items
        self.failUnlessEqual(records, ['foo.example.com.'])
    
    def test_names_root_A(self):
        records = self.zone.names['example.com.'].records('A').items
        self.failUnlessEqual(records, ['10.0.0.1'])
    
    def test_names_root_NS(self):
        records = self.zone.names['example.com.'].records('NS').items
        self.failUnlessEqual(records, ['ns1.example.com.', 'ns2.example.com.'])
    
    def test_names_root_MX(self):
        records = self.zone.names['example.com.'].records('MX').items
        self.failUnlessEqual(records, [(10, 'mail.example.com.'), (20, 'mail2.example.com.')])
    

class ZoneLoadFunctionTest(unittest.TestCase):
    '''Another load test to test the module function zone_from_file().
    '''
    def setUp(self):
        zone_file = os.path.join(os.path.dirname(__file__), 'files', 'example.com')
        self.zone = zone_from_file('example.com', zone_file)
    
    def test_type(self):
        self.failUnlessEqual(type(self.zone), Zone)
    
    def test_domain(self):
        self.failUnlessEqual(self.zone.domain, 'example.com.')
    
    def test_root_type(self):
        root = self.zone.root
        self.failUnlessEqual(type(root), Name)
    


class ZoneModifyTest(unittest.TestCase):
    def setUp(self):
        self.zone = Zone('example.com.')
        zone_file = os.path.join(os.path.dirname(__file__), 'files', 'example.com')
        self.zone.load_from_file(zone_file)
    
    def test_root_add_NS(self):
        # add another NS record to @
        self.zone.root.records('NS').add('ns3.example.com.')
        records = self.zone.names['example.com.'].records('NS').items
        self.failUnlessEqual(records, ['ns1.example.com.', 'ns2.example.com.', 'ns3.example.com.'])
    
    def test_root_add_duplicate_NS(self):
        # add a duplicate NS record to @ - has no effect
        self.zone.root.records('NS').add('ns1.example.com.')
        records = self.zone.names['example.com.'].records('NS').items
        self.failUnlessEqual(records, ['ns1.example.com.', 'ns2.example.com.'])
    
    def test_root_delete_NS(self):
        # delete NS record from @
        self.zone.root.records('NS').delete('ns2.example.com.')
        records = self.zone.names['example.com.'].records('NS').items
        self.failUnlessEqual(records, ['ns1.example.com.'])
    
    def test_root_delete_noexist_NS(self):
        # delete non-existent NS record from @
        self.failUnlessRaises(RecordsError, self.zone.root.records('NS').delete, 'ns99.example.com.')
    
    def test_root_add_A(self):
        # add another A record to @
        self.zone.root.records('A').add('10.2.3.4')
        records = self.zone.names['example.com.'].records('A').items
        self.failUnlessEqual(records, ['10.0.0.1', '10.2.3.4'])
    
    def test_names_add_root_MX(self):
        # add MX record to @ via names attribute
        self.zone.names['example.com.'].records('MX').add( (30, 'mail3.example.com.') )
        records = self.zone.names['example.com.'].records('MX').items
        self.failUnlessEqual(records, [(10, 'mail.example.com.'), (20, 'mail2.example.com.'), (30, 'mail3.example.com.')])
    
    def test_names_delete_root_MX(self):
        # delete MX record from @ via names attribute
        self.zone.names['example.com.'].records('MX').delete( (10, 'mail.example.com.') )
        records = self.zone.names['example.com.'].records('MX').items
        self.failUnlessEqual(records, [(20, 'mail2.example.com.')])
    
    def test_names_add_bar_A(self):
        # add A record to bar.example.com.
        self.zone.names['bar.example.com.'].records('A').add('10.20.30.40')
        records = self.zone.names['bar.example.com.'].records('A').items
        self.failUnlessEqual(records, ['10.0.0.2', '10.0.0.3', '10.20.30.40'])
    
    def test_names_delete_bar_A(self):
        # delete A record from bar.example.com.
        self.zone.names['bar.example.com.'].records('A').delete('10.0.0.2')
        records = self.zone.names['bar.example.com.'].records('A').items
        self.failUnlessEqual(records, ['10.0.0.3'])
    
    def test_names_add_poppy_CNAME(self):
        # add CNAME record poppy.example.com.
        self.zone.add_name('poppy.example.com.')
        self.zone.names['poppy.example.com.'].records('CNAME', create=True).add('bar.example.com.')
        records = self.zone.names['poppy.example.com.'].records('CNAME').items
        self.failUnlessEqual(records, ['bar.example.com.'])
    
    def test_names_add_bar_MX(self):
        # add MX record to bar.example.com.
        self.zone.names['bar.example.com.'].records('MX', create=True).add( (100, 'backupmx.example.com.') )
        records = self.zone.names['bar.example.com.'].records('MX').items
        self.failUnlessEqual(records, [(100, 'backupmx.example.com.')])
    
    def test_names_delete_foo_MX(self):
        # delete MX record from foo.example.com.
        self.zone.names['foo.example.com.'].records('MX').delete( (10, 'mail.example.com.') )
        records = self.zone.names['foo.example.com.'].records('MX').items
        self.failUnlessEqual(records, [])
    
    def test_names_bar_NS(self):
        # try to fetch NS records from bar.example.com. - should fail (non-root nodes can't contain NS records)
        node = self.zone.names['bar.example.com.'].records('NS')
        self.failUnlessEqual(node, None)
    
    def test_names_replace_foo_MX(self):
        # replace MX record for foo.example.com.
        mx = self.zone.names['foo.example.com.'].records('MX')
        mx.delete( (10, 'mail.example.com.') )
        mx.add( (30, 'anothermail.example.com.') )
        records = self.zone.names['foo.example.com.'].records('MX').items
        self.failUnlessEqual(records, [(30, 'anothermail.example.com.')])
    
    def test_add_name_zip_A(self):
        # add new name zip.example.com. with A record
        self.zone.add_name('zip.example.com.')
        self.zone.names['zip.example.com.'].records('A', create=True).add('10.9.8.7')
        records = self.zone.names['zip.example.com.'].records('A').items
        self.failUnlessEqual(records, ['10.9.8.7'])
    
    def test_delete_name_foo(self):
        # delete name foo.example.com. from zone (and hence all associated nodes for that name)
        self.zone.delete_name('foo.example.com.')
        self.failUnlessEqual(self.zone.names.keys(), ['foofoo.example.com.', 'bar.example.com.', 'example.com.'])
    
    def test_names_bar_clear_all_records(self):
        # clear all records for bar.example.com.
        self.zone.names['bar.example.com.'].clear_all_records()
        self.failUnlessEqual(self.zone.names.keys(), ['foo.example.com.', 'foofoo.example.com.', 'bar.example.com.', 'example.com.'])
        self.failUnlessEqual(self.zone.names['bar.example.com.'].records('A'), None)
    
    def test_names_foo_clear_all_records_exclude(self):
        # clear records for foo.example.com. excluding some
        self.zone.names['foo.example.com.'].clear_all_records(exclude='MX')
        self.failUnlessEqual(self.zone.names.keys(), ['foo.example.com.', 'foofoo.example.com.', 'bar.example.com.', 'example.com.'])
        self.failUnlessEqual(self.zone.names['foo.example.com.'].records('A'), None)
        self.failUnlessEqual(self.zone.names['foo.example.com.'].records('MX').items, [(10, 'mail.example.com.')])
    
    def test_names_add_bar_TXT_simple(self):
        # add simple TXT record to bar.example.com.
        self.zone.names['bar.example.com.'].records('TXT', create=True).add('"v=spf1 a mx ?all"')
        records = self.zone.names['bar.example.com.'].records('TXT').items
        self.failUnlessEqual(records, ['"v=spf1 a mx ?all"'])
    
    def test_names_add_bar_TXT_with_periods(self):
        # add TXT record to bar.example.com. containing periods
        self.zone.names['bar.example.com.'].records('TXT', create=True).add('"v=spf1 a mx include:mailseat.com include:cluster3.eu.messagelabs.com ?all"')
        records = self.zone.names['bar.example.com.'].records('TXT').items
        self.failUnlessEqual(records, ['"v=spf1 a mx include:mailseat.com include:cluster3.eu.messagelabs.com ?all"'])
    
    def test_names_add_bar_TXT_no_quotes(self):
        # add TXT record to bar.example.com. excluding surrounding quotes
        self.zone.names['bar.example.com.'].records('TXT', create=True).add('v=spf1 a mx include:mailseat.com include:cluster3.eu.messagelabs.com ?all')
        records = self.zone.names['bar.example.com.'].records('TXT').items
        self.failUnlessEqual(records, ['"v=spf1 a mx include:mailseat.com include:cluster3.eu.messagelabs.com ?all"'])
    


class ZoneModifySaveTest(unittest.TestCase):
    def setUp(self):
        self.zone = Zone('example.com.')
        zone_file = os.path.join(os.path.dirname(__file__), 'files', 'example.com')
        self.zone.load_from_file(zone_file)
        
        self.zone.root.soa.mname = 'mname.example.com.'
        self.zone.root.soa.rname = 'rname.example.com.'
        self.zone.root.soa.serial += 1
        self.zone.root.soa.refresh = 1
        self.zone.root.soa.retry = 2
        self.zone.root.soa.expire = 3
        self.zone.root.soa.minttl = 4
        
        self.zone.add_name('zip.example.com.')
        self.zone.names['zip.example.com.'].records('A', create=True).add('10.9.8.7')
        
        mx = self.zone.names['foo.example.com.'].records('MX')
        mx.delete( (10, 'mail.example.com.') )
        mx.add( (30, 'anothermail.example.com.') )
        
        self.zone.names['bar.example.com.'].records('A').add('10.20.30.40')
        
        self.zone.delete_name('foofoo.example.com.')
        
        self.saved_filename = tempfile.mkstemp()[1]
        # self.saved_filename = '/var/tmp/foo.tmp'
        self.zone.save(self.saved_filename)
    
    def test_file_exists(self):
        self.failUnless(os.path.exists(self.saved_filename))
    
    def test_file_size(self):
        size = os.stat(self.saved_filename)[6]
        self.failUnlessEqual(size, 299)
    
    def test_save_autoserial_greater(self):
        saved_filename = tempfile.mkstemp()[1]
        self.zone.save(saved_filename, autoserial=True)
        
        z = Zone('example.com.')
        z.load_from_file(saved_filename)
        self.failUnless(z.root.soa.serial >= self.zone.root.soa.serial)
    






if __name__ == '__main__':
    unittest.main()