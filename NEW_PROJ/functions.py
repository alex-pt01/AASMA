#QL2 functions ---------------------------------------------------------------------------------------
def get_coordinates_from_file(filename):
    with open(filename, "r") as file:
        layout = file.readlines()
        layout = [x.replace('\n','') for x in layout]
        layout = [','.join(layout[i]) for i in range(len(layout))]
        layout = [x.split(',') for x in layout]
        maxColsNum = max([len(x) for x in layout])
        wall_coordinates = set()
        box_coordinates = set()
        storage_coordinates = set()
        #agent_button = set()
        #end_flag = set()

        initial_player_location = (0,0)
        rows = 0

        for irow in range(len(layout)):
            rows +=1
            for icol in range(len(layout[irow])):

                if layout[irow][icol] == '#':
                    wall_coordinates.add((irow,icol)) # wall
                elif layout[irow][icol] == '.' or layout[irow][icol] == 'd' or layout[irow][icol] == 'b' or layout[irow][icol] == 'e': 
                    storage_coordinates.add((irow,icol))#storage
                elif layout[irow][icol] == '$' or layout[irow][icol] == '2' or layout[irow][icol] == '4' or layout[irow][icol] == '5': 
                    box_coordinates.add((irow,icol))  # box
                elif layout[irow][icol] == '@': 
                    initial_player_location = (irow,icol)  #agent
                #elif layout[irow][icol] == '.': 
                #    agent_button = (irow,icol)  #agent
                #elif layout[irow][icol] == 'z': 
                #    end_flag = (irow,icol)  #agent
            colsNum = len(layout[irow])
            #print("colsNum" ,colsNum)
            if colsNum < maxColsNum:
                layout[irow].extend([1 for _ in range(maxColsNum-colsNum)]) 

        return rows,colsNum,initial_player_location, wall_coordinates, box_coordinates, storage_coordinates

def manhattan_distance(coords1, coords2):
    return abs(coords1[0] - coords2[0]) + abs(coords1[1] - coords2[1])

#effect of an action on the agent and the boxes
def future_agent_box_coords(action, current_coords):
    future_agent_coords = None
    future_box_coords = None
    if action == 'U':
        future_agent_coords = (current_coords[0] - 1, current_coords[1])
        future_box_coords = (current_coords[0] - 2, current_coords[1])
    elif action == 'D':
        future_agent_coords = (current_coords[0] + 1, current_coords[1])
        future_box_coords = (current_coords[0] + 2, current_coords[1])
    elif action == 'R':
        future_agent_coords = (current_coords[0], current_coords[1] + 1)
        future_box_coords = (current_coords[0], current_coords[1] + 2)
    elif action == 'L':
        future_agent_coords = (current_coords[0], current_coords[1] - 1)
        future_box_coords = (current_coords[0], current_coords[1] - 2)
    return future_agent_coords, future_box_coords    

def box_is_deadlock(box,docks_coords, wall_coords ):
    if box in docks_coords:
        return False
    for adjacent in [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]:
        if (box[0] + adjacent[0], box[1]) in wall_coords and (box[0], box[1] + adjacent[1]) in  wall_coords:
            return True
    return False








#ENV functions ---------------------------------------------------------------------------------------
def is_valid_value(char):
    if ( char == ' 'or #floor
        char == '#' or #wall
        
        char == '@' or #agent1
        char == '=' or #agent2
        
        char == '+' or #agent1 on dock
        char == '-' or #agent2 on dock           
        char == '.' or #button
        
        char == '*' or #box on right place 
        char == '!' or #box on wrong place 

        char == '$' or #barrier
        char == '%' or #dividing wall
        
        char == '1' or #num1
        char == '2' or #num2
        char == '3' or #num3
        char == '4' or #num4
        char == '5' or #num5

        char == 'a' or #box on dock_num1
        char == 'b' or #box on dock_num2
        char == 'c' or #box on dock_num3
        char == 'd' or #box on dock_num4
        char == 'e' or #box on dock_num5
        char == 'p' or #box 2 on . dock
        char == 'o' or #box 3 on . dock
        char == 'l' or #agent1 on number docks
        char == 'm' or #agent2 on number docks
        char == 'z' #finish
        ):
        return True
    else:
        return 




def get_coordinates_puzzle13(filename):
    with open(filename, "r") as file:
        layout = file.readlines()
        layout = [x.replace('\n','') for x in layout]
        layout = [','.join(layout[i]) for i in range(len(layout))]
        layout = [x.split(',') for x in layout]
        maxColsNum = max([len(x) for x in layout])
        wall_coordinates = []

        goal_coordinate = set()
        #agent_button = set()
        #end_flag = set()

        initial_player_location = (0,0)
        rows = 0

        for irow in range(len(layout)):
            rows +=1
            for icol in range(len(layout[irow])):

                if layout[irow][icol] == '#' or layout[irow][icol] == '*':
                    wall_coordinates.append((irow,icol)) 
                elif layout[irow][icol] == '.' or layout[irow][icol] == 'z':
                    goal_coordinate = (irow,icol)
                elif layout[irow][icol] == '@': 
                    initial_player_location = (irow,icol) 
            colsNum = len(layout[irow])

            if colsNum < maxColsNum:
                layout[irow].extend([1 for _ in range(maxColsNum-colsNum)]) 

        return rows,colsNum,initial_player_location, wall_coordinates, goal_coordinate 



        

