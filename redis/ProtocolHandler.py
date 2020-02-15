import re
LINE_SEPARATOR = '\r\n'
SEPARATOR_LENGTH = len(LINE_SEPARATOR)    # Line Separator Length

class ProtocolHandler:

    def __init__(self):
        pass

    def deserialize_string(self, s):
        return s[1 : -SEPARATOR_LENGTH]

    def serialize_string(self, s):
        return "+" + s + LINE_SEPARATOR

    def deserialize_integer(self, s):
        s = s[1 : (-SEPARATOR_LENGTH)]
        return int(s)
    
    def serialize_integer(self, n):
        return ":" + str(n) + LINE_SEPARATOR

#    def deserialize_error(self, s):
#        return s[1:-2]
#
#    def serialize_error(self, e):
#        return "-" + e + "\r\n"

    def deserialize_binary(self, s):
        int_end = s.find(LINE_SEPARATOR)
        n_bytes = int(s[1:int_end])
        data = s[(int_end + SEPARATOR_LENGTH) : (-SEPARATOR_LENGTH)]
        return bytearray(data, 'ascii')

    def serialize_binary(self, binary):
        n_bytes = len(binary)
        return "$" + str(n_bytes) + LINE_SEPARATOR + binary.decode("ascii") + LINE_SEPARATOR

#---------------------------------------------------

#    Array:
#            *{number of bytes}-{number of elements}\r\n{0 or more of above}
#    where   
#            {number of bytes} is the number of bytes in {0 or more of above} only 

    def deserialize_array(self, s):
        minus_in_line_1 = s.find('-')
        end_of_line_1 = s.find(LINE_SEPARATOR)
        n_elements = int(s[(minus_in_line_1 + 1) : end_of_line_1])
        ret_array = []
        if (n_elements == 0):
            return ret_array

        start_of_element = end_of_line_1 + SEPARATOR_LENGTH
        end_of_element = 0
        for i in range(n_elements):
            element_type = s[start_of_element]
            assert(element_type in '+:$')           # Do we need this at all?
            if element_type == '+':
                end_of_element = s.find(LINE_SEPARATOR, start_of_element)
                end_of_element += SEPARATOR_LENGTH
                ret_array.append(self.deserialize_string(s[start_of_element : end_of_element]))
            elif element_type == ':':
                end_of_element = s.find(LINE_SEPARATOR, start_of_element)
                end_of_element += SEPARATOR_LENGTH
                ret_array.append(self.deserialize_integer(s[start_of_element : end_of_element]))
            elif element_type == '$':
                end_of_first_line = s.find(LINE_SEPARATOR, start_of_element)
                end_of_element = s.find(LINE_SEPARATOR, end_of_first_line + SEPARATOR_LENGTH)
                end_of_element += SEPARATOR_LENGTH
                ret_array.append(self.deserialize_binary(s[start_of_element : end_of_element]))
            else:
                raise(Exception('Wrong element type in Array Deserialization'))
            
            start_of_element = end_of_element
        return  ret_array


    def serialize_array(self, a):
        n_elements = len(a)
        s = ''
        for i in a:
            if type(i) is int:      
                s += self.serialize_integer(i)
            elif type(i) is str:
                s += self.serialize_string(i)
            elif type(i) is bytearray:
                s += self.serialize_binary(i)
            else:
                raise(Exception("Wrong element type in Array Serialization"))

        return ('*' + str(len(s)) + '-' + str(n_elements) + LINE_SEPARATOR + s)

#---------------------------------------------------

