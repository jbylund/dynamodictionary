import os
import random
import unittest
from string import ascii_lowercase

import dynamodict

random.seed(0)


def randstr():
    return "".join(random.choice(ascii_lowercase) for _ in range(20))


class TestDynamodictionary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cwd = os.getcwd()
        assert cwd in dynamodict.__file__
        cls.test_table_name = "test_" + randstr()
        cls.mytable = dynamodict.DynamoDictionary(cls.test_table_name)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_testing_right_thing(self):
        assert os.getcwd() in dynamodict.__file__

    def test_construction(self):
        pass  # was constructed in setUpClass

    def test_coverage(self):
        dynamodict_methods = [
            x
            for x in dir(self.mytable)
            if hasattr(getattr(self.mytable, x), '__call__') and not x.startswith('_')
        ]
        test_methods = [x[5:] for x in dir(self) if x.startswith('test_')]
        untested = set(dynamodict_methods) - set(test_methods)
        if untested:
            raise AssertionError("Following dynamodict methods are not tested: {}".format(", ".join(sorted(untested))))

    def test_clear(self):
        self.mytable.clear()
        assert 0 == len(self.mytable)
        for _ in range(100):
            self.mytable[randstr()] = randstr()
        assert 100 == len(self.mytable)
        self.mytable.clear()
        assert 0 == len(self.mytable)

    def test_create_table(self):
        pass

    def test_drop_table(self):
        pass

    def test_get(self):
        self.mytable['foo'] = 'bar'
        assert self.mytable.get('foo') == 'bar'
        self.mytable.clear()
        assert self.mytable.get('foo') is None

    def test_items(self):
        self.mytable.clear()
        keys = sorted(randstr() for _ in range(10))
        for ikey in keys:
            self.mytable[ikey] = ikey
        assert sorted(self.mytable.items()) == sorted({ikey: ikey for ikey in keys}.items())

    def test_iteritems(self):
        pass

    def test_iterkeys(self):
        pass

    def test_itervalues(self):
        pass

    def test_keys(self):
        pass

    def test_len(self):
        self.mytable.clear()
        assert 0 == len(self.mytable)
        for _ in range(20):
            self.mytable[randstr()] = randstr()
        assert 20 == len(self.mytable)
        self.mytable.clear()

    def test_multi_delete(self):
        pass

    def test_pop(self):
        self.mytable.clear()
        sentinel = object()
        assert sentinel is self.mytable.pop(randstr(), sentinel)
        with self.assertRaises(KeyError):
            self.mytable.pop(randstr())
        key = randstr()
        self.mytable[key] = key
        assert self.mytable.pop(key) == key
        with self.assertRaises(KeyError):
            self.mytable.pop(key)

    def test_values(self):
        pass
