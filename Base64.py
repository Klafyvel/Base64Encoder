#! /usr/bin/python3
# -*- coding: utf-8 -*-

CHAR= 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='

def add_null_bytes(string, nb_of_null):
	working_string = string
	for i in range(0, nb_of_null):
		working_string += b'\0'
	return working_string

def to_base_64(string):
	output_string = ''
	nb_of_null_bytes_needed = (3 - len(string))%3 
	working_string = add_null_bytes(string, nb_of_null_bytes_needed)

	while len(working_string) >= 3:
		cutted_string = working_string[:3]
		working_string = working_string[3:]

		num_val = cutted_string[0] << 16
		num_val |= cutted_string[1] << 8
		num_val |= cutted_string[2]

		third_part_is_eq = len(working_string) < 3 and nb_of_null_bytes_needed is 2
		fourth_part_is_eq = len(working_string) < 3 and nb_of_null_bytes_needed in [1, 2]

		output_string += CHAR[(num_val & 0xFC0000) >> 18]
		output_string += CHAR[(num_val & 0x3F000)>>12]
		output_string += CHAR[(num_val & 0xFC0)>>6] if not third_part_is_eq else CHAR[-1]
		output_string += CHAR[num_val & 0x3F] if not fourth_part_is_eq else CHAR[-1]

	return output_string

def is_valid_base_64(string):
	returned = True
	for c in string:
		returned &= c in CHAR

	returned &= len(string) % 4 is 0

	#A Base64 string should not end with '==='
	returned &= not(string[-1] is '=' and string[-2] is '=' and string[-3] is '=')
	return returned

def found_a_char_value(char):
	if char is '=':
		return 0
	else:
		return CHAR.find(char)

def from_base_64(string):
	if not is_valid_base_64(string):
		raise ValueError('"{}" is not a valid base 64 string.'.format(string))

	output_string = []
	working_string = string

	nb_eq = (1 if string[-1] is '=' else 0) + (1 if string[-2] is '=' else 0)

	while len(working_string) >= 4:
		cutted_string = working_string[:4]
		working_string = working_string[4:]

		first_char_val = found_a_char_value(cutted_string[3])
		second_char_val = found_a_char_value(cutted_string[2])
		third_char_val = found_a_char_value(cutted_string[1])
		fourth_char_val = found_a_char_value(cutted_string[0])

		num_val =  first_char_val | (second_char_val << 6)
		num_val |= third_char_val << 12
		num_val |= fourth_char_val << 18
		
		output_string.append(num_val>>16)
		if len(working_string) >= 4 or nb_eq <= 1:
			output_string.append((num_val & 0xFF00) >> 8)
		if len(working_string) >= 4 or nb_eq is 0: 
			output_string.append((num_val & 0xFF))

	return bytes(output_string)

def encode_file(filename):
	string = []
	with open(filename, 'rb') as in_file:
		string = in_file.read()
	with open(filename + '.base64', 'w') as out_file:
		out_file.write(to_base_64(string))

def decode_file(filename):
	string = ''
	with open(filename, 'r') as in_file:
		string = in_file.read()
	string = from_base_64(string)
	with open(filename + '.dec', 'wb') as out_file:
		out_file.write(string)

def encode_string(string):
	return to_base_64(string.encode('utf-8'))
def decode_string(string):
	return from_base_64(string).decode('utf-8')