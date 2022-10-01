from .dynamodict import DynamoDictionary, deserialize, serialize
from .utils import install_patches

__versioninfo__ = (1, 0, 2)
__version__ = ".".join(str(x) for x in __versioninfo__)
install_patches()
