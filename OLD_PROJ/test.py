from re import sub
from QL2 import QL2
import json
import ast

def testQL2():
    qLearning_Agent_Boxes = QL2("./puzzle_splited2.txt")
    allPaths, steps, time = qLearning_Agent_Boxes.get_allAgentPaths()
    print(allPaths, steps, time)

submap = "[['#', '$', '$', '$', '$', '%', '$', '$', '$', '$', '#'], ['#', ' ', ' ', ' ', ' ', '%', ' ', ' ', ' ', ' ', '#'], ['#', ' ', ' ', ' ', ' ', '%', ' ', ' ', ' ', ' ', '#'], ['#', 'a', ' ', ' ', 'd', '%', 'b', ' ', ' ', 'e', '#'], ['#', ' ', ' ', ' ', ' ', '%', ' ', ' ', ' ', ' ', '#'], ['#', '1', ' ', ' ', '4', '%', '5', ' ', ' ', '2', '#'], ['#', ' ', ' ', ' ', ' ', '%', ' ', ' ', ' ', ' ', '#'], ['#', ' ', ' ', '.', ' ', '%', ' ', ' ', ' ', '.', '#']]"

def test(list_):
    print(list_)
    #split half
    new_list = []
    for sublist in list_:
        for elem in sublist:
            print(elem)
            if elem =='#' or elem == '$':
                sublist.index(elem) == '#'         
    print(new_list)

def main():
    lst = [] 
    lst.append(ast.literal_eval("['#', '$', '$', '$', '$', '%', '$', '$', '$', '$', '#']"))
    lst.append(ast.literal_eval("['#', ' ', ' ', ' ', ' ', '%', ' ', ' ', ' ', ' ', '#']"))
    lst.append(ast.literal_eval("['#', '$', '$', '$', '$', '%', '$', '$', '$', '$', '#']"))
    lst.append(ast.literal_eval("['#', ' ', ' ', ' ', ' ', '%', ' ', ' ', ' ', ' ', '#']"))
    lst.append(ast.literal_eval("['#', 'a', ' ', ' ', 'd', '%', 'b', ' ', ' ', 'e', '#']"))
    lst.append(ast.literal_eval("['#', ' ', ' ', ' ', ' ', '%', ' ', ' ', ' ', ' ', '#']"))
    lst.append(ast.literal_eval("['#', '1', ' ', ' ', '4', '%', '5', ' ', ' ', '2', '#']"))
    lst.append(ast.literal_eval("['#', ' ', ' ', ' ', ' ', '%', ' ', ' ', ' ', ' ', '#']"))
    lst.append(ast.literal_eval("['#', ' ', ' ', '.', ' ', '%', ' ', ' ', ' ', '.', '#']")) 
    #test(lst)


    testQL2()
    
if __name__ == '__main__':
    # This code won't run if this file is imported.
    main()
    