import tkinter as tk

class Proyecto(tk.Frame):
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
		index = self.lista.index()
		print('index: ', index)
		#self.lista.insert(1, 'Agente: SO  Ultimo reinicio...')

	def eliminar(self):
		try:
			index = self.lista.curselection()
			self.lista.delete(index)
		except ValueError: pass
		

	def ver(self):
		print('Ip: ')


def main():
	root = tk.Tk()
	title = root.title('ESCOMservium')
	size = root.geometry('500x300')
	Proyecto(root).pack(fill="both", expand=False)
	root.mainloop()
	

main()