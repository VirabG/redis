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
	
	def deserialize_error(self, e):
		return e[1:-2]

	def serialize_error(self, e):
		return "-" + e + "\r\n"

	def deserialize_binary(self, s):
		int_end = s.find("\r")		
		n_bytes = int(s[1:int_end])
		data = s[(int_end+4):-2]
		return n_bytes, data

	def serialize_binary(self, s):
		n_bytes = len(s)
		return "$" + str(n_bytes) + "\r\n" + s + "\r\n"

