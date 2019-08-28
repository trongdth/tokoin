"""Logging utility functions."""
import os
import sys
import json
import logging
import logging.config
import linecache


def setup_logging(default_path='logging.json', default_level=logging.INFO,
                  env_key='LOG_CFG'):
    """Setup logging configuration"""
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    current_path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(current_path, path)
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)

        filename = config['handlers']['file_handler']['filename']
        filename = os.path.join(current_path, filename)
        # if os.path.exists(filename):
        #     f = open(filename, 'w')
        #     f.close()
        config['handlers']['file_handler']['filename'] = filename

        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def get_exception_str():
    """Get pretty exception string."""
    _, exc_obj, tb = sys.exc_info()
    last_tb = tb
    while True:
        try:
            tb.tb_frame
        except Exception:
            break
        else:
            last_tb = tb
            tb = tb.tb_next

    f = last_tb.tb_frame
    lineno = last_tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    err_str = 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(
        filename, lineno, line.strip(), exc_obj)

    return err_str
