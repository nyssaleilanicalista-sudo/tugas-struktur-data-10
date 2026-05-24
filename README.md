# Advanced Sorting & Binary Tree — Implementasi Python

Proyek ini mengimplementasikan algoritma sorting lanjutan (Bab 12) dan struktur binary tree (Bab 13) dalam satu file Python tunggal: `advanced_sorter.py`.

---

## Daftar Isi

1. [Struktur File](#struktur-file)
2. [Cara Menjalankan](#cara-menjalankan)
3. [Modul 1 – Array Merge Sort](#modul-1--array-merge-sort)
4. [Modul 2 – Linked List Merge Sort](#modul-2--linked-list-merge-sort)
5. [Modul 3 – Quick Sort Median-of-Three](#modul-3--quick-sort-median-of-three)
6. [Modul 4 – Expression Tree](#modul-4--expression-tree)
7. [Modul 5 – In-Place Heapsort](#modul-5--in-place-heapsort)
8. [Modul 6 – Complete Tree Validator](#modul-6--complete-tree-validator)
9. [Jawaban Pertanyaan Analisis](#jawaban-pertanyaan-analisis)
10. [Kompleksitas Ringkasan](#kompleksitas-ringkasan)

---

## Struktur File

```
advanced_sorter.py   ← satu-satunya file implementasi
README.md            ← dokumen ini
```

---

## Cara Menjalankan

Tidak memerlukan library eksternal. Cukup Python 3.7+.

```bash
python advanced_sorter.py
```

Output yang diharapkan:

```
[1] Array Merge Sort
  Sebelum : [23, 10, 18, 51, 5, 13, 31, 54, 48, 62, 29, 8, 37]
  Sesudah : [5, 8, 10, 13, 18, 23, 29, 31, 37, 48, 51, 54, 62]

[4] Expression Tree – ((8*5)+(9/(7-4)))
  Hasil evaluasi : 43.0
  ...
```

---

## Modul 1 – Array Merge Sort

**Kelas:** `AdvancedSorter` → metode `sort_array()`

### Cara Kerja

Mengimplementasikan Improved Merge Sort dari **Listing 12.2 & 12.4** buku:

1. **`sort_array(arr)`** mengalokasikan **satu** `tmp_array` berukuran `n` di awal, lalu memanggil `_rec_merge_sort`.
2. **`_rec_merge_sort(arr, first, last, tmp_array)`** membagi secara rekursif menggunakan indeks virtual (tidak membuat sublist fisik).
3. **`_merge_virtual(arr, left_start, mid, right_end, tmp_array)`** menggabungkan dua virtual sublist bersebelahan dengan menyimpan hasil sementara di `tmp_array`, lalu menyalinnya kembali.

### Keunggulan vs Versi Slice

| Aspek | Versi Slice (Listing 12.1) | Versi Virtual (Listing 12.2) |
|---|---|---|
| Alokasi memori | O(n) **per rekursi** | O(n) **sekali** saja |
| Sublist fisik | Dibuat tiap split | Tidak ada, pakai indeks |
| Kompatibilitas | Hanya Python list | Array atau list |

### Stabilitas

Menggunakan `<=` saat perbandingan: jika `arr[a] == arr[b]`, elemen dari sublist kiri (posisi asli lebih awal) diambil terlebih dahulu.

### Kompleksitas

- **Waktu:** O(n log n) semua kasus
- **Ruang:** O(n) untuk `tmp_array` + O(log n) untuk stack rekursi

---

## Modul 2 – Linked List Merge Sort

**Kelas:** `AdvancedSorter` → metode `sort_linked_list()`

### Cara Kerja (sesuai Listing 12.8)

#### `_split_linked_list()` – Fast-Slow Pointer

Menemukan titik tengah dalam **satu kali traversal** tanpa menghitung panjang list:

```
midPoint → bergerak 1 langkah per iterasi   (pointer lambat)
curNode  → bergerak 2 langkah per iterasi   (pointer cepat)
```

Ketika `curNode` mencapai ujung list, `midPoint` berada tepat di **node tengah**.
Link `midPoint.next = None` memutus list menjadi dua sublist independen.

**Mengapa ini benar?** Karena rasio kecepatan 2:1, ketika fast pointer menempuh n langkah, slow pointer baru menempuh n/2 langkah — tepat di tengah.

#### `_merge_linked_lists()` – Dummy Node & Tail Reference

- **Dummy node:** menghilangkan penanganan khusus untuk node pertama hasil merge.
- **Tail reference:** memungkinkan append O(1) tanpa menelusuri ulang list.
- **Tidak mengalokasikan node baru** — hanya memodifikasi pointer `.next` dari node yang sudah ada.
- Bersifat **stable** karena menggunakan `<=` (listA diutamakan jika nilai sama).

### Kompleksitas

- **Waktu:** O(n log n)
- **Ruang:** O(log n) untuk stack rekursi (jauh lebih baik dari versi array yang butuh O(n) tmpArray)

---

## Modul 3 – Quick Sort Median-of-Three

**Kelas:** `AdvancedSorter` → metode `sort_quick()`

### Pemilihan Pivot: Median-of-Three

```
Kandidat: arr[first], arr[mid], arr[last]
Hasil:    arr[first] ← nilai median dari ketiganya
```

Strategi ini menghindari kasus terburuk O(n²) yang terjadi ketika:
- Data sudah terurut menaik/menurun dan pivot dipilih dari elemen pertama/terakhir.
- Setiap partisi menghasilkan satu segmen kosong dan satu berisi n-1 elemen.

### Depth-Limited Fallback

```python
max_depth = int(2 * math.log2(n))
```

Jika kedalaman rekursi melebihi batas ini, algoritma otomatis beralih ke **Merge Sort** untuk subarray tersebut. Ini mencegah O(n²) pada data patologis yang lolos dari median-of-three.

### Mengapa Median-of-Three Sulit di Linked List

Pada linked list, mengakses elemen tengah memerlukan O(n) traversal (tidak ada random access). Biaya menghitung tiga kandidat pivot menjadi O(n), yang mengurangi efisiensi keseluruhan. Solusi praktis untuk linked list adalah tetap menggunakan **Merge Sort** (sudah diimplementasikan di Modul 2).

---

## Modul 4 – Expression Tree

**Kelas:** `ExprHeapSorter` → metode `parse_and_evaluate()`

### Format Input

Ekspresi **fully parenthesized** (setiap operator diapit tanda kurung):

```
((8*5)+(9/(7-4)))
```

### Cara Kerja `_build_tree()` (Listing 13.9)

Menggunakan `deque` sebagai antrian token dan rekursi:

| Token | Aksi |
|---|---|
| `(` | Buat node, rekursi ke kiri, baca operator, rekursi ke kanan, konsumsi `)` |
| digit/huruf | Buat node daun, kembalikan |
| `)` | Dikonsumsi oleh pemanggil |

### Traversal & Notasi

| Traversal | Notasi yang Dihasilkan | Perlu Kurung? |
|---|---|---|
| Postorder | Postfix (valid langsung) | Tidak |
| Inorder | Infix (tapi tanpa kurung) | Ya (seperti Listing 13.7) |
| Preorder | Prefix (valid langsung) | Tidak |

Postorder menghasilkan postfix yang valid secara otomatis karena operator ditempatkan **setelah** kedua operandnya diproses — sesuai urutan evaluasi bottom-up.

### Contoh Evaluasi

```
((8*5)+(9/(7-4))) → 40 + (9/3) → 40 + 3 → 43
```

### Error Handling

- **Pembagian nol:** melempar `ValueError`
- **Token tidak valid:** melempar `ValueError`

---

## Modul 5 – In-Place Heapsort

**Kelas:** `ExprHeapSorter` → metode `heapsort_inplace()`

### Dua Fase (Listing 13.12)

**Fase 1 – Bangun Max-Heap:**
```
Iterasi dari n//2 - 1 turun ke 0, panggil sift_down pada tiap indeks.
```
Pendekatan bottom-up ini lebih efisien dari memasukkan elemen satu per satu (O(n) vs O(n log n) untuk fase pembangunan).

**Fase 2 – Ekstraksi:**
```
for end = n-1 turun ke 1:
    tukar arr[0] (maksimum) ↔ arr[end]
    sift_down(arr, end, 0)   ← heap mengecil, elemen terurut mengumpul di kanan
```

### `_sift_down()` – Iteratif

Implementasi iteratif (bukan rekursif) untuk efisiensi:
```python
while True:
    largest = idx
    if arr[left] > arr[largest]: largest = left
    if arr[right] > arr[largest]: largest = right
    if largest == idx: break
    arr[idx], arr[largest] = arr[largest], arr[idx]
    idx = largest
```

**Jumlah perbandingan maksimum per sift-down:** 2 × h = 2 × log₂(n)

### Perbandingan Simple vs In-Place Heapsort

| Aspek | Simple (Listing 13.11) | In-Place (Listing 13.12) |
|---|---|---|
| Ruang tambahan | O(n) untuk MaxHeap | O(1) — hanya variabel indeks |
| Cache locality | Buruk (dua array berbeda) | Baik (satu array kontigu) |
| Risiko overflow | Tinggi (alokasi heap besar) | Minimal |
| Kompleksitas waktu | O(n log n) | O(n log n) |

---

## Modul 6 – Complete Tree Validator

**Kelas:** `ExprHeapSorter` → metode `is_complete_tree()`

### Definisi Complete Binary Tree

Pohon biner disebut complete jika:
1. Semua level kecuali yang terbawah penuh.
2. Level terbawah diisi dari kiri ke kanan tanpa celah.

### Cara Validasi via Array

Dengan pemetaan array (heap representation):
- Node di indeks `i` → anak kiri di `2i+1`, anak kanan di `2i+2`.
- Jika ditemukan "slot kosong" (indeks melebihi n), tidak boleh ada node valid di indeks yang lebih besar.

Algoritma: tandai `found_none = True` begitu menemukan node tanpa anak kiri. Jika setelah itu ada node beranak → **bukan complete tree**.

---

## Jawaban Pertanyaan Analisis

### a. Mengapa Radix Sort tidak memenuhi O(1) untuk Modul A?

Radix Sort standar menggunakan **10 queue** (satu per digit 0–9). Setiap queue dapat menampung hingga n elemen, sehingga total ruang tambahan adalah **O(n + k)** di mana k = 10. Ini melanggar batasan O(1) Modul A.

**Improved Merge Sort menekan overhead** karena hanya mengalokasikan **satu** `tmpArray` berukuran n di awal, bukan array baru di setiap rekursi seperti versi slice.

**Alternatif Radix Sort dengan O(1)?** Tidak ada versi murni — sifat distribusi digit secara inheren membutuhkan bucket/queue. Satu-satunya pendekatan adalah menggunakan **American Flag Sort** (in-place radix) yang menggunakan penghitungan frekuensi (O(k) ruang konstan untuk k digit), tetapi kompleksitas waktunya tetap O(dn) dengan konstanta lebih besar.

### b. Fast-Slow Pointer untuk titik tengah

Rasio kecepatan 2:1 antara `curNode` dan `midPoint` menjamin bahwa ketika fast pointer menempuh seluruh list, slow pointer ada di tepat tengah. Dummy node pada `_merge_linked_lists` menghilangkan edge case penanganan node pertama, sehingga tidak perlu alokasi memori tambahan — hanya menggeser pointer yang sudah ada.

### c. Quick Sort worst-case pada data descending

Dengan pivot = elemen pertama dan data descending [n, n-1, ..., 1]:
- Setiap partisi: pivot (terkecil) tidak bertukar, segmen kiri kosong, segmen kanan berisi n-1 elemen.
- Kedalaman rekursi: n → rekursi stack O(n).
- Jumlah total perbandingan: n + (n-1) + ... + 1 = O(n²).

Median-of-three memilih nilai tengah sebagai pivot, sehingga kedua segmen seimbang → kedalaman rekursi kembali ke O(log n).

### d. Radix Sort tidak melanggar batas Ω(n log n)

Batas bawah Ω(n log n) hanya berlaku untuk **comparison sort** (algoritma yang hanya menggunakan perbandingan <, >, =). Radix Sort bukan comparison sort — ia mengakses **struktur internal** digit kunci, bukan membandingkan kunci secara keseluruhan. Dua asumsi implisit yang membuatnya "melampaui" batas:
1. **k terbatas** (digit 0–9, atau karakter ASCII) — jumlah bucket konstan.
2. **d terbatas** (jumlah digit maksimum kecil, misalnya d ≤ 10 untuk integer 32-bit) — jumlah pass konstan.

Jika k atau d tumbuh seiring n (misalnya kunci berupa string panjang), kompleksitas efektifnya bisa melebihi O(n log n).

---

## Kompleksitas Ringkasan

| Algoritma | Waktu | Ruang Tambahan | Stabil |
|---|---|---|---|
| Array Merge Sort | O(n log n) | O(n) tmpArray | Ya |
| Linked List Merge Sort | O(n log n) | O(log n) stack | Ya |
| Quick Sort (median-of-3) | O(n log n) avg | O(log n) stack | Tidak |
| Quick Sort worst-case | O(n²) → fallback O(n log n) | O(log n) | Tidak |
| Heapsort In-Place | O(n log n) | O(1) | Tidak |
| Expression Tree Build | O(n) token | O(h) stack | — |
| Expression Tree Eval | O(n) node | O(h) stack | — |
