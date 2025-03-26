import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

iris = datasets.load_iris()
X = iris.data        
y = iris.target       

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)


y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("=== Supervised Learning (Klasifikasi) ===")
print("Prediksi:       ", y_pred)
print("Label sebenarnya:", y_test)
print(f"Akurasi model:  {accuracy:.2f}")
