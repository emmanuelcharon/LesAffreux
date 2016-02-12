'''
Created on 11 fvr. 2016

@author: emmanuelcharon
'''
import math
from reader import Reader, Warehouse, Order, Load, Deliver, readFile

def dist(r1, c1, r2, c2):
  d = math.sqrt((r1-r2)*(r1-r2) + (c1-c2)*(c1-c2))
  return math.ceil(d)

class Drone(object):
  def __init__(self, reader, ID):
    self.R = reader.WAREHOUSES[0].R
    self.C = reader.WAREHOUSES[0].C
    self.items = [0]*reader.P # start with 0 items
    self.nextAvailableTime = 0 # available now
    self.commands = []
    self.ID = ID
    self.weight = 0
 
class Job(object):
  def __init__(self, R, C, productType, orderID):
    self.R = R
    self.C = C
    self.productType = productType
    self.orderID = orderID
    
def availableWorkers(reader, drones, t):
  result = []
  for drone in drones:
    if drone.nextAvailableTime <= t:
      result.append(drone)
  return result

def doAllJobs(reader):
  
  sortedOrders = reader.ORDERS[:]
  sortedOrders.sort(cmp=lambda x,y: cmp(x.weight, y.weight))
  #sortedOrders.sort(cmp=lambda x,y: cmp(x.L, y.L))
  
  
  allJobs = []
  for order in sortedOrders:
    for item in order.rawItems:
      job = Job(order.R, order.C, item, order.ID)
      allJobs.append(job)
  totalJobs = len(allJobs)

  drones = []
  for _ in range(0, reader.D):
    drone = Drone(reader, _)
    drones.append(drone)
  
  commands = []



  for t in range(0, reader.T):
    
     #avDrones = availableWorkers(reader, drones, t)
#     
#     tookJob = True
#     while tookJob and len(avDrones)>0 and len(allJobs)>0:
#       job = allJobs[0]
#       closestWHindex = closestWwithP(job.productType, reader, job.R, job.C)
#       wh = reader.WAREHOUSES[closestWHindex]
#       
#       closestDrone = None
#       minDist = 1000*1000*1000
#       jobTime = 0
#       
#       for drone in avDrones:
#         d = dist(wh.R, wh.C, drone.R, drone.C)
#         
#         t1 = dist(drone.R, drone.C, wh.R, wh.C) 
#         t2 = dist(wh.R, wh.C, job.R, job.C) 
#         _jobTime = t1 + t2 + 2
#         
#         if d< minDist and t+_jobTime<reader.T:
#           
#           minDist=d
#           closestDrone = drone
#           jobTime = _jobTime
#       
#       if closestDrone!=None:
#         drone = closestDrone
#         allJobs.pop(0)
#         commands.append(Load(drone.ID, closestWHindex, job.productType, 1))
#         wh.ITEMS[job.productType] -= 1
#         commands.append(Deliver(drone.ID, job.orderID, job.productType, 1))
#  
#         drone.R = job.R
#         drone.C = job.C
#         drone.nextAvailableTime += jobTime + 1
#       else:
#         tookJob = False
#         
#       avDrones = availableWorkers(reader, drones, t)
#     
#       
      
    avDrones = availableWorkers(reader, drones, t)
      
    for drone in avDrones:
       
       
      if len(allJobs) == 0:
        print "Finished all jobs at {}/{}={}".format(t, reader.T, t*1.0/reader.T)
        return commands
       
      job = allJobs[0]
       
      closestWHindex = closestWwithP(job.productType, reader, drone.R, drone.C)
      wh = reader.WAREHOUSES[closestWHindex]
       
      t1 = dist(drone.R, drone.C, wh.R, wh.C) 
      t2 = dist(wh.R, wh.C, job.R, job.C) 
      jobTime = t1 + t2 + 2
       
      if t + jobTime < reader.T:
        
        tripJobs = [job]
        peekIdx = 1
        drone.weight = reader.PRODUCT_WEIGHTS[job.productType]
        wh.ITEMS[job.productType] -= 1
            
        while peekIdx < len(allJobs) and allJobs[peekIdx].orderID == job.orderID:
          nextJob = allJobs[peekIdx]
          if t + jobTime + 2 < reader.T and wh.ITEMS[nextJob.productType]>0 and reader.PRODUCT_WEIGHTS[nextJob.productType] + drone.weight<=reader.MAX_LOAD :
            tripJobs.append(nextJob)
            wh.ITEMS[nextJob.productType] -= 1
            jobTime+=2
            drone.weight += reader.PRODUCT_WEIGHTS[nextJob.productType]
            peekIdx+=1  
          else:
            break
          
          
        #print len(tripJobs)
        
        countsPT = [0]*reader.P
        for tripJob in tripJobs:
          allJobs.pop(0)
          countsPT[tripJob.productType]+=1
        
        for pT in range(0, len(countsPT)):
          if countsPT[pT]>0:
            commands.append(Load(drone.ID, closestWHindex, pT, countsPT[pT]))
        for pT in range(0, len(countsPT)):
          if countsPT[pT]>0:
            commands.append(Deliver(drone.ID, job.orderID, pT, countsPT[pT]))
        
        drone.R = job.R
        drone.C = job.C
        drone.nextAvailableTime += jobTime + 1
        drone.weight = 0
      
  print "Finished time with {}/{} remaining jobs".format(len(allJobs), totalJobs)
          
  return commands

