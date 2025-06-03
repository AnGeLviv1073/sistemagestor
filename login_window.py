import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from db_connector import conectar_bd
from db_window import mostrar_gestor

def crear_login():
    root = tk.Tk()
    root.title("Gestor de Base de Datos")
    root.geometry("400x500")
    root.resizable(False, False)
    root.configure(bg="#0B2E6B")  # Fondo negro

    # Centrar ventana
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (400 // 2)
    y = (root.winfo_screenheight() // 2) - (500 // 2)
    root.geometry(f"+{x}+{y}")

    # Marco principal con fondo negro
    frame = tk.Frame(root, bg="#0B2E6B")
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Imagen centrada
    try:
        imagen_original = Image.open("imagen.png")
        imagen_redimensionada = imagen_original.resize((100, 100))
        logo = ImageTk.PhotoImage(imagen_redimensionada)

        img_label = tk.Label(frame, image=logo, bg="#0B2E6B")
        img_label.image = logo
        img_label.grid(row=0, column=0, columnspan=2, pady=(10, 10))
    except Exception as e:
        print("Error al cargar imagen:", e)

    # Título
    titulo = tk.Label(frame, text="Iniciar sesión", font=("Helvetica", 18, "bold"), bg="#0B2E6B", fg="white")
    titulo.grid(row=1, column=0, columnspan=2, pady=(0, 20))

    # Etiquetas
    style_label = {"font": ("Helvetica", 12), "bg": "#0B2E6B", "fg": "white"}
    tk.Label(frame, text="Usuario:", **style_label).grid(row=2, column=0, sticky="e", pady=5, padx=5)
    tk.Label(frame, text="Contraseña:", **style_label).grid(row=3, column=0, sticky="e", pady=5, padx=5)
    tk.Label(frame, text="Base de datos:", **style_label).grid(row=4, column=0, sticky="e", pady=5, padx=5)

    # Entradas de texto estilo oscuro
    style_entry = {"font": ("Helvetica", 12), "bg": "#222222", "fg": "white", "insertbackground": "white"}
    entry_user = tk.Entry(frame, **style_entry)
    entry_pass = tk.Entry(frame, show="*", **style_entry)
    entry_db = tk.Entry(frame, **style_entry)

    entry_user.grid(row=2, column=1, pady=5, padx=5)
    entry_pass.grid(row=3, column=1, pady=5, padx=5)
    entry_db.grid(row=4, column=1, pady=5, padx=5)

    # Botón conectar
    def intentar_conexion():
        usuario = entry_user.get()
        clave = entry_pass.get()
        base_datos = entry_db.get()
        conn = conectar_bd(usuario, clave, base_datos)
        if conn:
            root.destroy()
            mostrar_gestor(conn)
        else:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.\nVerifica tus credenciales.")

    btn = tk.Button(
        frame,
        text="Conectar",
        font=("Helvetica", 12, "bold"),
        bg="#1DB954",  # Verde Spotify
        fg="black",
        width=15,
        command=intentar_conexion
    )
    btn.grid(row=5, column=0, columnspan=2, pady=20)

    root.mainloop()
