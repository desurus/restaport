import subprocess
import re


class TctlHandler:
	"""
	Provides methods to manipulate tctl cli utility.
	"""

	def get_all_tokens(self):
		"""
		Returns list of all tokens.
		"""
		result = []

		res = self.run_shell('sudo /usr/local/bin/tctl tokens ls')
		for l in res.splitlines():
			if "No active tokens found." in l:
				return ['No active tokens found.']
			# skip first two lines of text
			if "Token" in l or "---" in l:
				continue
			# parse line for works
			m = re.search('(\w+)\s+(\w+,{0,1}\w+)\s+(.*)', l)
			result.append({
				"token": m.group(1).strip(),
				"type": m.group(2).strip(),
				"expires": m.group(3).strip(),
			})

		return result


	def create_token(self, request):
		"""
		Create new token to add new node to the cluster.
		"""
		result = []

		res = self.run_shell("sudo /usr/local/bin/tctl nodes add --ttl={}m --roles=node,proxy".format(request.form['ttl']))
		for l in res.splitlines():
			if "The invite token" in l:
				m = re.search('(\w+)$', l)
				result.append({"token": m.group(1).strip()})

		return result


	def run_shell(self, cmd):
		"""
		Run shell command that is not suppose to run in the background and get
		results immediately.
		:param: cmd: String of params and shell command, i.e. "ls -l"
		"""
		# execute shell command
		res = subprocess.check_output(cmd, shell=True)
		return res
