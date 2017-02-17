from distutils.core import setup

setup(
    name='dyanmodictionary',
    version='0.0.1',
    description='Dictionary like thing built on top of dynamodb',
    author='Joe Bylund',
    author_email='joseph.bylund@gmail.com',
    packages=['dynamodict'],
    package_dir={'dynamodict': 'src/dynamodict'},
)
