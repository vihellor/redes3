import tkinter as tk
from datos import datos 
from Agregar import Agregar
<<<<<<< HEAD
from proyecto import start
=======
from pysnmp.hlapi import *
>>>>>>> 3a0859532d7739836801bddc2b0999e79a7b5209

class Proyecto(tk.Frame):
	
	global detalles
	Comunidad = 'SNMPwindows'
	Ip = 'localhost'

	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		
		message = tk.Label(self, text='Lista de agentes:', anchor="w")
		message.pack(side="top")

		self.lista = tk.Listbox(self)
		self.lista.config(height = 9, width = 80)
		self.lista.pack()

		btnAdd = tk.Button(self, text ='Agregar', command = self.agregar)
		btnAdd.pack(side='right')

		btnErase = tk.Button(self, text ='Eliminar', command = self.eliminar)
		btnErase.pack(side='bottom')

		btnShow = tk.Button(self, text ='Ver variables', command = self.ver)
		btnShow.pack(side='left')

	def agregar(self):
		index = self.lista.size()
		root1 = tk.Tk()
		Agregar(root1).pack(fill="both", expand=False)
		root1.mainloop()
		#Aqui van los datos del archivo datos :(

	def eliminar(self):
		try:
			index = self.lista.curselection()
			self.lista.delete(index)
		except ValueError: pass

	def ver(self):
<<<<<<< HEAD
		print()
		#start(Comunidad, Ip)
=======
		print('Ip: ')
        vis = new Visual()
        #Visual.an()  ##sólo falta agregar el 
    def datos(comunidad, ip):
	    errorIndication, errorStatus, errorIndex, varBinds = next(
		    nextCmd(SnmpEngine(),
		    CommunityData(comunidad, mpModel=0),
		    UdpTransportTarget((ip, 161)),
		    ContextData(),
		    ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0')),
		    ObjectType(ObjectIdentity('1.3.6.1.2.1.1.2.0')),
		    ObjectType(ObjectIdentity('1.3.6.1.2.1.1.3.0')),
		    ObjectType(ObjectIdentity('1.3.6.1.2.1.1.4.0')),
		    ObjectType(ObjectIdentity('1.3.6.1.2.1.1.5.0')),
		    ObjectType(ObjectIdentity('1.3.6.1.2.1.1.6.0'))))

	    if errorIndication:
		    print(errorIndication)
		    return None

	    elif errorStatus:
		    print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
		    return None
		
	    else:
		    datos = '' 
		    for varBind in varBinds:
			    data = str(varBind).split('=')
			    datos = datos + ' ' + data[1] 
		    return datos
>>>>>>> 3a0859532d7739836801bddc2b0999e79a7b5209


def main():
	root = tk.Tk()
	title = root.title('ESCOMservium')
	size = root.geometry('500x300')
	Proyecto(root).pack(fill="both", expand=False)
	root.mainloop()
	

main()
