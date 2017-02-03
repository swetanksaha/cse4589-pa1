import re

def parseAUTHOR(output):
	match = re.match('I, (.*?), have read and understood the course academic integrity policy.\\n', output)

	if match: return match.group(1)
	else: return None

def parseIP(output):
	match = re.match('IP:(.*?)\\n', output)
	
	if match: return match.group(1)
	else: return None

def parsePORT(output):
	match = re.match('PORT:(.*?)\\n', output)
	
	if match: return match.group(1)
	else: return None

def parseLIST(output):
	try:
		host_list = output.rstrip('\n').split('\n')
		hosts = []
		for host in host_list:
			hosts.append(host.split())

		return hosts
	except:
		return None

def parseRELAYED(output):
	match = re.match('msg from:(.*?), to:(.*?)\\n\[msg\]:(.*?)\\n', output)

	if match:
		return [match.group(1), match.group(2), match.group(3).rstrip()] 
	else: return None

def parseRECEIVED(output):
	match = re.match('msg from:(.*?)\\n\[msg\]:(.*?)\\n', output)

	if match: return [match.group(1), match.group(2).rstrip()]
	else: return None

def parseSTATISTICS(output):
	try:
		host_list = output.rstrip('\n').split('\n')
		if len(host_list) != 0:
			hosts = [] 
			for host in host_list:
				hosts.append(host.split())
			
			return hosts
	except:
		return None