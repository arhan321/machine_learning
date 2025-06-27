# from flask import Flask, render_template
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import os

# app = Flask(__name__)
# os.makedirs("static", exist_ok=True)

# @app.route("/")
# def index():
#     df = pd.read_csv("Student_performance_data.csv")

#     plots = []

#     # Plot 1: Histogram StudyTimeWeekly
#     plt.figure(figsize=(6, 4))
#     sns.histplot(df['StudyTimeWeekly'], kde=True, color='blue')
#     plt.title('Distribusi Waktu Belajar Mingguan')
#     path = "static/plot1.png"
#     plt.savefig(path)
#     plt.close()
#     plots.append({"src": path, "title": "Distribusi Waktu Belajar", "desc": "Histogram waktu belajar mingguan mahasiswa."})

#     # Plot 2: Histogram Absences
#     plt.figure(figsize=(6, 4))
#     sns.histplot(df['Absences'], kde=True, color='green')
#     plt.title('Distribusi Absensi')
#     path = "static/plot2.png"
#     plt.savefig(path)
#     plt.close()
#     plots.append({"src": path, "title": "Distribusi Absensi", "desc": "Histogram jumlah ketidakhadiran mahasiswa."})

#     # Plot 3: Histogram GPA
#     plt.figure(figsize=(6, 4))
#     sns.histplot(df['GPA'], kde=True, color='red')
#     plt.title('Distribusi GPA')
#     path = "static/plot3.png"
#     plt.savefig(path)
#     plt.close()
#     plots.append({"src": path, "title": "Distribusi GPA", "desc": "Distribusi nilai akhir mahasiswa."})

#     # Plot 4: Countplot GradeClass
#     plt.figure(figsize=(6, 4))
#     sns.countplot(x='GradeClass', data=df)
#     plt.title('Distribusi Grade Kelas')
#     path = "static/plot4.png"
#     plt.savefig(path)
#     plt.close()
#     plots.append({"src": path, "title": "Distribusi GradeClass", "desc": "Jumlah mahasiswa per kelas."})

#     # Plot 5: Heatmap Korelasi
#     plt.figure(figsize=(6, 5))
#     corr = df[['StudyTimeWeekly', 'Absences', 'GPA', 'Age', 'ParentalEducation']].corr()
#     sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
#     plt.title('Korelasi Antar Variabel')
#     path = "static/plot5.png"
#     plt.savefig(path)
#     plt.close()
#     plots.append({"src": path, "title": "Korelasi Fitur Utama", "desc": "Heatmap korelasi antara GPA, Absensi, dll."})

#     # Plot 6: Boxplot StudyTimeWeekly vs GradeClass
#     plt.figure(figsize=(6, 4))
#     sns.boxplot(x='GradeClass', y='StudyTimeWeekly', data=df)
#     plt.title('Waktu Belajar vs GradeClass')
#     path = "static/plot6.png"
#     plt.savefig(path)
#     plt.close()
#     plots.append({"src": path, "title": "Study Time vs GradeClass", "desc": "Perbandingan waktu belajar dengan nilai kelas."})

#     # Plot 7: Boxplot Absences vs GradeClass
#     plt.figure(figsize=(6, 4))
#     sns.boxplot(x='GradeClass', y='Absences', data=df)
#     plt.title('Absensi vs GradeClass')
#     path = "static/plot7.png"
#     plt.savefig(path)
#     plt.close()
#     plots.append({"src": path, "title": "Absensi vs GradeClass", "desc": "Hubungan absensi dengan nilai kelas."})

#     # Plot 8: Boxplot GPA vs GradeClass
#     plt.figure(figsize=(6, 4))
#     sns.boxplot(x='GradeClass', y='GPA', data=df)
#     plt.title('GPA vs GradeClass')
#     path = "static/plot8.png"
#     plt.savefig(path)
#     plt.close()
#     plots.append({"src": path, "title": "GPA vs GradeClass", "desc": "Perbandingan GPA terhadap kelas."})

#     return render_template("index.html", plots=plots)

# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0")

from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import os

app = Flask(__name__)

@app.route("/")
def index():
    df = pd.read_csv("Student_performance_data.csv")

    plots = []

    # Plot 1: Histogram interaktif (Study Time)
    fig1 = px.histogram(df, x="StudyTimeWeekly", nbins=20, title="Distribusi Waktu Belajar Mingguan")
    plots.append({
        "div": fig1.to_html(full_html=False),
        "title": "Distribusi Waktu Belajar",
        "desc": "Grafik ini menunjukkan sebaran jam belajar mingguan mahasiswa. Pola ini dapat membantu mengidentifikasi waktu optimal untuk belajar."
    })

    # Plot 2: Histogram Absensi
    fig2 = px.histogram(df, x="Absences", nbins=20, title="Distribusi Absensi", color_discrete_sequence=["green"])
    plots.append({
        "div": fig2.to_html(full_html=False),
        "title": "Distribusi Absensi",
        "desc": "Histogram absensi memperlihatkan frekuensi ketidakhadiran mahasiswa. Dapat digunakan untuk melihat korelasi terhadap GPA."
    })

    # Plot 3: Histogram GPA
    fig3 = px.histogram(df, x="GPA", nbins=20, title="Distribusi GPA", color_discrete_sequence=["red"])
    plots.append({
        "div": fig3.to_html(full_html=False),
        "title": "Distribusi GPA",
        "desc": "Grafik ini menggambarkan sebaran nilai akhir mahasiswa (GPA). Dapat menunjukkan apakah distribusinya normal atau condong."
    })

    # Plot 4: Barplot GradeClass
    fig4 = px.histogram(df, x="GradeClass", title="Distribusi Grade Kelas")
    plots.append({
        "div": fig4.to_html(full_html=False),
        "title": "Distribusi GradeClass",
        "desc": "Bar chart ini menunjukkan jumlah mahasiswa pada tiap kelas (GradeClass). Ini membantu memetakan persebaran prestasi akademik."
    })

    # Plot 5: Heatmap Korelasi
    corr = df[['StudyTimeWeekly', 'Absences', 'GPA', 'Age', 'ParentalEducation']].corr()
    fig5 = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu", title="Heatmap Korelasi")
    plots.append({
        "div": fig5.to_html(full_html=False),
        "title": "Korelasi Antar Variabel",
        "desc": "Heatmap ini menunjukkan kekuatan hubungan antar fitur seperti GPA, absensi, usia, dll. Warna merah/biru menandakan korelasi kuat positif atau negatif."
    })

    # Konversi DataFrame ke HTML Table
    table_html = df.to_html(classes="table table-bordered table-striped table-sm", index=False)

    return render_template("index.html", plots=plots, table=table_html)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")


