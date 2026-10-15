import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageTk

# ==========================================
# KONFIGURASI UTAMA WINDOW
# ==========================================
root = tk.Tk()
root.title("Login Mahasiswa UPB")
root.geometry("400x320")        # Ukuran wajib
root.resizable(False, False)

# ==========================================
# TEMA WARNA (Dark Navy & Light)
# ==========================================
current_theme = "dark"

THEMES = {
    "dark": {
        "bg": "#0F172A", "blob1": "#1E293B", "blob2": "#1E3A8A", "blob3": "#172554",
        "card": "#1E293B", "border": "#334155", "input_bg": "#0F172A",
        "primary": "#3B82F6", "primary_hover": "#2563EB",
        "reset_bg": "#334155", "reset_hover": "#475569",
        "text": "#F1F5F9", "text_muted": "#94A3B8", "accent": "#60A5FA",
        "eye_off": "#94A3B8", "eye_on": "#60A5FA",
        "footer": "#64748B", "toggle_bg": "#1E293B", "toggle_fg": "#FBBF24",
    },
    "light": {
        "bg": "#F0F4F8", "blob1": "#DBEAFE", "blob2": "#E0E7FF", "blob3": "#BFDBFE",
        "card": "#FFFFFF", "border": "#E2E8F0", "input_bg": "#F8FAFC",
        "primary": "#2563EB", "primary_hover": "#1D4ED8",
        "reset_bg": "#E2E8F0", "reset_hover": "#CBD5E1",
        "text": "#0F172A", "text_muted": "#64748B", "accent": "#2563EB",
        "eye_off": "#64748B", "eye_on": "#2563EB",
        "footer": "#64748B", "toggle_bg": "#FFFFFF", "toggle_fg": "#F59E0B",
    },
}

def c(key):
    return THEMES[current_theme][key]

# ==========================================
# FUNGSI MEMBUAT LOGO BULAT FULL PUTIH
# ==========================================
def buat_logo_bulat(path, size=52, inner_ratio=0.78):
    """
    Membuat logo di dalam lingkaran putih penuh.
    - size        : diameter total (px)
    - inner_ratio : rasio ukuran logo terhadap diameter (0.0 - 1.0)
    """
    img = Image.open(path).convert("RGBA")

    inner = int(size * inner_ratio)
    img = img.resize((inner, inner), Image.Resampling.LANCZOS)

    # Kanvas putih bulat penuh
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    mask_bulat = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask_bulat).ellipse((0, 0, size, size), fill=255)

    # Isi putih di dalam mask bulat
    white_circle = Image.new("RGBA", (size, size), (255, 255, 255, 255))
    canvas.paste(white_circle, (0, 0), mask=mask_bulat)

    # Tempelkan logo di tengah
    offset = (size - inner) // 2
    canvas.paste(img, (offset, offset), mask=img)

    # Terapkan mask bulat pada hasil akhir
    final = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    final.paste(canvas, (0, 0), mask=mask_bulat)
    return final

# ==========================================
# FUNGSI LOGIKA
# ==========================================
def toggle_password():
    if entry_password.cget('show') == '*':
        entry_password.config(show='')
        btn_eye.config(fg=c("eye_on"))
    else:
        entry_password.config(show='*')
        btn_eye.config(fg=c("eye_off"))

def proses_login():
    username = entry_username.get()
    password = entry_password.get()
    if not username or not password:
        messagebox.showwarning("Peringatan", "Username dan Password tidak boleh kosong!")
    elif username == "admin" and password == "12345":
        messagebox.showinfo("Sukses", "Login Berhasil!")
    else:
        messagebox.showerror("Error", "Username atau Password salah!")

def proses_reset():
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    entry_password.config(show='*')
    btn_eye.config(fg=c("eye_off"))
    var_ingat.set(0)
    entry_username.focus_set()

def lupa_password(event):
    messagebox.showinfo("Lupa Password", "Silakan hubungi Administrator untuk mereset password Anda.")

def on_enter_login(e):  btn_login.config(bg=c("primary_hover"))
def on_leave_login(e):  btn_login.config(bg=c("primary"))
def on_enter_reset(e):  btn_reset.config(bg=c("reset_hover"))
def on_leave_reset(e):  btn_reset.config(bg=c("reset_bg"))

# ==========================================
# BACKGROUND CANVAS + BLOB DEKORATIF
# ==========================================
bg_canvas = tk.Canvas(root, width=400, height=320, bd=0,
                      highlightthickness=0, bg=c("bg"))
bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)

blob1 = bg_canvas.create_oval(-70, -70, 110, 110, fill=c("blob1"), outline="")
blob2 = bg_canvas.create_oval(300, 230, 470, 400, fill=c("blob2"), outline="")
blob3 = bg_canvas.create_oval(330, -50, 430, 50,  fill=c("blob3"), outline="")

