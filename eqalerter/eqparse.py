class EqParser():
	def __init__(self, query_data_dict):
		self.query_data_dict = query_data_dict
		
	def parse(self, json_data):
		parsed_data = {}
		for key in self.query_data_dict:
			path = self.query_data_dict[key]
			
			#explode path to get all the elements of a path
			path_ele = path.split('/')
			value = json_data
			
			#drill down to specific element value
			for ele in path_ele:
				if (value):
					value = self.expand(value,ele)
			parsed_data[key] = value
		return parsed_data
		
	def expand(self, json_value, ele):
		if ele in json_value:
			return json_value[ele]
			