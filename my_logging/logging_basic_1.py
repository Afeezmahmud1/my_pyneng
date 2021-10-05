import logging

logging.basicConfig(filename='mylog.log',level=logging.DEBUG)

logging . debug ( 'Debug level message: \ n % s ' , str ( globals ()))
logging.info('Message level Info')
logging.warning('Message level Warning')
