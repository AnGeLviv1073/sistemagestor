import tkinter as tk
from tkinter import ttk, messagebox

def mostrar_gestor(conn):
    ventana = tk.Tk()
    ventana.title("Gestor de Base de Datos")
    ventana.geometry("900x500")

    # --- Frame izquierdo: Tablas
    frame_tablas = tk.Frame(ventana)
    frame_tablas.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    tk.Label(frame_tablas, text="Tablas:").pack()
    lista_tablas = tk.Listbox(frame_tablas, width=25)
    lista_tablas.pack(fill=tk.BOTH, expand=True)

    # --- Frame central: Consulta
    frame_consulta = tk.Frame(ventana)
    frame_consulta.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

    texto_sql = tk.Text(frame_consulta, height=4, width=80)
    texto_sql.pack()

    # --- Frame inferior: Resultados
    frame_resultado = tk.Frame(ventana)
    frame_resultado.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    resultado = ttk.Treeview(frame_resultado)
    resultado.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scroll_y = ttk.Scrollbar(frame_resultado, orient="vertical", command=resultado.yview)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    resultado.configure(yscrollcommand=scroll_y.set)

    # --- Función: cargar nombres de tabla
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    for tabla in cursor.fetchall():
        lista_tablas.insert(tk.END, tabla[0])

    # --- Función: al seleccionar tabla, mostrar columnas
    def mostrar_columnas(event):
        seleccion = lista_tablas.curselection()
        if seleccion:
            nombre_tabla = lista_tablas.get(seleccion)
            query = f"SELECT * FROM `{nombre_tabla}` LIMIT 100"
            texto_sql.delete("1.0", tk.END)
            texto_sql.insert(tk.END, query)
            ejecutar_consulta(query)

    lista_tablas.bind("<<ListboxSelect>>", mostrar_columnas)

    # --- Función: ejecutar consulta
    def ejecutar_consulta(query=None):
        query = query or texto_sql.get("1.0", tk.END).strip()
        if not query:
            messagebox.showwarning("Consulta vacía", "Por favor, ingresa una consulta SQL.")
            return

        try:
            cursor.execute(query)
            if cursor.description:
                columnas = [desc[0] for desc in cursor.description]
                resultado.delete(*resultado.get_children())
                resultado["columns"] = columnas
                resultado["show"] = "headings"
                for col in columnas:
                    resultado.heading(col, text=col)
                    resultado.column(col, width=100, anchor=tk.W)
                for fila in cursor.fetchall():
                    resultado.insert("", tk.END, values=fila)
            else:
                conn.commit()
                messagebox.showinfo("Éxito", "Consulta ejecutada correctamente.")
        except Exception as e:
            messagebox.showerror("Error al ejecutar la consulta", str(e))

    tk.Button(frame_consulta, text="Ejecutar consulta", command=ejecutar_consulta).pack(pady=5)

    ventana.mainloop()
