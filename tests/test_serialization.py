import datetime
import sys
import unittest

if True:
    sys.path = ["./src"] + sys.path
    import dynamodict

if "site-packages" in dynamodict.__file__:
    raise AssertionError("import is wrong")


class TestEncoder(unittest.TestCase):
    def test_roundtrip_datetime(self):
        test_obj = datetime.date.today()
        rtd = dynamodict.deserialize(dynamodict.serialize(test_obj))
        if rtd != test_obj:
            raise AssertionError("xxx")

    def test_roundtrip_dict(self):
        test_obj = {(1, 2): 3, "foo": 1, ("foo", 1): "bar", "today": datetime.date.today()}
        rtd = dynamodict.deserialize(dynamodict.serialize(test_obj))
        if rtd != test_obj:
            raise AssertionError("xxx")

    def test_roundtrip_int(self):
        test_obj = 1
        rtd = dynamodict.deserialize(dynamodict.serialize(test_obj))
        if rtd != test_obj:
            raise AssertionError("xxx")

    def test_roundtrip_list(self):
        test_obj = ["foo", 1, None]
        rtd = dynamodict.deserialize(dynamodict.serialize(test_obj))
        if rtd != test_obj:
            raise AssertionError("xxx")

    def test_roundtrip_str(self):
        test_obj = "foo"
        rtd = dynamodict.deserialize(dynamodict.serialize(test_obj))
        if rtd != test_obj:
            raise AssertionError("xxx")

    def test_roundtrip_tuple(self):
        test_obj = (1, "foo", None)
        rtd = dynamodict.deserialize(dynamodict.serialize(test_obj))
        if rtd != test_obj:
            raise AssertionError("xxx")
