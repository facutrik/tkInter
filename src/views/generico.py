# src/views/generic_view.py

import tkinter as tk
from tkinter import ttk, messagebox

class VistaGenericaCRUD(ttk.Frame):
    def __init__(self, parent, nombre_entidad, clave_primaria, campos, controlador):
        super().__init__(parent)
        self.nombre_entidad = nombre_entidad
        self.clave_primaria = clave_primaria
        self.campos = campos  # Lista de tuplas: [("clave_campo", "Etiqueta Visible")]
        self.controlador = controlador
        
        # Diccionario para almacenar las referencias a los Entry
        self.entradas = {}
        self.clave_seleccionada = None

        self._construir_interfaz()
        self._actualizar_tabla()

    def _construir_interfaz(self):
        # 1. Encabezado
        titulo = ttk.Label(self, text=f"Gestión de {self.nombre_entidad}", font=("Arial", 14, "bold"))
        titulo.pack(pady=10)

        # 2. Formulario Generado Dinámicamente (Mediante un bucle for)
        marco_formulario = ttk.LabelFrame(self, text=" Datos del Registro ")
        marco_formulario.pack(fill="x", padx=15, pady=5)

        for i, (clave, etiqueta) in enumerate(self.campos):
            lbl = ttk.Label(marco_formulario, text=f"{etiqueta}:")
            lbl.grid(row=i, column=0, sticky="e", padx=5, pady=5)

            entrada = ttk.Entry(marco_formulario, width=30)
            entrada.grid(row=i, column=1, sticky="w", padx=5, pady=5)

            # Guardamos la referencia en el diccionario con la clave del campo
            self.entradas[clave] = entrada

        # 3. Botones del CRUD
        marco_botones = ttk.Frame(self)
        marco_botones.pack(pady=10)

        ttk.Button(marco_botones, text="Crear", command=self._al_crear).grid(row=0, column=0, padx=5)
        ttk.Button(marco_botones, text="Actualizar", command=self._al_actualizar).grid(row=0, column=1, padx=5)
        ttk.Button(marco_botones, text="Eliminar", command=self._al_eliminar).grid(row=0, column=2, padx=5)
        ttk.Button(marco_botones, text="Limpiar", command=self.limpiar_campos).grid(row=0, column=3, padx=5)

        # 4. Tabla de Visualización (Treeview)
        marco_tabla = ttk.Frame(self)
        marco_tabla.pack(fill="both", expand=True, padx=15, pady=10)

        columnas = [campo[0] for campo in self.campos]
        self.tabla = ttk.Treeview(marco_tabla, columns=columnas, show="headings", height=8)

        for clave, etiqueta in self.campos:
            self.tabla.heading(clave, text=etiqueta)
            self.tabla.column(clave, width=120, anchor="center")

        self.tabla.pack(side="left", fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self._al_seleccionar_fila)

        barra_desplazamiento = ttk.Scrollbar(marco_tabla, orient="vertical", command=self.tabla.yview)
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

    # --- Eventos y Manejo de Errores ---

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
        # Escenario de Error: Intento de actualizar sin selección en la tabla
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
        # Escenario de Error: Intento de eliminar sin selección en la tabla
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