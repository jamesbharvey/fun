### BEGIN INIT INFO
# Provides:          set-hostname.sh
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      
# Short-Description: set hostname based on mac address at boot time
# Description:       See short desctiption.
### END INIT INFO


MAC="xxx-""$(echo `ifconfig -a | grep -o ".\{0,12\}enx.\{0,12\}" | cut -c 10-15`)"
MAC=orangepi4-lts-$(ip -o -4 link | grep eth0 | perl -ne '/ether (\S+)/; print $1;' | sed -e 's/://g')
CURRENT_HOSTNAME=$(cat /proc/sys/kernel/hostname)
chattr -i /etc/hostname
echo "$MAC" > "/etc/hostname"
chattr -i /etc/hosts
sed -i "s/$CURRENT_HOSTNAME/$MAC/g" /etc/hosts
hostname $MAC
chattr +i /etc/hostname
chattr +i /etc/hosts

exit 0
