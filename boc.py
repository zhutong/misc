import os
import time

strftime = time.strftime
gmtime = time.gmtime

folder = '/Users/zhutong/Downloads/ah/bj'

data_list = []
for fn in os.listdir(folder):
    for l in open(os.path.join(folder, fn)).readlines():
        if l.startswith('<datalogelement>'):
            str_list = l[16:].split('|')
            second = int(str_list[0]) + (3600 * 8)
            time_str = strftime("%Y%m%d %H:%M:%S", gmtime(second))
            data_list.append(','.join((time_str, str_list[4], str_list[5])))

open('dataset.csv', 'w').write('\n'.join(data_list))