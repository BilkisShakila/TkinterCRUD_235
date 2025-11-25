import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# ------------------------------
# Buat / Hubungkan Database SQLite
# ------------------------------
conn = sqlite3.connect("nilai_siswa.db") # Membuat database atau menghubungkan jika sudah ada
cursor = conn.cursor() # Membuat cursor untuk eksekusi perintah SQL

cursor.execute(""" # Membuat tabel jika belum ada
CREATE TABLE IF NOT EXISTS nilai_siswa(  # Membuat tabel nilai_siswa
    id INTEGER PRIMARY KEY AUTOINCREMENT, # Kolom ID sebagai primary key
    nama_siswa TEXT, # Kolom nama siswa
    biologi INTEGER,
    fisika INTEGER,
    inggris INTEGER,
    prediksi_fakultas TEXT # Kolom prediksi fakultas
)
""") # Simpan perubahan
conn.commit() # Simpan perubahan


# Fungsi Prediksi Fakultas
def prediksi_fakultas(bio, fis, ing): # Fungsi untuk memprediksi fakultas
    nilai_max = max(bio, fis, ing) # Mencari nilai tertinggi
    if nilai_max == bio: #membuat kondisi untuk menentukan fakultas
        return "Kedokteran" # Jika nilai biologi tertinggi
    elif nilai_max == fis:
        return "Teknik"
    elif nilai_max == ing:
        return "Bahasa"
    else:
        return "Tidak dapat diprediksi" # Jika tidak ada nilai tertinggi


# Tampilkan Data ke Tabel (Treeview)
def load_data(): # Memuat data dari database ke tabel
    for row in tree.get_children(): # Hapus data lama di tabel
        tree.delete(row) # Hapus data lama di tabel

    cursor.execute("SELECT * FROM nilai_siswa") # Ambil semua data dari tabel nilai_siswa
    for row in cursor.fetchall(): # Masukkan data ke tabel
        tree.insert("", tk.END, values=row) # Masukkan data ke tabel

# CREATE - Simpan Data
def submit_data(): # Simpan data ke database
    try:
        nama = entry_nama.get() # Ambil data dari entry
        bio = int(entry_biologi.get()) # Nilai biologi 
        fis = int(entry_fisika.get())
        ing = int(entry_inggris.get())

        hasil = prediksi_fakultas(bio, fis, ing) # Prediksi fakultas

        cursor.execute(""" #memasukkan data ke database
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
        """, (nama, bio, fis, ing, hasil)) # Menyisipkan data ke tabel
        conn.commit() # Simpan perubahan

        messagebox.showinfo("Berhasil", f"Data tersimpan! Prediksi: {hasil}") # Tampilkan pesan sukses
        load_data() # Muat ulang data di tabel

    except ValueError:
        messagebox.showerror("Error", "Nilai harus berupa angka!")

# -------------------------------------------------
# PILIH DATA DARI TABEL
# -------------------------------------------------
def pilih_data(event):
    try:
        selected_item = tree.selection()[0]
        data = tree.item(selected_item, "values")

        lbl_selected_id.config(text=f"ID: {data[0]}")

        entry_nama.delete(0, tk.END)
        entry_nama.insert(0, data[1])

        entry_biologi.delete(0, tk.END)
        entry_biologi.insert(0, data[2])

        entry_fisika.delete(0, tk.END)
        entry_fisika.insert(0, data[3])

        entry_inggris.delete(0, tk.END)
        entry_inggris.insert(0, data[4])

    except:
        pass

# -------------------------------------------------
# UPDATE DATA
# -------------------------------------------------
def update_data():
    try:
        selected_id = lbl_selected_id.cget("text").replace("ID: ", "")
        if selected_id == "":
            messagebox.showwarning("Peringatan", "Pilih data dulu!")
            return

        nama = entry_nama.get()
        bio = int(entry_biologi.get())
        fis = int(entry_fisika.get())
        ing = int(entry_inggris.get())

        hasil = prediksi_fakultas(bio, fis, ing)

        cursor.execute("""
        UPDATE nilai_siswa
        SET nama_siswa=?, biologi=?, fisika=?, inggris=?, prediksi_fakultas=?
        WHERE id=?
        """, (nama, bio, fis, ing, hasil, selected_id))

        conn.commit()
        messagebox.showinfo("Berhasil", "Data berhasil diupdate!")
        load_data()

    except ValueError:
        messagebox.showerror("Error", "Nilai harus berupa angka!")

# -------------------------------------------------
# DELETE DATA
# -------------------------------------------------
def delete_data():
    try:
        selected_item = tree.selection()[0]
        data = tree.item(selected_item, "values")
        data_id = data[0]

        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus data ini?"):
            cursor.execute("DELETE FROM nilai_siswa WHERE id=?", (data_id,))
            conn.commit()
            load_data()

    except:
        messagebox.showwarning("Peringatan", "Pilih data dari tabel!")

# -------------------------------------------------
# GUI Tkinter
# -------------------------------------------------
root = tk.Tk()
root.title("Prediksi Fakultas")
root.geometry("750x600")

# Frame Input
tk.Label(root, text="Nama Siswa").pack()
entry_nama = tk.Entry(root)
entry_nama.pack()

tk.Label(root, text="Nilai Biologi").pack()
entry_biologi = tk.Entry(root)
entry_biologi.pack()

tk.Label(root, text="Nilai Fisika").pack()
entry_fisika = tk.Entry(root)
entry_fisika.pack()

tk.Label(root, text="Nilai Inggris").pack()
entry_inggris = tk.Entry(root)
entry_inggris.pack()

btn_submit = tk.Button(root, text="Submit", bg="lightblue", command=submit_data)
btn_submit.pack(pady=5)

btn_update = tk.Button(root, text="Update", bg="orange", command=update_data)
btn_update.pack(pady=5)

btn_delete = tk.Button(root, text="Delete", bg="red", fg="white", command=delete_data)
btn_delete.pack(pady=5)

lbl_selected_id = tk.Label(root, text="ID: ")
lbl_selected_id.pack()

# ---------------------------
# TABLE / TREEVIEW OUTPUT
# ---------------------------
columns = ("ID", "Nama", "Biologi", "Fisika", "Inggris", "Prediksi")

tree = ttk.Treeview(root, columns=columns, show="headings", height=12)
tree.pack(pady=10)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)

tree.bind("<<TreeviewSelect>>", pilih_data)

load_data()

root.mainloop()