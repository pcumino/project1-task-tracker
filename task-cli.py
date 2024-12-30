#!/usr/bin/env python3

#===========================================================#
#File Name:			TaskCLI.py
#Author:			Pedro Cumino
#Email:				pedro.cumino@av.it.pt
#Creation Date:		Mon 30 Dec 17:10:45 2024
#Last Modified:		Mon 30 Dec 17:10:46 2024
#Description:
#Args:
#Usage:
#===========================================================#

import os
import json
from datetime import datetime
from configparser import ConfigParser as cfgp

from Task import Task

def markInProgress(taskid, filename):
	assert type(taskid) == int, "Task id must be an integer."
	try:
		with open(filename, 'r') as file:
			content = json.load(file)
		
		data_dict = {int(i['id']):i for i in content}
		if taskid not in data_dict:
			print(f'Task id "{taskid}" not found.')
			return False
		
		for i in content:
			if i['id'] == taskid:
				i['status'] = 'in-progress'
				i['updatedAt'] = f'{datetime.today()}'

		res = str(content).replace("'",'"').replace(': ',':')
		with open(filename, 'w') as file:
			file.write(res)
		return True
	except Exception as e:
		print('Error while updating task:', taskid)
		return False

def markDone(taskid, filename):
	assert type(taskid) == int, "Task id must be an integer."
	try:
		with open(filename, 'r') as file:
			content = json.load(file)
		
		data_dict = {int(i['id']):i for i in content}
		if taskid not in data_dict:
			print(f'Task id "{taskid}" not found.')
			return False
		
		for i in content:
			if i['id'] == taskid:
				i['status'] = 'done'
				i['updatedAt'] = f'{datetime.today()}'

		res = str(content).replace("'",'"').replace(': ',':')
		with open(filename, 'w') as file:
			file.write(res)
		return True
	except Exception as e:
		print('Error while updating task:', taskid)
		return False





def updateTask(taskid, newDesc, filename=None):
	assert type(filename) == str, "File name must be set as a string."
	assert type(taskid) == int, "Task id must be an integer."
	assert type(newDesc) == str, "New description must be a string."

	try:
		with open(filename, 'r') as file:
			content = json.load(file)
		
		data_dict = {int(i['id']):i for i in content}
		if taskid not in data_dict:
			print(f'Task id "{taskid}" not found.')
			return False
		
		for i in content:
			if i['id'] == taskid:
				i['description'] = newDesc
				i['updatedAt'] = f'{datetime.today()}'

		res = str(content).replace("'",'"').replace(': ',':')
		with open(filename, 'w') as file:
			file.write(res)
		return True
	except Exception as e:
		print('Error while updating task:', taskid)
		return False


def deleteTask(taskid, filename=None):
	assert type(filename) == str, "File name must be set as a string."
	assert type(taskid) == int, "Task id must be an integer."

	try:
		with open(filename, 'r') as file:
			content = json.load(file)
		
		data_dict = {int(i['id']):i for i in content}
		if taskid not in data_dict:
			print(f'Task id "{taskid}" not found.')
			return False
		
		content = [i for i in content if i['id'] != taskid]
		res = str(content).replace("'",'"').replace(': ',':')
		with open(filename, 'w') as file:
			file.write(res)
		return True
	except Exception as e:
		print('Error while deleting task:', taskid)
		return False


def addTask(taskName, dueDate, filename=None):
	assert type(filename) == str, "File name must be set as a string"

	newTask = Task(taskName, dueDate)
	# print('newTask:')
	# print(newTask)
	content = []
	try:
		with open(filename, 'r') as file:
			content = json.load(file)

		taskData = newTask.getData()
		
		for i in content:
			if taskData['description'] == i['description']:
				print('This task name already exists.')
				return False

		if len(content) == 0:
			taskData['id'] = 1
		else:
			maxId = 0
			for i in content:
				maxId = max(int(i['id']),maxId)
			taskData['id'] = maxId+1
		
		content.append(taskData)

		res = str(content).replace("'",'"').replace(': ',':')
		with open(filename, 'w') as file:
			file.write(res)
		
		print('Task added successfully (ID: {}).'.format(taskData['id']))
		return True

	except Exception as e:
		print('Error while adding a new task:', e)
		return False

