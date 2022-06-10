from arena_QL2 import arena_QL2
#from puzzle2 import get_all_possible_actions

class agentArena_QL2:
    # static
    qtable = {}

    def __init__(self, box_coordinates_inp, location, storage_coordinates, wall_coordinates):
        self.current_state = arena_QL2(box_coordinates_inp, location, storage_coordinates, wall_coordinates)

    def clear_qtable(self):
        self.__class__.qtable.clear()

    #def get_current_state_actions(self):
    #    return get_all_possible_actions(self.current_state.player_location, self.current_state.box_coordinates)

    def set_QValue(self, state, action, newValue):
        self.__class__.qtable[(state, action)] = newValue

    def get_QValue(self, state, action):
        if state.goal_reached():
            self.set_QValue(state, action, float("inf"))
            return float("inf")
        if state.is_stuck():
            self.set_QValue(state, action, float("-inf"))
            return float("-inf")
        return self.__class__.qtable.get((state, action), 0)

    def test(self):
        print("H")