# ==========================================
# FOOTER
# ==========================================
footer_frame = tk.Frame(root, bg=c("bg"), pady=2)
footer_frame.pack(side="bottom", fill="x")
footer_frame.lift()

lbl_footer1 = tk.Label(footer_frame, text="© 2026 Universitas Pelita Bangsa",
                       font=("Segoe UI", 7), bg=c("bg"), fg=c("footer"))
lbl_footer1.pack()
lbl_footer2 = tk.Label(footer_frame, text="S1 Teknik Informatika",
                       font=("Segoe UI", 7, "bold"), bg=c("bg"), fg=c("footer"))
lbl_footer2.pack()

# ==========================================
# HEADER (Logo Bulat & Judul)
# ==========================================
header_frame = tk.Frame(root, bg=c("bg"), pady=4)
header_frame.pack(side="top", fill="x")
header_frame.lift()

# -- LOGO BULAT FULL PUTIH --
try:
    circular_logo = buat_logo_bulat("logo.png", size=52, inner_ratio=0.78)
    logo_img = ImageTk.PhotoImage(circular_logo)
    lbl_logo = tk.Label(header_frame, image=logo_img, bg=c("bg"), bd=0)
    lbl_logo.image = logo_img
    lbl_logo.pack(pady=(2, 0))
except Exception:
    lbl_logo = tk.Label(header_frame, text="◆",
                        font=("Segoe UI", 22, "bold"),
                        bg=c("bg"), fg=c("primary"))
    lbl_logo.pack(pady=(2, 0))

lbl_title = tk.Label(header_frame, text="Sistem Login Mahasiswa",
                     font=("Segoe UI", 11, "bold"),
                     bg=c("bg"), fg=c("text"))
lbl_title.pack(pady=(2, 0))

# ==========================================
# TOMBOL TOGGLE TEMA
# ==========================================
btn_theme = tk.Button(root, text="☀", font=("Segoe UI", 11),
                      bg=c("toggle_bg"), fg=c("toggle_fg"),
                      bd=0, relief="flat", cursor="hand2",
                      activebackground=c("toggle_bg"),
                      activeforeground=c("toggle_fg"))
btn_theme.place(x=364, y=8, width=28, height=28)
btn_theme.lift()

# ==========================================
# CARD FORM LOGIN
# ==========================================
card_frame = tk.Frame(root, bg=c("card"), bd=0,
                      highlightthickness=1,
                      highlightbackground=c("border"),
                      highlightcolor=c("border"))
card_frame.pack(fill="both", expand=True, padx=22, pady=(4, 4))
card_frame.lift()

form_frame = tk.Frame(card_frame, bg=c("card"), padx=14, pady=8)
form_frame.pack(fill="both", expand=True)

# -- USERNAME --
lbl_username = tk.Label(form_frame, text="  Username",
                        font=("Segoe UI", 8, "bold"),
                        bg=c("card"), fg=c("accent"), anchor="w")
lbl_username.pack(fill="x")

entry_username = tk.Entry(form_frame, font=("Segoe UI", 10),
                          bd=0, relief="flat",
                          bg=c("input_bg"), fg=c("text"),
                          insertbackground=c("text"),
                          highlightthickness=1,
                          highlightbackground=c("border"),
                          highlightcolor=c("primary"))
entry_username.pack(fill="x", pady=(2, 6), ipady=4)

# -- PASSWORD --
lbl_password = tk.Label(form_frame, text="  Password",
                        font=("Segoe UI", 8, "bold"),
                        bg=c("card"), fg=c("accent"), anchor="w")
lbl_password.pack(fill="x")

pass_container = tk.Frame(form_frame, bg=c("input_bg"),
                          highlightthickness=1,
                          highlightbackground=c("border"),
                          highlightcolor=c("primary"))
pass_container.pack(fill="x", pady=(2, 8))

entry_password = tk.Entry(pass_container, font=("Segoe UI", 10),
                          bd=0, relief="flat",
                          bg=c("input_bg"), fg=c("text"),
                          insertbackground=c("text"), show="*")
entry_password.pack(side="left", fill="x", expand=True,
                    padx=(6, 0), ipady=4)

btn_eye = tk.Button(pass_container, text="👁",
                    font=("Segoe UI", 11),
                    bg=c("input_bg"), fg=c("eye_off"),
                    bd=0, relief="flat", cursor="hand2",
                    activebackground=c("input_bg"),
                    activeforeground=c("eye_on"),
                    command=toggle_password)
btn_eye.pack(side="right", padx=(0, 6))

# -- CHECKBOX + LINK --
opsi_frame = tk.Frame(form_frame, bg=c("card"))
opsi_frame.pack(fill="x", pady=(0, 10))

