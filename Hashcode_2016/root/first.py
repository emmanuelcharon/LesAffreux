'''
Created on 11 fvr. 2016

@author: emmanuelcharon
'''


def solveOrder():
    
  # order is a cell and a list of items
  # find closest warehouse with item 0
  # then build the list of items this warehouse (still), this will be the last stop of the drone
  # go on to the next closest warehouse with the next missing item
  # stop when: either the order is fully satisfied, or the drone is completely loaded
  #   if order is satisfied, tell drone to take this trip (starting with the furthest warehouse)
  #   if drone is full: tell the drone to take this trip
  #                     take another drone to do the rest
  # 
  # for this order, we can compute the num drones needed and the duration (max time for all drones) 
  # we choose a start time when all drones are available
  # remember for each drone the time when they get available  
  
  pass

def first():
  
  pass
  # sort orders by total weight to bring there or by number of items
  # then solve each order, goal is to solve the easiest orders very fast
  
  

if __name__ == '__main__':
  
  pass