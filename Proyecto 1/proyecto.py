import time
from getSNMP import consultaSNMP
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from math import *
import os

comunidad = "comunSNMP"
ip = "localhost"

style.use('fivethirtyeight')

fig = plt.figure('name of variable')
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    total_input_traffic = int(
        consultaSNMP('SNMPwindows','localhost',
                     '1.3.6.1.2.1.2.2.1.10.3'))
    total_output_traffic = int(
        consultaSNMP('SNMPwindows','localhost',
                     '1.3.6.1.2.1.2.2.1.16.3'))
    total_system_time = consultaSNMP('SNMPwindows','localhost','1.3.6.1.2.1.1.2.0')

    valor = "N:" + str(total_input_traffic) + ':' + str(total_output_traffic)
    #print(valor)

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

fig = plt.figure()
ax1 = fig.add_subplot(3,2,1)
ax2 = fig.add_subplot(3,2,2)
ax3 = fig.add_subplot(3,2,3)
ax4 = fig.add_subplot(3,2,4)
ax5 = fig.add_subplot(3,2,5)


def borrar():
	if os.path.exists("example.txt"):
		os.remove("example.txt")

def animate(i):
	if (i>0):
		total_input_traffic = int(
			consultaSNMP(comunidad,ip,
                     '1.3.6.1.2.1.2.2.1.10.3'))
		total_output_traffic = int(
			consultaSNMP(comunidad,ip,
                     '1.3.6.1.2.1.2.2.1.16.3'))
		interfaces_ethernet = int(
			consultaSNMP(comunidad,ip,
                     '1.3.6.1.2.1.2.1.0'))
		diagramas_udp = int(
			consultaSNMP(comunidad,ip,
                     '1.3.6.1.2.1.7.1.0'))
		mensajes_tcp = int(
			consultaSNMP(comunidad,ip,
                     '1.3.6.1.2.1.6.6.0'))
		valor = "N:" + str(total_input_traffic) + ':' + str(total_output_traffic)
	    #print(valor)
		rrdtool.update('net3.rrd', valor)
		rrdtool.dump('net3.rrd','net3.xml')
		time.sleep(1)
		appendFile = open('example.txt','a')
		val = str(i) + "," + str(total_output_traffic) + "," + str(total_input_traffic) + "," + str(interfaces_ethernet) + "," + str(diagramas_udp) + "," + str(mensajes_tcp) + "\n"
		print(val)
		appendFile.write(val)
		appendFile.close()
		graph_data = open('example.txt','r').read()
		lines = graph_data.split('\n')
		xs = []
		ys = []
		zs = []
		ws = []
		vs = []
		us = []
		for line in lines:
			if len(line) > 1:
				x, y, z, w, v, u = line.split(',')
				xs.append(x)
				ys.append(y)
				zs.append(z)
				ws.append(w)
				vs.append(v)
				us.append(u)
        
		ax1.clear()
		ax2.clear()
		ax3.clear()
		ax4.clear()
		ax5.clear()

		
		ax1.plot(xs[-10:], ys[-10:])
		ax2.plot(xs[-10:], zs[-10:])
		ax3.plot(xs[-10:], ws[-10:])
		ax4.plot(xs[-10:], vs[-10:])
		ax5.plot(xs[-10:], us[-10:])
		ax1.set_title('Trafico entrada')
		ax2.set_title('Trafico salida')
		ax3.set_title('Interfaces ethernet')
		ax4.set_title('Diagramas UDP')
		ax5.set_title('Mensajes TCP')

def an(): 
	borrar()
	i=0
	while 1:
		ani = animation.FuncAnimation(fig, animate, interval=100)
		i += 1
		plt.show()
an()
