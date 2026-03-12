"""
Streamlit demo for the BigCodeBench LLM Project — Code Quality Classifier.
Four tabs: Code Quality Predictor · Model Dashboard · Code Explorer · LLM Pipeline
"""

import os
import joblib
import numpy as np
import pandas as pd
from scipy.sparse import hstack
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# ── page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BigCodeBench LLM — Code Quality",
    page_icon="🤖",
    layout="wide",
)

# ── load model bundle ─────────────────────────────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "bigcode_demo.pkl")


@st.cache_resource(show_spinner="Loading model…")
def load_bundle():
    return joblib.load(MODEL_PATH)


bundle  = load_bundle()
clf     = bundle["model"]
tfidf   = bundle["tfidf"]
scaler  = bundle["scaler"]
metrics = bundle["metrics"]
classes = bundle["classes"]
df      = bundle["df"]


# ── helper: feature extraction ────────────────────────────────────────────────
def extract_code_metrics(code: str) -> dict:
    lines = code.split("\n")
    return {
        "num_lines":       len(lines),
        "num_functions":   code.count("def "),
        "has_docstring":   int('"""' in code or "'''" in code),
        "num_imports":     code.count("import "),
        "code_length":     len(code),
        "avg_line_length": np.mean([len(l) for l in lines]) if lines else 0,
        "num_comments":    sum(1 for l in lines if l.strip().startswith("#")),
        "has_return":      int("return" in code),
        "num_args":        code.count(",") + (1 if "def " in code else 0),
    }


def predict_quality(code: str):
    x_tfidf   = tfidf.transform([code])
    m         = extract_code_metrics(code)
    x_metrics = scaler.transform([[m[k] for k in bundle["metric_cols"]]])
    x         = hstack([x_tfidf, x_metrics])
    pred      = clf.predict(x)[0]
    proba     = clf.predict_proba(x)[0]
    return pred, proba


# ── tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🧑‍💻 Code Quality Predictor",
    "📊 Model Dashboard",
    "🔍 Code Explorer",
    "🤖 LLM Pipeline",
])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — CODE QUALITY PREDICTOR
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.title("🧑‍💻 Code Quality Predictor")
    st.markdown(
        "Paste any Python snippet below and click **Analyse** to get an instant "
        "code-quality score powered by a TF-IDF + RandomForest classifier trained "
        "on the BigCodeBench-style code corpus."
    )

    DEFAULT_CODE = '''def binary_search(arr, target):
    """Binary search returning index or -1."""
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1'''

    col_editor, col_result = st.columns([3, 2], gap="large")

    with col_editor:
        code_input = st.text_area(
            "Python code",
            value=DEFAULT_CODE,
            height=340,
            key="code_input",
        )
        analyse_btn = st.button("🔍 Analyse", use_container_width=True, type="primary")

    with col_result:
        st.subheader("Quality Analysis")
        if analyse_btn:
            if not code_input.strip():
                st.warning("Please enter some code first.")
            else:
                pred, proba = predict_quality(code_input)
                label = classes[pred]
                score = proba[1] * 100
                color = "#2ecc71" if pred == 1 else "#e74c3c"

                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=score,
                    number={"suffix": "%", "font": {"size": 40}},
                    title={"text": f"<b>{label}</b>", "font": {"size": 22}},
                    gauge={
                        "axis": {"range": [0, 100]},
                        "bar": {"color": color},
                        "steps": [
                            {"range": [0, 40],  "color": "rgba(231,76,60,0.15)"},
                            {"range": [40, 65], "color": "rgba(241,196,15,0.15)"},
                            {"range": [65, 100],"color": "rgba(46,204,113,0.15)"},
                        ],
                        "threshold": {
                            "line": {"color": color, "width": 4},
                            "thickness": 0.75,
                            "value": score,
                        },
                    },
                ))
                fig.update_layout(height=300, margin=dict(t=30, b=0, l=20, r=20))
                st.plotly_chart(fig, use_container_width=True)

                m = extract_code_metrics(code_input)
                st.metric("Lines of code",  m["num_lines"])
                st.metric("Has docstring",  "Yes" if m["has_docstring"] else "No")
                st.metric("Has comments",   "Yes" if m["num_comments"] > 0 else "No")

                if pred == 1:
                    st.success("✅ Good quality code detected.", icon="🟢")
                else:
                    tips = []
                    if not m["has_docstring"]:
                        tips.append("Add a docstring to describe the function.")
                    if not m["num_comments"]:
                        tips.append("Add inline comments for clarity.")
                    if m["num_functions"] and len(code_input) < 80:
                        tips.append("Function body seems very short — consider adding logic.")
                    st.error("⚠️ Code quality may need improvement.", icon="🔴")
                    for tip in tips:
                        st.markdown(f"- {tip}")
        else:
            st.info("Enter code and click **Analyse** to see the result.")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — MODEL DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.title("📊 Model Dashboard")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Accuracy",    f"{metrics['accuracy']*100:.2f}%")
    m2.metric("ROC-AUC",     f"{metrics['roc_auc']:.4f}")
    m3.metric("Estimators",  clf.n_estimators)
    m4.metric("TF-IDF feats", tfidf.max_features)

    st.divider()
    col_fi, col_dist = st.columns(2, gap="large")

    with col_fi:
        st.subheader("Top Feature Importances")
        # TF-IDF feature names + metric names
        feat_names = list(tfidf.get_feature_names_out()) + bundle["metric_cols"]
        importances = pd.Series(clf.feature_importances_, index=feat_names,
                                name="importance") \
                        .sort_values(ascending=False).head(15)
        fig_fi = px.bar(
            importances.reset_index(),
            x="importance", y="index",
            orientation="h",
            labels={"index": "Feature", "importance": "Importance"},
            color="importance",
            color_continuous_scale="Blues",
        )
        fig_fi.update_layout(yaxis={"categoryorder": "total ascending"},
                             coloraxis_showscale=False, height=420)
        st.plotly_chart(fig_fi, use_container_width=True)

    with col_dist:
        st.subheader("Training Set Class Distribution")
        counts = df["label"].map({0: "Poor Quality", 1: "Good Quality"}).value_counts()
        fig_pie = px.pie(
            values=counts.values,
            names=counts.index,
            color=counts.index,
            color_discrete_map={"Good Quality": "#2ecc71", "Poor Quality": "#e74c3c"},
            hole=0.4,
        )
        fig_pie.update_layout(height=420)
        st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("Model Parameters")
    st.json({k: v for k, v in clf.get_params().items() if v is not None})

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — CODE EXPLORER
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.title("🔍 Code Explorer")
    st.markdown(f"**{len(df)} training samples · binary quality target**")

    # Compute metrics for all training samples
    metrics_df = pd.DataFrame([extract_code_metrics(c) for c in df["code"]])
    metrics_df["label"] = df["label"].map({0: "Poor Quality", 1: "Good Quality"}).values
    metrics_df["code_preview"] = [c[:60] + "…" if len(c) > 60 else c for c in df["code"]]

    st.subheader("Training Samples")
    st.dataframe(metrics_df[["code_preview", "label", "num_lines", "has_docstring",
                              "code_length"]].rename(columns={
        "code_preview": "Code preview",
        "label": "Quality",
        "num_lines": "Lines",
        "has_docstring": "Docstring",
        "code_length": "Length",
    }), use_container_width=True, height=280)

    st.divider()
    col_hist, col_box = st.columns(2, gap="large")
    numeric_cols = [c for c in metrics_df.columns if c not in ("label", "code_preview")]

    with col_hist:
        st.subheader("Metric Distribution")
        sel = st.selectbox("Select metric", numeric_cols, key="hist_metric")
        fig_h = px.histogram(
            metrics_df, x=sel, color="label",
            barmode="overlay", opacity=0.75,
            color_discrete_map={"Good Quality": "#2ecc71", "Poor Quality": "#e74c3c"},
            labels={"color": "Class"},
        )
        fig_h.update_layout(height=360)
        st.plotly_chart(fig_h, use_container_width=True)

    with col_box:
        st.subheader("Box Plot by Class")
        sel_b = st.selectbox("Select metric", numeric_cols, key="box_metric",
                             index=min(1, len(numeric_cols)-1))
        fig_b = px.box(
            metrics_df, x="label", y=sel_b, color="label",
            color_discrete_map={"Good Quality": "#2ecc71", "Poor Quality": "#e74c3c"},
        )
        fig_b.update_layout(height=360, showlegend=False)
        st.plotly_chart(fig_b, use_container_width=True)

    st.subheader("Correlation Matrix (code metrics)")
    corr = metrics_df[numeric_cols].corr()
    fig_corr = px.imshow(
        corr, text_auto=".2f", aspect="auto",
        color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
    )
    fig_corr.update_layout(height=460)
    st.plotly_chart(fig_corr, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 — LLM PIPELINE
# ═══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.title("🤖 LLM Pipeline Architecture")
    st.markdown("""
This project implements an end-to-end pipeline for **evaluating Large Language Models
on BigCodeBench** — a comprehensive coding benchmark for Python.
""")

    stages = [
        ("📥 Data Ingestion",
         "Stream `bigcode/bigcodebench` from HuggingFace Hub · cache locally · validate schema"),
        ("🔤 Tokenisation",
         "CodeBERT / GraphCodeBERT tokenizer · `max_length=512` · padding + truncation"),
        ("🧠 Model Inference",
         "HuggingFace `AutoModelForSequenceClassification` (CodeBERT-base) · GPU/CPU"),
        ("📊 Evaluation",
         "Accuracy · Precision · Recall · F1 · Confusion Matrix · Classification Report"),
        ("🚀 REST API",
         "Flask `/api/predict` · `/api/predict_batch` · `/api/tokenize` · `/api/info`"),
        ("📈 Monitoring",
         "JSON structured logging · MLflow experiment tracking · W&B integration"),
        ("🐳 Containerisation",
         "Dockerfile · Docker Compose · Nginx reverse proxy · GitHub Actions CI/CD"),
    ]

    for title, desc in stages:
        with st.expander(title, expanded=False):
            st.markdown(f"**{desc}**")

    st.divider()
    st.subheader("REST API Endpoints")
    api_data = {
        "Endpoint":    ["/health", "/api/predict", "/api/predict_batch",
                        "/api/tokenize", "/api/info"],
        "Method":      ["GET", "POST", "POST", "POST", "GET"],
        "Description": [
            "Health check — device + model-loaded status",
            "Single code snippet inference (quality classification)",
            "Batch inference over multiple samples",
            "Tokenize text and return token IDs",
            "Model metadata, parameter count, device",
        ],
    }
    st.table(pd.DataFrame(api_data))

    st.subheader("Project Structure")
    st.code("""
Bigcodebench-llm-project/
├── src/
│   ├── data/           # BigCodeBenchLoader, CodeBenchPreprocessor, TokenizerManager
│   ├── features/       # CodeFeatureExtractor, TextFeatureExtractor, FeatureEngineer
│   ├── models/         # ModelEvaluator, MetricsComputer
│   ├── utils/          # config, helpers, logger
│   └── visualization/  # DataVisualizer, MetricsVisualizer
├── tests/              # pytest suite (18 tests, all passing)
├── flask_app.py        # REST API (Flask)
├── streamlit_app.py    # This dashboard
├── train_demo.py       # Demo model training (TF-IDF + RandomForest)
├── models/
│   └── bigcode_demo.pkl
├── config/config.yaml
├── Dockerfile
├── docker-compose.yml
├── requirements.txt        # Streamlit Cloud runtime
├── requirements-ci.txt     # CI-safe dependencies
└── .github/workflows/ci.yml
""", language="text")

    st.subheader("Supported Model Backends")
    model_data = {
        "Alias":        ["codebert", "graphcodebert", "codet5", "codeberta", "gpt2"],
        "HuggingFace ID": [
            "microsoft/codebert-base",
            "microsoft/graphcodebert-base",
            "Salesforce/codet5-base",
            "huggingface/CodeBERTa-small-v1",
            "gpt2",
        ],
    }
    st.table(pd.DataFrame(model_data))
