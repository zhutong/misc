from time import time, sleep
from subprocess import check_output, STDOUT
import logging

def clear_all_pppoe_connection():
    check_output('%s; exit 0'%DISCONNECT_CMD, stderr=STDOUT, shell=True)
    while True:
        sleep(0.1)
        output = check_output('ifconfig; exit 0', stderr=STDOUT, shell=True)
        if 'ppp' not in output:
            break

formatter = logging.Formatter('[%(asctime)s - %(levelname)7s] %(message)s')
filename='pppoe_test.log'

console = logging.StreamHandler()
console.setFormatter(formatter)
console.setLevel(logging.DEBUG)
logfile = logging.FileHandler(filename)
logfile.setFormatter(formatter)
logfile.setLevel(logging.DEBUG)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(console)
logger.addHandler(logfile)

PPPOE_TEST_LOOPS = 1000
LOOP_WAIT_SECONDS = 2
DIAL_TIMEOUT_IN_SECOND = 5

CONNECT_CMD = 'pon dsl-provider'
DISCONNECT_CMD = 'poff -a'

# clear all exist pppoe connections
clear_all_pppoe_connection()

time_spend_list = []
try:
    for i in range(1, PPPOE_TEST_LOOPS+1):
        start = time()
        successed = False
    
        # start dial
        logger.debug('Start the %d dial tries' % i)
        check_output('%s; exit 0'%CONNECT_CMD, stderr=STDOUT, shell=True)         

        # ensure ppp interface up OR timeout
        while True:
            sleep(0.01)
            time_spend = time() - start
            output = check_output('ifconfig; exit 0', stderr=STDOUT, shell=True)      
            if 'ppp' in output:
                logger.info('Dial sucess in %.3f seconds' % time_spend)
                successed = True
                time_spend_list.append(time_spend)
                break
            if time_spend >= DIAL_TIMEOUT_IN_SECOND:
                logger.warn('Dial timeout')
                break
        if successed:
            clear_all_pppoe_connection()

        if i < PPPOE_TEST_LOOPS and successed:
            sleep(LOOP_WAIT_SECONDS)
except KeyboardInterrupt:
    pass

# print dial statistics
print
print '#' * 10, 'PPPoE dial statistics', '#' * 10
test_times, success_times = i, len(time_spend_list)
fail_percent = (test_times - success_times) * 100.0 / test_times
print 'dial %d times, %d succeed, %.2f%% failed' % (test_times, success_times, fail_percent)
min_time, max_time = min(time_spend_list), max(time_spend_list)
avg_time = sum(time_spend_list)/len(time_spend_list)
print 'dial-time min/avg/max = %.3f/%.3f/%.3f seconds' % (min_time, avg_time, max_time)
print