#    Dictionary:
#            %{number of bytes}-{number of keys}\r\n{0 or more of above}
#    where   
#            {number of bytes} is the number of bytes in {0 or more of above} only 
#            and the {0 or more of above} part consists of alternating key - value pairs,
#            st keys can be only integer or a string, and the values - integer, string, binary and array

    def deserialize_dictionary(self, s):
        minus_in_line_1 = s.find('-')
        end_of_line_1 = s.find(LINE_SEPARATOR)
        n_elements = int(s[(minus_in_line_1 + 1) : end_of_line_1])
        ret_dict = {}
        if (n_elements == 0):
            return ret_dict

        start_of_key = end_of_line_1 + SEPARATOR_LENGTH
        end_of_key = 0
        start_of_value = 0
        end_of_value = 0

        for i in range(n_elements):
            # first we identifay the key of the current element
            key_type = s[start_of_key]
            key = 0
            value = 0
            assert(key_type in '+:')            # Do we need this at all?

            if key_type == '+':
                end_of_key = s.find(LINE_SEPARATOR, start_of_key)
                end_of_key += SEPARATOR_LENGTH
                key = self.deserialize_string(s[start_of_key : end_of_key])
            elif key_type == ':':
                end_of_key = s.find(LINE_SEPARATOR, start_of_key)
                end_of_key += SEPARATOR_LENGTH
                key = self.deserialize_integer(s[start_of_key : end_of_key])
            else:
                raise(Exception('Wrong key type in Dictionary Deserialization'))
            start_of_value = end_of_key

            # now we find the value
            value_type = s[start_of_value]
            if value_type == '+':
                end_of_value = s.find(LINE_SEPARATOR, start_of_value)
                end_of_value += SEPARATOR_LENGTH
                value = self.deserialize_string(s[start_of_value : end_of_value])
            elif value_type == ':':
                end_of_value = s.find(LINE_SEPARATOR, start_of_value)
                end_of_value += SEPARATOR_LENGTH
                value = self.deserialize_integer(s[start_of_value : end_of_value])
            elif value_type == '$':
                end_of_first_line = s.find(LINE_SEPARATOR, start_of_value)
                end_of_value = s.find(LINE_SEPARATOR, end_of_first_line + SEPARATOR_LENGTH)
                end_of_value += SEPARATOR_LENGTH
                value = self.deserialize_binary(s[start_of_value : end_of_value])
            elif value_type == '*':  #    *{number of bytes}-{number of elements}\r\n{0 or more of above}
                # extracting number of bytes
                minus_in_line_1_array = s.find('-', start_of_value)
                n_bytes = int(s[(start_of_value + 1) : minus_in_line_1_array])
                end_of_first_line = s.find(LINE_SEPARATOR, start_of_value)
                end_of_value = end_of_first_line + SEPARATOR_LENGTH + n_bytes
                value = self.deserialize_array(s[start_of_value : end_of_value])
            else:
                raise(Exception('Wrong value type in Dictionary Deserialization'))
            
            start_of_key = end_of_value
            ret_dict[key] = value
        return  ret_dict


    def serialize_dictionary(self, d):
        n_elements = len(d)
        s = ''
        for i in d:
            if type(i) is int:      
                s += self.serialize_integer(i)
            elif type(i) is str:
                s += self.serialize_string(i)
            else:
                raise(Exception("Wrong key type in Dictionary Serialization"))


            if type(d[i]) is int:
                s += self.serialize_integer(d[i])
            elif type(d[i]) is str:
                s += self.serialize_string(d[i])
            elif type(d[i]) is bytearray:
                s += self.serialize_binary(d[i])
            elif type(d[i]) is list:
                s += self.serialize_array(d[i])
            else:
                raise(Exception("Wrong value type in Dictionary Serialization"))

        # %{number of bytes}-{number of keys}\r\n{0 or more of above}

        return ('%' + str(len(s)) + '-' + str(n_elements) + LINE_SEPARATOR + s)


    def deserialize(self, s):
        if s[0] == '+':
            return self.deserialize_string(s)
        elif s[0] == ':':
            return self.deserialize_integer(s)
        elif s[0] == '$':
            return self.deserialize_binary(s)
        elif s[0] == '*':
            return self.deserialize_array(s)
        elif s[0] == '%':
            return self.deserialize_dictionary(s)
        else:
            raise Exception('Wrong type indicator while deserializing')


    def serialize(self, anytype):
        if type(anytype) is int:
            return self.serialize_integer(anytype)
        elif type(anytype) is str:
            return self.serialize_string(anytype)
        elif type(anytype) is bytearray:
            return self.serialize_binary(anytype)
        elif type(anytype) is list:
            return self.serialize_array(anytype)
        elif type(anytype) is dict:
            return self.serialize_dictionary(anytype)
        else:
            raise Exception('Wrong type to be serialized. Only the following types can be serialized: int, str, bytearray, list, dict')


