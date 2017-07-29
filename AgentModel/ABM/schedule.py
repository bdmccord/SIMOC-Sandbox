import random
from collections import defaultdict

from mesa.time import RandomActivation


class RandomActivationBySpecies(RandomActivation):

    agents_by_type = defaultdict(list)

    def __init__(self, model):
        super().__init__(model)
        self.agents_by_type = defaultdict(list)

    def add(self, agent):
        self.agents.append(agent)
        agent_class = type(agent)
        self.agents_by_type[agent_class].append(agent)

    def remove(self, agent):

        while agent in self.agents:
            self.agents.remove(agent)

        agent_class = type(agent)
        while agent in self.agents_by_type[agent_class]:
            self.agents_by_type[agent_class].remove(agent)

    def step(self, by_type=True):
        if by_type:
            for agent_class in list(self.agents_by_type):
                self.step_type(agent_class)
            self.steps += 1
            self.time += 1
        else:
            super().step()

    def step_type(self, species):

        agents = self.agents_by_type[species]
        random.shuffle(agents)

        for agent in agents:
            agent.step()


    def get_agent_count(self, type_class):

        return len(self.agents_by_type[type_class])

    def get_random_agent(self, type_class):

        agents = self.agents_by_type[type_class]
        return agents[random.randint(0,self.get_agent_count(type_class))]
