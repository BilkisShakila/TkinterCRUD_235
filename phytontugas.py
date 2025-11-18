import tkinter as tk # GUI library
from tkinter import messagebox # Untuk menampilkan pesan    
import sqlite3 # Library database SQLite

# ------------------------------
# Buat / Hubungkan Database SQLite
# ------------------------------
conn = sqlite3.connect("nilai_siswa.db") # Membuat database atau menghubungkan jika sudah ada
cursor = conn.cursor() # Membuat cursor untuk eksekusi perintah SQL

# Membuat tabel jika belum ada
cursor.execute("""   
CREATE TABLE IF NOT EXISTS nilai_siswa( # Membuat tabel nilai_siswa
    id INTEGER PRIMARY KEY AUTOINCREMENT, # Kolom ID sebagai primary key
    nama_siswa TEXT, # Kolom nama siswa
    biologi INTEGER,
    fisika INTEGER,
    inggris INTEGER,
    prediksi_fakultas TEXT
)
""")
conn.commit() # Simpan perubahan

# -------------------------------------------------
# Fungsi Prediksi Fakultas Berdasarkan Nilai Tertinggi
# -------------------------------------------------
def prediksi_fakultas(bio, fis, ing): # Fungsi untuk memprediksi fakultas
    nilai_max = max(bio, fis, ing) # Mencari nilai tertinggi

    if nilai_max == bio:
        return "Kedokteran"
    elif nilai_max == fis:
        return "Teknik"
    elif nilai_max == ing:
        return "Bahasa"
    else : 
        return "Tidak dapat diprediksi"

# -------------------------------------------------
# Fungsi Simpan Data ke Database
# -------------------------------------------------
def submit_data():
    try: # Mengambil data dari entry
        nama = entry_nama.get() # Nama siswa
        bio = int(entry_biologi.get()) # Nilai biologi
        fis = int(entry_fisika.get()) # Nilai fisika
        ing = int(entry_inggris.get())

        # Prediksi fakultas
        hasil = prediksi_fakultas(bio, fis, ing)

        # Simpan ke database
        cursor.execute(""" 
            INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas) 
            VALUES (?, ?, ?, ?, ?) # Menyimpan data ke tabel
        """, (nama, bio, fis, ing, hasil)) # Menyisipkan data ke tabel
        conn.commit() # Simpan perubahan

        messagebox.showinfo("Berhasil", f"Data berhasil disimpan!\nPrediksi: {hasil}") # Tampilkan pesan sukses

    except ValueError:
        messagebox.showerror("Error", "Nilai harus berupa angka!") # Tampilkan pesan error jika input tidak valid

# ------------------------------
# GUI Tkinter
# ------------------------------
root = tk.Tk() # Membuat jendela utama
root.title("Prediksi Fakultas Berdasarkan Nilai") # Judul jendela
root.geometry("400x350") # Ukuran jendela 

# Label dan Entry
tk.Label(root, text="Nama Siswa").pack() # Label untuk nama siswa
entry_nama = tk.Entry(root) # Entry untuk nama siswa
entry_nama.pack() # Menempatkan entry di jendela

tk.Label(root, text="Nilai Biologi").pack()
entry_biologi = tk.Entry(root)
entry_biologi.pack()

tk.Label(root, text="Nilai Fisika").pack()
entry_fisika = tk.Entry(root)
entry_fisika.pack()

tk.Label(root, text="Nilai Inggris").pack()
entry_inggris = tk.Entry(root)
entry_inggris.pack()

# Tombol Submit
btn_submit = tk.Button(root, text="Submit Nilai", command=submit_data, bg="lightblue") # Tombol untuk submit data
btn_submit.pack(pady=20) # Menempatkan tombol di jendela

root.mainloop() # Menjalankan aplikasi GUI
