from mesa import Agent
import random

class Human(Agent):
    def __init__(self, name, model):
        super().__init__(name, model)
        self.name = name

    def step(self):
        #print("Human {} active".format(self.name+1))

        if self.model.oxygen < 15.17 or self.model.carbon > 0.53:
            self.model.schedule.remove(self)
        '''
        if self.model.oxygen < 16 or self.model.carbon > 0.4:
            plant = Plant(random.randint(1,50),self.model)
            self.model.schedule.add(plant)
        '''

class Plant(Agent):

    def __init__(self, name, model,turnCount=20):
        super().__init__(name, model)
        self.name = name
        self.turnCount = turnCount

    def step(self):
        #print("Plant {} active".format(self.name+1))

        self.turnCount-=1

        if self.turnCount <= 0:
            plant = Plant(random.randint(1,50),self.model)
            self.model.schedule.add(plant)
            self.turnCount = 20


        if self.model.carbon < 0.015:
            self.model.schedule.remove(self)
