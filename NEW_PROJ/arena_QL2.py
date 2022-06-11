from functions import box_is_deadlock

class arena_QL2:
    def __init__(self, box_coords, agent_coords, docks_coords, wall_coords):
        self.docks_coords = docks_coords
        self.box_coords = frozenset(box_coords)
        self.agent_coords = agent_coords
        self.wall_coords = wall_coords
        
    def __eq__(self, other):
        if type(other) is type(self):
            return (self.box_coords, self.agent_coords) == (other.box_coords, other.agent_coords)
        return False

    def __repr__(self):
        return str(self.box_coords) + " " + str(self.agent_coords)

    def boxes_not_docked(self):
        return len(self.box_coords.difference(self.docks_coords))

    def goal_reached(self):
        return len(self.docks_coords.difference(self.box_coords)) == 0
    
    def box_is_stuck(self):
        return any(map(lambda box: box_is_deadlock(box,self.docks_coords, self.wall_coords ), self.box_coords))

    def __hash__(self):
        return hash((self.box_coords, self.agent_coords))