var_ingat = tk.IntVar()
chk_ingat = tk.Checkbutton(opsi_frame, text="Ingat saya",
                           variable=var_ingat,
                           bg=c("card"), fg=c("text_muted"),
                           font=("Segoe UI", 8),
                           activebackground=c("card"),
                           activeforeground=c("text"),
                           selectcolor=c("input_bg"),
                           cursor="hand2", bd=0)
chk_ingat.pack(side="left")

lbl_lupa = tk.Label(opsi_frame, text="Lupa password?",
                    fg=c("accent"), bg=c("card"),
                    font=("Segoe UI", 8, "underline"),
                    cursor="hand2")
lbl_lupa.pack(side="right")
lbl_lupa.bind("<Button-1>", lupa_password)

# ==========================================
# BUTTONS — Dengan Ikon Modern
# ==========================================
btn_frame = tk.Frame(form_frame, bg=c("card"))
btn_frame.pack(fill="x", pady=(2, 0))

# Tombol LOGIN dengan ikon "→"
btn_login = tk.Button(btn_frame, text="→  Login",
                      font=("Segoe UI", 10, "bold"),
                      bg=c("primary"), fg="white",
                      bd=0, relief="flat", cursor="hand2",
                      activebackground=c("primary_hover"),
                      activeforeground="white",
                      command=proses_login)
btn_login.pack(side="left", expand=True, fill="x",
               padx=(0, 5), ipady=11)
btn_login.bind("<Enter>", on_enter_login)
btn_login.bind("<Leave>", on_leave_login)

# Tombol RESET dengan ikon "↻"
btn_reset = tk.Button(btn_frame, text="↻  Reset",
                      font=("Segoe UI", 10, "bold"),
                      bg=c("reset_bg"), fg=c("text"),
                      bd=0, relief="flat", cursor="hand2",
                      activebackground=c("reset_hover"),
                      activeforeground=c("text"),
                      command=proses_reset)
btn_reset.pack(side="right", expand=True, fill="x",
               padx=(5, 0), ipady=11)
btn_reset.bind("<Enter>", on_enter_reset)
btn_reset.bind("<Leave>", on_leave_reset)

# ==========================================
# FUNGSI APPLY THEME + TOGGLE
# ==========================================
def apply_theme():
    bg_canvas.config(bg=c("bg"))
    bg_canvas.itemconfig(blob1, fill=c("blob1"))
    bg_canvas.itemconfig(blob2, fill=c("blob2"))
    bg_canvas.itemconfig(blob3, fill=c("blob3"))

    header_frame.config(bg=c("bg"))
    lbl_logo.config(bg=c("bg"))
    lbl_title.config(bg=c("bg"), fg=c("text"))

    card_frame.config(bg=c("card"), highlightbackground=c("border"))
    form_frame.config(bg=c("card"))

    lbl_username.config(bg=c("card"), fg=c("accent"))
    lbl_password.config(bg=c("card"), fg=c("accent"))

    entry_username.config(bg=c("input_bg"), fg=c("text"),
                          insertbackground=c("text"),
                          highlightbackground=c("border"))
    pass_container.config(bg=c("input_bg"), highlightbackground=c("border"))
    entry_password.config(bg=c("input_bg"), fg=c("text"),
                          insertbackground=c("text"))

    is_visible = entry_password.cget("show") == ""
    btn_eye.config(bg=c("input_bg"),
                   fg=c("eye_on") if is_visible else c("eye_off"))

    opsi_frame.config(bg=c("card"))
    chk_ingat.config(bg=c("card"), fg=c("text_muted"),
                     activebackground=c("card"),
                     activeforeground=c("text"),
                     selectcolor=c("input_bg"))
    lbl_lupa.config(bg=c("card"), fg=c("accent"))

    btn_frame.config(bg=c("card"))
    btn_login.config(bg=c("primary"), fg="white",
                     activebackground=c("primary_hover"))
    btn_reset.config(bg=c("reset_bg"), fg=c("text"),
                     activebackground=c("reset_hover"))

    footer_frame.config(bg=c("bg"))
    lbl_footer1.config(bg=c("bg"), fg=c("footer"))
    lbl_footer2.config(bg=c("bg"), fg=c("footer"))

    btn_theme.config(bg=c("toggle_bg"), fg=c("toggle_fg"),
                     activebackground=c("toggle_bg"),
                     activeforeground=c("toggle_fg"),
                     text="☀" if current_theme == "dark" else "🌙")
    btn_theme.lift()


def toggle_theme():
    global current_theme
    current_theme = "light" if current_theme == "dark" else "dark"
    apply_theme()


btn_theme.config(command=toggle_theme)
btn_theme.config(text="☀" if current_theme == "dark" else "🌙")

# ==========================================
# MENJALANKAN APLIKASI
# ==========================================
root.mainloop()