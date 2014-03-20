from time import time, sleep, strftime
from subprocess import check_output, STDOUT
import logging


CONNECT_CMD = 'pon dsl-provider'
LOOP_WAIT_SECONDS = 2
DIAL_TIMEOUT_IN_SECOND = 5


def get_logger(filename=None):
    formatter = logging.Formatter('[%(asctime)s - %(levelname)7s] %(message)s')

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    console.setLevel(logging.DEBUG)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console)
    
    if filename:
        logfile = logging.FileHandler(filename)
        logfile.setFormatter(formatter)
        logfile.setLevel(logging.DEBUG)
        logger.addHandler(logfile)
    
    return logger
    

def clear_all_pppoe_connection():
    check_output('poff -a; exit 0', stderr=STDOUT, shell=True)
    while True:
        sleep(0.1)
        output = check_output('ifconfig; exit 0', stderr=STDOUT, shell=True)
        if 'ppp' not in output:
            break

def dial():
    start_timer = time()

    check_output('%s; exit 0'%CONNECT_CMD, stderr=STDOUT, shell=True)         

    # ensure ppp interface up or timeout
    while True:
        sleep(0.01)
        time_spend = time() - start_timer
        output = check_output('ifconfig; exit 0', stderr=STDOUT, shell=True)      
        if 'ppp' in output:
            logger.info('Dial sucess in %.3f seconds' % time_spend)
            succeed = True
            break
        if time_spend >= DIAL_TIMEOUT_IN_SECOND:
            logger.warn('Dial timeout')
            succeed = False
            break

    return succeed, time_spend, start_timer


def test_pppoe(logger, expect_test_loops=0):
    '''
    @expect_test_loops: if test_loops< 1 then loop infinity.
    '''

    # clear all exist pppoe connections
    clear_all_pppoe_connection()

    success_list = []
    test_times = 1
    try:
        while True:
            # start dial
            logger.debug('Start the %d dial tries' % test_times)
            succeed, time_spend, start_timer = dial()
            if succeed:
                success_list.append((time_spend, start_timer))
                clear_all_pppoe_connection()
            test_times += 1
            if test_times > expect_test_loops > 0:
                break
            sleep(LOOP_WAIT_SECONDS)
    except KeyboardInterrupt:
        pass
    
    return test_times - 1, success_list


def show_statis(test_times, success_list): 
    # print dial statistics, just like ping
    print
    print '#' * 10, 'PPPoE dial statistics', '#' * 10
    success_times = len(success_list)
    fail_percent = (test_times - success_times) * 100.0 / test_times
    print 'dial %d times, %d succeed, %.2f%% failed' % (test_times, success_times, fail_percent)
    if success_times:
        time_spend_list = [s[0] for s in success_list]
        min_time, max_time = min(time_spend_list), max(time_spend_list)
        avg_time = sum(time_spend_list)/len(time_spend_list)
        print 'dial-time min/avg/max = %.3f/%.3f/%.3f seconds' % (min_time, avg_time, max_time)
        print '\ndetail info:'
        for s in success_list:
            print '%f: %-5.0f ms' % (strftime('%Y-%m-%d %H:%M:%S', s[1]), s[0]*1000)
    print
    
if __name__ == '__main__':
    logfilename='pppoe_test.log'
    logger = get_logger(logfilename)
    test_loops_expect = 2
    test_times, time_spend_list = test_pppoe(logger, test_loops_expect)
    show_statis(test_times, time_spend_list) 

