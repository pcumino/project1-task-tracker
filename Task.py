#!/usr/bin/env python3

#===========================================================#
#File description:			Task.py
#Author:			Pedro Cumino
#Email:				pedro.cumino@av.it.pt
#Creation Date:		Mon 30 Dec 17:10:42 2024
#Last Modified:		Mon 30 Dec 17:10:44 2024
#Description:
#Args:
#Usage:
#===========================================================#

from datetime import datetime, timedelta
import itertools

class Task():
	'''
	- description: Task description
	- dueDate: Task due date
	'''

	def __init__(self, description: str, dueDate: str=None):
		super(Task, self).__init__()
		# self.id = next(Task.id_iter)
		self.description = description
		self.dueDate = datetime.today()
		self.status = 'todo'
		self.createdAt = datetime.today()
		self.updatedAt = datetime.today()

		if dueDate is not None:
			if dueDate == 'today':
				self.dueDate += timedelta(hours=1)
			elif dueDate == 'tomorrow':
				self.dueDate = self.dueDate + timedelta(days=1)
		else:
			self.dueDate += timedelta(hours=1)

	# def getData(self):
	def __repr__(self):
		hh = self.dueDate.hour
		mm = self.dueDate.minute
		if mm < 10:
			mm = f'0{mm}'
		res = dict(
			# id=self.id,
			description=self.description,
			status=self.status,
			createdAt=f'{self.createdAt}',
			updatedAt=f'{self.updatedAt}',
			# dueDate=f'{self.dueDate} {hh}:{mm}'
		)
		return str(res).replace("'",'"')
		# return
	def getData(self):
		hh = self.dueDate.hour
		mm = self.dueDate.minute
		if mm < 10:
			mm = f'0{mm}'
		res = dict(
			# id=self.id,
			description=self.description,
			status=self.status,
			dueDate=f'{self.dueDate}',
			createdAt=f'{self.createdAt}',
			updatedAt=f'{self.updatedAt}'
		)
		return res