from ProtocolHandler import ProtocolHandler

handler = ProtocolHandler()

def test_string_deserialization():
	serialized = "+OK\r\n"
	actual = handler.deserialize_string(serialized)
	expected = "OK"
	assert(actual == expected)
	print("test string deserialization passed.")

def test_string_serialization():
	input = "OK"
	actual = handler.serialize_string(input)
	expected = "+OK\r\n"
	assert(actual == expected)
	print("test string serialization passed.")

def test_integer_deserialization():
	serialized = ":111\r\n"
	actual = handler.deserialize_integer(serialized)
	expected = 111
	assert(actual == expected)
	print("test integer deserialization passed.")

def test_integer_serialization():
	input = 111
	actual = handler.serialize_integer(input)
	expected = ":111\r\n"
	assert(actual == expected)
	print("test integer serialization passed.")

def test_error_deserialization():
	serialized = "-I am an error\r\n"
	actual = handler.deserialize_error(serialized)
	expected = "I am an error"
	assert (actual == expected)
	print("test error deserialization passed.")

def test_error_serialization():
	input = "I am an error"
	actual = handler.serialize_error(input)
	expected = "-I am an error\r\n"
	assert (actual == expected)
	print("test error serialization passed.")

test_string_deserialization()
test_string_serialization()
test_integer_deserialization()
test_integer_serialization()
test_error_deserialization()
test_error_serialization()


