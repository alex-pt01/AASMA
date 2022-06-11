#QL2 functions
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

#env functions
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



        

