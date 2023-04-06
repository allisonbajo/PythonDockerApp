import logging

"""
level=logging.DEBUG defines the lowest level of logging that is visible.
default is set to logging.WARNING

WARNING:
root level logging is discouraged since the ability to determine the source of the log will be difficult

RECOMMENDED:
It is recommended to acquire a module/file specific logger by using the getLogger() method and passing an appropriate name.
Generally the __name__ is a good candidate since it resolves to the module name

A more efficient format for the log is needed to be able to capture the timing, level, and other artifacts related to the log
"""
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(levelname)-8s %(name)-10s: %(message)s')
log = logging.getLogger(__name__)
log.debug('DEBUG message')
log.info('INFO message')
log.warning('WARNING message')
log.error('ERROR message')
log.critical('CRITICAL message')