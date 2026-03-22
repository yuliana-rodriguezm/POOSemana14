import tkinter as tk
from tkinter import ttk, messagebox
from modelos.visitante import Visitante

class AppVisitas(tk.Tk):

    def __init__(self, servicio):
        super().__init__()

        # Servicio que maneja la lógica del CRUD
        self.servicio = servicio

        # Guarda la cédula del visitante seleccionado en la tabla
        self._cedula_seleccionada = None

        # Configuración general de la ventana
        self.title("SISTEMA DE REGISTRO DE VISITANTES")
        self.geometry("750x450")
        self.configure(bg="#24d5db")

        # Métodos que construyen la interfaz
        self._aplicar_estilos()
        self._configurar_interfaz()
        self._actualizar_tabla()

    def _aplicar_estilos(self):
        style = ttk.Style(self)
        style.theme_use('clam')

        # Apariencia de la tabla
        style.configure("Treeview",
                        background="#ffb2cf",
                        foreground="#000000",
                        rowheight=25)

        style.configure("Treeview.Heading",
                        font=("Arial", 10, "bold"),
                        background="#62f5ffd3")

        style.map('Treeview', background=[('selected', '#4a90e2')])

        # Estilos personalizados para botones
        style.configure("Guardar.TButton",
                        font=("Arial", 10, "bold"),
                        background="#0EBE14",
                        foreground="white",
                        padding=5)

        style.configure("Actualizar.TButton",
                        font=("Arial", 10, "bold"),
                        background="#3583C2",
                        foreground="white",
                        padding=5)

        style.configure("Eliminar.TButton",
                        font=("Arial", 10, "bold"),
                        background="#AA2652",
                        foreground="white",
                        padding=5)

        style.configure("Limpiar.TButton",
                        font=("Arial", 10, "bold"),
                        background="#a70808",
                        foreground="white",
                        padding=5)

    def _configurar_interfaz(self):

        # FORMULARIO 
        frame_form = tk.Frame(self, bg="#24d5db")
        frame_form.pack(pady=15, padx=20, fill="x")

        tk.Label(frame_form, text="Cédula:",
                 bg="#24d5db",
                 font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.ent_cedula = ttk.Entry(frame_form, width=20)
        self.ent_cedula.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Nombre:",
                 bg="#24d5db",
                 font=("Arial", 10)).grid(row=0, column=2, padx=5, pady=5, sticky="w")

        self.ent_nombre = ttk.Entry(frame_form, width=35)
        self.ent_nombre.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_form, text="Motivo:",
                 bg="#24d5db",
                 font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.ent_motivo = ttk.Entry(frame_form, width=64)
        self.ent_motivo.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="w")

        # ===== BOTONES =====
        frame_btns = tk.Frame(self, bg="#24d5db")
        frame_btns.pack(pady=5, padx=20, fill="x")

        ttk.Button(frame_btns,
                   text="Registrar",
                   style="Guardar.TButton",
                   command=self._registrar).pack(side=tk.LEFT, padx=5)

        ttk.Button(frame_btns,
                   text="Editar",
                   style="Actualizar.TButton",
                   command=self._actualizar).pack(side=tk.LEFT, padx=5)

        ttk.Button(frame_btns,
                   text="Eliminar",
                   style="Eliminar.TButton",
                   command=self._eliminar).pack(side=tk.LEFT, padx=5)

        ttk.Button(frame_btns,
                   text="Limpiar campos",
                   style="Limpiar.TButton",
                   command=self._limpiar_campos).pack(side=tk.RIGHT, padx=5)

        # TABLA
        frame_tabla = tk.Frame(self)
        frame_tabla.pack(pady=10, padx=20, fill="both", expand=True)

        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=("Cédula", "Nombre", "Motivo"),
            show='headings'
        )

        self.tabla.heading("Cédula", text="Cédula")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Motivo", text="Motivo")

        # Evento cuando se selecciona una fila
        self.tabla.bind("<<TreeviewSelect>>", self._seleccionar_fila)

        self.tabla.pack(fill="both", expand=True)

    # EVENTOS DE LA INTERFAZ
    def _seleccionar_fila(self, event):

        seleccion = self.tabla.selection()

        if seleccion:
            item = self.tabla.item(seleccion[0])
            valores = item['values']

            self._limpiar_campos()

            # Guarda la cédula del visitante seleccionado
            self._cedula_seleccionada = str(valores[0])

            self.ent_cedula.insert(0, valores[0])
            self.ent_nombre.insert(0, valores[1])
            self.ent_motivo.insert(0, valores[2])

            # La cédula no debe modificarse al editar
            self.ent_cedula.config(state="disabled")

    def _registrar(self):

        cedula = self.ent_cedula.get().strip()
        nombre = self.ent_nombre.get().strip()
        motivo = self.ent_motivo.get().strip()

        if not cedula or not nombre or not motivo:
            messagebox.showwarning(
                "Campos incompletos",
                "Por favor, complete todos los campos para registrar su visita."
            )
            return
        try:
            nuevo = Visitante(cedula, nombre, motivo)

            self.servicio.registrar_visitante(nuevo)

            self._actualizar_tabla()
            self._limpiar_campos()

            messagebox.showinfo(
                "Registro guardado",
                "Fue agregado correctamente como visitante."
            )

        except ValueError as e:
            messagebox.showwarning("Datos incorrectos", str(e))

    def _actualizar(self):

        if not self._cedula_seleccionada:
            messagebox.showwarning(
                "Selección requerida",
                "Debe elegir un visitante de la tabla."
            )
            return

        nombre = self.ent_nombre.get().strip()
        motivo = self.ent_motivo.get().strip()

        try:
            visitante_editado = Visitante(
                self._cedula_seleccionada,
                nombre,
                motivo
            )

            self.servicio.actualizar_visitante(visitante_editado)

            self._actualizar_tabla()
            self._limpiar_campos()

            messagebox.showinfo(
                "Actualización",
                "La información del visitante fue modificada."
            )

        except ValueError as e:
            messagebox.showwarning("Error", str(e))

    def _eliminar(self):

        if not self._cedula_seleccionada:
            messagebox.showwarning(
                "Selección requerida",
                "Primero seleccione un visitante."
            )
            return

        respuesta = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Desea eliminar al visitante con cédula {self._cedula_seleccionada}?"
        )

        if respuesta:
            try:
                self.servicio.eliminar_visitante(self._cedula_seleccionada)

                self._actualizar_tabla()
                self._limpiar_campos()

                messagebox.showinfo(
                    "Eliminado",
                    "El visitante fue removido del registro."
                )

            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def _actualizar_tabla(self):

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for v in self.servicio.obtener_todos():
            self.tabla.insert("", tk.END,
                              values=(v.cedula, v.nombre, v.motivo))

    def _limpiar_campos(self):

        self._cedula_seleccionada = None

        self.ent_cedula.config(state="normal")
        self.ent_cedula.delete(0, tk.END)
        self.ent_nombre.delete(0, tk.END)
        self.ent_motivo.delete(0, tk.END)