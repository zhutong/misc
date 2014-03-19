from time import time, sleep
from subprocess import check_output, call, STDOUT
import logging

formatter = logging.Formatter('[%(asctime)s - %(levelname)8s] %(message)s')
filename='pppoe_test.log'

console = logging.StreamHandler()
console.setFormatter(formatter)
console.setLevel(logging.INFO)
logfile = logging.FileHandler(filename)
logfile.setFormatter(formatter)
logfile.setLevel(logging.DEBUG)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(console)
logger.addHandler(logfile)


PPPOE_TEST_LOOPS = 10
LOOP_WAIT_SECONDS = 2

DILD_COMMAND = 'ping -c 1 -t 2 www.cisco.com'
DISCONNECT_COMMAND = 'ls'
SUCCESS_STRING = 'min/avg/max/stddev'

for i in range(PPPOE_TEST_LOOPS):
    start = time()
    logger.debug('Start %d dial tries' % (i+1) )
    output = check_output('%s; exit 0'%DILD_COMMAND, stderr=STDOUT, shell=True)
    if SUCCESS_STRING in output:
        logger.debug(output.splitlines()[-1])
        logger.info('Spend %3f seconds for %d dial' % (time()-start, i+1))
        output = check_output(DISCONNECT_COMMAND.split())
    else:
        logger.warn('Dial failed')
    if i < PPPOE_TEST_LOOPS-1:
        sleep(LOOP_WAIT_SECONDS)
