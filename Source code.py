import pwinput
import json
import os.path
from prettytable import PrettyTable
tabel_data = PrettyTable()
tabel_riwayat = PrettyTable()

# membuat judul tabel bagian atas
tabel_data.field_names = ["List", "harga", "Tipe Smartphone", "Stok barang"]
tabel_riwayat.field_names = ['Nama Pembeli',
                             "Tipe smartphone", 'Kuantitas', 'Total harga']
# Tempat untuk menyimpan data ke dalam dictionary
data_riwayat = []
data_barang = []
data_login = [{
    "username":  "admin",
    "password": "admin",
    "permission": True
}]
harga = 0
tipe = ""
stok = 0


def isExist(file):
    return os.path.isfile(file)


if isExist('data_login.json'):
    with open("data_login.json", "r") as json_login:
        data_login = json.load(json_login)

if isExist('data_barang.json'):
    with open("data_barang.json", "r") as json_barang:
        data_barang = json.load(json_barang)

if isExist('data_riwayat.json'):
    with open("data_riwayat.json", "r") as json_riwayat:
        data_riwayat = json.load(json_riwayat)


# buat melakukan penginputan data


def input_data():
    while True:
        try:
            global harga, tipe, stok
            harga = int(input("Harga :Rp. "))
            tipe = input("Tipe Smartphone : ")
            stok = int(input("Jumlah stok : "))
            if harga > 0 and stok > 0:
                break
            else:
                print("masukkan inputan dengan benar")
        except:
            print("input salah")
            return input_data()

    data_barang.append({
        'harga': harga,
        'Tipe Handphone': tipe,
        'stok': stok
    })

    perbarui_tabel()

# untuk memperbarui Tabel


def perbarui_tabel():
    barang = data_barang
    riwayat = data_riwayat

    with open('data_barang.json', 'w') as file:
        json.dump(barang, file, indent=4)

    with open('data_riwayat.json', 'w') as file:
        json.dump(riwayat, file, indent=4)

    tabel_data.clear_rows()
    for i in range(len(barang)):
        tabel_data.add_row([i + 1, barang[i].get('harga'),
                           barang[i].get('Tipe Handphone'), barang[i].get('stok')])

    tabel_riwayat.clear_rows()
    for i in range(len(riwayat)):
        tabel_riwayat.add_row([riwayat[i].get('nama_pembeli'),
                               riwayat[i].get('tipe_smartphone'), riwayat[i].get('kuantitas'), riwayat[i].get('total_harga')])

def delete_data():
    show_data()
    try:
        urutan_del_row = int(input(" Pilih Data Yang Akan dihapus : "))
        if urutan_del_row > 0:
            data_barang.pop(urutan_del_row - 1)
            print("Data yang dipilih Berhasil dihapus")
        else:
            print("Salah input ")
    except:
        print("salah")

    perbarui_tabel()
    show_data()


def ubah_data():
    show_data()
    while True:
        try:
            urutan_ubah_row = int(
                input(" Pilih Data Yang Akan diubah harga dan stok nya: "))
            if urutan_ubah_row > 0:
                harga = int(input('Masukkan harga baru : '))
                stok = int(input("Jumlah stok : "))
                data_barang[urutan_ubah_row - 1]['harga'] = harga
                data_barang[urutan_ubah_row - 1]['stok'] = stok
                if stok > 0 and harga > 0:
                    break
                else:
                    print("Input Salah, Silahkan coba lagi")
            else:
                print('Masukkan input dengan benar')
                return ubah_data()
        except:
            print("Input Salah")
            return menu('admin')

    perbarui_tabel()


# untuk menampilkan tabel
def show_data():
    perbarui_tabel()
    print(tabel_data)


def show_history():
    perbarui_tabel()
    print(tabel_riwayat)

# untuk login


def login(name, password):
    global loginAs
    for akun in data_login:
        if name == akun.get('username') and password == akun.get('password'):
            print('Login Berhasil, Silahkan Masuk >_<'.center(32))
            loginAs = akun
            return True

    print("Username atau Password yang Anda Input Salah, Silahkan login Ulang")
    return begin()

# penginputan data buat register


def register(username, password):
    for akun in data_login:
        if username == akun.get("username"):
            print('Akun Sudah ada ')
            return begin()
    data_login.append({
        "username": username,
        "password": password,
        "permission": False
    })

    with open('data_login.json', 'w') as file:
        json.dump(data_login, file, indent=3)


def akses(option):
    if(option == "login"):
        username = input("Username : ")
        password = pwinput.pwinput("Password : ")
        isLogin = login(username, password)
        if isLogin == True:
            return isLogin
        else:
            return akses('login')
    else:
        print("Input Username dan Password akun baru anda")
        username = input("Masukkan Username : ")
        password = pwinput.pwinput("Masukkan password anda: ")
        register(username, password)
        print("Register anda berhasil, Silahkan Masuk")
        return False


