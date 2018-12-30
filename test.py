import sys
sys.path.insert(0, 'classes/')
from graph import *

g = createGraph('samples/example.txt', 1)
# print(g.getTotalResidents(), g.getTotalHospitals())
g.initResidentCapacities()
g.initAllResidentClass()
g.printFormat()