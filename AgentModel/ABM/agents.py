from mesa import Agent
from ABM.walk import Walker
import random

class Human(Walker):
    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.pos = pos

    def step(self):

        if self.model.schedule.get_agent_count(Plant)>0:
            self.move(Plant)

        self.model.oxygen -= 0.0416*0.06265
        self.model.carbon += 0.0416*0.05776

        if self.model.oxygen < 15.17 or self.model.carbon > 0.53:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)

        if self.model.oxygen < 16 or self.model.carbon > 0.4:
            plant = Plant(self.pos,self.model,self.model.spread)
            self.model.grid.place_agent(plant, self.pos)
            self.model.schedule.add(plant)

        if self.model.carbon < 0.04 and self.model.schedule.get_agent_count(Plant)>0:
            plant = self.model.schedule.get_random_agent(Plant)
            self.model.grid._remove_agent(plant.pos, plant)
            self.model.schedule.remove(plant)


class Plant(Agent):

    def __init__(self, pos, model, turnCount=20):
        super().__init__(pos, model)
        self.pos = pos
        self.turnCount = turnCount

    def step(self):

        self.model.oxygen += 0.0416*0.00429
        self.model.carbon -= 0.0416*0.00429

        if (self.model.carbon<0):
            self.model.carbon = 0

        if self.turnCount <= 0 and self.model.regrowth:
            neighbors = self.model.grid.get_neighborhood(self.pos,moore=False)
            coords = self.model.schedule.empty_neighbor_finder(neighbors, Plant)
            plant = Plant(coords,self.model,self.model.spread)
            self.model.grid.place_agent(plant, coords)
            self.model.schedule.add(plant)
            self.turnCount = self.model.spread

        self.turnCount-=1

        if self.model.carbon < 0.015:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
