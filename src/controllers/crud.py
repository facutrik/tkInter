# src/controllers/crud.py

class ControladorMemoriaCRUD:
    def __init__(self, clave_primaria):
        self.clave_primaria = clave_primaria
        self.datos = []

    def _validar_datos(self, registro: dict):
        # 1. Campos vacíos
        for clave, valor in registro.items():
            if not valor:
                raise ValueError(f"El campo '{clave}' no puede estar vacío.")

        # 2. Vehículos - Año: solo números y 4 dígitos
        if "anio" in registro:
            anio = registro["anio"].strip()
            if not anio.isdigit():
                raise ValueError("El Año del vehículo debe contener únicamente números.")
            if len(anio) != 4:
                raise ValueError("El Año del vehículo debe tener exactamente 4 dígitos (ej: 2022).")

        # 3. Propietarios - DNI: solo números y al menos 7 dígitos
        if "dni" in registro:
            dni = registro["dni"].strip()
            if not dni.isdigit() or len(dni) < 7:
                raise ValueError("El DNI debe contener únicamente números y tener al menos 7 dígitos.")

        # 4. Propietarios - Nombre: al menos dos palabras
        if "nombre" in registro:
            palabras = [p for p in registro["nombre"].strip().split() if p]
            if len(palabras) < 2:
                raise ValueError("El Nombre Completo debe contener al menos dos palabras (nombre y apellido).")

        # 5. Propietarios - Teléfono: solo números
        if "telefono" in registro:
            telefono = registro["telefono"].strip()
            if not telefono.isdigit():
                raise ValueError("El Teléfono debe contener únicamente números.")

        # 6. Propietarios - Correo: contener @ y terminar en .com
        if "email" in registro:
            email = registro["email"].strip().lower()
            if "@" not in email or not email.endswith(".com"):
                raise ValueError("El Correo Electrónico debe incluir '@' y terminar en '.com'.")

    def crear(self, registro: dict):
        self._validar_datos(registro)

        valor_clave = registro.get(self.clave_primaria)
        if any(item[self.clave_primaria] == valor_clave for item in self.datos):
            raise ValueError(f"Ya existe un registro con {self.clave_primaria} = {valor_clave}.")

        self.datos.append(registro)
        return True

    def actualizar(self, valor_clave, registro_actualizado: dict):
        self._validar_datos(registro_actualizado)

        for i, item in enumerate(self.datos):
            if item[self.clave_primaria] == valor_clave:
                self.datos[i] = registro_actualizado
                return True
        raise ValueError("No se encontró el registro para actualizar.")

    def eliminar(self, valor_clave):
        for i, item in enumerate(self.datos):
            if item[self.clave_primaria] == valor_clave:
                del self.datos[i]
                return True
        raise ValueError("No se encontró el registro para eliminar.")

    def obtener_todos(self):
        return self.datos