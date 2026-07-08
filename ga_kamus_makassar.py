import random
import string

# ---------------------------------------------------------------------------
# DATASET: KAMUS BAHASA MAKASSAR (minimal 10 kata)
# Catatan: silakan sesuaikan arti kata bila diperlukan.
# ---------------------------------------------------------------------------
KAMUS = {
    "JAPPA":   "Jalan / Berjalan",
    "JARANG":  "Kuda",
    "KASA":    "Kain",
    "KANA":    "Kata / Ucapan",
    "KANRE":   "Nasi / Makanan",
    "SAKRA":   "Suara",
    "SASSA":   "Mencuci",
    "SAMBUNG": "Menyambung",
    "LAMPA":   "Pergi / Berangkat",
    "LAMPU":   "Lampu / Penerangan",
}

# ---------------------------------------------------------------------------
# PARAMETER ALGORITMA GENETIKA
# ---------------------------------------------------------------------------
GEN_ALFABET     = string.ascii_uppercase  # himpunan gen (A-Z)
UKURAN_POPULASI = 6                       # jumlah kromosom dalam satu populasi
PC              = 0.8                     # probabilitas cross over
PM              = 0.1                     # probabilitas mutasi
MAKS_GENERASI   = 1000                    # batas generasi untuk mode otomatis

GARIS = "=" * 70


