import logging

VERSION = (1, 0, 0)

logger = logging.getLogger('restrict_ip_country')

logger.setLevel(logging.DEBUG)


def get_version():
    bits = [str(bit) for bit in VERSION]
    version = bits[0]
    for bit in bits[1:]:
        version += (bit.isdigit() and '.' or '') + bit
    return version

