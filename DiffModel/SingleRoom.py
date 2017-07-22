import matplotlib.pyplot as plt

class People(object):
    def __init__(self,number=0):
        self.number = number
        self.oxygen = 0
        self.carbon = 0
    def breath(self,o2,co2):
        # Assumption that the carbon dioxide and oxygen are ideal gases
        self.oxygen=o2-(float)(self.number)*(0.818/0.032)*(8.28*10**-3)*(296)/(1000)
        self.carbon=co2+(float)(self.number)*(1.037/0.044)*(8.28*10**-3)*(296)/(1000)
        return self.oxygen, self.carbon # return change in carbon and oxygen kPa per day
    def perspire(self):
        pass
    def addPeople(self,add=1):
        self.number+=add
    def removePeople(self,remove=1):
        if (self.number-remove>0):
            self.number-=remove
        else:
            self.number=0

class Plant(object):
    def __init__(self, area=0,maxArea=0):
        self.area = area
        self.oxygen = 0
        self.carbon = 0
        self.water = 0
    def breath(self,o2,co2):
        # Values based on wheat
        # Assumption that the carbon dioxide and oxygen are ideal gases
        self.carbon=co2-(float)(self.area)*(77/44)*(8.28*10**-3)*(296)/(1000)
        self.oxygen=o2+(float)(self.area)*(56/32)*(8.28*10**-3)*(296)/(1000)
        return self.oxygen,self.carbon
    def waterUptake(self,h2o):
        self.water = h2o-(self.area)*(11.79)
    def addCrops(self,size):
        if (self.area+size >= maxArea):
            self.area = maxArea
            return
        self.area += size
    def removeCrops(self,size):
        if (self.area-size<=0):
            self.area=0
            return
        self.area-=size

# Starting amounts of carbon and oxygen in the air
# Amounts based on Baseline Values and Assumptions Document 2015
# 101 kPa and 21% oxygen - 21.21 kPa Oxygen

# recommmended values in kPa
oxygen = 21.21
carbon = 0.15

area = input("Area of crops (in m^2): ")

# Initialize one People object
person = People(1)
wheat = Plant(area)

totOxy = []
totCarbon = []

for i in range(100): # Each iteration is a day
    oxygen, carbon = person.breath(oxygen,carbon)
    oxygen, carbon = wheat.breath(oxygen,carbon)
    if (carbon>0.53):
        person.remove()
    totOxy.append(oxygen)
    totCarbon.append(carbon)

plt.plot(range(100),totOxy, 'r', label="Oxygen")
plt.plot(range(100),totCarbon, 'g', label="Carbon Dioxide")
plt.xlabel('Time (Days)')
plt.ylabel('Gas (kPa)')
plt.title('Oxygen and Carbon Dioxide')
plt.grid(True)
plt.legend(loc='best')

plt.show()
