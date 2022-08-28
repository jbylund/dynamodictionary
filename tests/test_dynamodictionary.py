import datetime
import os
import random
import sys
import unittest
from string import ascii_lowercase

sys.path = ["./src"] + sys.path
import dynamodict

if "site-packages" in dynamodict.__file__:
    raise AssertionError("import is wrong")

# random.seed(0)


def randstr():
    return "".join(random.choice(ascii_lowercase) for _ in range(20))


class TestDynamodictionary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cwd = os.getcwd()
        # assert cwd in dynamodict.__file__
        cls.test_table_name = "test_" + randstr()
        cls.mytable = dynamodict.DynamoDictionary(cls.test_table_name)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.mytable.clear()

    def tearDown(self):
        self.mytable.clear()

    def test_construction(self):
        pass  # was constructed in setUpClass

    def test_coverage(self):
        dynamodict_methods = [
            x for x in dir(self.mytable) if hasattr(getattr(self.mytable, x), "__call__") and not x.startswith("_")
        ]
        test_methods = [x[5:] for x in dir(self) if x.startswith("test_")]
        untested = set(dynamodict_methods) - set(test_methods)
        if untested:
            raise AssertionError("Following dynamodict methods are not tested: {}".format(", ".join(sorted(untested))))

    def test_clear(self):
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
        self.mytable["foo"] = "bar"
        assert self.mytable.get("foo") == "bar"
        self.mytable.clear()
        assert self.mytable.get("foo") is None

    def test_items(self):
        keys = sorted(randstr() for _ in range(10))
        for ikey in keys:
            self.mytable[ikey] = ikey
        assert sorted(self.mytable.items()) == sorted({ikey: ikey for ikey in keys}.items())

    def test_iteritems(self):
        keys = sorted(randstr() for _ in range(10))
        for ikey in keys:
            self.mytable[ikey] = "value_" + ikey
        idx = 0
        indices_seen = set()
        for idx, obs in enumerate(self.mytable.iteritems()):
            obskey, obsval = obs
            obsidx = keys.index(obskey)
            assert obskey == keys[obsidx]
            assert obsval == "value_" + keys[obsidx]
            indices_seen.add(obsidx)
        assert 9 == idx
        assert 10 == len(indices_seen)

    def test_iterkeys(self):
        keys = sorted(randstr() for _ in range(10))
        for ikey in keys:
            self.mytable[ikey] = 1
        indexes = set()
        for ikey in self.mytable.iterkeys():
            indexes.add(keys.index(ikey))
        assert len(indexes) == len(keys)

    def test_itervalues(self):
        unique_values = sorted(randstr() for _ in range(10))
        for ival in unique_values:
            self.mytable[randstr()] = ival
        unseen_vals = set(unique_values)
        for ival in self.mytable.values():
            unseen_vals.remove(ival)
        if unseen_vals:
            raise AssertionError("There were values that were not seen")

    def test_keys(self):
        keys = sorted(randstr() for _ in range(10))
        for ikey in keys:
            self.mytable[ikey] = "v" + ikey
        keys_back = self.mytable.keys()
        assert isinstance(keys_back, set)
        assert set(keys) == keys_back

    def test_len(self):
        assert 0 == len(self.mytable)
        for _ in range(20):
            self.mytable[randstr()] = randstr()
        assert 20 == len(self.mytable)

    def test_multi_delete(self):
        keys_to_keep = sorted(randstr() for _ in range(10))
        keys_to_drop = sorted(randstr() for _ in range(10))
        for ikey in keys_to_keep + keys_to_drop:
            self.mytable[ikey] = ikey
        assert sorted(self.mytable) == sorted(keys_to_keep + keys_to_drop)
        self.mytable.multi_delete(keys_to_drop)
        assert sorted(self.mytable) == sorted(keys_to_keep)

    def test_bool(self):
        if self.mytable:
            assert False
        self.mytable["foo"] = "bar"
        if not self.mytable:
            raise False

    def test_pop(self):
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
        """Values should give back the values as a list."""
        keys = sorted(randstr() for _ in range(10))
        for ikey in keys:
            self.mytable["k" + ikey] = ikey
        values = self.mytable.values()
        assert isinstance(values, list)
        assert sorted(values) == sorted(keys)
