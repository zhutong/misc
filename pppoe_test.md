# PPPoE拨号测试工具原型
PPPoE拨号测试工具用来测量PPPoE客户端拨号的成功率、拨通所需的时间。

## 测试环境
PPPoE客户端采用Ubuntu12.0.4下PPPoE命令行的拨号软件pppoeconfig，而服务器端则用IOL模拟。
本工具采用Python的subporcess库调用linux的命令，

## 问题及解决方法
PPPOE拨号命令为pon，但无论成功或失败输出结果都一样，没有办法判断是否拨通，更无法测量时间。
    root@controller:~# pon dsl-provider
    Plugin rp-pppoe.so loaded.

但是拨通后Linux会有相应的ppp接口出现，如：
    root@controller:~# ifconfig eth0
    ppp0      Link encap:Point-to-Point Protocol  
              inet addr:12.1.1.115  P-t-P:192.168.221.101  Mask:255.255.255.255
              UP POINTOPOINT RUNNING NOARP MULTICAST  MTU:1492  Metric:1
              RX packets:19 errors:0 dropped:0 overruns:0 frame:0
              TX packets:19 errors:0 dropped:0 overruns:0 carrier:0
              collisions:0 txqueuelen:3 
              RX bytes:892 (892.0 B)  TX bytes:1153 (1.1 KB)
而如果拨号失败则不会出现PPP接口。
因此可以通过ifconfig命令检查是否出现PPP接口来判断成功与否。

检查PPP接口是否出现采用循环语句实现，为了保障测量的精度，循环间隔设置为10ms，同时设置了超时时间避免出现死循环。
一旦检查到PPP接口，则计算并保存拨通所需的时间，然后使用poff命令断开PPPOE的连接。
如果超时，则退出循环。


### 测试输出示例
下面是用Python程序原型的输出：

    root@controller:~# python pppoe_test.py 
    [2014-03-20 14:15:11,154 -   DEBUG] Start the 1 dial tries
    [2014-03-20 14:15:11,243 -    INFO] Dial sucess in 0.087 seconds
    [2014-03-20 14:15:13,362 -   DEBUG] Start the 2 dial tries
    [2014-03-20 14:15:13,448 -    INFO] Dial sucess in 0.083 seconds
    [2014-03-20 14:15:15,569 -   DEBUG] Start the 3 dial tries
    [2014-03-20 14:15:15,661 -    INFO] Dial sucess in 0.088 seconds
    [2014-03-20 14:15:17,784 -   DEBUG] Start the 4 dial tries
    [2014-03-20 14:15:22,789 - WARNING] Dial timeout
    [2014-03-20 14:15:22,790 -   DEBUG] Start the 5 dial tries
    [2014-03-20 14:15:27,798 - WARNING] Dial timeout
    [2014-03-20 14:15:27,799 -   DEBUG] Start the 6 dial tries
    [2014-03-20 14:15:32,812 - WARNING] Dial timeout
    [2014-03-20 14:15:32,813 -   DEBUG] Start the 7 dial tries
    [2014-03-20 14:15:32,875 -    INFO] Dial sucess in 0.057 seconds
    [2014-03-20 14:15:34,999 -   DEBUG] Start the 8 dial tries
    [2014-03-20 14:15:35,089 -    INFO] Dial sucess in 0.088 seconds
    [2014-03-20 14:15:37,210 -   DEBUG] Start the 9 dial tries
    [2014-03-20 14:15:37,301 -    INFO] Dial sucess in 0.089 seconds
    [2014-03-20 14:15:39,422 -   DEBUG] Start the 10 dial tries
    [2014-03-20 14:15:39,494 -    INFO] Dial sucess in 0.069 seconds
    [2014-03-20 14:15:41,616 -   DEBUG] Start the 11 dial tries
    [2014-03-20 14:15:41,700 -    INFO] Dial sucess in 0.081 seconds
    [2014-03-20 14:15:43,824 -   DEBUG] Start the 12 dial tries
    [2014-03-20 14:15:43,919 -    INFO] Dial sucess in 0.093 seconds
    [2014-03-20 14:15:46,044 -   DEBUG] Start the 13 dial tries
    [2014-03-20 14:15:46,123 -    INFO] Dial sucess in 0.077 seconds
    [2014-03-20 14:15:48,245 -   DEBUG] Start the 14 dial tries
    [2014-03-20 14:15:48,328 -    INFO] Dial sucess in 0.081 seconds
    [2014-03-20 14:15:50,448 -   DEBUG] Start the 15 dial tries
    [2014-03-20 14:15:50,541 -    INFO] Dial sucess in 0.089 seconds
    [2014-03-20 14:15:52,674 -   DEBUG] Start the 16 dial tries
    [2014-03-20 14:15:52,748 -    INFO] Dial sucess in 0.071 seconds
    [2014-03-20 14:15:54,873 -   DEBUG] Start the 17 dial tries
    [2014-03-20 14:15:54,952 -    INFO] Dial sucess in 0.078 seconds
    [2014-03-20 14:15:57,076 -   DEBUG] Start the 18 dial tries
    [2014-03-20 14:15:57,191 -    INFO] Dial sucess in 0.112 seconds
    [2014-03-20 14:15:59,314 -   DEBUG] Start the 19 dial tries
    [2014-03-20 14:15:59,403 -    INFO] Dial sucess in 0.086 seconds
    [2014-03-20 14:16:01,524 -   DEBUG] Start the 20 dial tries
    [2014-03-20 14:16:01,610 -    INFO] Dial sucess in 0.081 seconds
    [2014-03-20 14:16:03,738 -   DEBUG] Start the 21 dial tries
    [2014-03-20 14:16:03,823 -    INFO] Dial sucess in 0.083 seconds
    [2014-03-20 14:16:05,946 -   DEBUG] Start the 22 dial tries
    [2014-03-20 14:16:06,029 -    INFO] Dial sucess in 0.081 seconds
    [2014-03-20 14:16:08,154 -   DEBUG] Start the 23 dial tries
    [2014-03-20 14:16:08,236 -    INFO] Dial sucess in 0.080 seconds
    [2014-03-20 14:16:10,357 -   DEBUG] Start the 24 dial tries
    [2014-03-20 14:16:10,444 -    INFO] Dial sucess in 0.085 seconds
    [2014-03-20 14:16:12,564 -   DEBUG] Start the 25 dial tries
    [2014-03-20 14:16:12,659 -    INFO] Dial sucess in 0.093 seconds
    ^C
    ########## PPPoE dial statistics ##########
    dial 25 times, 22 succeed, 12.00% failed
    dial-time min/avg/max = 0.057/0.083/0.112 seconds

    root@controller:~# 

# 附、PPPoE服务器配置参考
本测试中使用的IOL版本为15.3，配置参考如下：

    version 15.3
    !
    hostname R101
    !
    aaa new-model
    aaa authentication ppp default local
    !
    username cisco password cisco
    !
    bba-group pppoe TEST
     virtual-template 1
    !
    interface Loopback0
     ip address 1.1.1.1 255.255.255.255
    !
    interface Ethernet0/0
     ip address 192.168.221.101 255.255.255.0
     pppoe enable group TEST
    !
    interface Virtual-Template1
     ip unnumbered Ethernet0/0
     peer default ip address pool TEST
     ppp authentication chap callin
     ppp ipcp dns 8.8.8.8
    !
    ip local pool TEST 12.1.1.100 12.1.1.200
