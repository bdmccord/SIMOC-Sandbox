from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from ABM.schedule import RandomActivationBySpecies
from ABM.agents import Human, Plant

import numpy as np
import random
import json

class SingleRoomModel(Model):


    '''
    CDRA (carbon dioxide removal assembly) uses ~2.1 kW per kg of CO2 removed

    ~ 6 kg of co2 removed
    '''
    description = ("A model for simulating the exchange of carbon dioxide and oxygen between plants and humans."
                  " Most parameters are set automatically, but to change any parameter "
                  "simply adjust the sliders and click reset.")

    def __init__(self, scrubber,regrowth,excess_co2,excess_amount,solar,h_agents=1, p_agents=5, plants_spread=20,oxygen=21.21, carbon=0.13):
        self.schedule = RandomActivationBySpecies(self)
        self.grid = MultiGrid(20, 20, torus=True)
        self.oxygen = oxygen
        self.carbon = carbon
        self.h_agents = h_agents
        self.p_agents = p_agents
        self.spread = plants_spread
        self.regrowth = regrowth
        self.excess_amount = excess_amount
        self.excess_co2 = excess_co2
        self.temp = 295
        self.solar = solar
        self.scrubber = scrubber

        with open('../data/data.json', 'r') as f:
            data = json.load(f)

        plant_type = 'White Potato'
        self.oxy = data['Plants'][plant_type]['Oxygen']
        self.co2 = data['Plants'][plant_type]['Carbon']
        edible = data['Plants'][plant_type]['Edible']
        inedible = data['Plants'][plant_type]['Inedible']

        for i in range(self.p_agents):
            coords = (random.randrange(0, 20), random.randrange(0, 20))
            plant = Plant(coords,self.oxy,self.co2,self,self.spread)
            self.grid.place_agent(plant, coords)
            self.schedule.add(plant)

        for i in range(self.h_agents):
            coords = (random.randrange(0, 20), random.randrange(0, 20))
            human = Human(coords,edible,inedible,self)
            self.grid.place_agent(human, coords)
            self.schedule.add(human)

        self.datacollector = DataCollector(
            {"Human": lambda m: m.schedule.get_agent_count(Human),
             "Plant": lambda m: m.schedule.get_agent_count(Plant)})

        self.datacollector2 = DataCollector(
            {"Carbon": lambda m: m.carbon}
        )
        self.running = True

    def step(self):
        self.schedule.step()
        if self.excess_co2:
            self.carbon += 0.001*(self.excess_amount)
        if self.scrubber and self.carbon > 0.1:
            self.carbon -= 0.415*0.041666*(self.solar/400)
        if self.carbon < 0:
            self.carbon = 0
        self.datacollector.collect(self)
        self.datacollector2.collect(self)

        #print ("Oxygen: {}".format(self.oxygen))
        #print ("Carbon: {}".format(self.carbon))

        self.h_agents = self.schedule.get_agent_count(Human)
        self.p_agents = self.schedule.get_agent_count(Plant)

    def run_model(self, step_count=200):
        co2 = []
        oxy = []
        for i in range(step_count):
            self.step()
            co2.append(self.carbon)
            oxy.append(self.oxygen)
