#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 21:36:36 2019

@author: nirav
"""
import time
import heapq
import gc
#----------------------------- Class node defined -------------------------------------------#
class node:
    #Functions:
    # __init__ :  Used to initiate the object for any node.
    # __lt__    : overrides less than comparator for nodes.
    
    def __init__(self, locations, parent, transition, out_Mat):
    #   Parameters:
    #           'locations' - List of coordinates of each tile.
    #           'transition' - Transition to reach this state from parent state.
    #           'parent'     - References the parent object of the current object . 
    #           'out_Mat'    - Goal State of the problem.
    
        self.locations  = locations                                            #Stores location coordinates as 2D list
        self.parent     = parent                                               #References parent object
        self.transition = transition                                           #Stores transition from parent to current object
        
        #level : Stores current level in the graph from starting node. i.e. the path length
        if(parent == None):
            self.level = 0       
        else:
            self.level      = parent.level + 1
        
        #If out_Mat is None than we don't need cost and will do normal bfs.Cost will be zero.
        if(out_Mat != None):
            
            #3 axis defined with coordinates of tiles
            axis1       = [[0, 0], [30, 0], [60, 0], [90, 0], [120, 0], [150, 0], [180, 180], [150,180], [120, 180], [90, 180], [60, 180], [30, 180]]
            axis2       = [[0, 0], [30, 90], [60, 90], [90, 90], [120, 90], [150, 90], [180, 180],[150, 270], [120, 270], [90, 270], [60, 270], [30, 270]]
            axis3       = [[90, 0], [90, 30], [90, 60], [90, 90], [90, 120], [90, 150], [90, 180], [90, 210], [90, 240], [90, 270], [90, 300], [90, 330]]
            
            ############################-----------------Heuristic Cost Calculation-----------------------###################################
            if parent == None:
                self.cost = 0                                                  #If it is the starting object then cost is 0 
            else:
                g       = locations                                            #Assigned locations to g for easy usage for future formulations      
                cost    = 0                                                    #Initialized cost to 0
                
                #Iterating through every tile and calculating the moves required for it to reach its destination. Explained in detail in report.
                
                for tile in range(len(g)):
                    if g[tile][1] == 0 or g[tile][1] == 180:
                        if out_Mat[tile][1] == 90 or out_Mat[tile][1] == 270:
                            cost1 = abs(axis1.index([0,0]) - axis1.index(g[tile])) + abs(axis2.index([0,0]) - axis2.index(out_Mat[tile]))
                            cost2 = abs(axis1.index([180,180]) - axis1.index(g[tile])) + abs(axis2.index([180,180]) - axis2.index(out_Mat[tile]))
                            cost  += min(cost1,cost2)
                        elif out_Mat[tile][0] == 90:
                            cost1 = abs(axis1.index([90,0]) - axis1.index(g[tile])) + abs(axis3.index([90,0]) - axis3.index(out_Mat[tile]))
                            cost2 = abs(axis1.index([90,180]) - axis1.index(g[tile])) + abs(axis3.index([90,180]) - axis3.index(out_Mat[tile]))
                            cost  += min(cost1,cost2)
                        else :
                            cost1 = abs(axis1.index(out_Mat[tile]) - axis1.index(g[tile]))
                            cost  += cost1
                    elif g[tile][1] == 90 or g[tile][1] == 270:
                        if out_Mat[tile][1] == 0 or out_Mat[tile][1] == 180:
                            cost1 = abs(axis2.index([0,0]) - axis2.index(g[tile])) + abs(axis1.index([0,0]) - axis1.index(out_Mat[tile]))
                            cost2 = abs(axis2.index([180,180]) - axis2.index(g[tile])) + abs(axis1.index([180,180]) - axis1.index(out_Mat[tile]))
                            cost  += min(cost1,cost2)
                        elif out_Mat[tile][0] == 90:
                            cost1 = abs(axis2.index([90,90]) - axis2.index(g[tile])) + abs(axis3.index([90,90]) - axis3.index(out_Mat[tile]))
                            cost2 = abs(axis2.index([90,270]) - axis2.index(g[tile])) + abs(axis3.index([90,270]) - axis3.index(out_Mat[tile]))
                            cost  += min(cost1,cost2)
                        else :
                            cost1 = abs(axis2.index(out_Mat[tile]) - axis2.index(g[tile]))
                            cost  += cost1
                    elif g[tile][0] == 90:
                        if out_Mat[tile][1] == 0 or out_Mat[tile][1] == 180:
                            cost1 = abs(axis3.index([90,0]) - axis3.index(g[tile])) + abs(axis1.index([90,0]) - axis1.index(out_Mat[tile]))
                            cost2 = abs(axis3.index([90,180]) - axis3.index(g[tile])) + abs(axis1.index([90,180]) - axis1.index(out_Mat[tile]))
                            cost  += min(cost1,cost2)
                        elif out_Mat[tile][1] == 90 or out_Mat[tile][1] == 270:
                            cost1 = abs(axis3.index([90,90]) - axis3.index(g[tile])) + abs(axis2.index([90,90]) - axis2.index(out_Mat[tile]))
                            cost2 = abs(axis3.index([90,270]) - axis3.index(g[tile])) + abs(axis2.index([90,270]) - axis2.index(out_Mat[tile]))
                            cost  += min(cost1,cost2)
                        else:
                            cost1 = abs(axis3.index(out_Mat[tile]) - axis3.index(g[tile]))
                            cost  += cost1
                
                path_cost   = self.level*12
                self.cost   = cost+path_cost
                
                ###############################################################################################################################
    # Override function to compare 2 node objects    
    def __lt__(self, N):
        return self.cost < N.cost
    
#Initialized global discovered list to avoid exploration of redundant nodes.
Discovered = {}
    
def find_children(inp, out_Mat = None):
    #Usage:
    #       used to find children by permuations of 3 axis rotations up and down from current state.
    #Parameters:
    #   inp     : input node to find children.
    #   out_Mat : used to pass to node object when initializing for it to calcualte cost in case of A* or RBFS.
    #Return:
    #   List of children in form of node objects.
    
    #Declaring the global variable
    global Discovered
    
    #3 axis defined with coordinates of tiles
    axis1       = [[0, 0], [30, 0], [60, 0], [90, 0], [120, 0], [150, 0], [180, 180], [150,180], [120, 180], [90, 180], [60, 180], [30, 180]]
    axis2       = [[0, 0], [30, 90], [60, 90], [90, 90], [120, 90], [150, 90], [180, 180],[150, 270], [120, 270], [90, 270], [60, 270], [30, 270]]
    axis3       = [[90, 0], [90, 30], [90, 60], [90, 90], [90, 120], [90, 150], [90, 180], [90, 210], [90, 240], [90, 270], [90, 300], [90, 330]]
    
    #Permute through all 6 possible ups and downs from three axis and generate children
    child1      = [axis1[(axis1.index(tile)+1)%len(axis1)] if tile in axis1 else tile for tile in inp.locations]
    transition1 = 'increase_0-180'
    child2      = [axis2[(axis2.index(tile)+1)%len(axis2)] if tile in axis2 else tile for tile in inp.locations]
    transition2 = 'increase_90-270'
    child3      = [axis3[(axis3.index(tile)+1)%len(axis3)] if tile in axis3 else tile for tile in inp.locations]
    transition3 = 'increase_Equator'

    child4      = [axis1[(axis1.index(tile)-1)%len(axis1)] if tile in axis1 else tile for tile in inp.locations]
    transition4 = 'decrease_0-180'
    child5      = [axis2[(axis2.index(tile)-1)%len(axis2)] if tile in axis2 else tile for tile in inp.locations]
    transition5 = 'decrease_90-270'
    child6      = [axis3[(axis3.index(tile)-1)%len(axis3)] if tile in axis3 else tile for tile in inp.locations]
    transition6 = 'decrease_Equator'
    
    children    = [child1, child4, child2, child5, child3, child6]
    transitions = [transition1, transition4, transition2, transition5, transition3, transition6]
    
    #Initialize children as node object and return it
    children    = [node(children[i],inp,transitions[i],out_Mat) for i in range(len(children)) if str(children[i]) not in Discovered.keys()]
    return children

###################################################------- Breadth First Search --------- #########################################################
def bfs(input_file):
    #Usage:
    #       used to find the path from start node to goal node using breadth first search
    #Paramerters:
    #       input_file : To get start and goal state coordinates of tiles
    #Return:
    #       steps : Total states explored
    #       queue_max : Maximum queue size during the search
    #       len(path)-1 : Length of path
    #       path[1:]    : Path in the form of transitions from start to goal state
    
    T0=time.time()
    print(input_file)
    input_file  = open(input_file).read()                                 #Read Input File 
    
    #Take the input of start and goal state in inp_Mat and out_Mat as 2d coordinate list
    tiles       = input_file.split("\n")[1:-2]                                
    inp_Mat = []
    out_Mat = []
    for tile in tiles:
        tile = tile.strip('Tile()').split(", ")
        inp  = tile[1].strip('()').split(",")
        inp_Mat.append([int(inp[0]),int(inp[1])])
        out  = tile[2].strip('Exact()').split(",")
        out_Mat.append([int(out[0]),int(out[1])])
    
    #Initialize queue_max,steps,queue,curr_level
    queue_max = 0
    steps=0
    queue = [node(inp_Mat,None,None,None)]
    curr_level = None
    
    #Start iterating through the queue starting from first element while queue is not empty or we get a goal state
    while(len(queue) > 0):
        queue_max = max(len(queue),queue_max)                                  #Calculating max queue length 
        curr_state = queue.pop(0)                                              #initialize curr_state with front of queue 
        
        if(curr_level != curr_state.level):     
            curr_level = curr_state.level
            print(curr_level,time.time()-T0)
        
        if str(curr_state.locations) in Discovered.keys():                     #if State is already discovered then skip it
            continue
        
        Discovered[str(curr_state.locations)] = True                           #Mark current state as explored 
        
        #If current state is the goal state then traverse path and return path,path length,queue_max and steps
        if curr_state.locations == out_Mat:     
            print("AAi gayu",steps,time.time()-T0)
            traverse_node   = curr_state
            path            = []
            while traverse_node != None:
                path.append(traverse_node.transition)
                traverse_node = traverse_node.parent
            
            path.reverse()
        
            return steps, queue_max, len(path)-1, path[1:]
        
        if(time.time()- T0 >  1200):
            return steps, queue_max, None, None
        
        #If current state is not goal state then explore its children and append at the end of the queue
        children = find_children(curr_state,None)
        queue.extend(children)
        steps+=1
###################################################################################################################################################

####################################################------------- A* Search ------------- #########################################################
def A_star(input_file):
    #Usage:
    #       used to find the path from start node to goal node using Heuristic A* Search
    #Paramerters:
    #       input_file : To get start and goal state coordinates of tiles
    #Return:
    #       steps : Total states explored
    #       queue_max : Maximum queue size during the search
    #       len(path)-1 : Length of path
    #       path[1:]    : Path in the form of transitions from start to goal state
    T0=time.time()
    print(input_file)
    input_file  = open(input_file).read()                                 #Read The input file
    
    #Take the input of start and goal state in inp_Mat and out_Mat as 2d coordinate list
    tiles       = input_file.split("\n")[1:-2]
    inp_Mat = []
    out_Mat = []
    for tile in tiles:
        tile = tile.strip('Tile()').split(", ")
        inp  = tile[1].strip('()').split(",")
        inp_Mat.append([int(inp[0]),int(inp[1])])
        
        out  = tile[2].strip('Exact()').split(",")
        out_Mat.append([int(out[0]),int(out[1])])
    
    #Initialize queue_max,steps,queue,curr_level
    queue = [node(inp_Mat,None,None,out_Mat)]
    queue_max = 0
    curr_level = None
    steps=0
    
    #Start iterating through the heap queue starting from element with least cost while queue is not empty or we get a goal state
    while(len(queue) > 0):
        queue_max = max(len(queue),queue_max)                                  #Calculating max queue length 
        curr_state = heapq.heappop(queue)                                      #initialize curr_state with front of queue i.e. the element with lowest cost

        if(curr_level != curr_state.level):                             
            curr_level = curr_state.level
            #print(curr_level)
        
        if str(curr_state.locations) in Discovered.keys():                     #if State is already discovered then skip it 
            continue
         
        Discovered[str(curr_state.locations)] = True                           #Mark current state as explored 
        
        #If current state is the goal state then traverse path and return path,path length,queue_max and steps
        if curr_state.locations == out_Mat:
            print("AAi gayu",steps,time.time()-T0)
            traverse_node   = curr_state
            path            = []
            while traverse_node != None:
                path.append(traverse_node.transition)
                traverse_node = traverse_node.parent
            
            path.reverse()
            
            return steps, queue_max, len(path)-1, path[1:]
        
        #If current state is not goal state then explore its children and append according to cost in increasing order using heap push
        children = find_children(curr_state,out_Mat)
        for child in children:
            heapq.heappush(queue,child)
        steps+=1
###################################################################################################################################################
        
##################################################################----RBFS-----####################################################################
steps = 0                  #Used to calculate total states explored
queue_max = 0                    #Used to find maximum length of queue after execution
             
def rbfs_core(input_file):
    #Usage:
    #       used to find the path from start node to goal node using Heuristic Recursive Best First Search
    #Paramerters:
    #       input_file : To get start and goal state coordinates of tiles
    #Return:
    #       steps : Total states explored
    #       queue_max : Maximum queue size during the search
    #       len(path)-1 : Length of path
    #       path[1:]    : Path in the form of transitions from start to goal state
    
    input_file  = open(input_file_name).read()          #Read input file
    tiles       = input_file.split("\n")[1:-2]
    global steps, queue_max
    steps = 0
    queue_max = 0  
    #Take the input of start and goal state in inp_Mat and out_Mat as 2d coordinate list
    inp_Mat = []
    out_Mat = []
    for tile in tiles:
        tile = tile.strip('Tile()').split(", ")
        inp  = tile[1].strip('()').split(",")
        inp_Mat.append([int(inp[0]),int(inp[1])])
        
        out  = tile[2].strip('Exact()').split(",")
        out_Mat.append([int(out[0]),int(out[1])])
    
    
    #Main RBFS function which will be called recursively
    def rbfs(node, max_cost, out_Mat):

        global steps, queue_max                 #Declaring global variables to keep track of states and max Queue length
        
        #If Current State is Goal State then return the goal state
        if node.locations == out_Mat:
            return node, None
        
        #Find all children of current state and replace its cost by maximum of current state's cost and its own cost.
        children = find_children(node,out_Mat)
        queue    = []
        steps  = steps+1
        for child in children:
            child.cost = max(child.cost,node.cost)
        [heapq.heappush(queue,child) for child in children]                 #Push all children in heap
        
        queue_max += len(queue)
        
        #Iterate till we get goal and calculate best and second best node and call RBFS recursively on best node
        while True:
            Node        = heapq.heappop(queue)              #Best Node
            Max_cost    = min(queue[0].cost,max_cost)       #Calculate max cost which is minimum of Seconf best node's cost and current max cost
            
            #If Node's cost is greater then max cost then propogate the node cost to parent
            if Node.cost > max_cost:
                return None, Node.cost
            
            #Recurssively call rbfs on best node with Max cost as cut off cost.
            N, Node.cost = rbfs(Node, Max_cost, out_Mat)
            
            #If N is returned as goal state then recurssively return back the goal state
            if(N is not None):
                return N, None
            
            #Else push the current Node with its updated cost into the queue
            heapq.heappush(queue,Node)
                    
    #Call RBFS on root node
    r,_ = rbfs(node(inp_Mat,None,None,out_Mat), 1000, out_Mat)
    if(r == None):
        return steps, queue_max, None, None
    
    #traverse path and return path,path length,queue_max and steps
    traverse_node   = r
    path            = []
    while traverse_node != None:
        path.append(traverse_node.transition)
        traverse_node = traverse_node.parent
    
    path.reverse()
    
    return steps, queue_max, len(path)-1, path[1:] 
###################################################################################################################################################
    
if __name__ == '__main__':
    
    rbfs_done=[1,2,3,4,5,6,8,9,11,12,13,14,15,16,18]
    
    for i in rbfs_done[12:13]:
        input_file_name = "Assign2Files/Puzzle2-"+str(i)+".mb"
        T0 = time.time()
        #States_exp, Max_q, Path_len, Path = A_star(input_file_name)
        #States_exp, Max_q, Path_len, Path = bfs(input_file_name)
        print("Garbage Collection Started")
        gc.collect()
        print("Garbage Collection Finished")
        States_exp, Max_q, Path_len, Path =  rbfs_core(input_file_name)
#        print(path,path_len)
        print(States_exp, Max_q, Path_len, Path)
        out_file_name = input_file_name.replace("Puzzle2","Puzzle2sol_a_star")
        out_file = open("RBFS3.txt","a+")
        out_file.write(str(i+1)+".  Puzzle2-"+str(i)+"\n")
        if(Path == None):
            out_file.write(str(i+1)+"\tTerminated after 20 Mins.Following are the variables when terminated"+str(i)+"\n")
        out_file.write("\ta. States Expanded: "+str(States_exp)+"\n")
        out_file.write("\tb. Maximum Queue: "+str(Max_q)+"\n")
        if(Path != None):
            out_file.write("\tc. Path Length: "+str(Path_len)+"\n")
            out_file.write("\td. Path:\n")
            romans= ['i','ii','iii','iv','v','vi','vii','viii','ix','x','xi','xii','xiii','xiv','xv','xvi','xvii']
            [out_file.write("\t\t"+romans[p]+'\t'+Path[p]+"\n") for p in range(len(Path))]
        out_file.write("\te. Time Taken: "+str(round(time.time()-T0,2))+"\n\n")
        out_file.close()
    
    """
    ALG = sys.argv[1]
    input_file_name = sys.argv[2]
    print(sys.argv)
    
    if ALG == "BFS":
        print("BFS")
        States_exp, Max_q, Path_len, Path = bfs(input_file_name)
    elif ALG == "AStar":
        States_exp, Max_q, Path_len, Path = A_star(input_file_name)
    elif ALG == "RBFS":
        States_exp, Max_q, Path_len, Path =  rbfs_main(input_file_name)
    
    print("States Expanded : ",States_exp)
    print("Max Queue Length : ",Max_q)
    print("Path Length : ",Path_len)
    print("Path",Path)
    print(States_exp, Max_q, Path_len, Path)
"""

    
    
    
    
    
    