class arena_QL2:
    def __init__(self, box_coordinates_inp, player_location, storage_coordinates, wall_coordinates):
        self.storage_coordinates = storage_coordinates
        self.box_coordinates = frozenset(box_coordinates_inp)
        self.player_location = player_location
        self.wall_coordinates = wall_coordinates
    def __eq__(self, other):
        if type(other) is type(self):
            return (self.box_coordinates, self.player_location) == (other.box_coordinates, other.player_location)
        return False

    def __hash__(self):
        return hash((self.box_coordinates, self.player_location))

    def __repr__(self):
        return str(self.box_coordinates) + " " + str(self.player_location)

    def boxes_not_in_destination(self):
        return len(self.box_coordinates.difference(self.storage_coordinates))

    def goal_reached(self):
        return len(self.storage_coordinates.difference(self.box_coordinates)) == 0
    
    def is_deadlock(self,box):
        if box in self.storage_coordinates:
            return False
        for adjacent in [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]:
            if (box[0] + adjacent[0], box[1]) in self.wall_coordinates and (box[0], box[1] + adjacent[1]) in  self.wall_coordinates:
                return True
        return False

    def is_stuck(self):
        return any(map(lambda box: self.is_deadlock(box), self.box_coordinates))
