import tkinter as tk
import ttkbootstrap as ttk 
from ttkbootstrap.constants import *
from src.controllers.crud import ControladorMemoriaCRUD
from src.views.generico import VistaGenericaCRUD

def main():
    pantalla = ttk.Window(
        title="Sistema CRUD Genérico - Módulo Múltiple - Edición Rosario",
        themename="darkly",
        size=(1000, 650),
        minsize=(800, 550)
    )
    pestañas = ttk.Notebook(pantalla, bootstyle="dark")
    pestañas.pack(fill="both", expand=True, padx=10, pady=10)

    #Vehiculos
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
    pestañas.add(vista_vehiculos, text=" 🚗 VEHÍCULOS ")

    #Propietarios
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
    pestañas.add(vista_propietarios, text=" 👤 PROPIETARIOS ")
    pantalla.mainloop()

if __name__ == "__main__":
    main()