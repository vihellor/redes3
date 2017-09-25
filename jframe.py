import tkinter as tk

class Principal(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)

		title = tk.Label(self, text="Obserbium ESCOM", anchor="w")
		title.pack(side="top")

		message = tk.Label(self, text="Introduce la Comunidad: ", anchor="w")
		message.pack(side="left")

		self.comunidad = tk.Entry(self)
		self.comunidad.pack(side="top", padx=20)

		data = tk.Label(self, text="Introduce la direccion ip: ", anchor="w")
		data.pack(side="left")

		self.ip = tk.Entry(self)
		self.ip.pack(side="top", padx=20)
		
		btnAgregar = tk.Button(self, text ="Agregar", command = self.agregar)
		btnAgregar.pack(side="right")

	def agregar(self):
		print('Comunidad: ', self.comunidad.get())
		print('Ip: ' +  self.ip.get())
		#llamar a funcion para agregar agente.
root = tk.Tk()
Principal(root).pack(fill="both", expand=False)
root.mainloop()