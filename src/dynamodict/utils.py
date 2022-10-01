import socket
import logging
import functools
import time

PATCHES_HOLDER = {}

logger = logging.getLogger(__name__)


def install_patches():
    if PATCHES_HOLDER:
        logger.info("Patches already installed...")
        return
    logger.info("Installing patches...")

    PATCHES_HOLDER["getaddrinfo"] = real_getaddrinfo = socket.getaddrinfo

    @functools.lru_cache(maxsize=2**12)
    def cached_addrinfo(_timestamp_bust, *args, **kwargs):
        return real_getaddrinfo(*args, **kwargs)

    def getaddrinfo_with_caching(*args, **kwargs):
        return cached_addrinfo(time.time() // (10 * 60), *args, **kwargs)

    socket.getaddrinfo = getaddrinfo_with_caching


def remove_patches():
    if not PATCHES_HOLDER:
        logger.warning("Patches were not applied...")
        return
    logger.info("Removing patches...")
    socket.getaddrinfo = PATCHES_HOLDER.pop("getaddrinfo")
