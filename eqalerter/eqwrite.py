import csv

class EqWriter():
	def write(self, filepath, query_results, query_data_dict):
		with open(filepath, 'w') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=query_data_dict.keys())
			writer.writeheader()
			for entry in query_results:
				writer.writerow(entry)