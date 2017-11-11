from Tkinter import *
import Tkinter as tk
import ttk
import crudagentes
import time
from PIL import Image, ImageTk
import pygtk
import FuncionesSNMP
import multiprocessing
import rrdtool
import xml.etree.cElementTree as ET
from pysnmp.hlapi import *
import os



pygtk.require('2.0')


#Piscina de procesos
tiempoInicio= int(time.time())

url = ""
def open_url(url):
	os.system("eog " + url)

root = Tk()
nombreagentes = crudagentes.consultaragentes()
anombres = []
estadoagente = []
puertosagente = []
for agente in nombreagentes:
    anombres.append(agente) #Obtenemos el nombre del agente
    estadoagente.append(crudagentes.consultarestado(agente)) #Agregamos el estado
    puertosagente.append(crudagentes.consultarpuertos(agente)) #Agregamos los puertos 
print(anombres)

# Names of the gifts we can send
gifts = { 'agregar':'Agregar agente', 'eliminar':'Eliminar agente', 'estado':'Ver estado del agente', 'graficas':'Ver graficas del agente'}

# State variables
gift = StringVar()
sentmsg = StringVar()
statusmsg = StringVar()

def showPopulation(*args):
    idxs = lbox.curselection()
    if len(idxs)==1:
        idx = int(idxs[0])
        estado = estadoagente[idx]
        name = nombreagentes[idx]
        puertos = puertosagente[idx]
        statusmsg.set("Agent %s is %s and has ports %s" % (name, estado, puertos))
    sentmsg.set('')


def agregarAgente (win, nombre, version, comunidad):
    if FuncionesSNMP.VerificarArgumentos(nombre, comunidad) != "-1":
        crudagentes.agregaragente(nombre, version, comunidad) #FALTAN VALORES POR AGREGAR PERO POR EL MOMENTO SON ESTATICOS PORQUE SE OBTIENEN DE LAS PETICIONES SNMP
        nombreagentes.append(nombre)  # Obtenemos el nombre del agente
        estadoagente.append(crudagentes.consultarestado(nombre))  # Agregamos el estado
        puertosagente.append(crudagentes.consultarpuertos(nombre))  # Agregamos los puertos
        FuncionesSNMP.AgregarMultiProceso()
        win.destroy()
        lbox.insert(END, nombre)
        lbox.update()
    else:
        msg = Message(win, text="Agente no agregado")
        msg.pack()

def buscarAgente (win, tree, nombre, sistema, ubicacion, nombreCB, ubicacionCB, soCB):
    resultado = []
    if nombre!='':
        resultado.append(crudagentes.consultaragente("nombre", nombre))
    elif nombreCB!='':
        resultado.append(crudagentes.consultaragente("nombre", nombreCB))
    elif sistema!='':
        resultado.append(crudagentes.consultaragente("sistema-operativo", sistema))
    elif soCB!='':
        resultado.append(crudagentes.consultaragente("sistema-operativo", soCB))
    elif ubicacion!='':
        resultado.append(crudagentes.consultaragente("ubicacion", ubicacion))
    elif ubicacionCB!='':
        resultado.append(crudagentes.consultaragente("ubicacion", ubicacionCB))
    for i in tree.get_children():
        tree.delete(i)
    for nombreAgente in resultado:
        print(nombreAgente[0])
        tree.insert("", 0, values=(
        nombreAgente, crudagentes.consultarversion(nombreAgente[0]), crudagentes.consultarso(nombreAgente[0]),
        crudagentes.consultarubicacion(nombreAgente[0]), crudagentes.consultarpuertos(nombreAgente[0]),
        crudagentes.consultartiempo(nombreAgente[0])))

def newselection(cb):
        value_of_combo = cb.get()
        print(value_of_combo)

