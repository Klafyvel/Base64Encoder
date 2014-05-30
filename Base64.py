#! /usr/bin/python3

CHAR= 'ABCDEFGHIJKLMNOPGRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='

def add_null_bytes(string, nb_of_null):
	working_string = string
	for i in range(0, nb_of_null):
		working_string += '\0'

	return working_string

def to_base_64(string):
	output_string = ''
	nb_of_null_bytes_needed = (3 - len(string)%3)
	working_string = bytes(add_null_bytes(string, nb_of_null_bytes_needed), 'utf-8') 

	while len(working_string) >= 3:
		bytes_string = working_string[:3]
		working_string = working_string[3:]

		num_val = bytes_string[0] << 16
		num_val |= bytes_string[1] << 8
		num_val |= bytes_string[2]

		if len(working_string) >= 3 or (len(working_string) < 3 and nb_of_null_bytes_needed is 0):
			output_string += CHAR[(num_val & 0xFC0000) >> 18]
			output_string += CHAR[(num_val & 0x3F000)>>12]
			output_string += CHAR[(num_val & 0xFC0)>>6]
			output_string += CHAR[num_val & 0x3F]

		elif nb_of_null_bytes_needed is 1:
			output_string += CHAR[(num_val & 0xFC0000) >> 18]
			output_string += CHAR[(num_val & 0x3F000)>>12]
			output_string += CHAR[(num_val & 0xFC0)>>6]
			output_string += CHAR[-1]

		else: # nb_of_null_bytes_needed is 2:
			output_string += CHAR[(num_val & 0xFC0000) >> 18]
			output_string += CHAR[(num_val & 0x3F000)>>12]
			output_string += CHAR[-1]
			output_string += CHAR[-1]

	return output_string

def test_to_base_64():
	string = input('Chaîne à compresser :')
	print(to_base_64(string))