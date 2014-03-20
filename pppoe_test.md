# PPPoE拨号测试工具原型
PPPoE拨号测试工具用来测量PPPoE客户端拨号的成功率、拨通所需的时间。

## 测试环境
PPPoE客户端采用Ubuntu12.0.4下PPPoE命令行的拨号软件``pppoeconfig``，而服务器端则用IOL模拟。

本工具采用Python的``subprocess``库调用linux的命令，

## 问题及解决方法
PPPOE拨号命令为``pon``，但无论成功或失败输出结果都一样，没有办法判断是否拨通，更无法测量时间。

    root@controller:~# pon dsl-provider
    Plugin rp-pppoe.so loaded.

但是拨通后Linux会有相应的ppp接口出现，如：

    root@controller:~# ifconfig ppp0
    ppp0      Link encap:Point-to-Point Protocol  
              inet addr:12.1.1.115  P-t-P:192.168.221.101  Mask:255.255.255.255
              UP POINTOPOINT RUNNING NOARP MULTICAST  MTU:1492  Metric:1
              RX packets:19 errors:0 dropped:0 overruns:0 frame:0
              TX packets:19 errors:0 dropped:0 overruns:0 carrier:0
              collisions:0 txqueuelen:3 
              RX bytes:892 (892.0 B)  TX bytes:1153 (1.1 KB)
而如果拨号失败则不会出现PPP接口。
因此可以通过``ifconfig``命令检查是否出现PPP接口来判断成功与否。

检查PPP接口是否出现采用循环语句实现，为了保障测量的精度，循环间隔设置为10ms，同时设置了超时时间避免出现死循环。
* 一旦检查到PPP接口，则计算并保存拨通所需的时间，然后使用``poff``命令断开PPPOE的连接。
* 如果超时，则退出循环。


### 测试输出示例
下面是用Python程序原型的输出：

    root@controller:~# python pppoe_test.py  
    [2014-03-20 20:38:08,776 -   DEBUG] Start the 1 dial tries
    [2014-03-20 20:38:08,877 -    INFO] Dial sucess in 0.099 seconds
    [2014-03-20 20:38:11,005 -   DEBUG] Start the 2 dial tries
    [2014-03-20 20:38:11,108 -    INFO] Dial sucess in 0.098 seconds
    [2014-03-20 20:38:13,232 -   DEBUG] Start the 3 dial tries
    [2014-03-20 20:38:13,325 -    INFO] Dial sucess in 0.090 seconds
    [2014-03-20 20:38:15,444 -   DEBUG] Start the 4 dial tries
    [2014-03-20 20:38:15,527 -    INFO] Dial sucess in 0.079 seconds
    [2014-03-20 20:38:17,655 -   DEBUG] Start the 5 dial tries
    [2014-03-20 20:38:17,736 -    INFO] Dial sucess in 0.077 seconds
    [2014-03-20 20:38:19,863 -   DEBUG] Start the 6 dial tries
    [2014-03-20 20:38:19,949 -    INFO] Dial sucess in 0.083 seconds
    [2014-03-20 20:38:22,074 -   DEBUG] Start the 7 dial tries
    [2014-03-20 20:38:27,091 - WARNING] Dial timeout
    [2014-03-20 20:38:29,094 -   DEBUG] Start the 8 dial tries
    [2014-03-20 20:38:34,103 - WARNING] Dial timeout
    [2014-03-20 20:38:36,107 -   DEBUG] Start the 9 dial tries
    [2014-03-20 20:38:36,148 -    INFO] Dial sucess in 0.038 seconds
    [2014-03-20 20:38:38,268 -   DEBUG] Start the 10 dial tries
    [2014-03-20 20:38:38,372 -    INFO] Dial sucess in 0.098 seconds
    
    ########## PPPoE dial statistics ##########
    dial 10 times, 8 succeed, 20.00% failed
    dial-time min/avg/max = 0.038/0.083/0.099 seconds
    
    detail info:
    2014-03-20 20:38:08: 99    ms
    2014-03-20 20:38:11: 98    ms
    2014-03-20 20:38:13: 90    ms
    2014-03-20 20:38:15: 79    ms
    2014-03-20 20:38:17: 77    ms
    2014-03-20 20:38:19: 83    ms
    2014-03-20 20:38:36: 38    ms
    2014-03-20 20:38:38: 98    ms

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
