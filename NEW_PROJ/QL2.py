from arena_QL2 import arena_QL2
from agentArena_QL2 import agentArena_QL2
from functions import manhattan_distance, get_coordinates_from_file, future_agent_box_coords
import random
import time

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
        self.agent_coords = get_coordinates_from_file(filename)[2]
        self.wall_coords = get_coordinates_from_file(filename)[3]
        self.box_coords = get_coordinates_from_file(filename)[4]
        self.docks_coords = get_coordinates_from_file(filename)[5]
        self.allPaths = []


    #minimal distance from boxes to docks
    def heuristic(self, boxes, docks):
        heuristic = 0
        boxes_not_in_dock = boxes.difference(docks)
        empty_docks = docks.difference(boxes)
        for box in boxes_not_in_dock:
            min = 9999999
            min_dock = None
            for dock in empty_docks:
                distance = manhattan_distance(box, dock)
                if distance < min:
                    min = distance
                    min_dock = dock
            heuristic += min
            empty_docks.remove(min_dock)
        return heuristic

    #minimal distance from agent to boxes
    def distance_agent_boxes(self,box_coords, agent_coords):
        min_distance = 9999999
        for box in box_coords.difference(self.docks_coords):
            min_distance = min(manhattan_distance(agent_coords, box), min_distance)
        return min_distance

    #verify if agent or box movement is valid
    def invalid_step(self,agent_coords, action, box_coords):
        future_agent_coords, box_next_location_if_present = future_agent_box_coords(action, agent_coords)
        if future_agent_coords in self.wall_coords:
            return True
        elif future_agent_coords in box_coords and box_next_location_if_present in box_coords:
            return True
        elif future_agent_coords in box_coords and box_next_location_if_present in self.wall_coords:
            return True
        else:
            return False

    #get all valid actions
    def valid_actions(self, agent_coords, box_coords):
        valid_actions= []
        for action in self.actions:
            if not self.invalid_step(agent_coords, action, box_coords):
                valid_actions.append(action)
        return valid_actions
         

    #get state in arena after an action
    def action_state_effect(self,agent_coords, action, box_coords):
        target_coords, target_agent_coords = future_agent_box_coords(action, agent_coords)
        new_agent_coords = target_coords
        new_boxes_coords = set(box_coords.copy())
        if target_coords in new_boxes_coords:
            new_boxes_coords.remove(target_coords)
            new_boxes_coords.add(target_agent_coords)
        return arena_QL2(new_boxes_coords, new_agent_coords, self.docks_coords, self.wall_coords)

    #get list with max_qValue and the biggest possible action
    def max_qValue(self,agent_arena, state, actions):
        max_qvalue = float("-inf")
        biggest_action = None
        for action in actions: #all possible actions
            if max_qvalue <= agent_arena.get_QValue(state, action):
                biggest_action = action
                max_qvalue = agent_arena.get_QValue(state, action)
        return [max_qvalue, biggest_action]

    #get action with highest qValue
    def action_with_highest_qvalue(self,agent_arena):
        actions = self.valid_actions(agent_arena.current_state.agent_coords, agent_arena.current_state.box_coords)
        action_with_highest_qvalue = self.max_qValue(agent_arena, agent_arena.current_state, actions)[1]
        return action_with_highest_qvalue

    def perform_valid_action(self, agent_arena, action):
        #new state
        new_state = self.action_state_effect(agent_arena.current_state.agent_coords, action, agent_arena.current_state.box_coords)
        reward = -1
        
        #difference between boxes and docks
        boxes_docks = self.heuristic(new_state.box_coords, self.docks_coords) - \
                        self.heuristic(agent_arena.current_state.box_coords, self.docks_coords)
        if boxes_docks < 0:
            reward += 5
        elif boxes_docks > 0:
            reward += -5

        #difference between new state boxes and current state boxes                       
        boxes_difference = new_state.boxes_not_docked() - \
                                    agent_arena.current_state.boxes_not_docked()
        if boxes_difference < 0:
            reward += 15
        elif boxes_difference > 0:
            reward += -10

        #difference between agent and closest boxe
        agent_box = self.distance_agent_boxes(new_state.box_coords,
                                                                    new_state.agent_coords) \
                                            - self.distance_agent_boxes(agent_arena.current_state.box_coords,
                                                                        agent_arena.current_state.agent_coords)
        if agent_box < 0:
            reward += 1
        elif agent_box > 0:
            reward += -1

        actual_qValue = agent_arena.get_QValue(agent_arena.current_state, action)
        
        #formula https://en.wikipedia.org/wiki/Q-learning
        new_qValue = actual_qValue + self.learning_rate * (
                reward + self.discount * self.max_qValue(agent_arena, new_state,
                                            self.valid_actions(new_state.agent_coords,
                                                                    new_state.box_coords))[0]
                - actual_qValue)
        agent_arena.set_QValue(agent_arena.current_state, action, new_qValue)
        agent_arena.current_state = new_state


    def check_terminal_episode(self,agent_coords, max_moves, epsilon_inp):
        agent_arena = agentArena_QL2(self.box_coords, agent_coords, self.docks_coords, self.wall_coords)
        path = ""
        for _ in range(max_moves):
            if random.random() < epsilon_inp:
                action = random.choice(self.valid_actions(agent_arena.current_state.agent_coords,
                                                                agent_arena.current_state.box_coords))
                path += action
            else:
                action = self.action_with_highest_qvalue(agent_arena)
                path += action
                self.allPaths.append(path)
                self.perform_valid_action(agent_arena, action)
            if agent_arena.current_state.goal_reached():
                print("Number of moves ", len(path))
                self.steps = len(path)
                print("Path is %%%%%%% ", path)

                return True
        return False


    #VER
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
            episodeReachedTerminal= self.check_terminal_episode(self.agent_coords, max_max_moves, epsilon_max)
            
            if episodeReachedTerminal:
                break
      
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