# Algoritma Genetika — Pencarian Kata pada Kamus Bahasa Makassar

Implementasi Genetic Algorithm (GA) untuk mencari kata dalam kamus bahasa daerah
(Bahasa Makassar). Dataset berisi 10 kata beserta artinya.

## Cara Menjalankan

```bash
python ga_kamus_makassar.py
```

## Dataset (10 Kata Bahasa Makassar)

| No | Kata    | Arti                |
|----|---------|---------------------|
| 1  | JAPPA   | Jalan / Berjalan    |
| 2  | JARANG  | Kuda                |
| 3  | KASA    | Kain                |
| 4  | KANA    | Kata / Ucapan       |
| 5  | KANRE   | Nasi / Makanan      |
| 6  | SAKRA   | Suara               |
| 7  | SASSA   | Mencuci             |
| 8  | SAMBUNG | Menyambung          |
| 9  | LAMPA   | Pergi / Berangkat   |
| 10 | LAMPU   | Lampu / Penerangan  |

## Parameter Algoritma Genetika

| Parameter                    | Nilai                                   |
|------------------------------|-----------------------------------------|
| Ukuran populasi              | 6 kromosom                              |
| Gen                          | Huruf A–Z                               |
| Panjang kromosom             | Sama dengan panjang kata target         |
| Fitness                      | `1 / (1 + error)`                       |
| Seleksi                      | Roulette Wheel                          |
| Cross over                   | Satu titik potong, PC = 0.8             |
| Mutasi                       | `jumlah = round(PM × total gen)`, PM = 0.1 |
| Elitisme                     | Aktif pada mode otomatis (menu 3)       |

## Menu Program

```
=== Kamus Bahasa Daerah ===
1. Tampilkan Kamus
2. Cari Kata
3. Jalankan Algoritma Genetika
4. Tampilkan Populasi
5. Hasil Fitness
6. Seleksi Roulette
7. Cross Over
8. Mutasi
9. Generasi Baru
10. Keluar
```

## Tahapan Algoritma Genetika

1. **Inisialisasi** — kata yang dicari (menu 2) menjadi target; populasi awal
   berupa 6 kromosom huruf acak sepanjang kata target.
2. **Fitness** — `error` = jumlah gen yang tidak cocok dengan target,
   `fitness = 1 / (1 + error)`.
3. **Seleksi Roulette** — `P[i] = fitness[i] / total_fitness`, hitung
   kumulatif, putar roulette dengan bilangan acak `r` untuk memilih orang tua.
4. **Cross Over** — pasangan orang tua dipotong pada satu titik acak lalu
   ekornya dipertukarkan (jika `r < PC`).
5. **Mutasi** — sebanyak `round(PM × total gen)` gen dipilih acak dan diganti
   huruf acak baru.
6. **Generasi Baru** — hasil mutasi menjadi populasi generasi berikutnya lalu
   dievaluasi ulang; proses berulang sampai kata target ditemukan.

## Alur Pengambilan Data untuk Laporan

1. Menu **2** — cari kata (mis. `LAMPA`) → screenshot populasi awal (Generasi 0)
2. Menu **5** — perhitungan fitness → screenshot
3. Menu **6** — perhitungan seleksi roulette → screenshot
4. Menu **7** — perhitungan cross over → screenshot
5. Menu **8** — perhitungan mutasi → screenshot
6. Menu **9** — hasil generasi ke-1 (populasi baru + evaluasi) → screenshot
7. Menu **3** — jalankan otomatis hingga kata ditemukan → screenshot hasil akhir
