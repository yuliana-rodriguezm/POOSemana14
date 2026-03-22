from servicios.visita_servicio import VisitaServicio
from ui.app_tkinter import AppVisitas

def main():
    servicio = VisitaServicio()
    app = AppVisitas(servicio)
    app.mainloop()

if __name__ == "__main__":
    main()
