# views/planes_view.py

import tkinter as tk
from typing import Any
from tkinter import ttk, messagebox
from controllers.planes_controller import registrar_plan, listar_planes, borrar_plan

def abrir_planes(frame_contenido):
    # Limpia el contenido
    for widget in frame_contenido.winfo_children():
        widget.destroy()

    tk.Label(frame_contenido, text="Gestión de Planes", font=("Arial", 16, "bold")).pack(pady=10)

    # Frame formulario
    frame_form = tk.Frame(frame_contenido)
    frame_form.pack(pady=10)

    tk.Label(frame_form, text="Nombre:").grid(row=0, column=0, sticky="e")
    entry_nombre = tk.Entry(frame_form)
    entry_nombre.grid(row=0, column=1)

    tk.Label(frame_form, text="Descripción:").grid(row=1, column=0, sticky="e")
    entry_desc = tk.Entry(frame_form)
    entry_desc.grid(row=1, column=1)

    tk.Label(frame_form, text="Precio:").grid(row=2, column=0, sticky="e")
    entry_precio = tk.Entry(frame_form)
    entry_precio.grid(row=2, column=1)
    def formatear_precio(event=None):
        texto = entry_precio.get()
        texto = "".join(c for c in texto if c.isdigit())  # elimina letras y símbolos
        if texto:
            texto_formateado = "{:,}".format(int(texto)).replace(",", ".")
            entry_precio.delete(0, tk.END)
            entry_precio.insert(0, texto_formateado)

    entry_precio.bind("<KeyRelease>", formatear_precio)


    tk.Label(frame_form, text="Sesiones:").grid(row=3, column=0, sticky="e")
    entry_sesiones = tk.Entry(frame_form)
    entry_sesiones.grid(row=3, column=1)

    def agregar():
        try:
            nombre = entry_nombre.get().strip()
            desc = entry_desc.get().strip()
            precio = int(entry_precio.get().replace(".", ""))
            sesiones = int(entry_sesiones.get())

            registrar_plan(nombre, desc, precio, sesiones)

            messagebox.showinfo("Éxito", "Plan agregado correctamente.")
            actualizar_tabla()
            entry_nombre.delete(0, tk.END)
            entry_desc.delete(0, tk.END)
            entry_precio.delete(0, tk.END)
            entry_sesiones.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(frame_form, text="Agregar plan", command=agregar).grid(row=4, column=0, columnspan=2, pady=10)

    # Tabla
    tree = ttk.Treeview(frame_contenido, columns=("ID", "Nombre", "Precio", "Sesiones"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Precio", text="Precio")
    tree.heading("Sesiones", text="Sesiones")
    tree.column("ID", width=40)
    tree.column("Nombre", width=150)
    tree.column("Precio", width=100)
    tree.column("Sesiones", width=80)
    tree.pack(pady=10)

    def actualizar_tabla():
        for row in tree.get_children():
            tree.delete(row)
        for plan in listar_planes():
            plan:Any
            tree.insert("", tk.END, values=(plan["id"], plan["nombre"], plan["precio"], plan["sesiones"]))

    def eliminar():
        seleccionado = tree.selection()
        if not seleccionado:
            messagebox.showwarning("Seleccioná", "Seleccioná un plan para eliminar.")
            return

        valores = tree.item(seleccionado[0])["values"]
        plan_id = valores[0]

        if messagebox.askyesno("Confirmar", "¿Seguro que querés eliminar este plan?"):
            borrar_plan(plan_id)
            actualizar_tabla()

    def editar_precio():
        seleccionado = tree.selection()
        if not seleccionado:
            messagebox.showwarning("Seleccioná", "Seleccioná un plan para editar precio.")
            return

        valores = tree.item(seleccionado[0])["values"]
        plan_id, nombre, precio_actual, sesiones = valores

        popup = tk.Toplevel()
        popup.title("Editar precio")
        tk.Label(popup, text=f"Plan: {nombre}").pack(pady=5)
        entry_nuevo_precio = tk.Entry(popup)
        entry_nuevo_precio.insert(0, str(precio_actual))
        entry_nuevo_precio.pack(pady=5)

        def confirmar():
            try:
                nuevo_precio = float(entry_nuevo_precio.get())
                from models.db import conectar
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("UPDATE planes SET precio = %s WHERE id = %s", (nuevo_precio, plan_id))
                conn.commit()
                conn.close()
                popup.destroy()
                actualizar_tabla()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(popup, text="Actualizar", command=confirmar).pack(pady=10)

    tk.Button(frame_contenido, text="Eliminar plan", command=eliminar).pack(pady=5)
    tk.Button(frame_contenido, text="Editar precio", command=editar_precio).pack(pady=5)

    actualizar_tabla()
