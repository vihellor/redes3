import time
import rrdtool
from getSNMP import consultaSNMP
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from math import *

total_input_traffic = 0
total_output_traffic = 0
total_system_time = 0


style.use('fivethirtyeight')
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    total_input_traffic = int(
        consultaSNMP('comunSNMP','localhost',
                     '1.3.6.1.2.1.2.2.1.10.3'))
    total_output_traffic = int(
        consultaSNMP('comunSNMP','localhost',
                     '1.3.6.1.2.1.2.2.1.16.3'))
    total_system_time = consultaSNMP('comunSNMP','localhost','1.3.6.1.2.1.1.2.0')

    valor = "N:" + str(total_input_traffic) + ':' + str(total_output_traffic)
    #print(valor)
    
    rrdtool.update('net3.rrd', valor)
    rrdtool.dump('net3.rrd','net3.xml')
    time.sleep(1)
    appendFile = open('example.txt','a')
    if (i>0):
        val = str(i) + "," + str(total_output_traffic%10000) + "\n"
        appendFile.write(val)
        appendFile.close()
        graph_data = open('example.txt','r').read()
        lines = graph_data.split('\n')
        xs = []
        ys = []
        for line in lines:
            if len(line) > 1:
                x, y = line.split(',')
                xs.append(x)
                ys.append(y)
        print(val)
        ax1.clear()
        #print(xs,ys)
        ax1.plot(xs, ys)
        
ani = animation.FuncAnimation(fig, animate, interval=10)
plt.show()


