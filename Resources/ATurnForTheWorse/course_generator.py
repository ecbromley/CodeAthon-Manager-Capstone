#!/usr/bin/env python
import sys
import argparse
import random
import math

parser = argparse.ArgumentParser(
	description = 'Generates a randomly connected pipe grid to hold the snake',
	formatter_class=argparse.ArgumentDefaultsHelpFormatter
	)
parser.add_argument('-s', '--size', type = int, default = 10, help = 'Integer size and size of the grid > 1')
parser.add_argument('-d', '--delete', type = float, default = 0.15, help = 'Percentage of pipe connections to delete (0--1]')
parser.add_argument('-of', '--outfile', type = argparse.FileType('w'), default = 'field.dat', help = 'Output file name')
args = parser.parse_args()

arg_errors = False

if args.size <= 0:
	print('\nsize must be > 1')
	arg_errors = True

if args.delete <= 0.0 or args.delete > 1.0:
	print('\ndelete must be (0--1]')
	arg_errors = True

if args.outfile.closed:
	print('\nThe file is closed for some reason')
	arg_errors = True

if arg_errors:
	print('')
	parser.print_help()
	sys.exit(1)

size = args.size
delete = args.delete
f = args.outfile

cells_row = ('*-' * (size - 1)) + '*'
tween_row = ('|X' * (size - 1)) + '|'
grid_str = (cells_row + '\n' + tween_row + '\n') * (size - 1) + cells_row

delete_cnt = int(delete * (((size - 1) * 2 + size) * (size - 1) + size - 1))

print('deleting', delete_cnt, 'or so pipes\n')

def vertical(delete):
	return ' ' if random.uniform(0, 1) < delete else '|'

def horizontal(delete):
	return ' ' if random.uniform(0, 1) < delete else '-'

def cross(delete):
	rand_slash = random.uniform(0, 1) < delete
	rand_backslash = random.uniform(0, 1) < delete
	c = ''
	if rand_slash and rand_backslash:
		c = ' '
	elif rand_slash:
		c = '\\'
	elif rand_backslash:
		c = '/'
	else:
		c = 'X'

	return c

def nop_asterisk(delete):
	return '*'

def nop_newline(delete):
	return '\n'

table = {
	'|' : vertical,
	'-' : horizontal,
	'X' : cross,
	'*' : nop_asterisk,
	'\n' : nop_newline
}

trimmed = ''
for i in list(grid_str):
	trimmed += table[i](delete)

grid = [list(row) for row in trimmed.split('\n')]

while True:
	r = random.randint(0, size - 1) * 2
	c = random.randint(0, size - 1) * 2
	if grid[r][c] == '*':
		grid[r][c] = '@'
		break;

final = str('\n').join([str('').join(i) for i in grid])

print(final)
f.write(final)
