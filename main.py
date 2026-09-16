# main.py

import tkinter as tk
from tkinter import ttk

from src.controllers.crud_controller import ControladorMemoriaCRUD
from src.views.generic_view import VistaGenericaCRUD

def main():
    pantalla = tk.Tk()
    pantalla.title("Sistema CRUD Genérico - Módulo Múltiple")
    pantalla.geometry("600x550")
    pantalla.minsize(550, 500)

    pestañas = ttk.Notebook(pantalla)
    pestañas.pack(fill="both", expand=True)

    # --- INSTANCIACIÓN 1: VEHÍCULOS ---
    campos_vehiculos = [
        ("patente", "Patente / Dominio"),
        ("marca", "Marca"),
        ("modelo", "Modelo"),
        ("anio", "Año")
    ]
    controlador_vehiculos = ControladorMemoriaCRUD(clave_primaria="patente")
    vista_vehiculos = VistaGenericaCRUD(
        parent=pestañas,
        nombre_entidad="Vehículos",
        clave_primaria="patente",
        campos=campos_vehiculos,
        controlador=controlador_vehiculos
    )
    pestañas.add(vista_vehiculos, text="Vehículos")

    # --- INSTANCIACIÓN 2: PROPIETARIOS ---
    campos_propietarios = [
        ("dni", "DNI / CUIT"),
        ("nombre", "Nombre Completo"),
        ("telefono", "Teléfono"),
        ("email", "Correo Electrónico")
    ]
    controlador_propietarios = ControladorMemoriaCRUD(clave_primaria="dni")
    vista_propietarios = VistaGenericaCRUD(
        parent=pestañas,
        nombre_entidad="Propietarios",
        clave_primaria="dni",
        campos=campos_propietarios,
        controlador=controlador_propietarios
    )
    pestañas.add(vista_propietarios, text="Propietarios")

    pantalla.mainloop()

if __name__ == "__main__":
    main()