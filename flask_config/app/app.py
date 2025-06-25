from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__)

# Buat folder static jika belum ada
os.makedirs("static", exist_ok=True)

@app.route("/")
def index():
    df = pd.read_csv("Student_performance_data.csv")

    # Plot visualisasi
    fig, axs = plt.subplots(1, 3, figsize=(18, 5))
    sns.histplot(df['StudyTimeWeekly'], kde=True, ax=axs[0], color='blue')
    axs[0].set_title('Distribusi Waktu Belajar Mingguan')

    sns.histplot(df['Absences'], kde=True, ax=axs[1], color='green')
    axs[1].set_title('Distribusi Absensi')

    sns.histplot(df['GPA'], kde=True, ax=axs[2], color='red')
    axs[2].set_title('Distribusi GPA')

    plt.tight_layout()
    plot_path = os.path.join("static", "plot.png")
    plt.savefig(plot_path)
    plt.close()

    return render_template("index.html", plot_url=plot_path)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
