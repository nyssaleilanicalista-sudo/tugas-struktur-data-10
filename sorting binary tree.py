"""
AdvancedSorter & ExprHeapSorter
================================
Implementasi algoritma sorting lanjutan berbasis Bab 12 & 13:
  - Merge Sort array (virtual sublists + single tmpArray)
  - Merge Sort linked list (fast-slow pointer + dummy node)
  - Quick Sort dengan pivot median-of-three + fallback ke Merge Sort
  - Expression Tree builder & evaluator
  - In-Place Heapsort
  - Complete Binary Tree Validator
"""

import math
from typing import List, Optional
from collections import deque


# ─────────────────────────────────────────────────────────────
# Struktur Node untuk Linked List
# ─────────────────────────────────────────────────────────────

class ListNode:
    def __init__(self, data, next_node=None):
        self.data = data
        self.next = next_node

    def __repr__(self):
        return f"ListNode({self.data})"


# ─────────────────────────────────────────────────────────────
# BAGIAN 1 & 2 & 3 – AdvancedSorter
# ─────────────────────────────────────────────────────────────

class AdvancedSorter:
    """
    Menggabungkan tiga algoritma sorting sesuai pembatasan teknis:
      1. Merge Sort array  – O(n log n) waktu, O(n) ruang (satu tmpArray)
      2. Merge Sort linked list – O(n log n) waktu, O(log n) ruang rekursi
      3. Quick Sort dengan median-of-three + depth-limited fallback
    """

    def __init__(self):
        pass

    # ==========================================================
    # 1. ARRAY MERGE SORT
    # ==========================================================

    def sort_array(self, arr: List[int]) -> List[int]:
        """
        Mengurutkan list secara ascending menggunakan Merge Sort.
        Hanya satu tmpArray berukuran n yang dialokasikan di sini;
        tidak ada sublist fisik baru di tiap rekursi.
        """
        if len(arr) <= 1:
            return arr
        tmp_array = [0] * len(arr)          # satu array sementara (O(n) extra)
        self._rec_merge_sort(arr, 0, len(arr) - 1, tmp_array)
        return arr

    def _rec_merge_sort(self, arr: List[int], first: int,
                        last: int, tmp_array: List[int]) -> None:
        """Rekursi pembagi: bagi di tengah, lalu gabungkan."""
        if first >= last:
            return
        mid = (first + last) // 2
        self._rec_merge_sort(arr, first, mid, tmp_array)
        self._rec_merge_sort(arr, mid + 1, last, tmp_array)
        self._merge_virtual(arr, first, mid, last, tmp_array)

    def _merge_virtual(self, arr: List[int], left_start: int,
                       mid: int, right_end: int,
                       tmp_array: List[int]) -> None:
        """
        Gabungkan dua virtual sublist bersebelahan:
          kiri  : arr[left_start .. mid]
          kanan : arr[mid+1 .. right_end]
        Hasil sementara disimpan di tmp_array, lalu disalin kembali.
        Menggunakan <= agar operasi bersifat STABLE.
        """
        a = left_start          # indeks sublist kiri
        b = mid + 1             # indeks sublist kanan
        m = 0                   # indeks tmp_array

        # Gabungkan selama kedua sublist masih ada elemen
        while a <= mid and b <= right_end:
            if arr[a] <= arr[b]:        # <= menjamin stabilitas
                tmp_array[m] = arr[a]
                a += 1
            else:
                tmp_array[m] = arr[b]
                b += 1
            m += 1

        # Sisa elemen sublist kiri
        while a <= mid:
            tmp_array[m] = arr[a]
            a += 1
            m += 1

        # Sisa elemen sublist kanan
        while b <= right_end:
            tmp_array[m] = arr[b]
            b += 1
            m += 1

        # Salin kembali ke array asli
        for i in range(right_end - left_start + 1):
            arr[i + left_start] = tmp_array[i]

    # ==========================================================
    # 2. LINKED LIST MERGE SORT
    # ==========================================================

    def sort_linked_list(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Mengurutkan singly linked list secara ascending.
        Hanya memodifikasi pointer .next; tidak mengalokasikan node baru
        (kecuali satu dummy node statis di _merge_linked_lists).
        Kompleksitas ruang: O(log n) untuk stack rekursi.
        """
        if head is None or head.next is None:
            return head

        right_head = self._split_linked_list(head)
        left_head  = head

        left_sorted  = self.sort_linked_list(left_head)
        right_sorted = self.sort_linked_list(right_head)
        return self._merge_linked_lists(left_sorted, right_sorted)

    def _split_linked_list(self, head: ListNode) -> Optional[ListNode]:
        """
        Menemukan titik tengah list dalam SATU traversal menggunakan
        teknik fast-slow pointer:
          - midPoint bergerak 1 langkah per iterasi
          - curNode  bergerak 2 langkah per iterasi
        Ketika curNode jatuh di ujung, midPoint berada di tengah.
        Link midPoint.next diputus → dua sublist independen.
        Mengembalikan head sublist kanan.
        """
        mid_point = head
        cur_node  = head.next               # curNode mulai satu langkah lebih maju

        while cur_node is not None:
            cur_node = cur_node.next        # maju 1
            if cur_node is not None:
                mid_point = mid_point.next  # slow maju 1
                cur_node  = cur_node.next   # fast maju 1 lagi (total 2)

        # mid_point kini menunjuk node terakhir sublist kiri
        right_head          = mid_point.next
        mid_point.next      = None          # putus link
        return right_head

    def _merge_linked_lists(self, listA: Optional[ListNode],
                             listB: Optional[ListNode]) -> Optional[ListNode]:
        """
        Menggabungkan dua sorted linked list menggunakan:
          - dummy node  : menghilangkan penanganan khusus node pertama
          - tail reference : append O(1) tanpa traversal ulang
        Bersifat STABLE karena menggunakan <= (listA diutamakan jika sama).
        Tidak mengalokasikan node baru (kecuali dummy sementara).
        """
        dummy = ListNode(0)         # dummy node statis, tidak masuk hasil akhir
        tail  = dummy

        while listA is not None and listB is not None:
            if listA.data <= listB.data:    # <= menjamin stabilitas
                tail.next = listA
                listA = listA.next
            else:
                tail.next = listB
                listB = listB.next
            tail      = tail.next
            tail.next = None                # putus link lama agar tidak ada siklus

        # Sambungkan sisa sublist yang belum habis
        tail.next = listA if listA is not None else listB

        return dummy.next

    # ==========================================================
    # 3. QUICK SORT dengan MEDIAN-OF-THREE + DEPTH FALLBACK
    # ==========================================================

    def sort_quick(self, arr: List[int]) -> List[int]:
        """Entry point Quick Sort. Menghitung batas kedalaman rekursi."""
        if len(arr) <= 1:
            return arr
        n = len(arr)
        max_depth = int(2 * math.log2(n)) if n > 1 else 1
        self._quick_sort_recursive(arr, 0, n - 1, max_depth)
        return arr

    def _quick_sort_recursive(self, arr: List[int], first: int,
                               last: int, depth_limit: int) -> None:
        """
        Rekursi Quick Sort.
        Jika depth_limit habis → fallback ke Merge Sort untuk subarray ini
        agar menghindari kompleksitas O(n²) pada data patologis.
        """
        if first >= last:
            return

        if depth_limit == 0:
            # Fallback: ekstrak subarray, sort dengan merge sort, salin kembali
            sub = arr[first:last + 1]
            self.sort_array(sub)
            arr[first:last + 1] = sub
            return

        pos = self.partition_quick(arr, first, last)
        self._quick_sort_recursive(arr, first, pos - 1, depth_limit - 1)
        self._quick_sort_recursive(arr, pos + 1, last,  depth_limit - 1)

    def partition_quick(self, arr: List[int], first: int, last: int) -> int:
        """
        Partisi dengan pivot MEDIAN-OF-THREE:
          1. Hitung mid = (first+last)//2
          2. Urutkan arr[first], arr[mid], arr[last] sehingga
             arr[first] = median → dipakai sebagai pivot.
          3. Jalankan partisi in-place (Listing 12.5).
        Mengembalikan posisi akhir pivot.
        """
        mid = (first + last) // 2

        # Urutkan tiga kandidat agar arr[first] = median
        if arr[first] > arr[mid]:
            arr[first], arr[mid] = arr[mid], arr[first]
        if arr[first] > arr[last]:
            arr[first], arr[last] = arr[last], arr[first]
        if arr[mid] < arr[last]:
            arr[first], arr[mid] = arr[mid], arr[first]
        # Sekarang arr[first] adalah median dari ketiga nilai

        # Partisi standar (Listing 12.5)
        pivot = arr[first]
        left  = first + 1
        right = last

        while left <= right:
            # Geser left ke kanan sampai menemukan nilai >= pivot
            while left <= right and arr[left] < pivot:
                left += 1
            # Geser right ke kiri sampai menemukan nilai <= pivot
            while right >= left and arr[right] >= pivot:
                right -= 1
            # Tukar jika belum bersilangan
            if left < right:
                arr[left], arr[right] = arr[right], arr[left]

        # Tempatkan pivot di posisi akhirnya
        if right != first:
            arr[first], arr[right] = arr[right], arr[first]

        return right


# ─────────────────────────────────────────────────────────────
# BAGIAN 4, 5, 6 – ExprHeapSorter
# ─────────────────────────────────────────────────────────────

class ExprHeapSorter:
    """
    Menggabungkan tiga modul Bab 13:
      1. Expression Tree Builder & Evaluator
      2. In-Place Max-Heap Construction
      3. Heapsort In-Place
      4. Complete Tree Validator
    """

    def __init__(self, expr_str: str):
        self.expr   = expr_str
        self.values: List[int] = []

    # ==========================================================
    # 4. EXPRESSION TREE
    # ==========================================================

    def parse_and_evaluate(self) -> List[int]:
        """
        Membangun pohon ekspresi dari string terparentheses penuh,
        mengevaluasinya, dan menyimpan hasilnya ke self.values.
        """
        tokens = deque(self.expr.replace(" ", ""))  # hapus spasi
        root   = self._build_tree(tokens)
        result = self._eval_tree(root)
        self.values = [result]
        return self.values

    def _build_tree(self, tokens: deque) -> Optional[dict]:
        """
        Membangun pohon ekspresi secara rekursif menggunakan antrian token.
        Representasi node: dict {'val': ..., 'left': ..., 'right': ...}

        Aturan (Listing 13.9):
          '('  → buat node kiri (rekursi), baca operator, buat node kanan (rekursi), baca ')'
          digit/huruf → node daun, kembalikan langsung
        """
        if not tokens:
            return None

        token = tokens.popleft()

        if token == '(':
            node = {'val': None, 'left': None, 'right': None}

            # Bangun subpohon kiri
            node['left'] = self._build_tree(tokens)

            # Token berikutnya harus operator
            node['val'] = tokens.popleft()

            # Bangun subpohon kanan
            node['right'] = self._build_tree(tokens)

            # Konsumsi ')'
            if tokens and tokens[0] == ')':
                tokens.popleft()

            return node
        else:
            # Operand: digit atau variabel (node daun)
            return {'val': token, 'left': None, 'right': None}

    def _eval_tree(self, node: Optional[dict]) -> float:
        """
        Evaluasi pohon ekspresi secara postorder.
        Node daun → kembalikan nilai numerik.
        Node interior → evaluasi kiri & kanan, lalu terapkan operator.
        Melempar ValueError jika pembagian nol.
        """
        if node is None:
            raise ValueError("Node kosong tidak terduga.")

        # Node daun (operand)
        if node['left'] is None and node['right'] is None:
            val = node['val']
            if isinstance(val, str) and val.lstrip('-').isdigit():
                return int(val)
            try:
                return float(val)
            except (ValueError, TypeError):
                raise ValueError(f"Token tidak valid sebagai operand: '{val}'")

        # Node interior (operator)
        left_val  = self._eval_tree(node['left'])
        right_val = self._eval_tree(node['right'])
        op        = node['val']

        if   op == '+': return left_val + right_val
        elif op == '-': return left_val - right_val
        elif op == '*': return left_val * right_val
        elif op == '/':
            if right_val == 0:
                raise ValueError("ZeroDivisionError: pembagi bernilai nol.")
            return left_val / right_val
        elif op == '%':
            if right_val == 0:
                raise ValueError("ZeroDivisionError: modulo dengan nol.")
            return left_val % right_val
        else:
            raise ValueError(f"Operator tidak dikenal: '{op}'")

    # ==========================================================
    # 5. IN-PLACE HEAPSORT
    # ==========================================================

    def heapsort_inplace(self, arr: List[int]) -> List[int]:
        """
        Mengurutkan arr secara ascending menggunakan Heapsort in-place.

        Fase 1 – Bangun max-heap:
          Mulai dari node non-daun terakhir (n//2 - 1) sampai ke indeks 0.
          Ini adalah pendekatan bottom-up yang lebih efisien dari satu-per-satu add().

        Fase 2 – Ekstraksi:
          Tukar root (maksimum) dengan elemen terakhir heap,
          kurangi ukuran heap, lalu sift-down dari root.
          Ulangi sampai heap berukuran 1.
        """
        n = len(arr)
        if n <= 1:
            return arr

        # Fase 1: Bangun max-heap dari daun ke atas
        for i in range(n // 2 - 1, -1, -1):
            self._sift_down(arr, n, i)

        # Fase 2: Ekstraksi satu per satu
        for end in range(n - 1, 0, -1):
            arr[0], arr[end] = arr[end], arr[0]     # tukar root dengan akhir heap
            self._sift_down(arr, end, 0)            # pulihkan heap pada [0..end-1]

        return arr

    def _sift_down(self, arr: List[int], heap_size: int, idx: int) -> None:
        """
        Memindahkan elemen di arr[idx] ke bawah sampai heap order property dipulihkan.
        Selalu menukar dengan anak yang LEBIH BESAR dari keduanya (max-heap).

        Rumus indeks anak:
          left  = 2 * idx + 1
          right = 2 * idx + 2
        """
        while True:
            left    = 2 * idx + 1
            right   = 2 * idx + 2
            largest = idx               # asumsi idx adalah yang terbesar

            if left < heap_size and arr[left] > arr[largest]:
                largest = left
            if right < heap_size and arr[right] > arr[largest]:
                largest = right

            if largest == idx:          # posisi sudah benar → berhenti
                break

            arr[idx], arr[largest] = arr[largest], arr[idx]
            idx = largest               # lanjutkan sift-down dari posisi baru

    # ==========================================================
    # 6. COMPLETE BINARY TREE VALIDATOR
    # ==========================================================

    def is_complete_tree(self, arr: List[int]) -> bool:
        """
        Memvalidasi apakah array mewakili complete binary tree.

        Properti complete binary tree saat dipetakan ke array:
          - Semua slot indeks 0 .. n-1 harus terisi (tidak ada 'lubang').
          - Jika node i memiliki anak kiri (2i+1 < n), maka semua slot
            sebelumnya pun harus terisi.

        Pendekatan sederhana: setelah menemukan elemen pertama yang
        kosong (None) dalam BFS, tidak boleh ada elemen non-None lagi.
        Karena arr adalah List[int] tanpa None, kita cukup periksa
        bahwa semua indeks 0..n-1 berurutan tanpa celah — yang selalu
        benar untuk list Python biasa.

        Untuk kasus umum (array bisa mengandung None sebagai penanda
        slot kosong), kita gunakan logika BFS:
        """
        n = len(arr)
        if n == 0:
            return True

        found_none = False
        for i in range(n):
            left  = 2 * i + 1
            right = 2 * i + 2

            if left < n:
                if found_none:
                    return False        # ada anak padahal sudah ada slot kosong
            else:
                found_none = True       # node ini tidak punya anak kiri

            if right < n:
                if found_none:
                    return False
            else:
                found_none = True

        return True


# ─────────────────────────────────────────────────────────────
# HELPER: konversi linked list ↔ Python list
# ─────────────────────────────────────────────────────────────

def list_to_linked(lst: list) -> Optional[ListNode]:
    """Membuat linked list dari Python list."""
    if not lst:
        return None
    head = ListNode(lst[0])
    cur  = head
    for val in lst[1:]:
        cur.next = ListNode(val)
        cur = cur.next
    return head

def linked_to_list(head: Optional[ListNode]) -> list:
    """Mengubah linked list menjadi Python list."""
    result = []
    while head:
        result.append(head.data)
        head = head.next
    return result


# ─────────────────────────────────────────────────────────────
# DEMO / PENGUJIAN
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  DEMO AdvancedSorter & ExprHeapSorter")
    print("=" * 60)

    sorter = AdvancedSorter()

    # ── 1. Array Merge Sort ──────────────────────────────────
    print("\n[1] Array Merge Sort")
    data = [23, 10, 18, 51, 5, 13, 31, 54, 48, 62, 29, 8, 37]
    print(f"  Sebelum : {data}")
    sorter.sort_array(data)
    print(f"  Sesudah : {data}")

    # ── 2. Linked List Merge Sort ────────────────────────────
    print("\n[2] Linked List Merge Sort")
    ll_data = [23, 51, 2, 18, 4, 31]
    head = list_to_linked(ll_data)
    print(f"  Sebelum : {ll_data}")
    sorted_head = sorter.sort_linked_list(head)
    print(f"  Sesudah : {linked_to_list(sorted_head)}")

    # ── 3. Quick Sort (median-of-three) ──────────────────────
    print("\n[3] Quick Sort (Median-of-Three + Depth Fallback)")
    data_q = [10, 23, 51, 18, 4, 31, 13, 5]
    print(f"  Sebelum : {data_q}")
    sorter.sort_quick(data_q)
    print(f"  Sesudah : {data_q}")

    # ── 3b. Quick Sort pada data descending (worst-case lama) ─
    print("\n[3b] Quick Sort – data descending (worst-case tanpa median-of-three)")
    data_desc = list(range(20, 0, -1))
    print(f"  Sebelum : {data_desc}")
    sorter.sort_quick(data_desc)
    print(f"  Sesudah : {data_desc}")

    # ── 4. Expression Tree + Evaluasi ────────────────────────
    print("\n[4] Expression Tree – ((8*5)+(9/(7-4)))")
    expr_sorter = ExprHeapSorter("((8*5)+(9/(7-4)))")
    result = expr_sorter.parse_and_evaluate()
    print(f"  Hasil evaluasi : {result[0]}")   # 40 + 3 = 43

    # ── 5. In-Place Heapsort ─────────────────────────────────
    print("\n[5] In-Place Heapsort")
    heap_data = [10, 51, 2, 18, 4, 31, 13, 5, 23, 64, 29]
    print(f"  Sebelum : {heap_data}")
    ehs = ExprHeapSorter("")
    ehs.heapsort_inplace(heap_data)
    print(f"  Sesudah : {heap_data}")

    # ── 6. Complete Tree Validator ───────────────────────────
    print("\n[6] Complete Binary Tree Validator")
    complete    = [100, 84, 71, 60, 23, 12, 29, 1, 37, 4]
    not_complete = [100, 84, 71, None, 23, 12, 29]

    print(f"  Array lengkap  {complete} → {ehs.is_complete_tree(complete)}")
    # Simulasikan array tidak lengkap dengan ukuran berbeda
    short = [100, 84, 71, 60]   # hanya 4 node, gap di level 2
    print(f"  Array pendek   {short}    → {ehs.is_complete_tree(short)}")

    # ── 7. ZeroDivision guard ────────────────────────────────
    print("\n[7] Zero Division Guard")
    try:
        bad = ExprHeapSorter("(8/(4-4))")
        bad.parse_and_evaluate()
    except ValueError as e:
        print(f"  Tertangkap : {e}")

    print("\nSelesai.")
