import numpy as np
import json
import random

filename = 'busy_day'

class Reader(object):
	def __init__(self, ROWS, COLS, D, DEADLINE, MAX_LOAD, P, PRODUCT_WEIGHTS, W, WAREHOUSES, C, ORDERS):
		self.ROWS = ROWS 
		self.COLS = COLS 
		self.D = D # number of drones
		self.DEADLINE = DEADLINE # time
		self.MAX_LOAD = MAX_LOAD # per drone
		self.P = P # number of product types
		self.PRODUCT_WEIGHTS = PRODUCT_WEIGHTS # array of weigths
		self.W = W # number of warehouses
		self.WAREHOUSES = WAREHOUSES # array of warehouses
		self.C = C # number of customer orders
		self.ORDERS = ORDERS

class Warehouse(object):
	def __init__(self, R, C, p):
		self.R = R # num rows
		self.C = C # num slots per row
		self.ITEMS = [0]*p

class Order(object):
	def __init__(self, id, R, C, p):
		self.ID = id
		self.R = R # num rows
		self.C = C # num slots per row
		self.L = 0 # num of items
		self.ITEMS = [0] * p
		self.weight = 0


class Load(object):
	def __init__(self, drone, warehouse, product, number):
		self.drone = drone
		self.warehouse = warehouse
		self.product = product
		self.number = number

	def printCommand(self):
		return str(self.drone) + ' L ' + str(self.warehouse) + ' ' + str(self.product) + ' ' + str(self.number)

class Deliver(object):
	def __init__(self, drone, order, product, number):
		self.drone = drone
		self.order = order
		self.product = product
		self.number = number

	def printCommand(self):
		return str(self.drone) + ' D ' + str(self.order) + ' ' + str(self.product) + ' ' + str(self.number)

def readFile(filename):
	index = 0
	subIndex = 0
	curWharehouse = 0
	curOrder = 0
	P =0
	PRODUCT_WEIGHTS = []
	WAREHOUSES = []
	ORDERS = []
	with open('data/' + filename + '.in') as f:
		for line in f:
			line = line.split(' ')
			for i in range(len(line)):
				line[i] = int(line[i])
			if index == 0:
				ROWS = line[0]; COLS = line[1]; D = line[2]
				DEADLINE = line[3]; MAX_LOAD = line[4]
			elif index == 1:
				P = line[0]
			elif index == 2:
				PRODUCT_WEIGHTS = line
			elif index == 3:
				W = line[0]
			elif index < 2*W + 4 and subIndex == 0:
				WAREHOUSES.append(Warehouse(line[0], line[1], P))
				subIndex = 1
			elif index < 2*W + 4 and subIndex == 1:
				WAREHOUSES[curWharehouse].ITEMS = line
				curWharehouse += 1
				subIndex = 0
			elif index == 2*W + 4:
				C = line[0]
				subIndex = 0
			elif index < (2*W + 4 + 1 + 3 * C) and subIndex == 0:
				ORDERS.append(Order(curOrder, line[0], line[1], P))
				subIndex = 1
			elif index < (2*W + 4 + 1 + 3 * C) and subIndex == 1:
				ORDERS[curOrder].L = line[0]
				subIndex = 2
			elif index < (2*W + 4 + 1 + 3 * C) and subIndex == 2:
				for i in range(len(line)):
					ORDERS[curOrder].ITEMS[line[i]] += 1
					ORDERS[curOrder].weight += ORDERS[curOrder].ITEMS[line[i]] * PRODUCT_WEIGHTS[line[i]]
				curOrder += 1
				subIndex = 0
			index += 1

	return Reader(ROWS, COLS, D, DEADLINE, MAX_LOAD, P, PRODUCT_WEIGHTS, W, WAREHOUSES, C, ORDERS)

reader = readFile(filename)
for order in reader.ORDERS:
	print order.weight