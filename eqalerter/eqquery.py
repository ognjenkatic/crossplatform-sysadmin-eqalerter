import eqconfig
import eqdebug
from eqparse import EqParser
import requests
import json

class EqQuery():
	def __init__(self, req_json, req_auth, index_name, data_dict):
		self.page_index			= 0
		self.page_size			= eqconfig.PAGE_SIZE
		self.page_count			= 0
		
		self.req_auth			= req_auth
		self.req_json			= req_json
		self.req_json["size"]	= eqconfig.PAGE_SIZE
		self.host_address		= eqconfig.ES_SERVER_URL
		self.index_name 		= index_name
		self.data_dict			= data_dict
		self.results			= []
	
	def run(self):
		#set pagination start index
		self.req_json["from"] = self.page_index
		
		eqdebug.debug_print("Executing HTTP request...")
		#set request params
		post_request = requests.post("{}/{}/_search".format(self.host_address,self.index_name), headers = eqconfig.ES_REQ_HEADERS,data = json.dumps(self.req_json), auth = self.req_auth)

		eqdebug.debug_print("HTTP request executed")
		
		if post_request.status_code == 200:
			json_data = json.loads(post_request.text)
		
			hits			= json_data["hits"]["hits"]
			self.page_size	= json_data["hits"]["total"]["value"]
			
			if (len(hits) == 0):
				eqdebug.debug_print("No results found")
			else:
				eqdebug.debug_print("Parsing results...")
				for hit in hits:
					self.page_count	+=1
					parser			 = EqParser(self.data_dict)
					parsed_data		 = parser.parse(hit)
					self.results.append(parsed_data)
				
				eqdebug.debug_print("Parsed {} of {} results".format(self.page_count,self.page_size))
				#if more pages are left fetch	
				if (self.page_size > self.page_count):
					eqdebug.debug_print("Fetching the rest of the paged results...")
					self.run()
		else:
			eqdebug.debug_print("HTTP Query returned {} status".format(post_request.status_code),True)
		
