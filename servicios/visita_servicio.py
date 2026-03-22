from modelos.visitante import Visitante
from typing import List, Optional

class VisitaServicio:

    def __init__(self):
        # Lista que almacena los visitantes en memoria
        self._lista_visitantes: List[Visitante] = []

    def registrar_visitante(self, visitante: Visitante) -> None:

        cedula = visitante.cedula.strip()

        if self._buscar_por_cedula(cedula):
            raise ValueError(f"La cédula {cedula} ya se encuentra registrada.")

        self._lista_visitantes.append(visitante)


    def obtener_todos(self) -> List[Visitante]:
        return sorted(self._lista_visitantes, key=lambda v: v.nombre)


    def actualizar_visitante(self, visitante_actualizado: Visitante) -> None:

        cedula = visitante_actualizado.cedula.strip()

        for indice, visitante in enumerate(self._lista_visitantes):

            if visitante.cedula.strip() == cedula:
                self._lista_visitantes[indice] = visitante_actualizado
                return

        raise ValueError("No fue posible actualizar porque el visitante no existe.")


    def eliminar_visitante(self, cedula: str) -> None:

        cedula = cedula.strip()

        visitante = self._buscar_por_cedula(cedula)

        if visitante:
            self._lista_visitantes.remove(visitante)
        else:
            raise ValueError("No se encontró un visitante con esa cédula.")


    def _buscar_por_cedula(self, cedula: str) -> Optional[Visitante]:

        cedula = cedula.strip()

        for visitante in self._lista_visitantes:
            if visitante.cedula.strip() == cedula:
                return visitante

        return None