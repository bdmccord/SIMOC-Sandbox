from mesa import Agent
from ABM.walk import Walker
import random

class Human(Walker):
    def __init__(self, pos, ed, ined,model):
        super().__init__(pos, model)
        self.pos = pos
        self.energy = 100
        self.ed = ed
        self.ined = ined

    def step(self):
        '''
         self.model.schedule.get_agent_count(Plant)>0 and self.model.carbon > 0.4:
            self.move_from_plant(self)
            self.energy -= 11.82/(24)
            print ("b")
            self.model.oxygen -= 0.0416*0.06265*2.1
            self.model.carbon += 0.0416*0.05776*2
        '''
        self.model.temp += (((310-self.model.temp)*0.04372)/(1.29*1000*0.001005))
        cell = self.current_cell(self.pos,Plant)

        if self.model.oxygen < 15.17 or self.model.carbon > 0.53 or self.energy < 0:

            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)

        if self.model.schedule.get_agent_count(Plant)>0 and (self.energy < 75) and not(isinstance(cell,Plant)):
            self.move_toward_plant(Plant)

            self.energy -= 11.82*(1/24)
            self.model.oxygen -= 0.0416*0.06265*2.1
            self.model.carbon += 0.0416*0.05776*2

        elif (self.model.oxygen < 16 or self.model.carbon > 0.3 or (self.energy < 90 and self.energy > 80) or len(self.model.schedule.agents_by_type[Plant])<10):

            if not(isinstance(cell,Plant)):
                plant = Plant(self.pos,self.model.oxy,self.model.co2,self.model,self.model.spread)
                self.model.grid.place_agent(plant, self.pos)
                self.model.schedule.add(plant)
                self.move_from_plant(self)
                self.model.oxygen -= 0.0416*0.06265*2.1
                self.model.carbon += 0.0416*0.05776*2
                self.energy -= 11.82*(1/24)
            else:
                self.move_from_plant(Plant)

        elif (self.model.carbon < 0.04 or self.energy < 75) and isinstance(cell, Plant):
            if (cell.grown):

                self.model.grid._remove_agent(cell.pos, cell)
                self.model.schedule.remove(cell)
                self.move_toward_plant(Plant)
                self.energy -= 7.43*(1/24)
                self.model.oxygen -= 0.0416*0.06265*0.63
                self.model.carbon += 0.0416*0.05776*0.63
                self.energy += 0.00456*self.ed*4              # Edible dry mass times MJ/gram
                self.model.carbon += 0.0000969*self.ined    # Amount of carbon released from inedible dry mass
                self.model.oxygen += 0.0000972*self.ined    # Amount of oxygen released from inedible dry mass

        else:
            self.energy -= 7.43*(1/24)
            self.model.oxygen -= 0.0416*0.06265*0.63
            self.model.carbon += 0.0416*0.05776*0.63


class Plant(Agent):

    def __init__(self, pos,oxy,co2, model, turnCount=20, mature=10,grown=False):
        super().__init__(pos, model)
        self.pos = pos
        self.turnCount = turnCount
        self.grown = grown
        self.mature = mature
        self.co2 = co2
        self.oxy = oxy

    def step(self):
        if (self.mature>0):
            self.mature-=1
        else:
            self.grown = True

        self.model.oxygen += 0.0416*(self.oxy/32)*(3.369/1000)
        self.model.carbon -= 0.0416*(self.co2/44)*(3.369/1000)

        if (self.model.carbon<0):
            self.model.carbon = 0

        if self.turnCount <= 0 and self.model.regrowth:
            neighbors = self.model.grid.get_neighborhood(self.pos,moore=False)
            coords = self.model.schedule.empty_neighbor_finder(neighbors, Plant)
            plant = Plant(coords,oxy,co2,self.model,self.model.spread)
            self.model.grid.place_agent(plant, coords)
            self.model.schedule.add(plant)
            self.turnCount = self.model.spread


        if self.model.carbon < 0.015:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
