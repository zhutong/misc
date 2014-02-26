import os

filepath = '/Users/zhutong/Documents/logs/network2s/'

hosts = []
for fn in os.listdir(filepath):
    if '@' not in fn: continue
    hostname = fn.split('@')[0]
    f = open(os.path.join(filepath, fn))
    for line in f.readlines():
        if line.startswith('service timestamps log'):
            print '%-24s%s' % (hostname, line),
        elif line.startswith('clock timezone'):
            hosts.append(hostname)
            print '%-24s%s' % (hostname, line),
print

for h in set(hosts):
    print h