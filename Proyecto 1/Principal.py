import tkinter as tk
from datos import datos 
#from proyecto import start
#from pysnmp.hlapi import *


class Proyecto(tk.Frame):
	
	detalles = ''
	Comunidad = ''
	Ip = ''

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

		self.comunidad = tk.Entry(self)
		self.comunidad.pack(side="top", padx=20)

		self.ip = tk.Entry(self)
		self.ip.pack(side="top", padx=20)

	def agregar(self):
		index = self.lista.size()
		Comunidad = self.comunidad.get()
		Ip = self.ip.get()
		info = datos(Comunidad, Ip)
		detalles = 'Comunidad: ' + Comunidad + ' Ip: ' + Ip + '  Datos: ' + info 
		self.lista.insert(index, detalles )

	def eliminar(self):
		try:
			index = self.lista.curselection()
			self.lista.delete(index)
		except ValueError: pass

	def ver(self):
		index = self.lista.curselection()
		agente = self.lista.get(index)
		datos = agente.split(' ')
		print(datos)
		print(datos[1], datos[3])
		#manda llamar la funcion en proyecto .py con datos[1] datos[3]

def main():
	root = tk.Tk()
	title = root.title('ESCOMservium')
	size = root.geometry('500x300')
	Proyecto(root).pack(fill="both", expand=False)
	root.mainloop()
	

main()
