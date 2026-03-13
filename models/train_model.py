import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

print("Loading dataset...")

# Load CSV files with basic validation
try:
    fake = pd.read_csv("Fake.csv")
    true = pd.read_csv("True.csv")
except pd.errors.EmptyDataError as e:
    raise SystemExit("Error: one of the input CSV files is empty. "
                     "Please ensure 'Fake.csv' and 'True.csv' contain data.")
except FileNotFoundError as e:
    raise SystemExit(f"Error: could not find {e.filename}. "
                     "Place the CSV files in the workspace root or update the path.")

# verify data was loaded successfully
if fake.empty or true.empty:
    raise SystemExit("Error: one of the datasets is empty. "
                     "Make sure your CSV files have headers and content.")

# Add labels
fake["label"] = 0   # Fake = 0
true["label"] = 1   # Real = 1

# Combine datasets
data = pd.concat([fake, true], axis=0)

# Keep only text and label columns
data = data[["text", "label"]]

print("Cleaning text...")

# Clean text
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\d', '', text)
    return text

data["text"] = data["text"].apply(clean_text)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    data["text"], data["label"], test_size=0.2, random_state=42
)

print("Converting text to numbers...")

# Convert text to numbers
vectorizer = TfidfVectorizer(stop_words="english")
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

print("Training model...")

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, y_train)

# Accuracy
y_pred = model.predict(X_test_vec)

accuracy = accuracy_score(y_test, y_pred)

print("Model Accuracy:", accuracy)
print("✅ Training Completed Successfully!")