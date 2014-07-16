#!/usr/bin/env python
import sys
import os.path
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import formatdate


folder = 'D:\Iperf\Log\\'
msg_low_sh = ''
msg_normal = ''
msg_low_us = ''
msg_nodata = ''
for filename in os.listdir (folder):
    if (filename.split('.')[1] != "txt") :
        continue
    statinfo = os.stat(folder + filename)
    if (statinfo.st_size == 0):
        msg_nodata += "<tr color='#4c4c4c'  bgcolor='#4c4c4c' height = '20'><td>" + filename.split('.')[0] + "</td><td>.have now data.</td></tr>\n"
        continue
    fp = open(folder + filename,'r')
    for i, line in enumerate(fp):
        if (i == 6):
            speednumber = line.split()
            if (float(speednumber[5])) < 500 and (float(speednumber[5])) > 10:
               msg_low_sh += "<tr color=\"#ff0000\" bgcolor='ff0000' height = '20'><td>" + filename.split('.')[0] + "</td><td> Low Speed at ShangHai: " + speednumber[5] + "Mbits. We should notice this machine.</td></tr>\n"
               continue
            if (float(speednumber[5])) <1.2:
               msg_low_us +=  "<tr color=\"#ff6600\" bgcolor='ff6600'  height = '20'><td>" + filename.split('.')[0] + "</td><td>Low Speed at US: " + speednumber[5] + "Mbits. We should notice this machine.</td></tr>\n"
               continue
            else:
              msg_normal +=  "<tr color=\"#036803\" bgcolor='036803' height = '20'><td>" + filename.split('.')[0] + "</td><td> Normal Speed: " + speednumber[5] + "Mbits.</td></tr>\n"
    fp.close()
#print (msg_low_sh)
#print (msg_low_us)
#print (msg_normal)
#print (msg_nodata)

text_file = open("LANSpeedOutput.txt", "w")
text_file.write('<table width="800" border="1"  bordercolor="#000000">')
text_file.write(msg_low_sh)
text_file.write(msg_low_us)
text_file.write(msg_normal)
text_file.write(msg_nodata)
text_file.write('</table>')

text_file.close()

# Define these once; use them twice!
strFrom = "a"
strTo = ["a","b","c"]
date = datetime.datetime.now().strftime( "%d/%m/%Y " )

# Create the root message and fill in the from, to, and subject headers
msgRoot = MIMEMultipart('related')
msgRoot['Subject'] = "LAN Speed log at "+date
msgRoot['From'] = strFrom
msgRoot['To'] = ",".join(strTo)
msgRoot.preamble = 'This is a multi-part message in MIME format.'

# Encapsulate the plain and HTML versions of the message body in an
# 'alternative' part, so message agents can decide which they want to display.
msgAlternative = MIMEMultipart('alternative')
msgRoot.attach(msgAlternative)

msgText = MIMEText('This is the alternative plain text message.')
msgAlternative.attach(msgText)

# We reference the image in the IMG SRC attribute by the ID we give it below
fptxt = open(r'LANSpeedOutput.txt', 'r')
msgText = MIMEText('<img src="cid:image1"><font size = 4 > Iperf Intranet Speed Report  '+ date +'</font><br>'+fptxt.read(), 'html')
msgAlternative.attach(msgText)
fptxt.close()

# This example assumes the image is in the current directory
fp = open(logo.jpg', 'rb')
msgImage = MIMEImage(fp.read())
fp.close()

# Define the image's ID as referenced above
msgImage.add_header('Content-ID', '<image1>')
msgRoot.attach(msgImage)

# Send the email (this example assumes SMTP authentication is required)
import smtplib
smtp = smtplib.SMTP()
smtp.connect(‘1.2.3.4’)
smtp.login('a', '5678')
smtp.sendmail(strFrom, strTo, msgRoot.as_string())
smtp.quit()