def listTasks(filename=None, status=None):
	assert type(filename) == str, "File name must be set as a string"
	with open(filename, 'r') as file:
		content = json.load(file)
	
	if len(content) < 1:
		print('Empty task list')
		return
	header = f'{"":6}[Description]'
	header += f'{"":18}[Due date]'
	header += f'{"":21}[Status]'
	header += f'{"":8}[Created at]'
	header += f'{"":18}[Last update]'
	print(header)
	for i in content:
		if i['status'] != status and status is not None:
			continue
		msg = ""
		msg += f"{i['id']:4})"
		msg += f" {i['description']:30}"
		msg += f" {i['dueDate']:30}"
		msg += f" {i['status']:15}"
		msg += f" {i['createdAt']:29}"
		msg += f" {i['updatedAt']:30}"
		print(msg)

def main(argv):
	func = argv[0]
	
	config = cfgp()
	config.read('config.cfg')
	
	filename = config['DEFAULT']['filename']
	
	if func == 'set-list-name':
		assert len(argv) == 2, f"'{func}' requires an argument as the name for the task list"
		filename = argv[1]
		if '.json' not in filename:
			filename = filename+'.json'
		
		default_changed = config['DEFAULT']['filename'] == filename
		config.set('DEFAULT','filename',filename)
		with open('config.cfg', 'w') as configfile:
			config.write(configfile)
		
		if not default_changed:
			print('New default file name for the task list:', filename)
	if not os.path.isfile(filename):
		with open(filename, 'w') as file:
			file.write('[]')
		print(f'New file created: {filename}')
	
	if func == 'list':
		assert len(argv) > 0, f"'{func}' requires 1 argument for the task id and the new description."
		status = None
		if len(argv) == 2:
			assert type(argv[1]) == str, "Status must be a string."
			validStatus = argv[1] == 'done'
			validStatus |= argv[1] == 'in-progress'
			validStatus |= argv[1] == 'todo'
			validStatus |= argv[1] == None
			assert validStatus, "Status not valid."
			status = argv[1].lower()

		listTasks(filename, status)

	elif func == 'mark-in-progress':
		assert len(argv) == 2, f"'{func}' requires 1 argument for the task id and the new description."
		assert argv[1].isnumeric() == True, "Task id must be an integer."
		taskid = int(argv[1])
		markInProgress(taskid, filename)
		
	elif func == 'mark-done':
		assert len(argv) == 2, f"'{func}' requires 1 argument for the task id and the new description."
		assert argv[1].isnumeric() == True, "Task id must be an integer."
		taskid = int(argv[1])
		markDone(taskid, filename)
		
		
	elif func == 'update':
		assert len(argv) == 3, f"'{func}' requires 2 argument for the task id and the new description."
		assert argv[1].isnumeric() == True, "Task id must be an integer."
		assert argv[2].isnumeric() == False, "New description must be a string."
		
		taskid = int(argv[1])
		newDesc = argv[2]
		updateTask(taskid, newDesc, filename)
		
	elif func == 'delete':
		assert len(argv) == 2, f"'{func}' requires 1 argument for the task id."
		assert argv[1].isnumeric() == True, f"The id must be a number."
		
		taskid = int(argv[1])
		deleteTask(taskid, filename)

	elif func == 'add':
		assert len(argv) > 1, f"'{func}' requires at least an argument as the name for the task."
		assert argv[1].isnumeric() == False, "The argument must be a string"
		taskName = argv[1]
		dueDate = None
		if len(argv) > 2:
			dueDate = argv[2]
		addTask(taskName, dueDate, filename)
	else:
		print('Unknown command')


if __name__ == '__main__':
	import sys
	main(sys.argv[1:])


