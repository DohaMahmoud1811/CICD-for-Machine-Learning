import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from sklearn.metrics import accuracy_score, f1_score
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
import skops.io as sio


drug_df = pd.read_csv('Data/drug200.csv')
drug_df = drug_df.sample(frac= 1)
drug_df.head(3)

X = drug_df.drop('Drug', axis= 1).values
y = drug_df['Drug'].values

# Split our data:
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.3, random_state= 125)

cat_col = [1,2,3]
num_col = [0,4]

# Pipelines and Model Traininig:
transform = ColumnTransformer([
    ("encoder", OrdinalEncoder(), cat_col), 
    ("num_imputer", SimpleImputer(strategy= 'median'), num_col),
    ("num_scaler", StandardScaler(), num_col)
])

pipe = Pipeline(
    steps=[
        ("preprocessing", transform),
        ("model", RandomForestClassifier(n_estimators= 100, random_state= 125))
    ]
)

pipe.fit(X_train, y_train)

# Model Evaluation:
predictions = pipe.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
f1 = f1_score(y_test, predictions, average= 'macro')
print("Accuracy:", str(round(accuracy, 2) * 100) + "%", "F1:", round(f1, 2))

# Create metrics file in Results folder:
with open("Results/metrics.txt", "w") as outfile:
    outfile.write(f"\nAccuracy = {accuracy.round(2)}, F1 Score = {f1.round(2)}.")

# Create the Confusion matrix and save it into Results folder:
cm = confusion_matrix(y_test, predictions, labels=pipe.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=pipe.classes_)
disp.plot()
plt.savefig("Results/model_results.png", dpi=120)

# Save our model:
sio.load("Model/drug_pipeline.skops", trusted= True)