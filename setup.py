import setuptools

description = """
Dictionary like thing built on top of dynamodb
""".strip()

setuptools.setup(
    author_email="joseph.bylund@gmail.com",
    author="Joe Bylund",
    description=description,
    long_description=description,
    name="dynamodictionary",
    package_dir={"dynamodict": "src/dynamodict"},
    packages=["dynamodict"],
    url="https://github.com/jbylund/dynamodictionary",
    version="1.0.1",
)
