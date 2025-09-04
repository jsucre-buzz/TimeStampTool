"""
TimeStamp Tool
Autor: José Sucre
E-Mail: josemsucre@gmail.com
Licencia: MIT License
Año: 2025

Este software permite modificar la fecha de archivos y carpetas en Windows.

Donaciones: si este programa te resulta útil, puedes invitarme un café en:
[tu enlace de PayPal / BuyMeACoffee / Ko-fi]
"""
import tkinter as tk
import webbrowser
from tkinter import filedialog
from tkcalendar import Calendar
from datetime import datetime
import os
import random

# Funktion zum Ändern des Zugriffs- und Änderungsdatums der Datei oder des Ordners
ruta_seleccionada = None  # variable global

def ändere_daten():
    global ruta_seleccionada
    auswahl = auswahl_var.get()
    if auswahl == "Archivo":
        datei = filedialog.askopenfilename()
        if datei:
            ruta_seleccionada = datei
            ausgewählte_datei_label.config(text=f"Archivo seleccionado: {acortar_ruta(datei)}")
            bestätigen_button.config(state=tk.NORMAL)
        else:
            ausgewählte_datei_label.config(text="No se ha seleccionado ningún archivo.")
            bestätigen_button.config(state=tk.DISABLED)
    elif auswahl == "Cambiar el contenido de la carpeta":
        ordner = filedialog.askdirectory()
        if ordner:
            ruta_seleccionada = ordner
            ausgewählte_datei_label.config(text=f"Carpeta seleccionada: {acortar_ruta(ordner)}")
            bestätigen_button.config(state=tk.NORMAL)
        else:
            ausgewählte_datei_label.config(text="No se ha seleccionado ninguna carpeta.")
            bestätigen_button.config(state=tk.DISABLED)


# Funktion zum Generieren einer zufälligen Uhrzeit im Format HH:MM:SS
def generiere_zufällige_zeit():
    stunde = random.randint(7, 16)
    minute = random.randint(0, 59)
    sekunde = random.randint(0, 59)
    return f"{stunde:02}:{minute:02}:{sekunde:02}"

# Funktion zum Bestätigen und Durchführen der Datums- und Uhrzeitänderung
def bestätige_änderung():
    global ruta_seleccionada
    datum = kalender.get_date()
    zufällige_zeit = generiere_zufällige_zeit()
    neues_datum_uhrzeit = f"{datum} {zufällige_zeit}"
    
    try:
        neues_datum_uhrzeit_datetime = datetime.strptime(neues_datum_uhrzeit, "%d.%m.%Y %H:%M:%S")
        neuer_zeitstempel = neues_datum_uhrzeit_datetime.timestamp()
        
        pfad = ruta_seleccionada
        auswahl = auswahl_var.get()
        
        if os.path.isfile(pfad):
            os.utime(pfad, (neuer_zeitstempel, neuer_zeitstempel))
            ergebnis_label.config(text=f"Fecha modificada correctamente: {neues_datum_uhrzeit}")
        elif os.path.isdir(pfad):
            if auswahl == "Solo carpetas":
                os.utime(pfad, (neuer_zeitstempel, neuer_zeitstempel))
                ergebnis_label.config(text=f"Fecha modificada correctamente: {neues_datum_uhrzeit}")
            elif auswahl == "Cambiar el contenido de la carpeta":
                os.utime(pfad, (neuer_zeitstempel, neuer_zeitstempel))
                for root, dirs, files in os.walk(pfad):
                    for dir in dirs:
                        ordnerpfad = os.path.join(root, dir)
                        os.utime(ordnerpfad, (neuer_zeitstempel, neuer_zeitstempel))
                    for file in files:
                        dateipfad = os.path.join(root, file)
                        os.utime(dateipfad, (neuer_zeitstempel, neuer_zeitstempel))
                ergebnis_label.config(text=f"Fecha modificada correctamente: {neues_datum_uhrzeit}")
    except Exception as e:
        ergebnis_label.config(text=f"Error: {str(e)}")
