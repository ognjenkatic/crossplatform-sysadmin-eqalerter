from os import path
from os import listdir
from os import remove

from datetime import datetime
from time import strftime
from requests.auth import HTTPBasicAuth

from eqquery import EqQuery
from eqsend import EqSender
from eqwrite import EqWriter

import json
import sys
import argparse

import eqdebug
import eqconfig


conf_filename	= ""
conf_filepath	= ""

parser = argparse.ArgumentParser(description="This program executes elasticsearch queries based on provided configurations and alerts via email a list of recipients if results are returned.")

parser.add_argument("config",help = "the configuration file")
parser.add_argument("-v","--verbose",help = "increase the level of verbocity", action="count", default=0)

args = parser.parse_args()
eqconfig.VERBOCITY = args.verbose

#check if parameters and basic config are correct
if not path.exists(eqconfig.CONFIG_DIR):
	eqdebug.debug_print("Config directory '{}' not found, check config file.".format(eqconfig.CONFIG_DIR),True)
elif eqconfig.ES_USERNAME == "":
	eqdebug.debug_print("Elasticsearch username not present in configuration",True)
elif eqconfig.ES_PASSWORD == "":
	eqdebug.debug_print("Elasticsearch user password not present in configuration",True)
elif eqconfig.ES_SERVER_URL == "":
	eqdebug.debug_print("Elasticsearch server url not present in configuration",True)
elif eqconfig.EMAIL_ADDRESS == "":
	eqdebug.debug_print("Email address of alert sender not present in configuration",True)
elif eqconfig.EMAIL_PASSWORD == "":
	eqdebug.debug_print("Email password of alert sender not present in configuration",True)
elif eqconfig.SMTP_SERVER_URL == "":
	eqdebug.debug_print("SMTP server url not present in configuration",True)

elif not path.exists(path.join(eqconfig.CONFIG_DIR,args.config)):
	eqdebug.debug_print("Config file with name '{}' not found in config directory '{}'.".format(args.config,eqconfig.CONFIG_DIR),True)
else:
	conf_filename	= args.config
	conf_filepath	= path.join(eqconfig.CONFIG_DIR,conf_filename)
	with open(conf_filepath,'rb') as fileref:
		try:
			eqdebug.debug_print("Parsing configuration file...")
			config_data				= fileref.read()
			config_data_json		= json.loads(config_data)
			
			config_data_query		= config_data_json["query"]
			config_data_subject		= config_data_json["subject"]
			config_data_content		= config_data_json["content"]
			config_data_recipients	= config_data_json["recipients"]
			config_data_dict		= config_data_json["data_dict"]
			config_data_index_name	= config_data_json["index_name"]
			eqdebug.debug_print("Configuration file parsed")
			
			auth_data = HTTPBasicAuth(eqconfig.ES_USERNAME,eqconfig.ES_PASSWORD)
			
			filename = "alert_"+datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+".csv"
			
			eqdebug.debug_print("Executing query...")
			qry = EqQuery(config_data_query, auth_data, config_data_index_name,config_data_dict)
			qry.run()
			eqdebug.debug_print("Query executed")
			
			if len(qry.results)> 0:
				qwr = EqWriter()
				qsd = EqSender()
				eqdebug.debug_print("Writing temporary file...")
				qwr.write(filename,qry.results,qry.data_dict)
				eqdebug.debug_print("Written temporary file")
				for recipient in config_data_recipients:
					eqdebug.debug_print("Sending email to {}...".format(recipient))
					qsd.send(config_data_content,config_data_subject,filename,recipient)
					eqdebug.debug_print("Email sent")
				eqdebug.debug_print("Deleting temporary file...")
				remove(filename)
				eqdebug.debug_print("Temporary file deleted")
		except KeyError as exc:
			eqdebug.debug_print("KeyError exception while parsing config file. Key {} expected and not found in config file '{}'.".format(str(exc),conf_filename),True)
		except Exception as exc:
			eqdebug.debug_print("Unexpected exception {}, exiting script.".format(str(exc)),True)