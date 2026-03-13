import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

def load_data(train_path="data_train.csv", test_path="data_test.csv"):
    try:
        df_train = pd.read_csv(train_path, sep=';')
        df_test = pd.read_csv(test_path, sep=';')
        
        if df_train.empty or df_test.empty:
            print("Warning: One or both datasets are empty. Training cannot proceed properly.")
            return None, None
            
        print(f"Loaded {len(df_train)} training rows and {len(df_test)} test rows.")
        return df_train, df_test
    except FileNotFoundError:
         print(f"Dataset files {train_path} or {test_path} not found.")
         return None, None
    except pd.errors.EmptyDataError:
         print("Error: Empty dataset files encountered.")
         return None, None
    except Exception as e:
         print(f"Error loading datasets: {e}")
         return None, None

def main():
    print("Loading data...")
    df_train, df_test = load_data()
    if df_train is None:
        print("Dataset loading failed. Cannot proceed.")
        return
    
    # Fill NAs
    df_train['text'] = df_train['text'].fillna('')
    df_test['text'] = df_test['text'].fillna('')
    
    X_train = df_train['text']
    y_train = df_train['label']
    X_test = df_test['text']
    y_test = df_test['label']
    
    print("Vectorizing text (TF-IDF)...")
    vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    print("Training Logistic Regression Model...")
    model = LogisticRegression(random_state=42)
    model.fit(X_train_tfidf, y_train)
    
    print("Evaluating Model...")
    y_pred = model.predict(X_test_tfidf)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy * 100:.2f}%")
    print(classification_report(y_test, y_pred))
    
    print("Saving Model and Vectorizer...")
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/model.pkl')
    joblib.dump(vectorizer, 'models/vectorizer.pkl')
    print("Model saved to 'models/model.pkl'")
    print("Vectorizer saved to 'models/vectorizer.pkl'")
    print("Training completed successfully.")

if __name__ == "__main__":
    main()
