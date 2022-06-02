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
        

def print_game(matrix,screen):
    """
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    """
    screen.fill(background)
    x = 0
    y = 0
    for row in matrix:
        for char in row:
            if char == '%': #dividing_wall
                screen.blit(dividing_wall,(x,y)) 
            elif char == '#': #wall
                screen.blit(wall,(x,y))

            elif char == '=': #agent2
                screen.blit(agent1,(x,y)) 
            elif char == '@': #agent1 
                screen.blit(agent,(x,y))
            elif char == 'l':
                screen.blit(agent,(x,y)) #agent1 on numbered dock
            elif char == 'm':
                screen.blit(agent1,(x,y)) #agent2 on numbered dock
            if char == ' ': #floor
                screen.blit(floor,(x,y))
 

            elif char == '.': #button
                screen.blit(docker,(x,y))

            elif char == '*': #box on right place
                screen.blit(box_right_place,(x,y))
            elif char == '!': #box on wrong place
                screen.blit(box_wrong_place,(x,y))

            elif char == '$': #barrier
                screen.blit(box,(x,y))

            elif char == '+': #agent1 on dock
                screen.blit(agent_docked,(x,y))
            elif char == '-': #agent2 on dock
                screen.blit(agent1_docked,(x,y))

            elif char == '1': #num1
                screen.blit(num1,(x,y))
            elif char == '2': #num2
                screen.blit(num2,(x,y))
            elif char == '3': #num3
                screen.blit(num3,(x,y))
            elif char == '4': #num4
                screen.blit(num4,(x,y))
            elif char == '5': #num5
                screen.blit(num5,(x,y))

            elif char == 'a': #dock_num1
                screen.blit(dock_num1,(x,y))
            elif char == 'b': #dock_num2
                screen.blit(dock_num2,(x,y))
            elif char == 'c': #dock_num3
                screen.blit(dock_num3,(x,y))
            elif char == 'd': #dock_num4
                screen.blit(dock_num4,(x,y))
            elif char == 'e': #dock_num5
                screen.blit(dock_num5,(x,y))


            elif char == 'p': #box2 on dock .
                screen.blit(num2,(x,y))
            elif char == 'o':  #box3 on dock .
                screen.blit(num3,(x,y))

            elif char == 'z': #dock_num5
                screen.blit(finish,(x,y))

            x = x + 32
        x = 0
        y = y + 32
