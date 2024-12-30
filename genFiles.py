#!/usr/bin/env python3

#===========================================================#
#File Name:			buildFiles.py
#Author:			Pedro Cumino
#Email:				pedro.cumino@av.it.pt
#Creation Date:		Mon 30 Dec 16:57:57 2024
#Last Modified:		Mon 30 Dec 16:58:11 2024
#Description:
#Args:
#Usage:
#===========================================================#

import os

def main(argv):
	for file in argv:
		with open(file, 'r') as fileEntry:
			className = ''
			for line in fileEntry:
				if line[0] == "'":
					continue
				line = line.strip().split()
				line = [i for i in line if len(i) > 0]
				line = ' '.join(line)
				if 'class' in line:
					# new class found
					className = line.replace('{','').split()[-1]
					print(className)
					if not os.path.isfile(f'{className}.py'):
						cmd = f'vim {className}.py'
						os.system(cmd)
					continue
				if len(className) < 1:
					continue
				elif '}' in line and len(className) > 0:
					className = ''
				
				# if os.path.isfile(f'{className}.py'):
				# 	with open(f'{className}.py','a'):


if __name__ == '__main__':
	import sys
	main(sys.argv[1:])


