


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
        map = file.readlines()
        map = [x.replace('\n','') for x in map]
        map = [','.join(map[i]) for i in range(len(map))]
        map = [x.split(',') for x in map]
        maxColsNum = max([len(x) for x in map])
        wall_coordinates = []
        goal = set()
        initial_player_location = (0,0)
        rows = 0
        for irow in range(len(map)):
            rows +=1
            for icol in range(len(map[irow])):

                if map[irow][icol] == '#' or map[irow][icol] == '*':
                    wall_coordinates.append((irow,icol)) 
                elif map[irow][icol] == '.' or map[irow][icol] == 'z':
                    goal = (irow,icol)
                elif map[irow][icol] == '@': 
                    initial_player_location = (irow,icol) 
            colsNum = len(map[irow])

            if colsNum < maxColsNum:
                map[irow].extend([1 for _ in range(maxColsNum-colsNum)]) 

        return rows,colsNum,initial_player_location, wall_coordinates, goal 



def manhattan_distance(location1, location2):
    return abs(location1[0] - location2[0]) + abs(location1[1] - location2[1])

def get_coordinates_puzzle2(filename):
    with open(filename, "r") as file:
        map = file.readlines()
        map = [x.replace('\n','') for x in map]
        map = [','.join(map[i]) for i in range(len(map))]
        map = [x.split(',') for x in map]
        
        maxColsNum = max([len(x) for x in map])
        wall_coordinates = []
        dock_coordinates = []
        box_coordinates = []
        initial_player_location = (0,0)
        rows = 0
        for irow in range(len(map)):
            rows +=1
            for icol in range(len(map[irow])):

                if map[irow][icol] == '#' or map[irow][icol] == '*':
                    wall_coordinates.append((irow,icol)) 
                elif map[irow][icol] == 'b':
                    box_coordinates.append((irow,icol)) 
                elif map[irow][icol] == 'd':
                    dock_coordinates.append((irow,icol)) 
                elif map[irow][icol] == '@': 
                    initial_player_location = (irow,icol) 
            colsNum = len(map[irow])

            if colsNum < maxColsNum:
                map[irow].extend([1 for _ in range(maxColsNum-colsNum)]) 

        return rows,colsNum,initial_player_location, wall_coordinates, box_coordinates, dock_coordinates

        

