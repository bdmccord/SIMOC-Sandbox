from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from ABM.schedule import RandomActivationBySpecies
from ABM.agents import Human, Plant

import numpy as np
import random

class SingleRoomModel(Model):

    def __init__(self, h_agents=1, p_agents=5, plants_spread=20,oxygen=21.21, carbon=0.13):
        self.schedule = RandomActivationBySpecies(self)
        self.grid = MultiGrid(20, 20, torus=True)
        self.oxygen = oxygen
        self.carbon = carbon
        self.h_agents = h_agents
        self.p_agents = p_agents
        self.spread = plants_spread

        self.datacollector = DataCollector(
            {"Human": lambda m: m.schedule.get_agent_count(Human),
             "Plant": lambda m: m.schedule.get_agent_count(Plant)})

        for i in range(self.p_agents):
            coords = (random.randrange(1, 20), random.randrange(1, 20))
            plant = Plant(coords,self,self.spread)
            self.grid.place_agent(plant, coords)
            self.schedule.add(plant)

        for i in range(self.h_agents):
            coords = (random.randrange(1, 20), random.randrange(1, 20))
            human = Human(coords,self)
            self.grid.place_agent(human, coords)
            self.schedule.add(human)

        self.running = True

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

        print ("Oxygen: {}".format(self.oxygen))
        print ("Carbon: {}".format(self.carbon))
        
        self.h_agents = self.schedule.get_agent_count(Human)
        self.p_agents = self.schedule.get_agent_count(Plant)

        self.oxygen = self.oxygen - 0.0416*0.06265*self.h_agents + 0.0416*0.00429*self.p_agents
        self.carbon = self.carbon + 0.0416*0.05776*self.h_agents - 0.0416*0.00429*self.p_agents

        if (self.carbon<0):
            self.carbon = 0

    def run_model(self, step_count=200):

        for i in range(step_count):
            self.step()
