# PG Gold Tracker

Static GitHub Pages dashboard untuk menjejak **Public Gold GAP 24K (RM/gram)**.

## Cara ia berfungsi

1. GitHub Actions mengambil halaman Public Gold.
2. Scraper mencari harga **GOLD GAP ACCOUNT 24K**.
3. `data/gold.json` dikemas kini dan commit hanya apabila ada perubahan.
4. `index.html` membaca data itu secara client-side dan mengira:
   - harga terkini
   - purata 30/90 hari
   - low/high 30 hari
   - Buy Score
   - paras BUY / STRONG BUY / VERY STRONG

GAP dan harga fizikal Public Gold adalah produk/harga berbeza. Buy Score di sini hanyalah indikator matematik berdasarkan sejarah yang dikumpul, bukan nasihat kewangan.

## GitHub Pages

Pastikan Pages menggunakan branch **index.html** dan folder **/** (root).

## Nota scraper

Scraper menggunakan halaman Public Gold yang diketahui memaparkan GAP 24K. Struktur laman boleh berubah pada masa hadapan; jika Public Gold mengubah HTML, regex scraper mungkin perlu disesuaikan.
