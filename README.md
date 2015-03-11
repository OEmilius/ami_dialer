# ami_dialer
Create call using Asterisk manager interface, control cause, send mail if call not successful

Create call every 2 minutes
$crontab -e
# m h  dom mon dow   command
*/2 *  * * * /home/emilius/pyprojects/Ami_dialer.py

