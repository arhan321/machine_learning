# --------------------------------------------------
# Contoh Code Unsupervised Learning (Clustering)
# --------------------------------------------------

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# 1. Memuat dataset Iris kembali
iris = datasets.load_iris()
X_iris = iris.data  # (Tanpa menggunakan label)

# 2. Inisialisasi model K-Means untuk 3 cluster
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X_iris)

# 3. Prediksi cluster untuk data iris
cluster_labels = kmeans.labels_

print("\n=== Unsupervised Learning (Clustering) ===")
print("Hasil cluster dari model K-Means:", cluster_labels)

# (Opsional) Visualisasi dengan PCA hanya untuk 2D Plot
# ---------------------------------------------------
pca = PCA(n_components=2)
reduced_X = pca.fit_transform(X_iris)

plt.figure()
plt.scatter(reduced_X[:, 0], reduced_X[:, 1], c=cluster_labels)
plt.title("Visualisasi Clustering Iris dengan K-Means (2D PCA)")
plt.xlabel("Komponen Utama 1")
plt.ylabel("Komponen Utama 2")
plt.show()
