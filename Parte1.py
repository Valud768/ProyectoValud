from tkinter import Entry, Label, Frame, Tk, Button,ttk, Scrollbar, VERTICAL, HORIZONTAL,StringVar,END
from conexion import *


class Registro(Frame):

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
                                    
        self.frame1 = Frame(master)
        self.frame1.grid(columnspan=2, column=0,row=0)
        self.frame2 = Frame(master, bg='gray22')
        self.frame2.grid(column=0, row=1)
        self.frame3 = Frame(master)
        self.frame3.grid(rowspan=2, column=1, row=1)

        self.frame4 = Frame(master, bg='gray22')
        self.frame4.grid(column=0, row=2)

        self.codigo = StringVar()
        self.nombre = StringVar()
        self.modelo = StringVar()
        self.precio = StringVar()
        self.cantidad = StringVar()
        self.buscar = StringVar()

        self.base_datos = Registro_datos
        self.create_wietgs()


    def create_wietgs(self):
        Label(self.frame1, text = "V  A  L  U  D' S    S  H  O  P   ",bg='gray22',fg='white').grid(column=0, row=0)
        
        Label(self.frame2, text = 'AGREGAR NUEVOS DATOS',fg='black',).grid(columnspan=2, column=0,row=0, pady=5)
        Label(self.frame2, text = 'Codigo').grid(column=0,row=1, pady=15)
        Label(self.frame2, text = 'Nombre').grid(column=0,row=2, pady=15)
        Label(self.frame2, text = 'Modelo').grid(column=0,row=3, pady=15)
        Label(self.frame2, text = 'Precio').grid(column=0,row=4, pady=15)
        Label(self.frame2, text = 'Cantidad').grid(column=0,row=5, pady=15)

        Entry(self.frame2,textvariable=self.codigo).grid(column=1,row=1, padx =5)
        Entry(self.frame2,textvariable=self.nombre).grid(column=1,row=2)
        Entry(self.frame2,textvariable=self.modelo).grid(column=1,row=3)
        Entry(self.frame2,textvariable=self.precio).grid(column=1,row=4)
        Entry(self.frame2,textvariable=self.cantidad).grid(column=1,row=5)
       
        Label(self.frame4, text = 'CONTROL',fg='white', bg ='gray22').grid(columnspan=3, column=0,row=0, pady=1, padx=4)         
        Button(self.frame4,command= self.agregar_datos, text='REGISTRAR',fg="black").grid(column=0,row=1, pady=10, padx=4)
        Button(self.frame4,command = self.limpiar_datos, text='LIMPIAR',fg="black").grid(column=1,row=1, padx=10)        
        Button(self.frame4,command = self.eliminar_fila, text='ELIMINAR',fg="black").grid(column=2,row=1, padx=4)
        Button(self.frame4,command = self.mostrar_todo, text='MOSTRAR DATOS DE MYSQL', fg="black").grid(columnspan=3,column=0,row=3, pady=8)

        self.tabla = ttk.Treeview(self.frame3, height=21)
        self.tabla.grid(column=0, row=0)

        ladox = Scrollbar(self.frame3, orient = HORIZONTAL, command= self.tabla.xview)
        ladox.grid(column=0, row = 1, sticky='ew') 
        ladoy = Scrollbar(self.frame3, orient =VERTICAL, command = self.tabla.yview)
        ladoy.grid(column = 1, row = 0, sticky='ns')

        self.tabla.configure(xscrollcommand = ladox.set, yscrollcommand = ladoy.set)
       
        self.tabla['columns'] = ('Nombre', 'Modelo', 'Precio', 'Cantidad')

        self.tabla.column('#0', minwidth=100, width=120, anchor='center')
        self.tabla.column('Nombre', minwidth=100, width=130 , anchor='center')
        self.tabla.column('Modelo', minwidth=100, width=120, anchor='center' )
        self.tabla.column('Precio', minwidth=100, width=120 , anchor='center')
        self.tabla.column('Cantidad', minwidth=100, width=105, anchor='center')

        self.tabla.heading('#0', text='Codigo', anchor ='center')
        self.tabla.heading('Nombre', text='Nombre', anchor ='center')
        self.tabla.heading('Modelo', text='Modelo', anchor ='center')
        self.tabla.heading('Precio', text='Precio', anchor ='center')
        self.tabla.heading('Cantidad', text='Cantidad', anchor ='center')


        estilo = ttk.Style(self.frame3)
        estilo.theme_use('alt') #  ('clam', 'alt', 'default', 'classic')
        estilo.configure(".", foreground='red2')        
        estilo.configure("Treeview", foreground='black',  background='white')
        estilo.map('Treeview',background=[('selected', 'green2')], foreground=[('selected','black')] )

        self.tabla.bind("<<TreeviewSelect>>", self.obtener_fila)  # seleccionar  fila

    def agregar_datos(self):
        self.tabla.get_children()
        codigo = self.codigo.get()
        nombre = self.nombre.get()
        modelo = self.modelo.get()
        precio = self.precio.get()
        cantidad = self.cantidad.get()
        datos = (nombre, modelo, precio, cantidad)
        if codigo and nombre and modelo and precio and cantidad !='':        
            self.tabla.insert('',0, text = codigo, values=datos)
            self.base_datos.inserta_producto(codigo, nombre, modelo, precio, cantidad)


    def limpiar_datos(self):
        self.tabla.delete(*self.tabla.get_children())
        self.codigo.set('')
        self.nombre.set('')
        self.modelo.set('')
        self.precio.set('')
        self.cantidad.set('')


    def mostrar_todo(self):
        self.tabla.delete(*self.tabla.get_children())
        registro = self.base_datos.mostrar_productos()
        i = -1
        for dato in registro:
            i= i+1                       
            self.tabla.insert('',i, text = registro[i][1:2], values=registro[i][2:6])


    def eliminar_fila(self):
        fila = self.tabla.selection()
        if len(fila) !=0:        
            self.tabla.delete(fila)
            nombre = ("'"+ str(self.nombre_borar) + "'")       
            self.base_datos.elimina_productos(nombre)


    def obtener_fila(self, event):
        current_item = self.tabla.focus()
        if not current_item:
            return
        data = self.tabla.item(current_item)
        self.nombre_borar = data['values'][0]



def main():
    ventana = Tk()
    ventana.wm_title("LICORERIA DOÑA MADE")
    ventana.config(bg='gray22')
    ventana.geometry('900x500')
    ventana.resizable(0, 0)
    app = Registro(ventana)
    app.mainloop()


if __name__ == "__main__":
    main()