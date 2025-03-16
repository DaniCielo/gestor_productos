from tkinter import ttk
from tkinter import *
import sqlite3


class Producto:

    db = "database/productos.db"

    def __init__(self, root):
        self.ventana = root
        self.ventana.title("App Gestor de Productos")    # Título de la ventana
        self.ventana.resizable(1,1)                      # La ventana se hace redimensionable
        self.ventana.wm_iconbitmap("recursos/icon.ico")  # Agrega el icono a la ventana

        # Creación del contenedor Frame principal
        frame = LabelFrame(self.ventana, text="Registrar un nuevo Producto", font=('Calibri', 16, 'bold'))
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        # Label Nombre
        self.etiqueta_nombre = Label(frame, text="Nombre: ", font=('Calibri', 13))
        self.etiqueta_nombre.grid(row=1, column=0)

        # Entry Nombre (caja que recibe el nombre)
        self.nombre = Entry(frame, font=('Calibri', 13))
        self.nombre.focus()
        self.nombre.grid(row=1, column=1)

        # Label Categoría
        self.etiqueta_categoria = Label(frame, text="Categoría: ", font=('Calibri', 13))
        self.etiqueta_categoria.grid(row=2, column=0)

        # Entry Categoría (caja que recibe la categoría)
        self.categoria = Entry(frame, font=('Calibri', 13))
        self.categoria.grid(row=2, column=1)

        # Label Precio
        self.etiqueta_precio = Label(frame, text="Precio: ", font=('Calibri', 13))
        self.etiqueta_precio.grid(row=3, column=0)

        # Entry Precio (caja que recibe el precio)
        self.precio = Entry(frame, font=('Calibri', 13))
        self.precio.grid(row=3, column=1)

        # Label Stock
        self.etiqueta_stock = Label(frame, text="Stock: ", font=('Calibri', 13))
        self.etiqueta_stock.grid(row=4, column=0)

        # Entry stock
        self.stock = Entry(frame, font=('Calibri', 13))
        self.stock.grid(row=4, column=1)

        # Botón Añadir Producto
        s = ttk.Style()
        s.configure("my.TButton", font=("Calibri", 14, "bold"))
        self.boton_aniadir = ttk.Button(frame, text="Guardar Producto", command=self.add_producto, style="my.TButton")
        self.boton_aniadir.grid(row=5, columnspan=2, sticky=W+E)

        # Mensaje informativo
        self.mensaje = Label(text="", fg="red")
        self.mensaje.grid(row=5, column=0, columnspan=2, sticky=W+E)

        # Tabla de Productos
        # Estilo personalizado para la tabla
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, "bold"))
        style.layout("mystyle.Treeview", [("mystyle.Treeview.treearea", {"sticky":"nswe"})])

        # Estructura de la tabla
        self.tabla = ttk.Treeview(height=20, columns=(0,1,2,3), style="mystyle.Treeview")
        self.tabla.grid(row=6, column=0, columnspan=2)
        self.tabla.heading('#0', text="Nombre", anchor=CENTER)
        self.tabla.heading(0, text="ID")
        self.tabla.heading(1, text="Precio", anchor=CENTER)
        self.tabla.heading(2, text="Stock", anchor=CENTER)
        self.tabla.heading(3, text="Categoría")
        self.tabla.column(1, width=140, anchor=CENTER)
        self.tabla.column(2, width=120, anchor=CENTER)
        self.tabla["displaycolumns"]=(1,2)  # Mostramos columnas 1 y 2. El tree se muestra salvo que lo cambiemos en el método (show="headings")

        # Botones de Eliminar y Editar
        self.boton_eliminar = ttk.Button(text="ELIMINAR", command=self.del_producto, style="my.TButton")
        self.boton_eliminar.grid(row=7, column=0, sticky=W+E)
        self.boton_editar = ttk.Button(text="EDITAR", command=self.edit_producto, style="my.TButton")
        self.boton_editar.grid(row=7, column=1, sticky=W+E)

        # Llamada al método get_productos() para obtener el listado de productos al iniciar la app
        self.get_productos()

    def db_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db) as con:                 # Iniciamos una conexión con la DB con alias "con"
            cursor = con.cursor()                             # Generamos un cursor para operar en la DB
            resultado = cursor.execute(consulta, parametros)  # Preparar la consulta con SQL (parametros solo si hay)
            con.commit()                                      # Esto ejecuta la consulta
        return resultado                                      # Devuelve el resultado de la consulta SQL

    def get_productos(self):
        # Limpiar la tabla por si hubiera algo anterior
        registros_tabla = self.tabla.get_children()           # Esta instrucción trae los datos de la tabla
        for fila in registros_tabla:
            self.tabla.delete(fila)

        # Consulta SQL
        query = "SELECT * FROM producto ORDER BY categoria ASC, nombre ASC"
        registros_db = self.db_consulta(query)                # Consulta a la DB

        # Estilo personalizado para la línea "categoría"
        self.tabla.tag_configure(tagname="categoria", foreground='#088A08', font=('Calibri', 11, 'italic'))

        # Escribir los datos en pantalla
        categ_ant = ""
        for fila in registros_db:
            if categ_ant != fila[3]:
                self.tabla.insert('', END, text=" >>> "+fila[3]+" <<< ", tags=("categoria"))
                categ_ant = fila[3]
            print(fila)
            self.tabla.insert('', END, text=fila[1], values=(fila[0],fila[2],fila[4],fila[3]))

    def validacion_nombre(self):
        nombre_introducido_por_usuario = self.nombre.get()
        return len(nombre_introducido_por_usuario) != 0

    def validacion_precio(self):
        precio_introducido_por_usuario = self.precio.get()
        return len(precio_introducido_por_usuario) != 0

    def add_producto(self):
        if self.validacion_nombre() and self.validacion_precio():
            query = "INSERT INTO producto VALUES (NULL, ?, ?, ?, ?)"
            parametros = (self.nombre.get(), self.precio.get(), self.categoria.get(), self.stock.get())
            self.db_consulta(query, parametros)
            self.mensaje["text"] = "Producto {} añadido con éxito".format(self.nombre.get())
            self.nombre.delete(0, END)
            self.precio.delete(0, END)
            self.categoria.delete(0, END)
            self.stock.delete(0, END)

            self.get_productos()

        elif self.validacion_nombre() and self.validacion_precio() == False:
            self.mensaje["text"] = "El precio es obligatorio"
        elif self.validacion_nombre() == False and self.validacion_precio():
            self.mensaje["text"] = "El nombre es obligatorio"
        else:
            self.mensaje["text"] = "El nombre y el precio son obligatorios"

    def del_producto(self):
        self.mensaje["text"] = ""
        try:
            self.tabla.item(self.tabla.selection())["values"][0]
        except IndexError as e:
            self.mensaje["text"] = "Por favor, seleccione un producto"
            return

        nombre = self.tabla.item(self.tabla.selection())["text"]
        id = self.tabla.item(self.tabla.selection())["values"][0]
        query = "DELETE FROM producto WHERE id = ?"
        self.db_consulta(query, (id,))
        self.mensaje["text"] = "Producto {} eliminado con éxito".format(nombre)

        self.get_productos()

    def edit_producto(self):
        self.mensaje["text"] = ""
        try:
            self.tabla.item(self.tabla.selection())["values"][0]
        except IndexError as e:
            self.mensaje["text"] = "Por favor, seleccione un producto"
            return

        id = self.tabla.item(self.tabla.selection())["values"][0]
        old_nombre = self.tabla.item(self.tabla.selection())["text"]
        old_precio = self.tabla.item(self.tabla.selection())["values"][1]
        old_categoria = self.tabla.item(self.tabla.selection())["values"][3]
        old_stock = self.tabla.item(self.tabla.selection())["values"][2]
        self.ventana_editar = Toplevel()
        self.ventana_editar.title("Editar Producto")
        self.ventana_editar.resizable(1,1)
        self.ventana_editar.wm_iconbitmap("recursos/icon.ico")

        titulo = Label(self.ventana_editar, text="Edición de Productos", font=("Calibri", 30, "bold"))
        titulo.grid(column=0, row=0)

        # Creación del contenedor Frame de la ventana Editar Producto
        frame_ep = LabelFrame(self.ventana_editar, text="Editar el siguiente Producto", font=('Calibri', 16, 'bold'))
        frame_ep.grid(row=1, column=0, columnspan=20, pady=20)

        # Label Nombre antiguo
        self.etiqueta_nombre_antiguo = Label(frame_ep, text="Nombre antiguo: ", font=('Calibri', 13))
        self.etiqueta_nombre_antiguo.grid(row=2, column=0)
        # Entry Nombre antiguo
        self.input_nombre_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_nombre), state="readonly", font=('Calibri', 13))
        self.input_nombre_antiguo.grid(row=2, column=1)

        # Label Nombre nuevo
        self.etiqueta_nombre_nuevo = Label(frame_ep, text="Nombre nuevo: ", font=('Calibri', 13))
        self.etiqueta_nombre_nuevo.grid(row=3, column=0)
        # Entry Nombre nuevo
        self.input_nombre_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_nombre_nuevo.grid(row=3, column=1)

        # Label Precio antiguo
        self.etiqueta_precio_antiguo = Label(frame_ep, text="Precio antiguo: ", font=('Calibri', 13))
        self.etiqueta_precio_antiguo.grid(row=4, column=0)
        # Entry Precio antiguo
        self.input_precio_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_precio), state="readonly", font=('Calibri', 13))
        self.input_precio_antiguo.grid(row=4, column=1)

        # Label Precio nuevo
        self.etiqueta_precio_nuevo = Label(frame_ep, text="Precio nuevo: ", font=('Calibri', 13))
        self.etiqueta_precio_nuevo.grid(row=5, column=0)
        # Entry Precio nuevo
        self.input_precio_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_precio_nuevo.grid(row=5, column=1)

        # Label Categoría antigua
        self.etiqueta_categoria_antiguo = Label(frame_ep, text="Categoría antigua: ", font=('Calibri', 13))
        self.etiqueta_categoria_antiguo.grid(row=6, column=0)
        # Entry Categoría antigua
        self.input_categoria_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_categoria), state="readonly", font=('Calibri', 13))
        self.input_categoria_antiguo.grid(row=6, column=1)

        # Label Categoría nueva
        self.etiqueta_categoria_nuevo = Label(frame_ep, text="Categoría nueva: ", font=('Calibri', 13))
        self.etiqueta_categoria_nuevo.grid(row=7, column=0)
        # Entry Categoría nueva
        self.input_categoria_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_categoria_nuevo.grid(row=7, column=1)

        # Label Stock antiguo
        self.etiqueta_stock_antiguo = Label(frame_ep, text="Stock antiguo: ", font=('Calibri', 13))
        self.etiqueta_stock_antiguo.grid(row=8, column=0)
        # Entry Stock antiguo
        self.input_stock_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_stock), state="readonly", font=('Calibri', 13))
        self.input_stock_antiguo.grid(row=8, column=1)

        # Label Stock nuevo
        self.etiqueta_stock_nuevo = Label(frame_ep, text="Stock nuevo: ", font=('Calibri', 13))
        self.etiqueta_stock_nuevo.grid(row=9, column=0)
        # Entry Stock nuevo
        self.input_stock_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_stock_nuevo.grid(row=9, column=1)

        # Botón Actualizar Producto
        self.boton_actualizar = ttk.Button(frame_ep, text="Actualizar Producto", style="my.TButton", command=lambda:
                                           self.actualizar_productos(
                                           id,
                                           old_nombre,
                                           old_precio,
                                           old_categoria,
                                           old_stock,
                                           self.input_nombre_nuevo.get(),
                                           self.input_precio_nuevo.get(),
                                           self.input_categoria_nuevo.get(),
                                           self.input_stock_nuevo.get()))
        self.boton_actualizar.grid(row=10, columnspan=2, sticky=W+E)

        # debug
        #print(self.tabla.item(self.tabla.selection()))
        #print(self.tabla.item(self.tabla.selection())["text"])
        #print(self.tabla.item(self.tabla.selection())["values"])
        #print(self.tabla.item(self.tabla.selection())["values"][0])

    def actualizar_productos(self, id, old_nombre, old_precio, old_categoria, old_stock,
                                       nvo_nombre, nvo_precio, nvo_categoria, nvo_stock):
        producto_modificado = False
        query = "UPDATE producto SET nombre = ?, precio = ?, categoria = ?, stock = ? WHERE id = ?"
        if not (nvo_nombre == "" and nvo_precio == "" and nvo_categoria == "" and nvo_stock == ""):
            producto_modificado = True
            if nvo_nombre == "":
                nombre_query = old_nombre
            else:
                nombre_query = nvo_nombre
            if nvo_precio == "":
                precio_query = old_precio
            else:
                precio_query = nvo_precio
            if nvo_categoria == "":
                categoria_query = old_categoria
            else:
                categoria_query = nvo_categoria
            if nvo_stock == "":
                stock_query = old_stock
            else:
                stock_query = nvo_stock
            parametros = (nombre_query, precio_query, categoria_query, stock_query, id)

        if producto_modificado:
            self.db_consulta(query, parametros)
            self.ventana_editar.destroy()
            self.mensaje["text"] = "El producto {} ha sido actualizado con éxito".format(old_nombre)
            self.get_productos()
        else:
            self.ventana_editar.destroy()
            self.mensaje["text"] = "El producto {} NO ha sido actualizado".format(old_nombre)


if __name__ == '__main__':
    root = Tk()
    app = Producto(root)
    root.mainloop()
