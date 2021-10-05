import logging.handlers
import logging
import logging.config
import yaml

# create logger
logger = logging . getLogger ( 'superscript' )

#read config
with open ( 'log_config.yml' ) as f:
    log_config = yaml . load (f)
logging.config.dictConfig (log_config)

## message
logging.debug ( 'Message level debug % s ' , 'SOS' )
logger.info ( 'Message level info' )
logger.warning ( 'Message level warning' )
