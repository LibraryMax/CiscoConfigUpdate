from netmiko import ConnectHandler
import os, errno
import csv
import smtplib
from email.mime.text import MIMEText

cisco_2 = {
'device_type': 'cisco_ios',
'ip': '0.0.0.0',
'username': 'max',
'password': '****',
}

net_connect = ConnectHandler(**cisco_2)
output = net_connect.send_command("show config | include ! NVRAM config")

nvramTime = output[31:43]
nvramDate = output[44:59]

def comparrison():
	with open(r'C:\test.csv') as file:
		last_line = file.readlines()[-1]
		final = last_line.rstrip('\n')
	file.close()
	compare = "%s,%s" % (nvramTime,nvramDate)
	
	if final != compare:
		def writeLine():
			fields=[nvramTime,nvramDate]
			with open(r'C:\test.csv','ab') as f:
				writer = csv.writer(f)
				writer.writerow(fields)
			f.close()
		writeLine()
		def sendMail():
			with open(r'c:\test.txt', 'rb') as fp:
				msg = MIMEText(fp.read())

			msg['Subject'] = 'Configuration updated %s' % (compare)
			msg['From'] = 'test@example.org'
			msg['To'] = 'test2@example.org'
			s = smtplib.SMTP('SMTP.server.com')
			s.sendmail('test@example.org','test2@example.org', msg.as_string())
		sendMail()
	else:
		print("goodbye")
	
comparrison()