class AlgoritmaGenetika:
    """Menyimpan seluruh keadaan (state) proses Algoritma Genetika."""

    def __init__(self):
        self.target = ""        # kata target dari kamus
        self.populasi = []      # populasi generasi sekarang
        self.generasi = 0       # nomor generasi
        self.orang_tua = []     # hasil seleksi roulette
        self.keturunan = []     # hasil cross over
        self.hasil_mutasi = []  # hasil mutasi (calon generasi baru)

    # ------------------------- INISIALISASI -------------------------
    def buat_kromosom(self):
        return "".join(random.choice(GEN_ALFABET) for _ in range(len(self.target)))

    def set_target(self, kata):
        self.target = kata
        self.generasi = 0
        self.orang_tua = []
        self.keturunan = []
        self.hasil_mutasi = []
        self.populasi = [self.buat_kromosom() for _ in range(UKURAN_POPULASI)]

    # --------------------------- FITNESS ----------------------------
    def hitung_fitness(self, kromosom):
        """Mengembalikan (gen cocok, error, fitness) sebuah kromosom."""
        cocok = sum(1 for g, t in zip(kromosom, self.target) if g == t)
        error = len(self.target) - cocok
        return cocok, error, 1 / (1 + error)

    def daftar_fitness(self):
        return [self.hitung_fitness(k) for k in self.populasi]

    def kromosom_terbaik(self):
        return max(self.populasi, key=lambda k: self.hitung_fitness(k)[2])

    def target_ditemukan(self):
        return self.target in self.populasi

    def tampilkan_fitness(self):
        w = max(len(self.target), 8)
        data = self.daftar_fitness()
        total = sum(d[2] for d in data)
        print(f" {'No':<4}| {'Kromosom':<{w}} | {'Gen Cocok':^9} | {'Error':^5} | Perhitungan Fitness")
        print(" " + "-" * (w + 55))
        for i, (krom, (cocok, error, fit)) in enumerate(zip(self.populasi, data)):
            print(f" K{i+1:<3}| {krom:<{w}} | {cocok:^9} | {error:^5} | 1/(1+{error}) = {fit:.4f}")
        print(" " + "-" * (w + 55))
        print(f" Total fitness    : {total:.4f}")
        print(f" Rata-rata fitness: {total / len(data):.4f}")
        terbaik = self.kromosom_terbaik()
        c, _e, f = self.hitung_fitness(terbaik)
        print(f" Kromosom terbaik : {terbaik} (gen cocok {c}/{len(self.target)}, fitness {f:.4f})")

    # ---------------------- SELEKSI ROULETTE ------------------------
    def seleksi_roulette(self, tampil=True):
        data = self.daftar_fitness()
        fits = [d[2] for d in data]
        total = sum(fits)
        probs = [f / total for f in fits]
        kumulatif = []
        s = 0.0
        for p in probs:
            s += p
            kumulatif.append(s)
        kumulatif[-1] = 1.0  # jaga-jaga pembulatan floating point

        w = max(len(self.target), 8)
        if tampil:
            print(" Tahap 1: Hitung probabilitas -> P[i] = fitness[i] / total_fitness")
            print(f" Total fitness = {total:.4f}\n")
            print(f" {'No':<4}| {'Kromosom':<{w}} | {'Fitness':<8} | {'Probabilitas':<12} | Kumulatif")
            print(" " + "-" * (w + 50))
            for i, (krom, fit, p, k) in enumerate(zip(self.populasi, fits, probs, kumulatif)):
                print(f" K{i+1:<3}| {krom:<{w}} | {fit:<8.4f} | {p:<12.4f} | {k:.4f}")
            print(" " + "-" * (w + 50))
            print("\n Tahap 2: Putar roulette (bangkitkan bilangan acak r antara 0-1,")
            print("          pilih kromosom pertama dengan kumulatif >= r)\n")

        terpilih = []
        for putaran in range(len(self.populasi)):
            r = random.random()
            for j, batas in enumerate(kumulatif):
                if r <= batas:
                    terpilih.append(self.populasi[j])
                    if tampil:
                        print(f" Putaran-{putaran+1}: r = {r:.4f} -> jatuh pada K{j+1} -> {self.populasi[j]}")
                    break

        self.orang_tua = terpilih
        self.keturunan = []       # reset tahap berikutnya
        self.hasil_mutasi = []
        if tampil:
            print("\n Hasil seleksi roulette (calon orang tua):")
            for i, k in enumerate(terpilih, 1):
                print(f"   P{i} = {k}")

    # -------------------------- CROSS OVER --------------------------
    def crossover(self, tampil=True):
        ortu = self.orang_tua
        panjang = len(self.target)
        anak = []
        if tampil:
            print(f" Metode: cross over satu titik potong, PC = {PC}")
            print(" Aturan: jika bilangan acak r < PC maka pasangan melakukan cross over.")

        i = 0
        pasangan = 0
        while i + 1 < len(ortu):
            pasangan += 1
            p1, p2 = ortu[i], ortu[i + 1]
            r = random.random()
            if tampil:
                print(f"\n Pasangan {pasangan}: P{i+1} x P{i+2}")
            if r < PC:
                titik = random.randint(1, panjang - 1)
                c1 = p1[:titik] + p2[titik:]
                c2 = p2[:titik] + p1[titik:]
                if tampil:
                    print(f"   r = {r:.4f} < PC({PC}) -> TERJADI cross over, titik potong = {titik}")
                    print(f"   P{i+1} = {p1[:titik]} | {p1[titik:]}")
                    print(f"   P{i+2} = {p2[:titik]} | {p2[titik:]}")
                    print(f"   C{i+1} = {p1[:titik]} + {p2[titik:]} = {c1}")
                    print(f"   C{i+2} = {p2[:titik]} + {p1[titik:]} = {c2}")
            else:
                c1, c2 = p1, p2
                if tampil:
                    print(f"   r = {r:.4f} >= PC({PC}) -> TIDAK terjadi cross over (anak = salinan orang tua)")
                    print(f"   C{i+1} = {c1}")
                    print(f"   C{i+2} = {c2}")
            anak.extend([c1, c2])
            i += 2

        if i < len(ortu):  # jika jumlah orang tua ganjil
            anak.append(ortu[i])
            if tampil:
                print(f"\n P{i+1} tidak berpasangan -> disalin langsung menjadi C{i+1} = {ortu[i]}")

        self.keturunan = anak
        self.hasil_mutasi = []
        if tampil:
            print("\n Hasil cross over (keturunan):")
            for idx, c in enumerate(anak, 1):
                print(f"   C{idx} = {c}")

    # ---------------------------- MUTASI ----------------------------
    def mutasi(self, tampil=True):
        hasil = [list(k) for k in self.keturunan]
        n_krom = len(hasil)
        panjang = len(self.target)
        total_gen = n_krom * panjang
        jumlah = max(1, round(PM * total_gen))
        if tampil:
            print(f" Total gen populasi = {n_krom} kromosom x {panjang} gen = {total_gen}")
            print(f" Jumlah mutasi      = round(PM x total gen) = round({PM} x {total_gen}) = {jumlah}")
            print(" Cara: pilih kromosom & posisi gen secara acak, ganti dengan huruf acak baru.\n")

        for m in range(jumlah):
            ik = random.randrange(n_krom)
            ig = random.randrange(panjang)
            lama = hasil[ik][ig]
            baru = random.choice([c for c in GEN_ALFABET if c != lama])
            sebelum = "".join(hasil[ik])
            hasil[ik][ig] = baru
            if tampil:
                print(f" Mutasi-{m+1}: C{ik+1} gen ke-{ig+1}: '{lama}' -> '{baru}'  ({sebelum} -> {''.join(hasil[ik])})")

        self.hasil_mutasi = ["".join(k) for k in hasil]
        if tampil:
            print("\n Hasil mutasi (calon generasi baru):")
            for i, k in enumerate(self.hasil_mutasi, 1):
                print(f"   M{i} = {k}")

    # ------------------------- GENERASI BARU ------------------------
    def generasi_baru(self, tampil=True, elitisme=False):
        populasi_baru = self.hasil_mutasi[:]
        if elitisme:  # dipakai pada mode otomatis agar cepat konvergen
            terbaik_lama = self.kromosom_terbaik()
            fit_lama = self.hitung_fitness(terbaik_lama)[2]
            fits_baru = [self.hitung_fitness(k)[2] for k in populasi_baru]
            if fit_lama > max(fits_baru):
                populasi_baru[fits_baru.index(min(fits_baru))] = terbaik_lama

        self.populasi = populasi_baru
        self.generasi += 1
        self.orang_tua = []
        self.keturunan = []
        self.hasil_mutasi = []

        if tampil:
            print(f" Populasi Generasi {self.generasi} (diambil dari hasil mutasi):")
            for i, k in enumerate(self.populasi, 1):
                print(f"   K{i} = {k}")
            print()
            print(" Evaluasi populasi baru:")
            self.tampilkan_fitness()
            print()
            if self.target_ditemukan():
                print(f" >>> TARGET '{self.target}' DITEMUKAN pada Generasi {self.generasi}! <<<")
                print(f" Arti kata: {KAMUS[self.target]}")
            else:
                print(" Status: kata target BELUM ditemukan.")
                print(" Ulangi menu 6 -> 7 -> 8 -> 9 untuk generasi berikutnya,")
                print(" atau gunakan menu 3 untuk menjalankan otomatis.")


