import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from PIL import Image, ImageDraw
import math
import os

# ====== Tema Warna ======
PRIMARY = "#10B981"
PRIMARY_HOVER = "#059669"
PRIMARY_LIGHT = "#D1FAE5"
SECONDARY = "#6B7280"
SECONDARY_HOVER = "#4B5563"
DANGER = "#EF4444"
DANGER_HOVER = "#DC2626"
WARNING = "#F59E0B"
CARD_BG = "#FFFFFF"
CARD_BG_DARK = "#1F2937"
TEXT_MUTED = "#6B7280"
TEXT_MAIN = "#111827"

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green")


def rupiah(angka):
    return "Rp " + f"{angka:,.0f}".replace(",", ".")


# =========================================================================
# CARI FILE LOGO
# =========================================================================
def cari_logo(nama="logo.png"):
    if "__file__" in globals():
        base_dir = os.path.dirname(os.path.abspath(__file__))
    else:
        base_dir = os.getcwd()

    kandidat = [
        os.path.join(base_dir, "images", nama),
        os.path.join(os.getcwd(), "images", nama),
        os.path.join(base_dir, nama),
        os.path.join(os.getcwd(), nama),
    ]
    for p in kandidat:
        if p and os.path.exists(p):
            return p
    return None


# =========================================================================
# IKON
# =========================================================================
def buat_ikon(bentuk, ukuran=20, warna="white"):
    scale = 4
    s = ukuran * scale
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    w = max(2, s // 12)

    if bentuk == "gear":
        cx = cy = s // 2
        r = s // 2 - 3 * scale
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            x1 = cx + int(r * math.cos(rad))
            y1 = cy + int(r * math.sin(rad))
            x2 = cx + int((r + 2 * scale) * math.cos(rad))
            y2 = cy + int((r + 2 * scale) * math.sin(rad))
            d.line([x1, y1, x2, y2], fill=warna, width=w)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=warna, width=w)
        d.ellipse([cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2],
                  outline=warna, width=w)

    elif bentuk == "trash":
        pad = 3 * scale
        d.rectangle([pad + scale, pad * 2, s - pad - scale, s - pad],
                    outline=warna, width=w)
        d.line([pad, pad * 2, s - pad, pad * 2], fill=warna, width=w)
        cx = s // 2
        d.line([cx - 2 * scale, pad, cx + 2 * scale, pad], fill=warna, width=w)
        for dx in [-3, 0, 3]:
            x = cx + dx * scale
            d.line([x, pad * 2 + 2 * scale, x, s - pad - 2 * scale],
                   fill=warna, width=max(1, w - 2))

    elif bentuk == "print":
        pad = 3 * scale
        d.rectangle([pad + scale, pad, s - pad - scale, pad * 3],
                    outline=warna, width=w)
        d.rectangle([pad, pad * 3, s - pad, s - pad * 2],
                    outline=warna, width=w)
        d.rectangle([pad + 2 * scale, s - pad * 3, s - pad - 2 * scale, s - pad],
                    outline=warna, width=w)

    elif bentuk == "clock":
        cx = cy = s // 2
        r = s // 2 - 2 * scale
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=warna, width=w)
        d.line([cx, cy, cx, cy - r // 2], fill=warna, width=w)
        d.line([cx, cy, cx + r // 2, cy], fill=warna, width=w)

    elif bentuk == "cart":
        pad = 2 * scale
        d.line([pad, pad, pad + 2 * scale, pad], fill=warna, width=w)
        d.line([pad + 2 * scale, pad, pad + 4 * scale, s - 6 * scale],
               fill=warna, width=w)
        d.line([pad + 4 * scale, s - 6 * scale, s - pad, s - 6 * scale],
               fill=warna, width=w)
        d.ellipse([pad + 3 * scale, s - 4 * scale,
                   pad + 5 * scale, s - 2 * scale], fill=warna)
        d.ellipse([s - pad - 6 * scale, s - 4 * scale,
                   s - pad - 4 * scale, s - 2 * scale], fill=warna)

    elif bentuk == "apple":
        cx = s // 2
        cy = s // 2 + scale
        r = s // 3
        d.ellipse([cx - r, cy - r // 2, cx + r, cy + r * 1.2], fill=PRIMARY)
        d.ellipse([cx - scale, cy - r, cx + 3 * scale, cy - r // 2],
                  fill="#22C55E")
        d.line([cx, cy - r, cx, cy - r - 2 * scale],
               fill="#78350F", width=w)

    return img.resize((ukuran, ukuran), Image.LANCZOS)


def make_ctk_icon(bentuk, ukuran=18, warna="white"):
    img = buat_ikon(bentuk, ukuran * 2, warna)
    return ctk.CTkImage(light_image=img, dark_image=img, size=(ukuran, ukuran))


def buat_logo_bulat(path=None, ukuran=52):
    """Bikin logo bulat putih dengan outline hijau."""
    size = ukuran * 3
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, size - 1, size - 1], fill=255)
    white_bg = Image.new("RGBA", (size, size), (255, 255, 255, 255))
    canvas.paste(white_bg, (0, 0), mask)

    logo_img = None
    if path and os.path.exists(path):
        try:
            logo_img = Image.open(path).convert("RGBA")
        except Exception:
            logo_img = None

    padding = size // 6
    inner = size - padding * 2

    if logo_img is not None:
        logo_resized = logo_img.resize((inner, inner), Image.LANCZOS)
        logo_mask = Image.new("L", (inner, inner), 0)
        ImageDraw.Draw(logo_mask).ellipse(
            [0, 0, inner - 1, inner - 1], fill=255)
        canvas.paste(logo_resized, (padding, padding), logo_mask)
    else:
        fallback = buat_ikon("apple", inner * 2).resize(
            (inner, inner), Image.LANCZOS).convert("RGBA")
        canvas.paste(fallback, (padding, padding), fallback)

    ImageDraw.Draw(canvas).ellipse(
        [1, 1, size - 2, size - 2], outline=PRIMARY, width=4)
    return canvas.resize((ukuran, ukuran), Image.LANCZOS)


# =========================================================================
# LOGIKA
# =========================================================================
class ManajerHarga:
    def __init__(self):
        self.harga = {
            "Apel": 25000, "Jeruk": 18000, "Mangga": 30000,
            "Anggur": 45000, "Pisang": 15000, "Semangka": 12000,
            "Stroberi": 35000, "Melon": 20000,
        }
    def get(self, nama): return self.harga.get(nama, 0)
    def set(self, nama, harga): self.harga[nama] = harga
    def get_all(self): return dict(self.harga)
    def get_nama_list(self): return list(self.harga.keys())


class ManajerTransaksi:
    def __init__(self):
        self.histori = []
        self.counter_id = 1

    def hitung(self, harga, jumlah, diskon):
        if harga < 0 or jumlah < 0:
            raise ValueError("Harga dan jumlah tidak boleh negatif.")
        if not 0 <= diskon <= 100:
            raise ValueError("Diskon harus 0-100 persen.")
        subtotal = harga * jumlah
        potongan = subtotal * diskon / 100
        return subtotal, potongan, subtotal - potongan

    def simpan(self, nama, harga, jumlah, diskon):
        subtotal, potongan, total = self.hitung(harga, jumlah, diskon)
        trx = {
            "id": self.counter_id, "nama": nama, "harga": harga,
            "jumlah": jumlah, "diskon": diskon, "subtotal": subtotal,
            "potongan": potongan, "total": total,
            "waktu": datetime.now().strftime("%H:%M:%S"),
        }
        self.histori.append(trx)
        self.counter_id += 1
        return trx

    def hapus(self, trx_id):
        self.histori = [t for t in self.histori if t["id"] != trx_id]

    def reset(self):
        self.histori.clear()
        self.counter_id = 1


# =========================================================================
# UI
# =========================================================================
class AplikasiTokoBuah(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Aplikasi Toko Buah Ustman bin Affan")

        # --- Default 450x450, fleksibel di-resize ---
        self.geometry("450x450")
        self.minsize(400, 420)

        self.manajer = ManajerTransaksi()
        self.manajer_harga = ManajerHarga()
        self.histori_visible = False

        self.var_nama = ctk.StringVar()
        self.var_harga = ctk.StringVar()
        self.var_jumlah = ctk.StringVar()
        self.var_diskon = ctk.StringVar()

        self.vcmd = self.register(self.validate_numeric)

        self.setup_treeview_style()
        self.buat_widget()

        # Center setelah widget selesai dibangun
        self.after(80, self.center_window_safe)

        # Responsif: bind resize untuk layout tree
        self.bind("<Configure>", self.on_window_resize)

    # ---------- Validasi ----------
    def validate_numeric(self, P):
        if P == "":
            return True
        if not all(c.isdigit() or c == "." for c in P):
            self.set_status("Hanya angka yang diperbolehkan", WARNING)
            return False
        if P.count(".") > 1:
            self.set_status("Hanya boleh 1 titik desimal", WARNING)
            return False
        if P.startswith("."):
            return False
        return True

    def attach_validation(self, entry_widget):
        try:
            entry_widget._entry.configure(validate="key",
                                          validatecommand=(self.vcmd, "%P"))
        except AttributeError:
            try:
                entry_widget.configure(validate="key",
                                       validatecommand=(self.vcmd, "%P"))
            except Exception:
                pass

    def setup_treeview_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#FFFFFF", fieldbackground="#FFFFFF",
                        rowheight=28, borderwidth=0,
                        font=("Segoe UI", 10))
        style.configure("Treeview.Heading",
                        background="#E5E7EB", foreground="#1F2937",
                        font=("Segoe UI", 10, "bold"),
                        relief="flat", padding=6)
        style.map("Treeview",
                  background=[("selected", PRIMARY)],
                  foreground=[("selected", "white")])

    # ---------- Center dengan clamp agar tidak keluar layar ----------
    def center_window_safe(self):
        """Posisikan window di tengah, tapi JANGAN sampai keluar layar."""
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()

        # Area yang benar-benar bisa dipakai (kurangi taskbar + margin)
        usable_h = sh - 80
        usable_w = sw - 20

        # Ambil ukuran window saat ini, tapi clamp
        w = min(self.winfo_width(), usable_w)
        h = min(self.winfo_height(), usable_h)

        # Hitung posisi tengah, clamp ke >= 0
        x = max(0, (sw - w) // 2)
        y = max(0, (usable_h - h) // 2)

        self.geometry(f"{w}x{h}+{x}+{y}")

    def tombol_ikon(self, parent, teks, ikon_nama, warna, hover, perintah,
                    lebar=None, tinggi=36, ukuran_font=12):
        ikon = make_ctk_icon(ikon_nama, 16, "white")
        return ctk.CTkButton(
            parent, text=teks, image=ikon, compound="left",
            command=perintah, fg_color=warna, hover_color=hover,
            font=ctk.CTkFont("Segoe UI", ukuran_font, "bold"),
            corner_radius=8, height=tinggi,
            width=lebar if lebar else 0)

    def set_status(self, pesan, warna=None):
        """Update status bar. Kosong = bar tetap ada tapi tanpa teks."""
        if not hasattr(self, "lbl_status"):
            return
        if warna is None:
            warna = TEXT_MUTED
        self.lbl_status.configure(text=pesan, text_color=warna)

    def on_window_resize(self, event=None):
        """Auto adjust tinggi tree histori sesuai ukuran window."""
        if event and event.widget is not self:
            return
        if not hasattr(self, "tree") or not self.histori_visible:
            return
        h = self.winfo_height()
        rows = max(4, min(20, (h - 420) // 30))
        try:
            self.tree.configure(height=rows)
        except Exception:
            pass

    # =====================================================================
    # LAYOUT UTAMA
    # =====================================================================
    def buat_widget(self):
        # Grid root
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # header (fixed)
        self.grid_rowconfigure(1, weight=0)  # toolbar (fixed)
        self.grid_rowconfigure(2, weight=0)  # top_section (fixed)
        self.grid_rowconfigure(3, weight=1)  # histori (expand / filler)
        self.grid_rowconfigure(4, weight=0)  # status bar (fixed)

        # ---------- STATUS BAR (row 4, paling bawah) ----------
        self.status_bar = ctk.CTkFrame(self, fg_color=("white", CARD_BG_DARK),
                                       corner_radius=8, height=28)
        self.status_bar.grid(row=4, column=0, sticky="ew",
                             padx=14, pady=(0, 10))
        self.status_bar.grid_propagate(False)

        self.lbl_status = ctk.CTkLabel(
            self.status_bar, text="",  # Kosong secara default
            font=ctk.CTkFont("Segoe UI", 10),
            text_color=TEXT_MUTED)
        self.lbl_status.pack(side="left", padx=12)

        # ---------- HEADER ----------
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.grid(row=0, column=0, sticky="ew",
                         padx=14, pady=(12, 6))

        logo_path = cari_logo("logo.png")
        logo_img = buat_logo_bulat(logo_path, ukuran=52)
        logo_icon = ctk.CTkImage(light_image=logo_img, dark_image=logo_img,
                                 size=(52, 52))

        ctk.CTkLabel(self.header, text="", image=logo_icon).pack(
            side="left", padx=(0, 10))

        title_block = ctk.CTkFrame(self.header, fg_color="transparent")
        title_block.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(title_block, text="Toko Buah Ustman bin Affan",
                     font=ctk.CTkFont("Segoe UI", 16, "bold"),
                     text_color=PRIMARY, anchor="w").pack(
            anchor="w", fill="x")
        ctk.CTkLabel(title_block, text="Sistem Kasir & Histori Pembelian",
                     font=ctk.CTkFont("Segoe UI", 10),
                     text_color=TEXT_MUTED, anchor="w").pack(
            anchor="w", fill="x", pady=(1, 0))

        # ---------- TOOLBAR ----------
        self.toolbar = ctk.CTkFrame(self, fg_color="transparent")
        self.toolbar.grid(row=1, column=0, sticky="ew",
                          padx=14, pady=(4, 6))

        self.tombol_ikon(self.toolbar, "Atur Harga", "gear",
                         SECONDARY, SECONDARY_HOVER,
                         self.buka_pengaturan_harga,
                         lebar=118, tinggi=32, ukuran_font=10).pack(side="left")

        self.btn_histori_icon = make_ctk_icon("clock", 15, "white")
        self.btn_toggle = ctk.CTkButton(
            self.toolbar, text="  Histori", image=self.btn_histori_icon,
            compound="left", command=self.toggle_histori,
            fg_color=PRIMARY, hover_color=PRIMARY_HOVER,
            font=ctk.CTkFont("Segoe UI", 10, "bold"),
            corner_radius=8, height=32, width=112)
        self.btn_toggle.pack(side="right")

        # ---------- TOP SECTION ----------
        self.top_section = ctk.CTkFrame(self, fg_color="transparent")
        self.top_section.grid(row=2, column=0, sticky="ew",
                              padx=14, pady=(0, 6))
        self.top_section.grid_columnconfigure(0, weight=1, minsize=170)
        self.top_section.grid_columnconfigure(1, weight=1, minsize=170)
        self.top_section.grid_rowconfigure(0, weight=0)

        # ===== KARTU INPUT (KIRI) =====
        self.kartu_input = ctk.CTkFrame(self.top_section,
                                        fg_color=("white", CARD_BG_DARK),
                                        corner_radius=12)
        self.kartu_input.grid(row=0, column=0, sticky="new", padx=(0, 4))

        hd = ctk.CTkFrame(self.kartu_input, fg_color="transparent")
        hd.pack(fill="x", padx=12, pady=(10, 8))
        ikon_cart2 = make_ctk_icon("cart", 14, PRIMARY)
        ctk.CTkLabel(hd, text="  Input Transaksi",
                     image=ikon_cart2, compound="left",
                     font=ctk.CTkFont("Segoe UI", 12, "bold"),
                     text_color=PRIMARY).pack(side="left")

        form = ctk.CTkFrame(self.kartu_input, fg_color="transparent")
        form.pack(fill="x", padx=12)

        def buat_field(parent, label, var, is_combo=False, suffix=""):
            wrap = ctk.CTkFrame(parent, fg_color="transparent")
            wrap.pack(fill="x", pady=(0, 6))

            ctk.CTkLabel(wrap, text=label,
                         font=ctk.CTkFont("Segoe UI", 9),
                         text_color=TEXT_MUTED,
                         anchor="w").pack(fill="x")

            if is_combo:
                w = ctk.CTkComboBox(
                    wrap, variable=var,
                    values=self.manajer_harga.get_nama_list(),
                    font=ctk.CTkFont("Segoe UI", 11),
                    corner_radius=6, height=30,
                    dropdown_font=ctk.CTkFont("Segoe UI", 10),
                    command=lambda v: self.on_buah_selected())
                w.pack(fill="x", pady=(2, 0))
            else:
                row = ctk.CTkFrame(wrap, fg_color="transparent")
                row.pack(fill="x", pady=(2, 0))
                w = ctk.CTkEntry(row, textvariable=var,
                                 font=ctk.CTkFont("Segoe UI", 11),
                                 corner_radius=6, height=30)
                w.pack(side="left", fill="x", expand=True)
                if suffix:
                    ctk.CTkLabel(row, text=suffix,
                                 font=ctk.CTkFont("Segoe UI", 10),
                                 text_color=TEXT_MUTED, width=26,
                                 anchor="w").pack(side="left", padx=(4, 0))
            return w

        self.cb_buah = buat_field(form, "Nama Buah", self.var_nama, is_combo=True)
        self.cb_buah.bind("<KeyRelease>", lambda e: self.on_buah_selected())

        self.entry_harga = buat_field(form, "Harga per kg", self.var_harga, suffix="Rp")
        self.entry_jumlah = buat_field(form, "Jumlah", self.var_jumlah, suffix="kg")
        self.entry_diskon = buat_field(form, "Diskon", self.var_diskon, suffix="%")

        self.attach_validation(self.entry_harga)
        self.attach_validation(self.entry_jumlah)
        self.attach_validation(self.entry_diskon)

        btn_row = ctk.CTkFrame(self.kartu_input, fg_color="transparent")
        btn_row.pack(fill="x", padx=12, pady=(4, 12))
        btn_row.grid_columnconfigure(0, weight=1)
        btn_row.grid_columnconfigure(1, weight=0)

        self.tombol_ikon(btn_row, "Hitung", "cart",
                         PRIMARY, PRIMARY_HOVER, self.proses_hitung,
                         tinggi=34, ukuran_font=11).grid(
            row=0, column=0, sticky="ew", padx=(0, 3))

        ctk.CTkButton(btn_row, text="Reset",
                      command=self.reset_input,
                      fg_color=SECONDARY, hover_color=SECONDARY_HOVER,
                      font=ctk.CTkFont("Segoe UI", 11, "bold"),
                      corner_radius=6, height=34, width=70).grid(
            row=0, column=1, padx=(3, 0))

        # ===== KARTU HASIL (KANAN) =====
        self.kartu_hasil = ctk.CTkFrame(self.top_section,
                                        fg_color=("#ECFDF5", "#064E3B"),
                                        corner_radius=12)
        self.kartu_hasil.grid(row=0, column=1, sticky="new", padx=(4, 0))

        hd2 = ctk.CTkFrame(self.kartu_hasil, fg_color="transparent")
        hd2.pack(fill="x", padx=12, pady=(10, 8))
        ctk.CTkLabel(hd2, text="Ringkasan",
                     font=ctk.CTkFont("Segoe UI", 12, "bold"),
                     text_color=PRIMARY).pack(side="left")

        body = ctk.CTkFrame(self.kartu_hasil, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=14, pady=(4, 12))

        ctk.CTkLabel(body, text="SUBTOTAL",
                     font=ctk.CTkFont("Segoe UI", 9, "bold"),
                     text_color=TEXT_MUTED, anchor="w").pack(fill="x", pady=(6, 0))
        self.val_subtotal = ctk.CTkLabel(
            body, text="Rp 0",
            font=ctk.CTkFont("Segoe UI", 12, "bold"),
            text_color=TEXT_MAIN, anchor="w")
        self.val_subtotal.pack(fill="x")

        ctk.CTkFrame(body, height=1, fg_color=("#D1D5DB", "#374151")).pack(
            fill="x", pady=8)

        self.lbl_diskon_j = ctk.CTkLabel(
            body, text="DISKON (0%)",
            font=ctk.CTkFont("Segoe UI", 9, "bold"),
            text_color=TEXT_MUTED, anchor="w")
        self.lbl_diskon_j.pack(fill="x")
        self.val_diskon = ctk.CTkLabel(
            body, text="Rp 0",
            font=ctk.CTkFont("Segoe UI", 12, "bold"),
            text_color=WARNING, anchor="w")
        self.val_diskon.pack(fill="x")

        ctk.CTkFrame(body, height=1, fg_color=("#D1D5DB", "#374151")).pack(
            fill="x", pady=8)

        ctk.CTkLabel(body, text="TOTAL BAYAR",
                     font=ctk.CTkFont("Segoe UI", 10, "bold"),
                     text_color=PRIMARY, anchor="w").pack(fill="x")
        self.val_total = ctk.CTkLabel(
            body, text="Rp 0",
            font=ctk.CTkFont("Segoe UI", 20, "bold"),
            text_color=PRIMARY, anchor="w")
        self.val_total.pack(fill="x", pady=(2, 0))

        # ---------- KARTU HISTORI (row 3, hidden default) ----------
        self.kartu_histori = ctk.CTkFrame(self,
                                          fg_color=("white", CARD_BG_DARK),
                                          corner_radius=12)

        header_hist = ctk.CTkFrame(self.kartu_histori, fg_color="transparent")
        header_hist.pack(fill="x", padx=12, pady=(10, 6))

        ikon_clock = make_ctk_icon("clock", 16, PRIMARY)
        ctk.CTkLabel(header_hist, text="  Histori",
                     image=ikon_clock, compound="left",
                     font=ctk.CTkFont("Segoe UI", 12, "bold"),
                     text_color=PRIMARY).pack(side="left")

        self.tombol_ikon(header_hist, "Cetak", "print",
                         PRIMARY, PRIMARY_HOVER, self.cetak_histori,
                         lebar=78, tinggi=28, ukuran_font=9).pack(
            side="right", padx=(3, 0))
        self.tombol_ikon(header_hist, "Reset", "trash",
                         DANGER, DANGER_HOVER, self.reset_histori,
                         lebar=72, tinggi=28, ukuran_font=9).pack(
            side="right", padx=3)
        self.tombol_ikon(header_hist, "Hapus", "trash",
                         DANGER, DANGER_HOVER, self.hapus_histori,
                         lebar=72, tinggi=28, ukuran_font=9).pack(
            side="right", padx=(0, 3))

        tree_frame = ctk.CTkFrame(self.kartu_histori, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        kolom = ("ID", "Waktu", "Buah", "Harga", "Qty", "Diskon", "Total")
        self.tree = ttk.Treeview(tree_frame, columns=kolom, show="headings",
                                 height=6)
        for k, v in {"ID": "ID", "Waktu": "Waktu", "Buah": "Buah",
                     "Harga": "Harga/kg", "Qty": "Qty", "Diskon": "Diskon",
                     "Total": "Total"}.items():
            self.tree.heading(k, text=v)

        self.tree.column("ID", width=35, anchor="center", stretch=False)
        self.tree.column("Waktu", width=65, anchor="center", stretch=False)
        self.tree.column("Buah", width=110, anchor="w")
        self.tree.column("Harga", width=90, anchor="e")
        self.tree.column("Qty", width=55, anchor="center")
        self.tree.column("Diskon", width=60, anchor="center")
        self.tree.column("Total", width=95, anchor="e")

        sb = ttk.Scrollbar(tree_frame, orient="vertical",
                           command=self.tree.yview)
        self.tree.configure(yscroll=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        # Bind keyboard
        self.bind("<Return>", lambda e: self.proses_hitung())
        self.bind("<Escape>", lambda e: self.reset_input())
        self.entry_harga.focus()

    # =====================================================================
    # LOGIKA UI
    # =====================================================================
    def on_buah_selected(self, event=None):
        nama = self.var_nama.get().strip()
        harga = self.manajer_harga.get(nama)
        if harga > 0:
            self.var_harga.set(str(int(harga)))
            self.set_status(f"Harga {nama}: {rupiah(harga)}/kg", PRIMARY)

    def toggle_histori(self):
        """Tampilkan/sembunyikan histori TANPA memaksa resize window."""
        if self.histori_visible:
            self.kartu_histori.grid_forget()
            self.btn_toggle.configure(
                text="  Histori", image=self.btn_histori_icon)
        else:
            self.kartu_histori.grid(row=3, column=0, sticky="nsew",
                                    padx=14, pady=(0, 6))
            self.btn_toggle.configure(text="  Tutup")
            self.update_tabel()
        self.histori_visible = not self.histori_visible

    def buka_pengaturan_harga(self):
        win = ctk.CTkToplevel(self)
        win.title("Pengaturan Harga")
        win.geometry("360x520")
        win.transient(self)
        win.grab_set()
        win.after(100, win.lift)

        # Center dialog
        win.update_idletasks()
        sw = win.winfo_screenwidth()
        sh = win.winfo_screenheight()
        w, h = 360, 520
        x = max(0, (sw - w) // 2)
        y = max(0, (sh - h - 60) // 2)
        win.geometry(f"{w}x{h}+{x}+{y}")

        ikon_gear = make_ctk_icon("gear", 20, PRIMARY)
        ctk.CTkLabel(win, text="  Pengaturan Harga",
                     image=ikon_gear, compound="left",
                     font=ctk.CTkFont("Segoe UI", 15, "bold"),
                     text_color=PRIMARY).pack(pady=(16, 2))
        ctk.CTkLabel(win, text="Harga default per kg untuk setiap buah",
                     font=ctk.CTkFont("Segoe UI", 10),
                     text_color=TEXT_MUTED).pack(pady=(0, 10))

        card = ctk.CTkScrollableFrame(win, fg_color=("white", CARD_BG_DARK),
                                      corner_radius=10)
        card.pack(fill="both", expand=True, padx=14, pady=(0, 8))
        card.grid_columnconfigure(1, weight=1)

        vcmd_harga = win.register(self.validate_numeric)

        entries = {}
        for i, (nama, harga) in enumerate(self.manajer_harga.get_all().items()):
            ctk.CTkLabel(card, text=nama,
                         font=ctk.CTkFont("Segoe UI", 11)).grid(
                row=i, column=0, sticky="w", padx=(10, 8), pady=5)
            var = ctk.StringVar(value=str(int(harga)))
            ent = ctk.CTkEntry(card, textvariable=var,
                               font=ctk.CTkFont("Segoe UI", 11),
                               corner_radius=6, height=30, justify="right")
            ent.grid(row=i, column=1, sticky="ew", padx=(0, 10), pady=5)
            try:
                ent._entry.configure(validate="key",
                                     validatecommand=(vcmd_harga, "%P"))
            except AttributeError:
                pass
            entries[nama] = var

        def simpan():
            try:
                for nama, var in entries.items():
                    val = var.get().strip()
                    if not val:
                        raise ValueError(f"Harga {nama} tidak boleh kosong.")
                    h = float(val)
                    if h < 0:
                        raise ValueError(f"Harga {nama} tidak boleh negatif.")
                    self.manajer_harga.set(nama, h)
                self.cb_buah.configure(values=self.manajer_harga.get_nama_list())
                cur = self.var_nama.get().strip()
                if cur and self.manajer_harga.get(cur) > 0:
                    self.var_harga.set(str(int(self.manajer_harga.get(cur))))
                messagebox.showinfo("Sukses", "Harga default disimpan!", parent=win)
                self.set_status("Harga default diperbarui", PRIMARY)
                win.destroy()
            except ValueError as e:
                messagebox.showerror("Error", f"Pastikan angka valid.\n\n{e}",
                                     parent=win)

        btn_row = ctk.CTkFrame(win, fg_color="transparent")
        btn_row.pack(fill="x", padx=14, pady=(0, 14))
        ctk.CTkButton(btn_row, text="Simpan", command=simpan,
                      fg_color=PRIMARY, hover_color=PRIMARY_HOVER,
                      font=ctk.CTkFont("Segoe UI", 12, "bold"),
                      corner_radius=6, height=36, width=140).pack(
            side="left", padx=(0, 6))
        ctk.CTkButton(btn_row, text="Batal", command=win.destroy,
                      fg_color=SECONDARY, hover_color=SECONDARY_HOVER,
                      font=ctk.CTkFont("Segoe UI", 12, "bold"),
                      corner_radius=6, height=36, width=140).pack(
            side="right", padx=(6, 0))

    def proses_hitung(self):
        nama = self.var_nama.get().strip()
        if not nama:
            messagebox.showwarning("Peringatan",
                                   "Pilih atau ketik Nama Buah terlebih dahulu!")
            self.cb_buah.focus()
            self.set_status("Nama buah belum diisi", DANGER)
            return

        raw_harga = self.var_harga.get().strip()
        raw_jumlah = self.var_jumlah.get().strip()
        raw_diskon = self.var_diskon.get().strip()

        if not raw_harga:
            messagebox.showwarning("Peringatan", "Harga tidak boleh kosong!")
            self.entry_harga.focus()
            self.set_status("Harga belum diisi", DANGER)
            return
        if not raw_jumlah:
            messagebox.showwarning("Peringatan", "Jumlah tidak boleh kosong!")
            self.entry_jumlah.focus()
            self.set_status("Jumlah belum diisi", DANGER)
            return
        if not raw_diskon:
            raw_diskon = "0"
            self.var_diskon.set("0")

        try:
            harga = float(raw_harga)
            jumlah = float(raw_jumlah)
            diskon = float(raw_diskon)
        except ValueError:
            messagebox.showerror("Input Tidak Valid",
                                 "Pastikan Harga, Jumlah, dan Diskon berupa angka.")
            self.set_status("Format angka salah", DANGER)
            return

        if harga <= 0:
            messagebox.showwarning("Peringatan", "Harga harus lebih dari 0!")
            self.entry_harga.focus()
            return
        if jumlah <= 0:
            messagebox.showwarning("Peringatan", "Jumlah harus lebih dari 0!")
            self.entry_jumlah.focus()
            return
        if not 0 <= diskon <= 100:
            messagebox.showwarning("Peringatan", "Diskon harus antara 0-100%!")
            self.entry_diskon.focus()
            return

        try:
            trx = self.manajer.simpan(nama, harga, jumlah, diskon)

            self.val_subtotal.configure(text=rupiah(trx['subtotal']))
            self.val_diskon.configure(text=rupiah(trx['potongan']))
            self.val_total.configure(text=rupiah(trx['total']))
            self.lbl_diskon_j.configure(text=f"DISKON ({trx['diskon']:g}%)")

            if self.histori_visible:
                self.update_tabel()

            self.set_status(
                f"Transaksi #{trx['id']} — {rupiah(trx['total'])}", PRIMARY)

            self.var_jumlah.set("")
            self.var_diskon.set("")
            self.entry_jumlah.focus()
        except ValueError as e:
            messagebox.showerror("Gagal", str(e))
            self.set_status(str(e), DANGER)

    def update_tabel(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for i, t in enumerate(self.manajer.histori):
            tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert("", "end", values=(
                t["id"], t["waktu"], t["nama"], rupiah(t["harga"]),
                f"{t['jumlah']:g}", f"{t['diskon']:g}%", rupiah(t["total"])
            ), tags=(tag,))
        self.tree.tag_configure("even", background="#FFFFFF")
        self.tree.tag_configure("odd", background="#F9FAFB")

    def hapus_histori(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Peringatan", "Pilih baris yang ingin dihapus!")
            return
        trx_id = self.tree.item(sel[0])['values'][0]
        if messagebox.askyesno("Konfirmasi", f"Hapus transaksi ID {trx_id}?"):
            self.manajer.hapus(trx_id)
            self.update_tabel()
            self.set_status(f"Transaksi #{trx_id} dihapus", PRIMARY)

    def reset_histori(self):
        if not self.manajer.histori:
            return
        if messagebox.askyesno("Konfirmasi", "Hapus SEMUA histori?"):
            self.manajer.reset()
            self.update_tabel()
            self.reset_input()
            self.set_status("Semua histori direset", PRIMARY)

    def cetak_histori(self):
        if not self.manajer.histori:
            messagebox.showwarning("Peringatan", "Tidak ada histori!")
            return
        fp = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text", "*.txt"), ("All", "*.*")],
            initialfile=f"Struk_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        if not fp:
            return
        try:
            total_semua = total_qty = 0
            with open(fp, "w", encoding="utf-8") as f:
                f.write("=" * 60 + "\n")
                f.write(" " * 10 + "TOKO BUAH USTMAN BIN AFFAN\n")
                f.write(" " * 6 + "Jl. Raya Buah No. 123, Jakarta\n")
                f.write(" " * 6 + "Telp: (021) 1234-5678\n")
                f.write("=" * 60 + "\n")
                f.write(f" Waktu Cetak : {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n")
                f.write(f" Jumlah Trx  : {len(self.manajer.histori)}\n")
                f.write("-" * 60 + "\n\n")
                for t in self.manajer.histori:
                    f.write(f"  [ID: {t['id']:>3}]   Waktu: {t['waktu']}\n")
                    f.write(f"  {'-' * 56}\n")
                    f.write(f"  {'Nama Buah':<18}: {t['nama']}\n")
                    f.write(f"  {'Harga/kg':<18}: {rupiah(t['harga'])}\n")
                    f.write(f"  {'Jumlah':<18}: {t['jumlah']:g} kg\n")
                    f.write(f"  {'Diskon':<18}: {t['diskon']:g}%\n")
                    f.write(f"  {'Subtotal':<18}: {rupiah(t['subtotal'])}\n")
                    f.write(f"  {'Potongan':<18}: -{rupiah(t['potongan'])}\n")
                    f.write(f"  {'Total Bayar':<18}: {rupiah(t['total'])}\n\n")
                    total_semua += t['total']
                    total_qty += t['jumlah']
                f.write("=" * 60 + "\n")
                f.write(" " * 22 + "RINGKASAN\n")
                f.write("=" * 60 + "\n")
                f.write(f"  {'Total Qty':<25}: {total_qty:g} kg\n")
                f.write(f"  {'Total Transaksi':<25}: {len(self.manajer.histori)}\n")
                f.write(f"  {'TOTAL PENDAPATAN':<25}: {rupiah(total_semua)}\n")
                f.write("=" * 60 + "\n")
                f.write(" " * 15 + "Terima Kasih Telah Berbelanja!\n")
                f.write("=" * 60 + "\n")
            messagebox.showinfo("Sukses", f"Struk tersimpan:\n{fp}")
            self.set_status("Struk berhasil dicetak", PRIMARY)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal cetak: {e}")
            self.set_status(f"Gagal cetak: {e}", DANGER)

    def reset_input(self):
        self.var_nama.set("")
        self.var_harga.set("")
        self.var_jumlah.set("")
        self.var_diskon.set("")
        self.val_subtotal.configure(text="Rp 0")
        self.val_diskon.configure(text="Rp 0")
        self.val_total.configure(text="Rp 0")
        self.lbl_diskon_j.configure(text="DISKON (0%)")
        self.set_status("")
        self.entry_harga.focus()


if __name__ == "__main__":
    app = AplikasiTokoBuah()
    app.mainloop()