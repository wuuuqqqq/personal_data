#!/bin/bash
#suto install zabbix_agentd
#author :swh
echo  "Now  this shell will install zabbix_agentd autoly:please wait"
yum install net-snmp-devel libxml2-devel libcurl-devel  gcc pcre-devel wget -y
echo "add zabbix group and user:"
groupadd zabbix
useradd   -r zabbix  -g  zabbix  -s /sbin/nologin
echo "download package -make and make install "
cd  /usr/local/src
wget -c  "https://jaist.dl.sourceforge.net/project/zabbix/ZABBIX%20Latest%20Stable/4.4.7/zabbix-4.4.7.tar.gz"
tar -xzvf zabbix-4.4.7.tar.gz
cd zabbix-4.4.7
./configure --prefix=/usr/local/zabbix/ --enable-agent
make
make install
ret=$?
if [ $? -eq 0 ]
  then
        #read  -p "please input zabbix_serverIP:"  zabbix_serverIP
        sed -i 's/Server=127.0.0.1/Server=192.168.18.17/' /usr/local/zabbix/etc/zabbix_agentd.conf
        sed -i 's/ServerActive=127.0.0.1/ServerActive=192.168.18.17/' /usr/local/zabbix/etc/zabbix_agentd.conf
        sed -i 's/Hostname=Zabbix server/Hostname='$HOSTNAME'/' /usr/local/zabbix/etc/zabbix_agentd.conf
        echo "zabbix install success,you need set hostname: $HOSTNAME"

else
        echo "install failed,please check"
fi
/usr/local/zabbix/sbin/zabbix_agentd
if [ $? -eq 0 ]
  then
        echo "set zabbix_agentd start with system"
        echo "/usr/local/zabbix/sbin/zabbix_agentd" >> /etc/rc.d/rc.local
                chmod +x /etc/rc.d/rc.local
else
        echo "start error,please check"
fi