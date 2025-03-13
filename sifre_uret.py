import customtkinter as ctk
import random
import string
import pyperclip
import pyodbc

def veritabani_baglanti():
    server='UGURS-VICTUS\SQLKODLAB'
    database='python'
    try:
        conn_str= f'DRIVER={{SQL Server}}; SERVER={server}; DATABASE={database}; Trusted_Connection=yes;'
        conn= pyodbc.connect(conn_str)
        cursor=conn.cursor()
        return conn, cursor
    except Exception as e:
        print("Veritabanı bağlantısı başarısız:",e)
        return None, None


def sifre_uret():
    try:
        uzunluk = int(giris.get())  # Kullanıcının girdiği uzunluğu al
    except ValueError:
        sonuc.set("Lütfen geçerli bir sayı girin!")
        return ""

    # Seçili şifre türüne göre karakterleri belirle
    karakterler = ""
    if harf_var.get():
        karakterler += string.ascii_letters
    if rakam_var.get():
        karakterler += string.digits
    if sembol_var.get():
        karakterler += string.punctuation

    if not karakterler:  # Eğer kullanıcı hiç bir şey seçmezse varsayılan olarak harf ve rakamdan oluşacak
        karakterler = string.ascii_letters + string.digits

    # Rastgele şifre oluştur
    sifre = "".join(random.choice(karakterler) for _ in range(uzunluk))
    sonuc.set(sifre)  # Şifreyi ekranda göster
    kaydet_veritabanina(sifre)
    
    return sifre  # Şifreyi geri döndür

def panoya_kopyala():
    pyperclip.copy(sonuc.get())  # Şifreyi panoya kopyala
    
    # Panoya kopyalandı mesajını göster
    kopya_bildirim.configure(text="Panoya kopyalandı!")
    kopya_bildirim.pack(pady=5)

    # Mesajı 2 saniye sonra gizle
    root.after(2000, lambda: kopya_bildirim.pack_forget())

# Geçmiş şifreyi kutuya ekle
def gecmis_sifre_ekle(sifre):
    gecmis_textbox.insert("0.0", sifre + "\n")  # En üstte göster

#Şifreyi veritabanına ekleme
def kaydet_veritabanina(sifre):
    conn, cursor= veritabani_baglanti()
    if conn is not None and cursor is not None:
        cursor.execute("INSERT INTO sifreler (sifre) VALUES (?)", (sifre,))
    conn.commit()
    conn.close

#Şifreleri getirme 
def sifreleri_getir():
    conn, cursor= veritabani_baglanti()
    if conn is not None and cursor is not None:
        cursor.execute("SELECT sifre FROM sifreler")
        sifreler = cursor.fetchall()
        conn.close()
        return [sifre[0] for sifre in sifreler]
    return[]


#Geçmiş şifreleri göster
def gecmis_sifreleri_yukle():
    gecmis_textbox.delete("1.0", "end")
    for sifre in sifreleri_getir():
        gecmis_textbox.insert("end", sifre +"\n")



# Ana pencere
root = ctk.CTk()
root.title("Şifre Üretici")
root.geometry("400x500")

# Şifre uzunluğu giriş kutusu
ctk.CTkLabel(root, text="Şifre Uzunluğu:").pack(pady=10)
giris = ctk.CTkEntry(root)
giris.pack(pady=5)

# Frame ekleyerek checkbutton'ları içine alıyoruz
checkbox_frame = ctk.CTkFrame(root)  # Bir frame ekledik
checkbox_frame.pack(pady=10)

# Şifre türü seçme kuralları
harf_var = ctk.BooleanVar(value=True)  # Varsayılan olarak açık
rakam_var = ctk.BooleanVar(value=True)
sembol_var = ctk.BooleanVar(value=True)

# Checkbutton'ları frame içine yerleştiriyoruz
ctk.CTkCheckBox(checkbox_frame, text="Harfler", variable=harf_var).pack(side="left", padx=10)
ctk.CTkCheckBox(checkbox_frame, text="Rakamlar", variable=rakam_var).pack(side="left", padx=10)
ctk.CTkCheckBox(checkbox_frame, text="Semboller", variable=sembol_var).pack(side="left", padx=10)

# Şifre gösterme etiketi
sonuc = ctk.StringVar()
ctk.CTkLabel(root, text="Üretilen Şifre:").pack(pady=10)
ctk.CTkLabel(root, textvariable=sonuc, text_color="blue").pack()

# Butonlar
ctk.CTkButton(root, text="Şifre Oluştur", command=lambda: gecmis_sifre_ekle(sifre_uret())).pack(pady=10)
ctk.CTkButton(root, text="Panoya Kopyala", command=panoya_kopyala).pack(pady=5)

# Geçmiş Şifreler Alanı
ctk.CTkLabel(root, text="Geçmiş Şifreler:").pack(pady=10)

# Geçmiş şifreleri gösterebilmek için CTkTextbox kullanıyoruz
gecmis_textbox = ctk.CTkTextbox(root, height=50, width=200)  # Yüksekliği ve genişliği arttırdık
gecmis_textbox.pack(pady=10)

# Panoya kopyalandı bildirim label'ı
kopya_bildirim = ctk.CTkLabel(root, text="", text_color="green")

# `Enter` tuşuna basıldığında şifre oluşturma butonunu tetiklemek için bind ekliyoruz
giris.bind("<Return>", lambda event: gecmis_sifre_ekle(sifre_uret()))

#şifreleri geri yükleme
gecmis_sifreleri_yukle()
# Pencereyi başlat
root.mainloop()
