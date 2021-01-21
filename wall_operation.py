class WallOperations:

    def execute_2D(self, box):
        box = self.intervals_extraction(box)
        walls = self.rotate_and_execute_2D(box)
        return walls

    def intervals_extraction(self, wall):
        wall_set = [wall.interval_x, wall.interval_y, wall.interval_z]
        return wall_set

    def rotate_and_execute_2D(self, box):
        walls = []
        for i in range(3):
            walls.append(box[i])
        return [walls]