# ===========================================================================
# FUNGSI-FUNGSI MENU
# ===========================================================================
def pastikan_target(ga):
    if not ga.target:
        print(" [!] Belum ada kata target. Gunakan menu 2 (Cari Kata) terlebih dahulu.")
        return False
    return True


def menu_tampilkan_kamus():
    print(GARIS)
    print(" KAMUS BAHASA MAKASSAR (DATASET)")
    print(GARIS)
    print(f" {'No':<4}| {'Kata':<10} | Arti")
    print(" " + "-" * 45)
    for i, (kata, arti) in enumerate(KAMUS.items(), 1):
        print(f" {i:<4}| {kata:<10} | {arti}")
    print(" " + "-" * 45)
    print(f" Jumlah kata: {len(KAMUS)}")


def menu_cari_kata(ga):
    print(GARIS)
    print(" CARI KATA DALAM KAMUS")
    print(GARIS)
    kata = input(" Masukkan kata yang dicari: ").strip().upper()
    if not kata:
        print(" [!] Kata tidak boleh kosong.")
        return
    if kata in KAMUS:
        print(f"\n Kata '{kata}' DITEMUKAN dalam kamus!")
        print(f" Arti: {KAMUS[kata]}")
        ga.set_target(kata)
        print(f"\n Kata '{kata}' ditetapkan sebagai TARGET Algoritma Genetika.")
        print(f" Populasi awal (Generasi 0) dibangkitkan acak sebanyak {UKURAN_POPULASI} kromosom:")
        for i, k in enumerate(ga.populasi, 1):
            print(f"   K{i} = {k}")
        print("\n Lanjutkan: menu 5 (fitness) -> 6 -> 7 -> 8 -> 9, atau menu 3 (otomatis).")
    else:
        print(f"\n [!] Kata '{kata}' TIDAK ditemukan dalam kamus.")
        mirip = [k for k in KAMUS if kata in k or k[:2] == kata[:2]]
        if mirip:
            print(" Mungkin maksud Anda: " + ", ".join(mirip))


