#!/usr/bin/python
"""a class that acts a little like a dictionary that uses dynamo as a backing"""
# std imports
import base64
import logging
import pickle
import sys
import time

# site imports
import boto3
import botocore.exceptions

KEY_ATTR_NAME = "k"
TTL_ATTR_NAME = "ttl"
VAL_ATTR_NAME = "v"

logging.basicConfig()
logger = logging.getLogger(__name__)


def serialize(obj):
    return base64.b64encode(pickle.dumps(obj))


def deserialize(obj):
    try:
        obj = obj.value
    except AttributeError:
        pass
    return pickle.loads(base64.b64decode(obj))


def is_permission_error(oops):
    if getattr(oops, "response", {}).get("Error", {}).get("Code") == "AccessDeniedException":
        return {
            "user": oops.response["Error"]["Message"].split()[1].partition("/")[-1],
            "action": oops.operation_name,
        }
    return False


class PermissionError(Exception):
    pass


class DynamoDictionary(object):
    """a class that acts a little like a dictionary that uses dynamo as a backing"""

    empty_sentinel = object()
    default_read_units = 25 // 2
    default_write_units = 25 // 2

    def __init__(self, table_name, read_units=None, write_units=None, ttl=None):
        self.table_name = table_name
        self.conn = boto3.resource("dynamodb", region_name="us-east-1")
        self.client = self.conn.meta.client
        self.table = self.conn.Table(self.table_name)
        self.ttl = ttl
        try:
            self.table.get_item(Key={KEY_ATTR_NAME: serialize("xxx")})
        except botocore.exceptions.ClientError as oops:
            perm_error = is_permission_error(oops)
            if perm_error:
                raise PermissionError(perm_error)
            # check if it's a table does not exist error
            self.create_table(read_units=read_units, write_units=write_units)
            self.table.wait_until_exists()

    def create_table(self, read_units=None, write_units=None):
        """create a table in case it doesn't exist"""
        self.client.create_table(
            TableName=self.table_name,
            AttributeDefinitions=[
                {
                    "AttributeName": KEY_ATTR_NAME,
                    "AttributeType": "B",
                },
            ],
            KeySchema=[
                {
                    "AttributeName": KEY_ATTR_NAME,
                    "KeyType": "HASH",
                },
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": read_units or self.default_read_units,
                "WriteCapacityUnits": write_units or self.default_write_units,
            },
        )

    def drop_table(self):
        """drop table"""
        self.client.delete_table(TableName=self.table_name)

    def __getitem__(self, key):
        """x.__getitem__(y) <==> x[y]"""
        got = self.table.get_item(Key={KEY_ATTR_NAME: serialize(key)})
        if "Item" not in got:
            raise KeyError(key)
        return deserialize(got["Item"][VAL_ATTR_NAME])

    def __setitem__(self, key, value):
        """x.__setitem__(i, y) <==> x[i]=y"""
        to_put = {
            KEY_ATTR_NAME: serialize(key),
            VAL_ATTR_NAME: serialize(value),
        }
        if self.ttl:
            to_put[TTL_ATTR_NAME] = time.time() + self.ttl
        for i in range(5):
            try:
                self.table.put_item(Item=to_put)
                break
            except botocore.exceptions.ClientError as oops:
                if oops.response["Error"]["Code"] != "ProvisionedThroughputExceededException":
                    perm_error = is_permission_error(oops)
                    if perm_error:
                        raise PermissionError(perm_error)
                    raise
                else:
                    logger.info("Over rate limit for table %s, backing off!", self.table_name)
                    time.sleep(0.1 * 2**i)
        else:
            raise Exception("Tried 5 times could not write item!")

    def get(self, key, default=None):
        """D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None."""
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, key, default=empty_sentinel):
        """D.pop(k[,d]) -> v, remove specified key and return the corresponding value.\nIf key is not found, d is returned if given, otherwise KeyError is raised"""
        try:
            deleted = self.table.delete_item(Key={KEY_ATTR_NAME: serialize(key)}, ReturnValues="ALL_OLD")
        except botocore.exceptions.ClientError as oops:
            perm_error = is_permission_error(oops)
            if perm_error:
                raise PermissionError(perm_error)
            raise
        if "Attributes" not in deleted:
            if default is not self.empty_sentinel:
                return default
            else:
                raise KeyError(key)
        return deserialize(deleted["Attributes"][VAL_ATTR_NAME])

    def iteritems(self):
        """D.iteritems() -> an iterator over the (key, value) items of D"""
        start_key = ""
        while True:
            kwargs = {
                "Limit": 1000,
                "Select": "ALL_ATTRIBUTES",
            }
            if start_key:
                kwargs["ExclusiveStartKey"] = start_key
            try:
                response = self.table.scan(**kwargs)
            except botocore.exceptions.ClientError as oops:
                perm_error = is_permission_error(oops)
                if perm_error:
                    raise PermissionError(perm_error)
                raise oops
            for item in response["Items"]:
                yield deserialize(item[KEY_ATTR_NAME]), deserialize(item[VAL_ATTR_NAME])
            start_key = response.get("LastEvaluatedKey")
            if start_key is None:
                break

    def items(self):
        """D.items() -> list of D's (key, value) pairs, as 2-tuples"""
        return [item for item in self.iteritems()]

    def keys(self):
        """D.keys() -> list of D's keys"""
        return {key for key, _ in self.iteritems()}

    def values(self):
        """D.values() -> list of D's values"""
        return [value for _, value in self.iteritems()]

    def itervalues(self):
        """D.itervalues() -> an iterator over the values of D"""
        for _, value in self.iteritems():
            yield value

    def iterkeys(self):
        """D.iterkeys() -> an iterator over the keys of D"""
        for key, _ in self.iteritems():
            yield key

    def __iter__(self):
        """x.__iter__() <==> iter(x)"""
        for key, _ in self.iteritems():
            yield key

    def __contains__(self, key):
        """D.__contains__(k) -> True if D has a key k, else False"""
        try:
            self.__getitem__(key)
            return True
        except KeyError:
            return False

    def __len__(self):
        """x.__len__() <==> len(x)"""
        count = 0
        for _ in self.__iter__():
            count += 1
        return count

    def clear(self):
        """D.clear() -> None.  Remove all items from D."""
        # do a batch get an then batch write deleting in chunks of 25
        chunk = []
        for key in self.iterkeys():
            chunk.append(key)
            if 25 <= len(chunk):
                self.multi_delete(chunk)
                chunk[:] = []
        self.multi_delete(chunk)

    def multi_delete(self, keys):
        if not keys:
            return
        # todo add retries and handle unprocessed items
        table_operations = []
        for ikey in keys:
            item_delete_request = {"DeleteRequest": {"Key": {KEY_ATTR_NAME: {"B": serialize(ikey)}}}}
            table_operations.append(item_delete_request)
        try:
            res = self.client.batch_write_item(RequestItems={self.table_name: table_operations})
        except botocore.exceptions.ClientError as oops:
            perm_error = is_permission_error(oops)
            if perm_error:
                raise PermissionError(perm_error)
            raise