def sendGift(*args):
    idxs = lbox.curselection()
    if len(idxs)==1:
        idx = int(idxs[0])
        lbox.see(idx)
        name = nombreagentes[idx]
        if gifts[gift.get()] == "Agregar agente": #Abrir ventana para agregar agente
            win = tk.Toplevel(root)
            frame1 = Frame(win)
            frame1.pack()

            Label(frame1, text="Nombre").grid(row=0, column=0, sticky=W)
            nombreVar = StringVar()
            nombre = Entry(frame1, textvariable=nombreVar)
            nombre.grid(row=0, column=1, sticky=W)

            Label(frame1, text="Version SNMP").grid(row=1, column=0, sticky=W)
            versionVar = StringVar()
            version = Entry(frame1, textvariable=versionVar)
            version.grid(row=1, column=1, sticky=W)

            Label(frame1, text="Comunidad").grid(row=2, column=0, sticky=W)
            comunidadVar = StringVar()
            comunidad = Entry(frame1, textvariable=comunidadVar)
            comunidad.grid(row=2, column=1, sticky=W)

            frame2 = Frame(win)  # Row of buttons
            frame2.pack()
            b1 = Button(frame2, text="Agregar agente", command=lambda:agregarAgente(win, nombreVar.get(), versionVar.get(), comunidadVar.get()))
            b1.pack(side=LEFT);



        elif gifts[gift.get()] == "Eliminar agente": #Eliminar agente
            lbox.delete(ANCHOR) #Elimina agente seleccionado de la lista
            crudagentes.eliminaragente(name) #Elimina agente del xml
            FuncionesSNMP.AgregarMultiProceso()
        elif gifts[gift.get()] == "Ver estado del agente":  # Muestra informacion del agente
            win = tk.Toplevel(root)

            frame = Frame(win)
            frame.pack()

            Label(frame, text="Nombre").grid(row=0, column=0, sticky=W)
            nombreVar = StringVar()
            nombre = Entry(frame, textvariable=nombreVar)
            nombre.grid(row=0, column=1, sticky=W)

            Label(frame, text="Sistema").grid(row=0, column=2, sticky=W)
            sistemaVar = StringVar()
            sistema = Entry(frame, textvariable=sistemaVar)
            sistema.grid(row=0, column=3, sticky=W)

            Label(frame, text="Ubicacion").grid(row=0, column=4, sticky=W)
            ubicacionVar = StringVar()
            ubicacion = Entry(frame, textvariable=ubicacionVar)
            ubicacion.grid(row=0, column=5, sticky=W)

            names = crudagentes.nombres()
            names.append('')
            nombresCB = StringVar()
            cbp2 = Label(frame, text="Host")
            cbp2.grid(row=1, column=0, sticky=W)
            cb2 = ttk.Combobox(frame, values=names, state='readonly', textvariable=nombresCB)
            cb2.grid(row=1, column=1, sticky=W)
            cb2.bind("<<ComboboxSelected>>", newselection(cb2))

            cities = crudagentes.ubicaciones()
            cities.append('')
            ubicacionCB = StringVar()
            cbp3 = Label(frame, text="Ubicacion")
            cbp3.grid(row=1, column=2, sticky=W)
            cb3 = ttk.Combobox(frame, values=cities, state='readonly', textvariable=ubicacionCB)
            cb3.grid(row=1, column=3, sticky=W)
            cb3.bind("<<ComboboxSelected>>", newselection(cb3))

            sos = crudagentes.sistemasoperativos()
            sos.append('')
            soCB = StringVar()
            cbp4 = Label(frame, text="Sistema operativo")
            cbp4.grid(row=1, column=4, sticky=W)
            cb4 = ttk.Combobox(frame, values=sos, state='readonly', textvariable=soCB)
            cb4.grid(row=1, column=5, sticky=W)
            cb4.bind("<<ComboboxSelected>>", newselection(cb4))

            frame1 = Frame(win)
            frame1.pack()

            tree = ttk.Treeview(win)

            tree["columns"] = (
            "Nombre", "Version", "Sistema-Operativo", "Ubicacion-geografica", "Puertos", "Tiempo-actividad")
            tree.column("Nombre", width=100)
            tree.column("Version", width=50)
            tree.column("Sistema-Operativo", width=100)
            tree.column("Ubicacion-geografica", width=200)
            tree.column("Puertos", width=50)
            tree.column("Tiempo-actividad", width=150)
            tree.heading("Nombre", text="Nombre")
            tree.heading("Version", text="Version")
            tree.heading("Sistema-Operativo", text="Sistema Operativo")
            tree.heading("Ubicacion-geografica", text="Ubicacion geografica")
            tree.heading("Puertos", text="# Puertos")
            tree.heading("Tiempo-actividad", text="Tiempo de actividad")

            for nombreAgente in crudagentes.consultaragentes():
                tree.insert("", 0, values=(
                nombreAgente, crudagentes.consultarversion(nombreAgente), crudagentes.consultarso(nombreAgente),
                crudagentes.consultarubicacion(nombreAgente), crudagentes.consultarpuertos(nombreAgente),
                crudagentes.consultartiempo(nombreAgente)))

            tree.pack()

            b1 = Button(frame1, text="Buscar",
                        command=lambda: buscarAgente(win, tree, nombreVar.get(), sistemaVar.get(), ubicacionVar.get(),
                                                     nombresCB.get(), ubicacionCB.get(), soCB.get()))
            b1.grid(row=0, column=6, sticky=W)

            win.mainloop()


        elif gifts[gift.get()] == "Ver graficas del agente":  # Muestra las graficas del agente

            win = tk.Toplevel(root)

            frame1 = Frame(win)

            frame1.pack()

            uptime = FuncionesSNMP.consultaSNMP(str(crudagentes.consultarcomunidad(name)), name, '1.3.6.1.2.1.1.3.0')

            contacto = FuncionesSNMP.consultaSNMP(str(crudagentes.consultarcomunidad(name)), name, '1.3.6.1.2.1.1.4.0')

            nomb = FuncionesSNMP.consultaSNMP(str(crudagentes.consultarcomunidad(name)), name, '1.3.6.1.2.1.1.5.0')

            ubicac = FuncionesSNMP.consultaSNMP(str(crudagentes.consultarcomunidad(name)), name, '1.3.6.1.2.1.1.6.0')

            servicios = FuncionesSNMP.consultaSNMP(str(crudagentes.consultarcomunidad(name)), name, '1.3.6.1.2.1.1.7.0')

            Label(frame1, text="Nombre: ").grid(row=0, column=0)

            Label(frame1, text=nomb).grid(row=0, column=1)

            Label(frame1, text="Servicios: ").grid(row=0, column=2)

            Label(frame1, text=servicios).grid(row=0, column=3)

            Label(frame1, text="Ubicacion: ").grid(row=0, column=4)

            Label(frame1, text=ubicac).grid(row=0, column=5)

            Label(frame1, text="Contacto: ").grid(row=0, column=6)

            Label(frame1, text=contacto).grid(row=0, column=7)

            Label(frame1, text="Encendido desde: ").grid(row=0, column=8)

            Label(frame1, text=uptime).grid(row=0, column=9)

            #image_icmp = Image.open(name + "_ICMP.png")

            #icmp = ImageTk.PhotoImage(image_icmp)

            # icmp_ = Label(win, image=icmp);

            # icmp_.image = icmp  # <== this is were we anchor the img object

            # icmp_.configure(image=icmp)

          #  icmp_.grid(column=0)

            #icmp_.pack(side=LEFT)

            #image_ips = Image.open(name + "_IPs.png")

            #ips = ImageTk.PhotoImage(image_ips)

            #ips_ = Label(win, image=ips);

            #ips_.image = ips  # <== this is were we anchor the img object

            #ips_.configure(image=ips)

         #   ips_.grid(column=0)

            #ips_.pack(side=BOTTOM)

            image_icmppack = Image.open(name + "_SNMPPackets.png")

            icmppack = ImageTk.PhotoImage(image_icmppack)

            icmppack_ = Label(win, image=icmppack);

            icmppack_.image = icmppack  # <== this is were we anchor the img object

            icmppack_.configure(image=icmppack)
	    icmppack_.bind("<Button-1>", lambda e, url = url:open_url(name + "_SNMPPackets.png"))

            #icmppack_.grid(column=0)

            icmppack_.pack(side=BOTTOM)

            image_tcpcon = Image.open(name + "_TCPConnections.png")

            tcpcon = ImageTk.PhotoImage(image_tcpcon)

            tcpcon_ = Label(win, image=tcpcon);

            tcpcon_.image = tcpcon  # <== this is were we anchor the img object

            tcpcon_.configure(image=tcpcon)
	    tcpcon_.bind("<Button-1>", lambda e, url = url:open_url(name + "_TCPConnections.png"))

           # tcpcon_.grid(column=0)
            tcpcon_.pack(side=BOTTOM)

            image_tcpseg = Image.open(name + "_TCPSegments.png")

            tcpseg = ImageTk.PhotoImage(image_tcpseg)

            tcpseg_ = Label(win, image=tcpseg);

            tcpseg_.image = tcpseg  # <== this is were we anchor the img object

            tcpseg_.configure(image=tcpseg)
	    tcpseg_.bind("<Button-1>", lambda e, url = url:open_url(name + "_TCPSegments.png"))

            #tcpseg_.grid(column=0)

            tcpseg_.pack()


