from QL2 import QL2

qLearning_Agent_Boxes = QL2("./puzzle_splited2.txt")
allPaths, steps, time = qLearning_Agent_Boxes.get_allAgentPaths()
print(allPaths, steps, time)