class ProtocolHandler:
	def deserialize_string(self, s):
		return s[1:-2]

	def serialize_string(self, s):
		return "+" + s + "\r\n"

	def deserialize_integer(self, s):
		s = s[1:-2]
		return int(s)
	
	def serialize_integer(self, n):
		return ":" + str(n) + "\r\n"
		
