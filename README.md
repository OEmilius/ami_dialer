# ami_dialer
Create call using Asterisk manager interface, control cause, send mail if call not successful

Create call every 2 minutes
$crontab -e
# m h  dom mon dow   command
*/2 *  * * * /home/emilius/pyprojects/Ami_dialer.py

$cat /etc/asterisk/manager.conf
[pbx]
secret=testpbx123
read = system,call,log,verbose,agent,user,config,dtmf,reporting,cdr,dialplan
write = system,call,agent,user,config,command,reporting,originate
read = all
write = all


