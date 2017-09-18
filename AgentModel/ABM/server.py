from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from ABM.agents import Human, Plant
from ABM.model import SingleRoomModel


def single_room(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Human:
        portrayal["Shape"] = "ABM/resources/people.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is Plant:
        portrayal["Color"] = "#00AA00"
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal

canvas_element = CanvasGrid(single_room, 20, 20, 500, 500)


chart_element = ChartModule([{"Label": "Human", "Color": "#AA0000"},
                             {"Label": "Plant", "Color": "#666666"}],
                             data_collector_name="datacollector")

chart_gas = ChartModule([{"Label": "Carbon", "Color": "#AA0000"}],
                             data_collector_name="datacollector2")

server = ModularServer(SingleRoomModel, [canvas_element, chart_element, chart_gas],
                       "Single Room Model",
                       model_params=dict(
                           excess_co2=UserSettableParameter('checkbox', 'Excess Carbon Enabled', False),
                           excess_amount=UserSettableParameter('slider', "Excess Carbon per Step", 1,1,100, description="Percentage of excess carbon dioxide to be added"),
                           regrowth=UserSettableParameter('checkbox', 'Plant Regrowth Enabled', False),
                           h_agents=UserSettableParameter('slider', 'Initial Human Population', 1, 0, 10),
                           p_agents=UserSettableParameter('slider', 'Initial Plant Population', 5, 0, 100),
                           plants_spread=UserSettableParameter('slider', 'Plants Spread Rate', 20, 1, 50, description="The number of steps it takes for a plant to spread.")
                           )
                       )
