import eqconfig

def debug_print(message,is_warning = False):
	try:
		if (eqconfig.VERBOCITY > 0 or is_warning == True):
			symbol = "[+] " if not is_warning else "[!] "
			print("{} {}".format(symbol,message))
	except Exception as exc:
		print(exc)