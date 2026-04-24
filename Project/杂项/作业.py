from sklearn import datasets
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn.model_selection import train_test_split
import numpy as np

iris = datasets.load_iris()
X = iris.data
y = iris.target

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, random_state=42)

model = tree.DecisionTreeClassifier(criterion = "gini", random_state = 10)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

x_new = np.array([[5.0, 2.9, 1.0, 0.2]])

print("Predicted class for new data:", model.predict(x_new))