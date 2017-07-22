from mesa import Agent, Model
from schedule import RandomActivationBySpecies
from mesa.space import MultiGrid
from agents import Human, Plant

import numpy as np
import random

class SingleRoomModel(Model):


    def __init__(self, h_agents=1, p_agents=5,oxygen=21.21, carbon=0.13):
        self.schedule = RandomActivationBySpecies(self)
        self.grid = MultiGrid(10, 10, torus=True)
        self.oxygen = oxygen
        self.carbon = carbon
        self.h_agents = h_agents
        self.p_agents = p_agents

        for i in range(self.p_agents):
            a = Plant(i,self)
            self.schedule.add(a)
            coords = (random.randrange(0, 10), random.randrange(0, 10))
            self.grid.place_agent(a, coords)

        for i in range(self.h_agents):
            a = Human(i,self)
            self.schedule.add(a)
            coords = (random.randrange(0, 10), random.randrange(0, 10))
            self.grid.place_agent(a, coords)

    def step(self):
        self.schedule.step()

    def run_model(self, step_count=200):
        x = []
        y = []
        z = []
        z1 = []
        for i in range(step_count):
            self.h_agents = self.schedule.get_agent_count(Human)
            self.p_agents = self.schedule.get_agent_count(Plant)

            self.oxygen = self.oxygen - 0.0416*0.06265*self.h_agents + 0.0416*0.00429*self.p_agents
            self.carbon = self.carbon + 0.0416*0.05776*self.h_agents - 0.0416*0.00429*self.p_agents
            if (self.carbon<0):
                self.carbon = 0
            x.append(self.oxygen)
            y.append(self.carbon)
            z.append(self.h_agents)
            z1.append(self.p_agents)
            self.step()

        return x, y, step_count, z, z1
