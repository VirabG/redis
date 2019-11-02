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

test_string_deserialization()
test_string_serialization()
test_integer_deserialization()
test_integer_serialization()


