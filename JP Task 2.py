import pandas as pd
import re
import os

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

def read_spam():
    category = 'spam'
    directory = './enron1/spam'
    return read_category(category, directory)

def read_ham():
    category = 'ham'
    directory = './enron1/ham'
    return read_category(category, directory)

def read_category(category, directory):
    emails = []
    for filename in os.listdir(directory):
        if not filename.endswith(".txt"):
            continue
        with open(os.path.join(directory, filename), 'r') as fp:
            try:
                content = fp.read()
                emails.append({'name': filename, 'content': content, 'category': category})
            except:
                print(f'skipped {filename}')
    return emails

def preprocessor(e):
    return re.sub('[^A-Za-z]', ' ', e).lower()


ham = read_ham()
spam = read_spam()

df = pd.DataFrame.from_records(ham)
df = df.append(pd.DataFrame.from_records(spam))

vectorizer = CountVectorizer(preprocessor=preprocessor)

X_train,X_test,y_train,y_test = train_test_split(df["content"],df["category"],test_size=0.2,random_state=1)
X_train_df = vectorizer.fit_transform(X_train)

model = LogisticRegression()
model.fit(X_train_df,y_train)

X_test_df = vectorizer.transform(X_test)
y_pred = model.predict(X_test_df)

print(f'Accuracy:\n{accuracy_score(y_test,y_pred)}\n')
print(f'Confusion Matrix:\n{confusion_matrix(y_test,y_pred)}\n')
print(f'Detailed Statistics:\n{classification_report(y_test,y_pred)}\n')