def menu_jalankan_ga(ga):
    if not pastikan_target(ga):
        return
    print(GARIS)
    print(f" JALANKAN ALGORITMA GENETIKA - TARGET: {ga.target}")
    print(GARIS)
    if ga.target_ditemukan():
        print(f" Target '{ga.target}' sudah ditemukan pada generasi {ga.generasi}.")
        print(" Gunakan menu 2 untuk memilih kata lain.")
        return

    masukan = input(f" Jumlah generasi maksimal [{MAKS_GENERASI}]: ").strip()
    maks = int(masukan) if masukan.isdigit() and int(masukan) > 0 else MAKS_GENERASI
    print(f" Parameter: populasi={UKURAN_POPULASI}, PC={PC}, PM={PM}, elitisme=aktif")
    print(" " + "-" * 68)

    terbaik = ga.kromosom_terbaik()
    fit_terbaik = ga.hitung_fitness(terbaik)[2]
    print(f" Generasi {ga.generasi:4d} | Terbaik: {terbaik} | Fitness: {fit_terbaik:.4f} (awal)")

    ditemukan = False
    for _ in range(maks):
        ga.seleksi_roulette(tampil=False)
        ga.crossover(tampil=False)
        ga.mutasi(tampil=False)
        ga.generasi_baru(tampil=False, elitisme=True)

        terbaik = ga.kromosom_terbaik()
        cocok, _e, fit = ga.hitung_fitness(terbaik)
        if fit > fit_terbaik or ga.generasi % 50 == 0:
            fit_terbaik = max(fit_terbaik, fit)
            print(f" Generasi {ga.generasi:4d} | Terbaik: {terbaik} | Gen cocok: {cocok}/{len(ga.target)} | Fitness: {fit:.4f}")
        if ga.target_ditemukan():
            ditemukan = True
            break

    print(" " + "-" * 68)
    if ditemukan:
        print(f" >>> KATA '{ga.target}' DITEMUKAN pada Generasi {ga.generasi}! <<<")
        print(f" Arti kata: {KAMUS[ga.target]}")
    else:
        terbaik = ga.kromosom_terbaik()
        cocok, _e, fit = ga.hitung_fitness(terbaik)
        print(f" Batas {maks} generasi tercapai, kata belum ditemukan.")
        print(f" Terbaik saat ini: {terbaik} (gen cocok {cocok}/{len(ga.target)}, fitness {fit:.4f})")
        print(" Pilih menu 3 lagi untuk melanjutkan evolusi.")


def menu_tampilkan_populasi(ga):
    if not pastikan_target(ga):
        return
    print(GARIS)
    print(f" POPULASI GENERASI {ga.generasi} (Target: {ga.target})")
    print(GARIS)
    for i, k in enumerate(ga.populasi, 1):
        print(f" K{i} = {k}")
    if ga.orang_tua:
        print("\n Hasil seleksi roulette (orang tua):")
        for i, k in enumerate(ga.orang_tua, 1):
            print(f" P{i} = {k}")
    if ga.keturunan:
        print("\n Hasil cross over (keturunan):")
        for i, k in enumerate(ga.keturunan, 1):
            print(f" C{i} = {k}")
    if ga.hasil_mutasi:
        print("\n Hasil mutasi (calon generasi baru):")
        for i, k in enumerate(ga.hasil_mutasi, 1):
            print(f" M{i} = {k}")


