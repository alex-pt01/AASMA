import random
import time
from collections import defaultdict
from arena_QL2 import arena_QL2
from agentArena_QL2 import agentArena_QL2
from functions import get_coordinates_from_file

start_time = time.time()
random.seed(0)


class QL2:
    def __init__(self,filename, actions = ["U", "D", "L", "R"],discount = 1.0,learning_rate =0.7 ):
        self.filename = filename
        self.actions = actions
        self.discount = discount
        self.learning_rate = learning_rate
        self.rows =  get_coordinates_from_file(filename)[0]
        self.cols = get_coordinates_from_file(filename)[1]
        self.initial_player_location = get_coordinates_from_file(filename)[2]
        self.wall_coordinates = get_coordinates_from_file(filename)[3]
        self.box_coordinates = get_coordinates_from_file(filename)[4]
        self.storage_coordinates = get_coordinates_from_file(filename)[5]
        self.allPaths = []


    def manhattan_distance(self,coordinates1, coordinates2):
        return abs(coordinates1[0] - coordinates2[0]) + abs(coordinates1[1] - coordinates2[1])

    def closeness_heuristic(self,boxes, storages):
        ans = 0
        boxes_not_in_storage = boxes.difference(storages)
        empty_storages = storages.difference(boxes)

        for box in boxes_not_in_storage:
            minx = float('inf')
            min_storage = None
            for storage in empty_storages:
                distance = self.manhattan_distance(box, storage)
                if distance < minx:
                    minx = distance
                    min_storage = storage
            ans += minx
            empty_storages.remove(min_storage)

        return ans
        
    def agent_to_box_min_distance(self,box_coordinates_inp, player_location):
        minx = float("inf")
        for box in box_coordinates_inp.difference(self.storage_coordinates):
            minx = min(self.manhattan_distance(player_location, box), minx)
        return minx


    def get_next_player_and_box_location(self,action, current_location):
        player_next_location = None
        box_next_location_if_present = None
        if action == 'U':
            player_next_location = (current_location[0] - 1, current_location[1])
            box_next_location_if_present = (current_location[0] - 2, current_location[1])
        elif action == 'D':
            player_next_location = (current_location[0] + 1, current_location[1])
            box_next_location_if_present = (current_location[0] + 2, current_location[1])
        elif action == 'R':
            player_next_location = (current_location[0], current_location[1] + 1)
            box_next_location_if_present = (current_location[0], current_location[1] + 2)
        elif action == 'L':
            player_next_location = (current_location[0], current_location[1] - 1)
            box_next_location_if_present = (current_location[0], current_location[1] - 2)
        return player_next_location, box_next_location_if_present


    def check_if_move_is_invalid(self,player_location, action, box_coordinates_inp):
        player_next_location, box_next_location_if_present = self.get_next_player_and_box_location(action, player_location)
        return (player_next_location in self.wall_coordinates) \
            or (player_next_location in box_coordinates_inp and box_next_location_if_present in box_coordinates_inp) \
            or (player_next_location in box_coordinates_inp and box_next_location_if_present in self.wall_coordinates)


    def get_all_possible_actions(self, player_location, box_coordinates_inp):
        return [action for action in self.actions if not self.check_if_move_is_invalid(player_location, action,
                                                                                box_coordinates_inp)]


    def get_state_for_action(self,player_location, action, box_coordinates_inp):
        targetLocation, targetNextLocation = self.get_next_player_and_box_location(action, player_location)
        newLocation = targetLocation
        newBoxCoordinates = set(box_coordinates_inp.copy())
        if targetLocation in newBoxCoordinates:
            newBoxCoordinates.remove(targetLocation)
            newBoxCoordinates.add(targetNextLocation)
        return arena_QL2(newBoxCoordinates, newLocation, self.storage_coordinates, self.wall_coordinates)






    def get_max_QValue(self,sokoban_board, state, possible_actions):
        max_qvalue = float("-inf")
        max_action = None
        for action in possible_actions:
            if max_qvalue <= sokoban_board.get_QValue(state, action):
                max_qvalue = sokoban_board.get_QValue(state, action)
                max_action = action

        return [max_qvalue, max_action]


    def get_action_with_highest_qvalue(self,sokoban_board):
        possible_actions = self.get_all_possible_actions(sokoban_board.current_state.player_location,
                                                    sokoban_board.current_state.box_coordinates)
        return self.get_max_QValue(sokoban_board, sokoban_board.current_state, possible_actions)[1]


    def perform_valid_action(self, sokoban_board, action):
        new_state = self.get_state_for_action(sokoban_board.current_state.player_location, action,
                                        sokoban_board.current_state.box_coordinates)

        R = -1

        # Boxes closeness to the storage locations
        step_difference = self.closeness_heuristic(new_state.box_coordinates, self.storage_coordinates) - \
                        self.closeness_heuristic(sokoban_board.current_state.box_coordinates, self.storage_coordinates)
        if step_difference < 0:
            R += 3
        elif step_difference > 0:
            R += -3

        # Move a box to storage
        remaining_boxes_difference = new_state.boxes_not_in_destination() - \
                                    sokoban_board.current_state.boxes_not_in_destination()
        if remaining_boxes_difference < 0:
            R += 15
        elif remaining_boxes_difference > 0:
            R += -10

        # Player is close to box
        distance_to_closest_box_difference = self.agent_to_box_min_distance(new_state.box_coordinates,
                                                                    new_state.player_location) \
                                            - self.agent_to_box_min_distance(sokoban_board.current_state.box_coordinates,
                                                                        sokoban_board.current_state.player_location)
        if distance_to_closest_box_difference < 0:
            R += 1
        elif distance_to_closest_box_difference > 0:
            R += -1

        current_q_value = sokoban_board.get_QValue(sokoban_board.current_state, action)
        new_q_value = current_q_value + self.learning_rate * (
                R + self.discount * self.get_max_QValue(sokoban_board, new_state,
                                            self.get_all_possible_actions(new_state.player_location,
                                                                    new_state.box_coordinates))[0]
                - current_q_value)
        sokoban_board.set_QValue(sokoban_board.current_state, action, new_q_value)
        sokoban_board.current_state = new_state




    def isSafe(idx, j, matrix):
        if 0 <= idx <= len(matrix) and 0 <= j <= len(matrix[0]):
            return True
        else:
            return False





    def run_an_episode_and_check_if_terminal(self,player_start_location_inp, max_moves_inp, epsilon_inp):
        # Print path if this episode is terminal. Return true if terminal
        sokoban_board = agentArena_QL2(self.box_coordinates, player_start_location_inp, self.storage_coordinates, self.wall_coordinates)
        path = ""
        
        for _ in range(max_moves_inp):
            if random.random() < epsilon_inp:
                action = random.choice(self.get_all_possible_actions(sokoban_board.current_state.player_location,
                                                                sokoban_board.current_state.box_coordinates))
                path += action
            else:
                action = self.get_action_with_highest_qvalue(sokoban_board)
                path += action
                print("PATH_ ", path)
                self.allPaths.append(path)
                self.perform_valid_action(sokoban_board, action)
            if sokoban_board.current_state.goal_reached():
                print("Number of moves ", len(path))
                self.steps = len(path)
                print("Path is %%%%%%% ", path)
                #allPaths.append(path)

                return True
        return False

    def run(self):
        print(self.rows)
        rows = int(self.rows)
        cols = int(self.cols)

        n_storage = 10 #VER why?
        max_episodes = rows * cols * n_storage * 1000
        max_max_moves = rows * cols* n_storage * 1
        min_max_moves = rows * cols* n_storage * 1
        epsilon_min = 0.2  # Less exploration after some episodes
        epsilon_max = 0.2  # explore lot in the beginning
        print('Total episodes: ', max_episodes)


        # Run the algorithm
        for i in range(max_episodes):
            episodeReachedTerminal= self.run_an_episode_and_check_if_terminal(self.initial_player_location, max_max_moves, epsilon_max)
            
            if episodeReachedTerminal:
                break
            if i % 1000 == 0:
                max_max_moves = max(int(max_max_moves * 0.9), min_max_moves)
                epsilon_max = max(epsilon_max * 0.9, epsilon_min)
                print("Max moves: ", max_max_moves)
                print("current epsilon: ", epsilon_max)
                print("Total Completed Episodes: ", i)
                print("Qtable size: ", len(agentArena_QL2.qtable))
                timeElapsed = time.time() - start_time
                print('Time elapsed: ', timeElapsed)
                if timeElapsed > 3600:
                    print('Timeout')
                    break

        end = time.time()
        self.time = end - start_time
        print('Total time for solution: ', end - start_time)


    def get_allAgentPaths(self):
        self.run()
        return self.allPaths, self.steps, self.time

def main():
    qLearning_Agent_Boxes = QL2("./puzzle_splited2.txt")
    qLearning_Agent_Boxes.run()
    print('Hello World')
    
if __name__ == '__main__':
    # This code won't run if this file is imported.
    main()  