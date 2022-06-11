from arena_QL2 import arena_QL2

class agentArena_QL2:
    qtable = {}
    def __init__(self, box_coordinates_inp, location, storage_coordinates, wall_coordinates):
        self.current_state = arena_QL2(box_coordinates_inp, location, storage_coordinates, wall_coordinates)
    
    def get_QValue(self, state, action):
        if state.goal_reached():
            self.set_QValue(state, action, 9999999)
            return 9999999
        if state.box_is_stuck():
            self.set_QValue(state, action, 9999999)
            return 9999999
        return self.__class__.qtable.get((state, action), 0)

    def set_QValue(self, state, action, newValue):
        self.__class__.qtable[(state, action)] = newValue
        
    def test(self):
        print("H")
