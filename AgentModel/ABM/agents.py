from mesa import Agent
from ABM.walk import Walker
import random

class Human(Walker):
    def __init__(self, pos, ed, ined,model):
        super().__init__(pos, model)
        self.pos = pos
        self.energy = 15
        self.ed = ed
        self.ined = ined

    def step(self):

        plant = self.current_cell(self.pos,Plant)

        if self.model.schedule.get_agent_count(Plant)>0 and (self.model.carbon < 0.1):
            self.move_toward_plant(Plant)
            self.energy -= 11.82/(24)

        if self.model.schedule.get_agent_count(Plant)>0 and self.model.carbon > 0.4:
            self.move_from_plant(self)
            self.energy -= 11.82/(24)

        if self.model.oxygen < 15.17 or self.model.carbon > 0.53 or self.energy < 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)

        if (self.model.oxygen < 16 or self.model.carbon > 0.3 or self.energy < 12):
            plant = Plant(self.pos,self.model,self.model.spread)
            self.model.grid.place_agent(plant, self.pos)
            self.model.schedule.add(plant)

        self.model.oxygen -= 0.0416*0.06265
        self.model.carbon += 0.0416*0.05776
        self.energy -= 7.43/(24)

        if (self.model.carbon < 0.04 or self.energy < 7) and isinstance(plant, Plant):
            print ('Remove')
            self.model.grid._remove_agent(plant.pos, plant)
            self.model.schedule.remove(plant)
            self.energy += 0.00456*self.ed              # Edible dry mass times MJ/gram
            self.model.carbon += 0.0000969*self.ined    # Amount of carbon released from inedible dry mass
            self.model.oxygen += 0.0000972*self.ined    # Amount of oxygen released from inedible dry mass


class Plant(Agent):

    def __init__(self, pos, model, turnCount=20):
        super().__init__(pos, model)
        self.pos = pos
        self.turnCount = turnCount

    def step(self):

        self.model.oxygen += 0.0416*0.00005
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
