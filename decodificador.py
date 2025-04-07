import customtkinter as ctk
from tkinter import filedialog, messagebox


ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("blue")  


diccionario = {
    "ADD": "00",
    
}

def instruccion_a_binario(numero):
    return f"{int(numero):05b}"

def seleccionar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos ASM", "*.asm")])
    if archivo:
        entry_path.delete(0, ctk.END)
        entry_path.insert(0, archivo)
        mostrar_contenido(archivo)

def mostrar_contenido(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read()
        text_area.delete("1.0", ctk.END)
        text_area.insert(ctk.END, contenido)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo leer el archivo\n{e}")

def convertir_a_binario():
    ruta = entry_path.get()
    if not ruta:
        messagebox.showwarning("Atención", "Selecciona un archivo primero")
        return

    try:
        with open(ruta, "r", encoding="utf-8") as f:
            lineas = f.readlines()
        
        resultados = []
        
        for linea in lineas:
            linea = linea.strip()
            if not linea:
                continue

            partes = linea.split()
            instruccion = partes[0].upper()
            if instruccion in diccionario:
                opcode = diccionario[instruccion]
                registros = [instruccion_a_binario(p.replace("$", "")) for p in partes[1:]]
                binario_completo = opcode + ''.join(registros)
                binario_completo = binario_completo.ljust(32, '0')
                partes_bin = [binario_completo[i:i+8] for i in range(0, 32, 8)]
                resultado_final = "_".join(partes_bin)
                resultados.append(resultado_final)

        ruta_salida = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivo Binario", "*.txt")])
        if ruta_salida:
            with open(ruta_salida, "w", encoding="utf-8") as f:
                f.write("\n".join(resultados))
            messagebox.showinfo("Éxito", f"Archivo binario guardado en:\n{ruta_salida}")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo procesar el archivo\n{e}")



root = ctk.CTk()
root.title("🛠️ Conversor ASM a Binario")
root.geometry("600x500")

frame = ctk.CTkFrame(master=root)
frame.pack(padx=20, pady=20, fill="both", expand=True)

label = ctk.CTkLabel(frame, text="Selecciona un archivo ASM", font=ctk.CTkFont(size=16))
label.pack(pady=(10, 5))

entry_path = ctk.CTkEntry(frame, width=400)
entry_path.pack(pady=5)

btn_select = ctk.CTkButton(frame, text="📂 Buscar", command=seleccionar_archivo)
btn_select.pack(pady=5)

text_area = ctk.CTkTextbox(frame, height=200)
text_area.pack(padx=10, pady=10, fill="both", expand=True)

btn_convert = ctk.CTkButton(frame, text="🔁 Convertir a Binario", command=convertir_a_binario)
btn_convert.pack(pady=10)

root.mainloop()