#closest warehouse with an item of type productType
def closestWwithP(productType, reader, r, c):
  
  d = 1000*1000*1000
  closest = 0
  
  for whID in range(len(reader.WAREHOUSES)):
    wh = reader.WAREHOUSES[whID]
    
    if wh.ITEMS[productType] > 0:
      d_wh = dist(wh.R, wh.C, r, c)
      if d_wh < d:
        closest = whID
  return closest

def locationCompare(jobA, jobB):
  if jobA.R < jobB.R:
    return 1
  elif jobA.R > jobB.R:
    return-1
  else: # same R
    if jobA.C < jobB.C:
      return 1
    elif jobA.C > jobB.C:
      return -1
    else:
      return cmp(jobA.weight, jobB.weight)
    

def secondAl(reader):
  
  sortedOrders = reader.ORDERS[:]
  #sortedOrders.sort(cmp=lambda x,y: cmp(x.weight, y.weight))
  #sortedOrders.sort(cmp=lambda x,y: cmp(x.L, y.L))
  sortedOrders.sort(cmp=lambda x,y: locationCompare(x, y))
  #
  
  allJobs = []
  for order in sortedOrders:
    for item in order.rawItems:
      job = Job(order.R, order.C, item, order.ID)
      allJobs.append(job)
  totalJobs = len(allJobs)

  drones = []
  for _ in range(0, reader.D):
    drone = Drone(reader, _)
    drones.append(drone)
  
  commands = []

  for t in range(0, reader.T):
    avDrones = availableWorkers(reader, drones, t)
      
    for drone in avDrones:
      if len(allJobs) == 0:
        print "Finished all jobs at {}/{}={}".format(t, reader.T, t*1.0/reader.T)
        return commands
       
      job = allJobs[0]
      closestWHindex = closestWwithP(job.productType, reader, drone.R, drone.C)
      wh = reader.WAREHOUSES[closestWHindex]
       
      t1 = dist(drone.R, drone.C, wh.R, wh.C) 
      t2 = dist(wh.R, wh.C, job.R, job.C) 
      jobTime = t1 + t2 + 2
       
      if t + jobTime < reader.T:
        tripJobs = [job]
        peekIdx = 1
        drone.weight = reader.PRODUCT_WEIGHTS[job.productType]
        wh.ITEMS[job.productType] -= 1
            
        while peekIdx < len(allJobs) and allJobs[peekIdx].R == job.R and allJobs[peekIdx].C == job.C:
          nextJob = allJobs[peekIdx]
          if t + jobTime + 2 < reader.T and wh.ITEMS[nextJob.productType]>0 and reader.PRODUCT_WEIGHTS[nextJob.productType] + drone.weight<=reader.MAX_LOAD :
            tripJobs.append(nextJob)
            wh.ITEMS[nextJob.productType] -= 1
            jobTime+=2
            drone.weight += reader.PRODUCT_WEIGHTS[nextJob.productType]
            peekIdx+=1  
          else:
            break
        
        for tripJob in tripJobs:
          allJobs.pop(0)
          commands.append(Load(drone.ID, closestWHindex, tripJob.productType, 1))
        for tripJob in tripJobs:
          commands.append(Deliver(drone.ID, tripJob.orderID, tripJob.productType, 1))
        
        drone.R = job.R
        drone.C = job.C
        drone.nextAvailableTime += jobTime + 1
        drone.weight = 0
      
  print "Finished time with {}/{} remaining jobs".format(len(allJobs), totalJobs)
          
  return commands

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

if __name__ == '__main__':
  filenames = ['busy_day', 'mother_of_all_warehouses', 'redundancy']
  for filename in filenames:
    rd = readFile(filename)

    commands = doAllJobs(rd)
    with open(filename + '-result.txt', 'w') as f:
      f.write(str(len(commands)) + "\n")
      for com in commands:
        f.write(com.printCommand() + "\n")
