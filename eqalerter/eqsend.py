from datetime import datetime
from time import strftime
import smtplib, ssl
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
import eqconfig
import eqdebug

class EqSender():
	def send(self, content, subject, attachment_filename, receiver_address):
		eqdebug.debug_print("Building mail...")
		#set email metadata
		email			= MIMEMultipart()
		email["From"] 	= eqconfig.EMAIL_ADDRESS
		email["To"] 	= receiver_address
		email["Subject"]= subject
		
		#extract alert data
		att_ref		= open(attachment_filename, "rb") 
		att_txt		= att_ref.read()
		
		#set text content of email
		email.attach(MIMEText(content,"plain"))
		
		email_att = MIMEBase("application","octet-stream")
		email_att.set_payload(att_txt)
		
		encoders.encode_base64(email_att)
		
		email_att.add_header("Content-Disposition","attatchment; filename = {}".format(attachment_filename))
		
		#set file attatchment
		email.attach(email_att)
		email_text = email.as_string()
		
		eqdebug.debug_print("Attempting to send mail to {} from {} using server".format(receiver_address,eqconfig.EMAIL_ADDRESS,eqconfig.SMTP_SERVER_URL))
		#send mail
		context = ssl.create_default_context()
		smtpref = smtplib.SMTP_SSL(eqconfig.SMTP_SERVER_URL,eqconfig.SMTP_SERVER_PORT, context = context)
		smtpref.login(eqconfig.EMAIL_ADDRESS, eqconfig.EMAIL_PASSWORD)
		smtpref.sendmail(eqconfig.EMAIL_ADDRESS,receiver_address,email_text)
		smtpref.quit()