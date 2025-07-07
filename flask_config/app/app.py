"""
app.py — Dashboard Plotly + API chat jam-belajar
• Tanpa model ML eksternal (heuristik sederhana)
• Deteksi kolom fleksibel + ENV override + fallback otomatis
"""

import os, re, sys
import pandas as pd
import plotly.express as px
from flask import Flask, render_template, request, jsonify

# ────────────────────────────────────────────────────────────────────
# 0. Inisialisasi
# ────────────────────────────────────────────────────────────────────
app = Flask(__name__, template_folder="templates")
DATA_PATH = "Student_performance_data.csv"

# ────────────────────────────────────────────────────────────────────
# 1. Muat dataset
# ────────────────────────────────────────────────────────────────────
try:
    df_master = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    sys.exit(f"[FATAL] CSV '{DATA_PATH}' tidak ditemukan di /app")

# ────────────────────────────────────────────────────────────────────
# 2. Utilitas
# ────────────────────────────────────────────────────────────────────
def canon(name: str) -> str:
    """huruf kecil + hapus selain alfanumerik"""
    return re.sub(r"[^0-9a-z]+", "", name.lower())

def first_match(df, *candidates):
    """kembalikan nama kolom asli yang canon()-nya cocok kandidat"""
    cmap = {canon(c): c for c in df.columns}
    for cand in candidates:
        hit = cmap.get(canon(cand))
        if hit:
            return hit
    return None

def safe_float(v, default=0.0):
    try:
        f = float(v)
        return f if pd.notna(f) else default
    except (ValueError, TypeError):
        return default

# ────────────────────────────────────────────────────────────────────
# 3. Konfigurasi kolom
# ────────────────────────────────────────────────────────────────────
COL_ID = first_match(df_master, "StudentID")
if not COL_ID:
    sys.exit("[FATAL] Kolom 'StudentID' tidak ditemukan di CSV.")

# a) coba baca override ENV
COL_LMS   = first_match(df_master, os.getenv("COL_LMS", ""))
COL_GRADE = first_match(df_master, os.getenv("COL_GRADE", ""))

# b) deteksi otomatis jika masih None
if not COL_LMS:
    COL_LMS = first_match(
        df_master,
        "LMSAccess", "lms_access", "LMSLogin", "LMS Login",
        "lms_hits", "accesscount", "totalaccess", "login"
    )
if not COL_GRADE:
    COL_GRADE = first_match(
        df_master,
        "AssignmentGrade", "assignment_grade", "Assignment Score",
        "TaskScore", "taskscore", "nilai_tugas", "grade", "score"
    )

# c) fallback ke StudyTimeWeekly & GPA jika tetap None
if not COL_LMS:
    COL_LMS = first_match(df_master, "StudyTimeWeekly")
    print(f"[INFO] Fallback COL_LMS  → '{COL_LMS}' (pakai StudyTimeWeekly)")

if not COL_GRADE:
    COL_GRADE = first_match(df_master, "GPA")
    print(f"[INFO] Fallback COL_GRADE → '{COL_GRADE}' (pakai GPA)")

print(f"[INFO] Kolom terpakai → ID: '{COL_ID}', LMS: '{COL_LMS}', Grade: '{COL_GRADE}'")

# ────────────────────────────────────────────────────────────────────
# 4. Prediksi heuristik
# ────────────────────────────────────────────────────────────────────
def predict_best_hours(lms_access: float, assignment_grade: float) -> float:
    base = 12
    adj  = (lms_access / 100) * 4 + (assignment_grade / 100) * 4
    return min(max(base + adj, 8), 20)

# ────────────────────────────────────────────────────────────────────
# 5. ROUTE DASHBOARD
# ────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    df = df_master.copy()

    q = request.args.get("q", "").strip().lower()
    if q:
        df = df[df.apply(
            lambda r: q in str(r[COL_ID]).lower()
                      or q in str(r.get("GradeClass", "")).lower(),
            axis=1
        )]

    plots = []
    def add(fig, t, d):
        plots.append({"div": fig.to_html(full_html=False), "title": t, "desc": d})

    add(px.histogram(df, x="StudyTimeWeekly", nbins=20,
                     title="Distribusi Waktu Belajar Mingguan"),
        "Distribusi Waktu Belajar",
        "Sebaran jam belajar mingguan mahasiswa.")

    add(px.histogram(df, x="Absences", nbins=20, color_discrete_sequence=["green"],
                     title="Distribusi Absensi"),
        "Distribusi Absensi",
        "Frekuensi ketidakhadiran mahasiswa.")

    add(px.histogram(df, x="GPA", nbins=20, color_discrete_sequence=["red"],
                     title="Distribusi GPA"),
        "Distribusi GPA",
        "Sebaran nilai akhir mahasiswa.")

    add(px.histogram(df, x="GradeClass", title="Distribusi Grade Kelas"),
        "Distribusi GradeClass",
        "Jumlah mahasiswa per kelas.")

    corr = df[["StudyTimeWeekly","Absences","GPA",
               "Age","ParentalEducation"]].corr()
    add(px.imshow(corr, text_auto=True, color_continuous_scale="RdBu",
                  title="Heatmap Korelasi"),
        "Korelasi Antar Variabel",
        "Kekuatan hubungan antar-fitur.")

    table_html = df.to_html(classes="table table-bordered table-striped table-sm",
                            index=False)

    return render_template("index.html", plots=plots, table=table_html)

# ────────────────────────────────────────────────────────────────────
# 6. API CHAT
# ────────────────────────────────────────────────────────────────────
@app.route("/api/chat", methods=["POST"])
def api_chat():
    payload = request.get_json(silent=True) or {}
    msg     = str(payload.get("message","")).strip()

    if not msg:
        return jsonify({"response":"Pesan kosong, silakan ketik pertanyaan."})

    m = re.search(r"\b\d+\b", msg)
    if m:
        sid = int(m.group())
        row = df_master[df_master[COL_ID] == sid]
        if row.empty:
            return jsonify({"response":f"StudentID {sid} tidak ditemukan."})

        lms   = safe_float(row[COL_LMS].iat[0])
        grade = safe_float(row[COL_GRADE].iat[0])
        hours = round(predict_best_hours(lms, grade), 1)

        return jsonify({"response":
            f"Berdasarkan akses LMS ({lms}) dan nilai tugas ({grade}), "
            f"jam belajar optimal Student {sid} ≈ **{hours} jam/minggu**."
        })

    if "help" in msg.lower():
        return jsonify({"response":
            "Contoh: 'Student 123 berapa jam belajar?'. Atau ketik StudentID saja."
        })

    return jsonify({"response":
        "Maaf, format belum dipahami. Contoh: 'Student 101 jam belajarnya?'."
    })

# ────────────────────────────────────────────────────────────────────
# 7. MAIN
# ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
