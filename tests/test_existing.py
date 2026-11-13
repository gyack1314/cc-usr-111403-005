"""已有接口的核心、边界及错误路径。"""
import unittest,tempfile
from pathlib import Path
from lake.storage import read_source,Objects,digest

class StorageTests(unittest.TestCase):
    def test_source_and_corruption(self):
        value=read_source()
        with tempfile.TemporaryDirectory() as d:
            o=Objects(d);key=o.put(value);self.assertEqual(o.get(key),value)
            self.assertEqual(o.put(value),key)
            Path(d,key).write_bytes(b'bad')
            with self.assertRaises(ValueError):o.get(key)
    def test_bad_object_identity(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):Objects(d).get('../bad')

from lake.types import check_columns,check_value
from lake.functions import local_call,registry_digest
from lake.wire import pack,unpack

class FeatureTests(unittest.TestCase):
    def test_types_and_function(self):
        check_columns([[1,None]],[{'kind':'int64','nullable':True}],['a','b'])
        self.assertEqual(local_call('double',[[2,None]]),[4,None])
        for x in [True,2**63]:
            with self.assertRaises(ValueError):check_value(x,{'kind':'int64'})
    def test_wire(self):
        m={'query_id':'q','execution_id':1,'call_id':'c','row_ids':['r'],'registry_digest':registry_digest()}
        self.assertEqual(unpack(pack(m)),m)
        with self.assertRaises(ValueError):unpack(pack(m)+b'other')
    def test_local_error(self):
        with self.assertRaises(ValueError):local_call('explode',[[1]])
