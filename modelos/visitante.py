class Visitante:
    def __init__(self, cedula: str, nombre: str, motivo: str):
       
        self.cedula = cedula
        self.nombre = nombre
        self.motivo = motivo
    
    @property
    def cedula(self) -> str:
        return self._cedula

    @cedula.setter
    def cedula(self, value: str):
        # Validación: La cédula es obligatoria
        if not value or not value.strip():
            raise ValueError("Debe ingresar su número de cédula.")
        self._cedula = value.strip()

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, value: str):
        # Validación: El nombre es obligatorio
        if not value or not value.strip():
            raise ValueError("Debe ingresar su nombre.")
        self._nombre = value.strip()

    @property
    def motivo(self) -> str:
        return self._motivo

    @motivo.setter
    def motivo(self, value: str):
        # Validación: El motivo es obligatorio
        if not value or not value.strip():
            raise ValueError("Debe ingresar el motivo de la visita.")
        self._motivo = value.strip()