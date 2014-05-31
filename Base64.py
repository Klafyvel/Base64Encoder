#! /usr/bin/python3
# -*- coding: utf-8 -*-

CHAR= 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='

def add_null_bytes(string, nb_of_null):
	working_string = string
	for i in range(0, nb_of_null):
		working_string += '\0'

	return working_string

def to_base_64(string):
	output_string = ''
	nb_of_null_bytes_needed = (3 - len(bytes(string, 'utf-8'))%3)
	working_string = bytes(add_null_bytes(string, nb_of_null_bytes_needed), 'utf-8') 

	while len(working_string) >= 3:
		bytes_string = working_string[:3]
		working_string = working_string[3:]

		num_val = bytes_string[0] << 16
		num_val |= bytes_string[1] << 8
		num_val |= bytes_string[2]

		third_part_is_eq = len(working_string) < 3 and nb_of_null_bytes_needed is 2
		fourth_part_is_eq = len(working_string) < 3 and nb_of_null_bytes_needed <= 2

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

def remove_null_char(string):
	output_string = ''
	for c in string:
		if not c is'\0':
			output_string += c

	return output_string


def from_base_64(string):
	if not is_valid_base_64(string):
		raise ValueError('"{}" is not a valid base 64 string.'.format(string))

	output_string = u''
	working_string = string

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

		print(bin(num_val>>16))
		print(bin((num_val & 0xFF00) >> 8))
		print(bin((num_val & 0xFF)))
		
		output_string += chr(num_val>>16)
		output_string += chr((num_val & 0xFF00) >> 8)
		output_string += chr((num_val & 0xFF))

	return remove_null_char(output_string)


def test_to_base_64():
	string = input('Chaîne à encoder :')
	print(to_base_64(string))

def test_from_base_64():
	string = input('Chaîne à décoder :')
	print(from_base_64(string))