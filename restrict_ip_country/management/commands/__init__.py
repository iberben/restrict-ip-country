import logging


LOGGING_LEVEL = {'0': logging.ERROR, '1': logging.WARNING, '2': logging.DEBUG, '3': logging.NOTSET}


def _validate_verbosity(verbosity=None):
    if verbosity is None:
        return LOGGING_LEVEL['1']
    
    verbosity = str(verbosity)
    if not verbosity in LOGGING_LEVEL.keys():
        raise KeyError("Verbosity key error: %s" % verbosity)
    else:
        return verbosity


def _create_handler(handler, verbosity, message):
    """
    Create a handler which can output logged messages to the console (the log
    level output depends on the verbosity level).
    """
    handler.setLevel(LOGGING_LEVEL[_validate_verbosity(verbosity)])
    formatter = logging.Formatter(message)
    handler.setFormatter(formatter)
    return handler


def create_file_handler(verbosity, filename, message='%(message)s'):
    """
    Create a handler which can output logged messages to the console (the log
    level output depends on the verbosity level).
    """
    handler = logging.FileHandler(filename, encoding='utf-8')
    return _create_handler(handler, verbosity, message)
    

def create_anon_handler(verbosity, message='%(message)s'):
    """
    Create a handler which can output logged messages to the console (the log
    level output depends on the verbosity level).
    """
    handler = logging.StreamHandler()
    return _create_handler(handler, verbosity, message)
