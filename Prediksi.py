
import tkinter as tk
from tkinter import messagebox
import sqlite3

def create_db():
    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT NOT NULL,
            biologi INTEGER NOT NULL,
            fisika INTEGER NOT NULL,
            inggris INTEGER NOT NULL,
            prediksi_fakultas TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

create_db()

def prediksi_fakultas(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Tidak Dapat Ditentukan"


def submit_nilai():
    nama = entry_nama.get().strip()

    if not nama:
        messagebox.showerror(
            "Error", "Nama siswa tidak boleh kosong!"
        )
        entry_nama.focus()
        return

    try:
        bio = int(entry_bio.get())
        fis = int(entry_fis.get())
        ing = int(entry_ing.get())
    except ValueError:
        messagebox.showerror(
            "Error",
            "Nilai Biologi, Fisika, dan Inggris harus berupa angka bulat!"
        )
        return

    if not all(0 <= nilai <= 100 for nilai in (bio, fis, ing)):
        messagebox.showerror(
            "Error", "Nilai harus berada di antara 0 sampai 100!"
        )
        return

    hasil_prediksi = prediksi_fakultas(bio, fis, ing)

    try:
        conn = sqlite3.connect("nilai_siswa.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO nilai_siswa
            (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
            VALUES (?, ?, ?, ?, ?)
        """, (nama, bio, fis, ing, hasil_prediksi))

        conn.commit()
        conn.close()

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Gagal menyimpan data:\n{error}"
        )
        return

    label_hasil.config(
        text=f"Prediksi Fakultas: {hasil_prediksi}",
        fg="#50fa7b"
    )

    messagebox.showinfo(
        "Hasil Prediksi",
        f"Nama Siswa: {nama}\n"
        f"Biologi: {bio}\n"
        f"Fisika: {fis}\n"
        f"Inggris: {ing}\n\n"
        f"Prediksi Fakultas: {hasil_prediksi}\n\n"
        "Data berhasil disimpan ke SQLite!"
    )

    entry_nama.delete(0, tk.END)
    entry_bio.delete(0, tk.END)
    entry_fis.delete(0, tk.END)
    entry_ing.delete(0, tk.END)
    entry_nama.focus()


def on_enter(event):
    btn_submit.config(
        bg="#50fa7b",
        fg="#282a36"
    )


def on_leave(event):
    btn_submit.config(
        bg="#44475a",
        fg="white"
    )


#Membuat GUI
root = tk.Tk()
root.title("Aplikasi Prediksi Fakultas")
root.geometry("390x530+200+100")
root.configure(bg="#282a36")
root.resizable(False, False)

judul = tk.Label(
    root,
    text="PREDIKSI FAKULTAS",
    font=("Arial", 16, "bold"),
    bg="#282a36",
    fg="#8be9fd"
)
judul.pack(pady=(25, 5))

subjudul = tk.Label(
    root,
    text="Masukkan data dan nilai siswa",
    font=("Arial", 9),
    bg="#282a36",
    fg="#f8f8f2"
)
subjudul.pack(pady=(0, 20))


frame_input = tk.Frame(
    root,
    bg="#343746",
    padx=18,
    pady=15
)
frame_input.pack(padx=20, fill="x")


def buat_input(teks, baris):
    label = tk.Label(
        frame_input,
        text=teks,
        font=("Arial", 10, "bold"),
        bg="#343746",
        fg="#f8f8f2",
        anchor="w"
    )
    label.grid(
        row=baris,
        column=0,
        sticky="w",
        pady=9,
        padx=(0, 10)
    )

    entry = tk.Entry(
        frame_input,
        font=("Arial", 10),
        bg="#f8f8f2",
        fg="#282a36",
        insertbackground="#282a36",
        relief="flat",
        width=19
    )
    entry.grid(
        row=baris,
        column=1,
        ipady=6,
        pady=9
    )

    return entry


entry_nama = buat_input("Nama Siswa", 0)
entry_bio = buat_input("Nilai Biologi", 1)
entry_fis = buat_input("Nilai Fisika", 2)
entry_ing = buat_input("Nilai Inggris", 3)


btn_submit = tk.Button(
    root,
    text="SUBMIT NILAI",
    font=("Arial", 11, "bold"),
    bg="#44475a",
    fg="white",
    activebackground="#50fa7b",
    activeforeground="#282a36",
    relief="flat",
    cursor="hand2",
    width=20,
    pady=9,
    command=submit_nilai
)
btn_submit.pack(pady=22)

btn_submit.bind("<Enter>", on_enter)
btn_submit.bind("<Leave>", on_leave)


frame_hasil = tk.Frame(
    root,
    bg="#343746",
    padx=10,
    pady=12
)
frame_hasil.pack(fill="x", padx=20)

label_hasil = tk.Label(
    frame_hasil,
    text="Prediksi Fakultas: -",
    font=("Arial", 11, "bold"),
    bg="#343746",
    fg="#f8f8f2"
)
label_hasil.pack()


label_database = tk.Label(
    root,
    text="Database: nilai_siswa.db",
    font=("Arial", 8),
    bg="#282a36",
    fg="#8be9fd"
)
label_database.pack(pady=12)


root.mainloop()
