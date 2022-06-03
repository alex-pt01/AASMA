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
        