# Funktion zum Kürzen langer Pfade für die Anzeige
def acortar_ruta(ruta, max_longitud=50):
    if len(ruta) <= max_longitud:
        return ruta
    else:
        inicio = ruta[:25]   # primeros 25 caracteres
        fin = ruta[-20:]     # últimos 20 caracteres
        return f"{inicio}...{fin}"


# Erstelle das Hauptfenster
fenster = tk.Tk()
fenster.title("TimeStamp Tool")
fenster.geometry("650x650")  # Größe des Fensters auf 650x550 Pixel ändern

# LabelFrame für die Auswahl für Datei oder Ordner
auswahl_frame = tk.LabelFrame(fenster, text="¿Qué le gustaría modificar?", font=("Tahoma", 11, "bold"))

auswahl_frame.pack(pady=20, padx=20, fill="x")

auswahl_var = tk.StringVar(value="Archivo")

datei_radio = tk.Radiobutton(auswahl_frame, text="Un archivo", variable=auswahl_var, value="Archivo", font=("Tahoma", 11, "bold"))
datei_radio.pack(side=tk.LEFT, padx=10, pady=5)

ordner_inhalt_radio = tk.Radiobutton(auswahl_frame, text="Todos los archivos en una carpeta", variable=auswahl_var, value="Cambiar el contenido de la carpeta", font=("Tahoma", 11, "bold"))
ordner_inhalt_radio.pack(side=tk.LEFT, padx=10, pady=5)

#nur_ordner_radio = tk.Radiobutton(auswahl_frame, text="Nur Ordner", variable=auswahl_var, value="Nur Ordner", font=("Tahoma", 11, "bold"))
#nur_ordner_radio.pack(side=tk.LEFT, padx=10, pady=5)

# Schaltfläche zum Auswählen der Datei oder des Ordners und Anzeigen ihres Namens
datei_auswählen_button = tk.Button(fenster, text="Buscar:", font=("Tahoma", 11, "bold"), command=ändere_daten)
datei_auswählen_button.pack(pady=20)

# Etikett zum Anzeigen des ausgewählten Dateinamens oder Ordners
ausgewählte_datei_label = tk.Label(fenster, text="ninguna selección...", fg="blue", font=("Tahoma", 11, "bold"))
ausgewählte_datei_label.pack(pady=5)

# Erstelle den Kalender zum Auswählen des Datums
kalender = Calendar(fenster, selectmode="day", date_pattern="dd.MM.yyyy")
kalender.pack(pady=20)

# Schaltfläche zur Bestätigung der Datums- und Uhrzeitänderung
bestätigen_button = tk.Button(fenster, text="Confirmar cambio", state=tk.DISABLED, font=("Tahoma", 11, "bold"), command=bestätige_änderung)
bestätigen_button.pack(pady=15)

# Etikett zum Anzeigen des Ergebnisses
ergebnis_label = tk.Label(fenster, text="", font=("Tahoma", 11))
ergebnis_label.pack(pady=10)

# ... todo tu código de selección de archivo/carpeta, calendario y botón de confirmar ...

# Etiqueta de autor/licencia (opcional)
autor_label = tk.Label(fenster, text="TimeStamp Tool © 2025 - Autor: Jose M Sucre\nMIT-Lizenz | Se aceptan donaciones", font=("Tahoma", 9), fg="gray")

autor_label.pack(side="bottom", pady=5)

# Botón de donación
def abrir_donacion():
    webbrowser.open("https://www.paypal.me/JoseSucre")  # Reemplaza con tu enlace de donación

donar_button = tk.Button(fenster, text="☕ Iniciar donaciones", font=("Tahoma", 10, "bold"), command=abrir_donacion)
donar_button.pack(side="bottom", pady=5)

# Inicia la ventana principal
fenster.mainloop()
