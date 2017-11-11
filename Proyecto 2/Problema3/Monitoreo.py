import FuncionesSNMP
import xml.etree.cElementTree as ET
import time
z=0
i=0
tree = ET.parse('agentesAgregados.xml')
root2 = tree.findall("dispositivo")
for dispositivo in root2:
    z+=1
    i+=1
while(1):
    FuncionesSNMP.Monitoreo()
    #time.sleep(1)