# Create and grid the outer content frame
c = ttk.Frame(root, padding=(5, 5, 12, 0))
c.grid(column=0, row=0, sticky=(N,W,E,S))
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0,weight=1)
lbox = Listbox(c)


#Se agregan los agentes a la tabla y se adjuntan sus procesos.
for agente in anombres:
    i=+1
    #verifica si el agente esta activo
    if FuncionesSNMP.VerificarActividad(agente) == -1:
        crudagentes.modificarestado(agente)
    else:
        print"Agrego Proceso"
    lbox.insert(END, agente)
    FuncionesSNMP.CreacionAgenteRDDTOOL(agente, tiempoInicio)

lbl = ttk.Label(c, text="Seleccione una accion:")
g1 = ttk.Radiobutton(c, text=gifts['agregar'], variable=gift, value='agregar')
g2 = ttk.Radiobutton(c, text=gifts['eliminar'], variable=gift, value='eliminar')
g3 = ttk.Radiobutton(c, text=gifts['estado'], variable=gift, value='estado')
g4 = ttk.Radiobutton(c, text=gifts['graficas'], variable=gift, value='graficas')
send = ttk.Button(c, text='Seleccionar', command=sendGift, default='active')
sentlbl = ttk.Label(c, textvariable=sentmsg, anchor='center')
status = ttk.Label(c, textvariable=statusmsg, anchor=W)

# Grid all the widgets
lbox.grid(column=0, row=0, rowspan=6, sticky=(N,S,E,W))
lbl.grid(column=1, row=0, padx=10, pady=5)
g1.grid(column=1, row=1, sticky=W, padx=20)
g2.grid(column=1, row=2, sticky=W, padx=20)
g3.grid(column=1, row=3, sticky=W, padx=20)
g4.grid(column=1, row=4, sticky=W, padx=20)
send.grid(column=2, row=4, sticky=E)
sentlbl.grid(column=1, row=5, columnspan=2, sticky=N, pady=5, padx=5)
status.grid(column=0, row=6, columnspan=2, sticky=(W,E))
c.grid_columnconfigure(0, weight=1)
c.grid_rowconfigure(5, weight=1)

lbox.bind('<<ListboxSelect>>', showPopulation)
lbox.bind('<Double-1>', sendGift)
root.bind('<Return>', sendGift)

# Colorize alternating lines of the listbox
for i in range(0,len(anombres),2):
    lbox.itemconfigure(i, background='#f0f0ff')
gift.set('card')
sentmsg.set('')
statusmsg.set('')
lbox.selection_set(0)
showPopulation()
root.mainloop()
