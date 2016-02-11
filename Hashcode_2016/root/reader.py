import numpy as np
import json
import random

filename = 'busy_day'

ROWS = 0; 
COLS = 0; 
D = 0; # number of drones
DEADLINE = 0; # time
MAX_LOAD = 0; # per drone
P = 0; # number of product types
PRODUCT_WEIGTHS = [] # array of weigths
W = 0; # number of warehouses
WAREHOUSES = [] # array of warehouses
C = 0; # number of customer orders
ORDERS = []

class Warehouse(object):
  def __init__(self, R, C):
    self.R = R # num rows
    self.C = C # num slots per row
    self.ITEMS = [0]*P

class Order(object):
  def __init__(self, R, C):
    self.R = R # num rows
    self.C = C # num slots per row
    self.L = 0 # num of items
    self.ITEMS = [0]*P

def readFile(filename):
  index = 0
  subIndex = 0
  curWharehouse = 0
  curOrder = 0
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
    	  PRODUCT_WEIGTHS = line
    	elif index == 3:
    	  W = line[0]
    	elif index < 2*W + 4 and subIndex == 0:
    	  WAREHOUSES.append(Warehouse(line[0], line[1]))
    	  subIndex = 1
    	elif index < 2*W + 4 and subIndex == 1:
          WAREHOUSES[curWharehouse].ITEMS = line
          curWharehouse += 1
          subIndex = 0
        elif index == 2*W + 4:
          C = line[0]
          subIndex = 0
        elif index < (2*W + 4 + 1 + 3 * C) and subIndex == 0:
		  ORDERS.append(Order(line[0], line[1]))
		  subIndex = 1
    	elif index < (2*W + 4 + 1 + 3 * C) and subIndex == 1:
          ORDERS[curOrder].L = line[0]
          subIndex = 2
        elif index < (2*W + 4 + 1 + 3 * C) and subIndex == 2:
          print P
          for i in range(len(line)):
          	print ORDERS[curOrder].ITEMS
          	ORDERS[curOrder].ITEMS[line[i]] += 1
          curOrder += 1
          subIndex = 0
    	index += 1

readFile(filename)