"""
Train and save a demo code-quality classifier without downloading CodeBERT.

Uses synthetic Python code snippets + TF-IDF + RandomForestClassifier as a
lightweight stand-in for the full CodeBERT pipeline described in the project.
Outputs: models/bigcode_demo.pkl
"""

import os
import joblib
import numpy as np
import pandas as pd
from scipy.sparse import hstack
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.preprocessing import StandardScaler

# ── synthetic demo dataset ──────────────────────────────────────────────────
SAMPLES = [
    # label 1 = good quality
    ("def add(a, b):\n    \"\"\"Return sum of a and b.\"\"\"\n    return a + b", 1),
    ("def factorial(n):\n    \"\"\"Return n!.\"\"\"\n    if n == 0:\n        return 1\n    return n * factorial(n - 1)", 1),
    ("def is_palindrome(s):\n    \"\"\"Check if string is palindrome.\"\"\"\n    s = s.lower().replace(' ', '')\n    return s == s[::-1]", 1),
    ("def binary_search(arr, target):\n    \"\"\"Binary search returning index or -1.\"\"\"\n    lo, hi = 0, len(arr) - 1\n    while lo <= hi:\n        mid = (lo + hi) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            lo = mid + 1\n        else:\n            hi = mid - 1\n    return -1", 1),
    ("def merge_sort(arr):\n    \"\"\"Sort list using merge sort.\"\"\"\n    if len(arr) <= 1:\n        return arr\n    mid = len(arr) // 2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])\n    return _merge(left, right)", 1),
    ("def flatten(lst):\n    \"\"\"Flatten nested list.\"\"\"\n    result = []\n    for item in lst:\n        if isinstance(item, list):\n            result.extend(flatten(item))\n        else:\n            result.append(item)\n    return result", 1),
    ("def count_words(text):\n    \"\"\"Count word frequency in text.\"\"\"\n    from collections import Counter\n    return Counter(text.lower().split())", 1),
    ("def gcd(a, b):\n    \"\"\"Return greatest common divisor.\"\"\"\n    while b:\n        a, b = b, a % b\n    return a", 1),
    ("def matrix_multiply(A, B):\n    \"\"\"Multiply two matrices.\"\"\"\n    rows_A, cols_A = len(A), len(A[0])\n    cols_B = len(B[0])\n    C = [[0] * cols_B for _ in range(rows_A)]\n    for i in range(rows_A):\n        for j in range(cols_B):\n            for k in range(cols_A):\n                C[i][j] += A[i][k] * B[k][j]\n    return C", 1),
    ("def validate_email(email):\n    \"\"\"Return True if email is valid.\"\"\"\n    import re\n    pattern = r'^[\\w.+-]+@[\\w-]+\\.[\\w.-]+$'\n    return bool(re.match(pattern, email))", 1),
    ("def fibonacci(n):\n    \"\"\"Return nth Fibonacci number.\"\"\"\n    a, b = 0, 1\n    for _ in range(n):\n        a, b = b, a + b\n    return a", 1),
    ("def chunk_list(lst, size):\n    \"\"\"Split list into chunks of given size.\"\"\"\n    return [lst[i:i+size] for i in range(0, len(lst), size)]", 1),
    ("def deep_copy(obj):\n    \"\"\"Return a deep copy of a dict/list structure.\"\"\"\n    import copy\n    return copy.deepcopy(obj)", 1),
    ("def cached_fib(n, memo={}):\n    \"\"\"Memoized Fibonacci.\"\"\"\n    if n in memo:\n        return memo[n]\n    if n <= 1:\n        return n\n    memo[n] = cached_fib(n-1, memo) + cached_fib(n-2, memo)\n    return memo[n]", 1),
    ("def quicksort(arr):\n    \"\"\"In-place quicksort.\"\"\"\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quicksort(left) + middle + quicksort(right)", 1),
    # label 0 = poor quality
    ("def f(x,y): return x+y", 0),
    ("def a(b): return b*b-3*b+1", 0),
    ("x=1\ny=2\nz=x+y\nprint(z)", 0),
    ("def calc(data):\n    r=0\n    for i in data:\n        r=r+i\n    return r", 0),
    ("def proc(a,b,c,d,e,f): return (a+b)*(c-d)/(e+f+0.0001)", 0),
    ("def fn(lst):\n    for i in range(len(lst)):\n        for j in range(len(lst)):\n            if lst[i]==lst[j] and i!=j:\n                lst[i]=0\n    return lst", 0),
    ("def run():\n    import os\n    import sys\n    import re\n    pass", 0),
    ("def p(n):\n    if n<2: return False\n    for i in range(2,n): \n        if n%i==0: return False\n    return True", 0),
    ("def magic(x):\n    return ((x**2+x)*2-x)//(x+1) if x != -1 else 0", 0),
    ("def thing(a,b): a=a+b; b=a-b; a=a-b; return a,b", 0),
    ("def x1(l):\n    return sorted(l,key=lambda x:x[1])", 0),
    ("def foo(bar,baz=None,qux=[]):\n    if baz: qux.append(bar)\n    return qux", 0),
    ("def d(s): return {c:s.count(c) for c in s}", 0),
    ("import random\ndef gen(): return [random.randint(0,100) for _ in range(10)]", 0),
    ("def s(n):\n    t=0\n    for i in range(1,n+1):\n        t+=i\n    return t", 0),
]

codes, labels = zip(*SAMPLES)
df = pd.DataFrame({"code": codes, "label": labels})

# ── feature engineering ───────────────────────────────────────────────────────

def extract_code_metrics(code):
    lines = code.split("\n")
    return {
        "num_lines": len(lines),
        "num_functions": code.count("def "),
        "has_docstring": int('"""' in code or "'''" in code),
        "num_imports": code.count("import "),
        "code_length": len(code),
        "avg_line_length": np.mean([len(l) for l in lines]) if lines else 0,
        "num_comments": sum(1 for l in lines if l.strip().startswith("#")),
        "has_return": int("return" in code),
        "num_args": code.count(",") + (1 if "def " in code else 0),
    }

metric_dfs = pd.DataFrame([extract_code_metrics(c) for c in df["code"]])

tfidf = TfidfVectorizer(max_features=200, analyzer="word", ngram_range=(1, 2))
X_tfidf = tfidf.fit_transform(df["code"])

scaler = StandardScaler()
X_metrics = scaler.fit_transform(metric_dfs.values)

X = hstack([X_tfidf, X_metrics])
y = df["label"].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

clf = RandomForestClassifier(
    n_estimators=200, class_weight="balanced", random_state=42
)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
y_prob = clf.predict_proba(X_test)[:, 1]
acc = accuracy_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_prob)

print(f"Accuracy : {acc:.4f}")
print(f"ROC-AUC  : {auc:.4f}")
print(classification_report(y_test, y_pred, target_names=["Poor Quality", "Good Quality"]))

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(MODEL_DIR, exist_ok=True)
MODEL_PATH = os.path.join(MODEL_DIR, "bigcode_demo.pkl")

bundle = {
    "model": clf,
    "tfidf": tfidf,
    "scaler": scaler,
    "metric_cols": list(metric_dfs.columns),
    "metrics": {"accuracy": round(acc, 4), "roc_auc": round(auc, 4)},
    "classes": ["Poor Quality", "Good Quality"],
    "df": df,
}

joblib.dump(bundle, MODEL_PATH)
print(f"Model saved → {MODEL_PATH}")
