import math

# Nama bulan Hijriyah
HIJRI_MONTHS = [
    "Muharram", "Safar", "Rabiul Awal", "Rabiul Akhir",
    "Jumadil Awal", "Jumadil Akhir", "Rajab", "Syaban",
    "Ramadhan", "Syawal", "Zulqaidah", "Zulhijjah"
]

# Tahun kabisat Hijriyah dalam siklus 30 tahun
HIJRI_LEAP_CYCLE = [2, 5, 7, 10, 13, 16, 18, 21, 24, 26, 29]


def is_hijri_leap(year):
    """Cek apakah tahun Hijriyah kabisat."""
    return (year % 30) in HIJRI_LEAP_CYCLE


def hijri_month_length(year, month):
    """Mengembalikan jumlah hari pada bulan Hijriyah tertentu."""
    if month % 2 == 1:  # bulan ganjil → 30 hari
        return 30
    else:  # bulan genap → 29 hari, kecuali Zulhijjah tahun kabisat
        if month == 12:
            return 30 if is_hijri_leap(year) else 29
        return 29


# ===============================
#  KONVERSI GREGORIAN ↔ JULIAN DAY
# ===============================
def gregorian_to_jd(year, month, day):
    """Konversi tanggal Gregorian ke Julian Day Number."""
    if month <= 2:
        year -= 1
        month += 12
    A = year // 100
    B = 2 - A + (A // 4)
    jd = int(365.25 * (year + 4716)) \
         + int(30.6001 * (month + 1)) \
         + day + B - 1524.5
    return jd


def jd_to_gregorian(jd):
    """Konversi Julian Day Number ke tanggal Gregorian."""
    jd += 0.5
    Z = int(jd)
    F = jd - Z

    if Z < 2299161:
        A = Z
    else:
        alpha = int((Z - 1867216.25) / 36524.25)
        A = Z + 1 + alpha - int(alpha / 4)

    B = A + 1524
    C = int((B - 122.1) / 365.25)
    D = int(365.25 * C)
    E = int((B - D) / 30.6001)

    day = B - D - int(30.6001 * E) + F
    month = E - 1 if E < 14 else E - 13
    year = C - 4716 if month > 2 else C - 4715

    return int(year), int(month), int(day)


# ===============================
#  KONVERSI HIJRIYAH ↔ JULIAN DAY
# ===============================
def hijri_to_jd(year, month, day):
    """Konversi tanggal Hijriyah ke Julian Day Number."""
    days = (year - 1) * 354
    days += math.floor((3 + 11 * year) / 30)  # akumulasi kabisat
    days += (month - 1) * 29.5
    days = math.floor(days) + day
    return days + 1948439.5


def jd_to_hijri(jd):
    """Konversi Julian Day Number ke tanggal Hijriyah."""
    jd = math.floor(jd) + 0.5
    year = int((30 * (jd - 1948439.5) + 10646) // 10631)

    # Cari bulan
    month = 1
    while month <= 12:
        month_start = hijri_to_jd(year, month, 1)
        next_month_start = (
            hijri_to_jd(year, month + 1, 1) if month < 12 else month_start + 30
        )
        if jd < next_month_start:
            break
        month += 1

    # Hitung tanggal
    day = int(jd - month_start + 1)

    # Validasi tanggal
    max_day = hijri_month_length(year, month)
    if day > max_day:
        day = max_day

    return year, month, day


# ===============================
#  KONVERSI UTAMA
# ===============================
def masehi_ke_hijriyah(day, month, year):
    jd = gregorian_to_jd(year, month, day)
    return jd_to_hijri(jd)


def hijriyah_ke_masehi(day, month, year):
    jd = hijri_to_jd(year, month, day)
    return jd_to_gregorian(jd)


# ===============================
#  MENU HELP
# ===============================
def tampilkan_help():
    print("\n=== HELP / CARA PENGGUNAAN APLIKASI ===")
    print("Aplikasi ini digunakan untuk mengonversi tanggal:")
    print("1. Dari Kalender Masehi → Kalender Hijriyah")
    print("2. Dari Kalender Hijriyah → Kalender Masehi")
    print("\nCara Menggunakan:")
    print("- Pilih menu 1 untuk konversi Masehi ke Hijriyah.")
    print("- Pilih menu 2 untuk konversi Hijriyah ke Masehi.")
    print("- Masukkan tanggal berupa angka tanpa leading zero.")
    print("\nContoh:")
    print("  1 Maret 2024 → pilih menu 1, masukkan 1, 3, 2024")
    print("  1 Ramadan 1445 H → pilih menu 2, masukkan 1, 9, 1445")
    print("\nMenu 3 digunakan untuk melihat bantuan ini.")
    print("Menu 0 untuk keluar dari aplikasi.")
    print("=========================================\n")


# ===============================
#  PROGRAM UTAMA
# ===============================
def main():
    while True:
        print("=== KONVERTER KALENDER MASEHI ↔ HIJRIYAH ===")
        print("1. Masehi → Hijriyah")
        print("2. Hijriyah → Masehi")
        print("3. Help / Cara Penggunaan")
        print("0. Keluar")

        try:
            mode = int(input("Pilih menu: "))

            if mode == 1:
                print("\nMasukkan Tanggal Masehi")
                d = int(input("Tanggal : "))
                m = int(input("Bulan   : "))
                y = int(input("Tahun   : "))
                hy, hmo, hd = masehi_ke_hijriyah(d, m, y)
                print("\nHasil:")
                print(f"{hd} {HIJRI_MONTHS[hmo - 1]} {hy} H\n")

            elif mode == 2:
                print("\nMasukkan Tanggal Hijriyah")
                d = int(input("Tanggal : "))
                m = int(input("Bulan   : "))
                y = int(input("Tahun   : "))
                gy, gmo, gd = hijriyah_ke_masehi(d, m, y)
                print("\nHasil:")
                print(f"{gd}-{gmo}-{gy} M\n")

            elif mode == 3:
                tampilkan_help()

            elif mode == 0:
                print("Terima kasih telah menggunakan aplikasi ini.")
                break

            else:
                print("Menu tidak valid.\n")

        except Exception as e:
            print("Terjadi kesalahan:", e, "\n")


if __name__ == "__main__":
    main()