def begin():
    print('=' * 69)
    print("Selamat datang di Toko Smartphone".center(73))
    print('=' * 69)
    print("Jika telah memiliki Akun, Silahkan mengetik 'login' untuk login".center(69))
    print("Jika belum memiliki Akun, Silahkan mengetik 'reg' untuk Registrasi".center(69))
    print('=' * 69)
    option = input("Silahkan Input Pilihan [login/reg]: ")
    if(option != "login" and option != "reg"):
        return begin()

    if akses(option):
        main()
    else:
        return begin()

# Tampilkan menu


def menu(user):
    if user == 'admin':
        print("""
        ==========================================
        | >>>>>>>>>>>>>> M E N U <<<<<<<<<<<<<<< |
        ==========================================
        |           > 1. Input Data              |
        |           > 2. Delete Data             |
        |           > 3. Tampilkan Data          |
        |           > 4. Ubah Data               |
        |           > 5. History Pembelian       |
        |           > 6. Exit                    |        
        ==========================================""".center(50))
    elif user == 'user':
        print("""
        ==========================================
        | >>>>>>>>>>>>>> M E N U <<<<<<<<<<<<<<< |
        ==========================================
        |           > 1. Tampilkan barang        |
        |           > 2. Beli barang             |
        |           > 3. Exit                    |
        ==========================================""".center(50))

    return input("pilih operasi : ")


def cekPermission(akun):
    if akun.get('permission') == True:
        return True
    else:
        return False


def beli_barang():
    # temp data
    show_data()
    total_bayar = 0
    temp_data = []  # atau bisa juga disebut keranjang belanja
    while True:
        try:
            pilih_barang = int(
                input('pilih barang yang ingin dibeli sesuai list : '))
            jumlah_beli = int(
                input('masukan jumlah barang yang ingin dibeli : '))
            if jumlah_beli > 0:
                if pilih_barang > 0 and data_barang[pilih_barang - 1]['stok'] >= jumlah_beli and data_barang[pilih_barang - 1]['stok'] != 0:
                    harga_barang = data_barang[pilih_barang - 1].get('harga')
                    data_barang[pilih_barang - 1]['stok'] = data_barang[pilih_barang - 1].get('stok')-jumlah_beli
                    total_bayar += harga_barang * jumlah_beli
                    temp_data.append({
                        "index": pilih_barang - 1,
                        "nama_item": data_barang[pilih_barang - 1].get('Tipe Handphone'),
                        "jumlah_item": jumlah_beli,
                        "harga_item": harga_barang
                    })
                else:
                    if total_bayar != 0 :
                        struk_belanjaan(temp_data, total_bayar)
                        return menu(user='user')
                    else :
                        print('Input yang anda masukan salah, silahkan coba lagi')
                        return beli_barang()
                pilih = input(
                    'Apakah Anda telah selesai memilih barang [y/t]: ').lower()
                if pilih == 'y':
                    struk_belanjaan(temp_data, total_bayar)
                    break
                elif pilih != 't':
                    return beli_barang()
            else:
                print('Input Salah, Masukan input dengan benar')

        except:
            print("Input Salah, Masukan input dengan benar")

    # untuk memperbarui data jika data telah terbeli
    for item in temp_data:
        index = item.get("index")
        stok_barang = data_barang[index].get('stok')
        data_barang[index]['stok'] = stok_barang - item.get('jumlah_item')

        data_riwayat.append({
            "nama_pembeli": loginAs.get("username"),
            "tipe_smartphone": item.get('nama_item'),
            "kuantitas": item.get('jumlah_item'),
            "total_harga": f'Rp. {item.get("harga_item") * item.get("jumlah_item")}'
        })

        perbarui_tabel()


def struk_belanjaan(item, total):
    # header struktur belanja
    print("""
=============================
|     Struktur belanjaan    |
-----------------------------""")

    for i in range(len(item)):
        print(f"{i + 1}. {item[i]['nama_item']} x {item[i]['jumlah_item']}")

    # footer struktur belanja
    print(f"""
----------------------------
| total     : Rp. {total * (30/100)}   |
-----------------------------
 Silahkan Menuju ke Teller 3
  untuk melakukan pembayaran
-----------------------------
        Terima kasih 
      telah berbelanja
=============================""")


def main():
    isAdmin = cekPermission(loginAs)
    while True:
        if isAdmin == True:
            pilihan = menu('admin')
            # proses input dan output
            if pilihan == "1":
                input_data()
            elif pilihan == "2":
                delete_data()
            elif pilihan == "3":
                show_data()
            elif pilihan == '4':
                ubah_data()
            elif pilihan == '5':
                show_history()
            elif pilihan == '6':
                break
            else:
                print("[--------- Input yang anda masukan tidak tersedia ---------]")
        else:
            pilihan = menu('user')
            if pilihan == "1":
                show_data()
            elif pilihan == "2":
                beli_barang()
            elif pilihan == '3':
                break
            else:
                print("[--------- Input yang anda masukan tidak tersedia ---------]")
        print()
    print("[-------------------- Terimakasih -------------------------]")
    return begin()


begin()
