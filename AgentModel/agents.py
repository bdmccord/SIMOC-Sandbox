from mesa import Agent
import random

class Human(Agent):
    def __init__(self, name, model):
        super().__init__(name, model)
        self.name = name

    def step(self):
        if self.model.oxygen < 15.17 or self.model.carbon > 0.53:
            self.model.schedule.remove(self)

        if self.model.oxygen < 16 or self.model.carbon > 0.4:
            plant = Plant(random.randint(1,50),self.model)
            self.model.schedule.add(plant)

        if self.model.oxygen < 0.04:
            self.mode.schedule.remove(self.model.schedule.get_random_agent(Plant))


class Plant(Agent):

    def __init__(self, name, model,turnCount=20):
        super().__init__(name, model)
        self.name = name
        self.turnCount = turnCount

    def step(self):
        self.turnCount-=1

        if self.turnCount <= 0:
            plant = Plant(random.randint(1,50),self.model)
            self.model.schedule.add(plant)
            self.turnCount = 20


        if self.model.carbon < 0.015:
            self.model.schedule.remove(self)
