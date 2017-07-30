from mesa import Agent
from math import hypot

class Walker(Agent):

    def __init__(self, pos, model):
        super().__init__(pos,model)
        self.pos = pos

    def nearest_neighbor(self, pos, agent_type):
        plants = self.model.schedule.agents_by_type[agent_type]
        x, y = pos
        minDist = hypot(20,20)
        nearest = None
        for plant in plants:
            x1, y1 = plant.pos
            dist = hypot(x1-x, y1-y)
            if (dist<minDist):
                minDist = dist
                nearest = plant
        return nearest

    def move(self, agent_type):
        next_moves = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=True)
        plant = self.nearest_neighbor(self.pos, agent_type)
        x, y = plant.pos
        x1, y1 = self.pos
        minDist = hypot(x1-x, y1-y)

        if not(minDist==0):
            action = None
            for move in next_moves:
                x1, y1 = move
                dist = hypot(x1-x, y1-y)
                if (dist < minDist):
                    action = move
            self.model.grid.move_agent(self, action)