def menu_hasil_fitness(ga):
    if not pastikan_target(ga):
        return
    print(GARIS)
    print(f" HASIL PERHITUNGAN FITNESS - GENERASI {ga.generasi}")
    print(f" Target: {ga.target}")
    print(" Rumus : fitness = 1 / (1 + error), error = jumlah gen yang salah")
    print(GARIS)
    ga.tampilkan_fitness()


def menu_seleksi(ga):
    if not pastikan_target(ga):
        return
    print(GARIS)
    print(f" SELEKSI ROULETTE WHEEL - GENERASI {ga.generasi} (Target: {ga.target})")
    print(GARIS)
    ga.seleksi_roulette(tampil=True)


def menu_crossover(ga):
    if not pastikan_target(ga):
        return
    if not ga.orang_tua:
        print(" [!] Belum ada hasil seleksi. Jalankan menu 6 (Seleksi Roulette) dahulu.")
        return
    print(GARIS)
    print(f" CROSS OVER - GENERASI {ga.generasi} (Target: {ga.target})")
    print(GARIS)
    ga.crossover(tampil=True)


def menu_mutasi(ga):
    if not pastikan_target(ga):
        return
    if not ga.keturunan:
        print(" [!] Belum ada hasil cross over. Jalankan menu 7 (Cross Over) dahulu.")
        return
    print(GARIS)
    print(f" MUTASI - GENERASI {ga.generasi} (Target: {ga.target})")
    print(GARIS)
    ga.mutasi(tampil=True)


def menu_generasi_baru(ga):
    if not pastikan_target(ga):
        return
    if not ga.hasil_mutasi:
        print(" [!] Belum ada hasil mutasi. Jalankan menu 8 (Mutasi) dahulu.")
        return
    print(GARIS)
    print(f" PEMBENTUKAN GENERASI BARU (Generasi {ga.generasi} -> {ga.generasi + 1})")
    print(GARIS)
    ga.generasi_baru(tampil=True)


def tampilkan_menu(ga):
    print()
    print(GARIS)
    print("                === Kamus Bahasa Daerah ===")
    print("                    (Bahasa Makassar)")
    print(GARIS)
    if ga.target:
        status = "YA" if ga.target_ditemukan() else "BELUM"
        print(f" Target: {ga.target} | Generasi: {ga.generasi} | Ditemukan: {status}")
    else:
        print(" Target: (belum dipilih - gunakan menu 2 untuk mencari kata)")
    print(GARIS)
    print("  1. Tampilkan Kamus")
    print("  2. Cari Kata")
    print("  3. Jalankan Algoritma Genetika")
    print("  4. Tampilkan Populasi")
    print("  5. Hasil Fitness")
    print("  6. Seleksi Roulette")
    print("  7. Cross Over")
    print("  8. Mutasi")
    print("  9. Generasi Baru")
    print(" 10. Keluar")
    print(GARIS)


def main():
    ga = AlgoritmaGenetika()
    while True:
        tampilkan_menu(ga)
        pilih = input(" Pilih menu [1-10]: ").strip()
        print()
        if pilih == "1":
            menu_tampilkan_kamus()
        elif pilih == "2":
            menu_cari_kata(ga)
        elif pilih == "3":
            menu_jalankan_ga(ga)
        elif pilih == "4":
            menu_tampilkan_populasi(ga)
        elif pilih == "5":
            menu_hasil_fitness(ga)
        elif pilih == "6":
            menu_seleksi(ga)
        elif pilih == "7":
            menu_crossover(ga)
        elif pilih == "8":
            menu_mutasi(ga)
        elif pilih == "9":
            menu_generasi_baru(ga)
        elif pilih == "10":
            print(" Terima kasih. Program selesai.")
            break
        else:
            print(" [!] Pilihan tidak valid. Masukkan angka 1-10.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n Program dihentikan.")
