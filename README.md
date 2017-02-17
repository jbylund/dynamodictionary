### dynamodictionary

This package provides a dictionary like interface for interacting with dynamodb tables, example:

```
In [1]: import dynamodict

In [2]: mytable = dynamodict.DynamoDictionary("footable")

In [3]: mytable['monty'] = 'python'

In [4]: print mytable['monty']
python

In [5]: mytable['cheeses'] = ['applewood', 'brie', 'cheddar', 'duddleswell']

In [6]: print mytable['cheeses']
['applewood', 'brie', 'cheddar', 'duddleswell']
```
