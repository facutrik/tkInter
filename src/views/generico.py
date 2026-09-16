import tkinter as tk
import ttkbootstrap as ttk 
from ttkbootstrap.constants import *
from tkinter import messagebox

class VistaGenericaCRUD(ttk.Frame):
    def __init__(self, parent, nombre_entidad, clave_primaria, campos, controlador):
        super().__init__(parent, padding=15)
        self.nombre_entidad = nombre_entidad
        self.clave_primaria = clave_primaria
        self.campos = campos
        self.controlador = controlador
        self.entradas = {}
        self.clave_seleccionada = None
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(1, weight=1)
        self._construir_interfaz()
        self._actualizar_tabla()

    def _construir_interfaz(self):
        titulo_frame = ttk.Frame(self)
        titulo_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        ttk.Label(
            titulo_frame, 
            text=f"Gestión de {self.nombre_entidad}", 
            font=("Helvetica", 18, "bold"),
            bootstyle="primary"
        ).pack(side="left")
        #2 Formulario y Botones
        marco_izquierdo = ttk.Frame(self)
        marco_izquierdo.grid(row=1, column=0, sticky="nsew", padx=(0, 15))
        marco_formulario = ttk.LabelFrame(marco_izquierdo, text=" Datos del Registro ", padding=10, bootstyle="info")
        marco_formulario.pack(fill="x", pady=(0, 15))
        for i, (clave, etiqueta) in enumerate(self.campos):
            lbl = ttk.Label(marco_formulario, text=f"{etiqueta}:")
            lbl.grid(row=i*2, column=0, sticky="w", padx=5, pady=(5, 0))
            entrada = ttk.Entry(marco_formulario)
            entrada.grid(row=i*2+1, column=0, sticky="ew", padx=5, pady=(0, 10))
            self.entradas[clave] = entrada
        marco_formulario.columnconfigure(0, weight=1)
        #3 Botones del CRUD
        marco_botones = ttk.LabelFrame(marco_izquierdo, text=" Acciones ", padding=10, bootstyle="secondary")
        marco_botones.pack(fill="x")
        # Botones
        for c in range(2): marco_botones.columnconfigure(c, weight=1)
        ttk.Button(marco_botones, text="Crear", bootstyle="success", command=self._al_crear).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ttk.Button(marco_botones, text="Actualizar", bootstyle="info", command=self._al_actualizar).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(marco_botones, text="Eliminar", bootstyle="danger", command=self._al_eliminar).grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        ttk.Button(marco_botones, text="Limpiar", bootstyle="secondary-outline", command=self.limpiar_campos).grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        #4 Tabla de Visualización
        marco_tabla = ttk.LabelFrame(self, text=" TABLA DE REGISTROS ", padding=5, bootstyle="primary")
        marco_tabla.grid(row=1, column=1, sticky="nsew")
        columnas = [campo[0] for campo in self.campos]
        self.tabla = ttk.Treeview(marco_tabla, columns=columnas, show="headings", bootstyle="primary", selectmode="browse")
        for clave, etiqueta in self.campos:
            self.tabla.heading(clave, text=etiqueta.upper())
            self.tabla.column(clave, anchor="center")
        self.tabla.pack(side="left", fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self._al_seleccionar_fila)
        barra_desplazamiento = ttk.Scrollbar(marco_tabla, orient="vertical", command=self.tabla.yview, bootstyle="primary-round")
        self.tabla.configure(yscrollcommand=barra_desplazamiento.set)
        barra_desplazamiento.pack(side="right", fill="y")

    def obtener_datos(self):
        """Lectura limpia de datos accediendo al diccionario de entradas."""
        return {clave: entrada.get().strip() for clave, entrada in self.entradas.items()}

    def limpiar_campos(self):
        """Limpieza mediante iteración del diccionario."""
        for entrada in self.entradas.values():
            entrada.delete(0, tk.END)
        self.clave_seleccionada = None
        if self.tabla.selection():
            self.tabla.selection_remove(self.tabla.selection())

    def _actualizar_tabla(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        for registro in self.controlador.obtener_todos():
            valores = [registro[campo[0]] for campo in self.campos]
            self.tabla.insert("", "end", values=valores)

    def _al_seleccionar_fila(self, evento):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        item = self.tabla.item(seleccion[0])
        valores = item["values"]
        for i, (clave, _) in enumerate(self.campos):
            self.entradas[clave].delete(0, tk.END)
            self.entradas[clave].insert(0, str(valores[i]))
            if clave == self.clave_primaria:
                self.clave_seleccionada = str(valores[i])

    def _al_crear(self):
        datos = self.obtener_datos()
        try:
            self.controlador.crear(datos)
            self._actualizar_tabla()
            self.limpiar_campos()
            messagebox.showinfo("Éxito", "Registro creado correctamente.")
        except ValueError as error:
            messagebox.showwarning("Atención", str(error))

    def _al_actualizar(self):
        if self.clave_seleccionada is None:
            messagebox.showerror("Error de Selección", "Debe seleccionar un registro de la tabla para actualizar.")
            return
        datos = self.obtener_datos()
        try:
            self.controlador.actualizar(self.clave_seleccionada, datos)
            self._actualizar_tabla()
            self.limpiar_campos()
            messagebox.showinfo("Éxito", "Registro actualizado correctamente.")
        except ValueError as error:
            messagebox.showwarning("Atención", str(error))

    def _al_eliminar(self):
        if self.clave_seleccionada is None:
            messagebox.showerror("Error de Selección", "Debe seleccionar un registro de la tabla para eliminar.")
            return
        try:
            self.controlador.eliminar(self.clave_seleccionada)
            self._actualizar_tabla()
            self.limpiar_campos()
            messagebox.showinfo("Éxito", "Registro eliminado correctamente.")
        except ValueError as error:
            messagebox.showwarning("Atención", str(error))