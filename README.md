# Smart Attendance - AI Model

Predicts which students are at risk of low attendance in the coming week, and flags suspicious attendance patterns, for the Smart Attendance & Classroom Verification project (ATT).

## What this does

- **Risk prediction**: a Logistic Regression model estimates the probability that a student's attendance will drop below 70% next week, using their recent attendance history (previous attendance rate, 3-week trend, late/absence rates, course load).
- **Rule-based anomaly detection**: flags repeated lateness, low attendance, and manually-entered records for review.
- **Baseline comparison**: the model is benchmarked against a simple rule-based baseline (per the project's AI release gate requirement). Current results:

| Metric | Rule-Based Baseline | Balanced Logistic Regression |
|---|---|---|
| Accuracy | 81.4% | 82.9% |
| Precision | 77.8% | 77.8% |
| Recall | 79.3% | 84.1% |
| F1 Score | 78.5% | 80.9% |

All metrics are measured on an untouched test set; only the training set was class-balanced.

## Files

| File | Purpose |
|---|---|
| `ai model.ipynb` | Full pipeline: data cleaning, feature engineering, model training, evaluation, calibration, anomaly detection |
| `attendance_history_60000.csv` | Training/test data (synthetic) |

## Requirements

```
pandas
numpy
matplotlib
scikit-learn
```

Install with:
```
pip install pandas numpy matplotlib scikit-learn
```

## How to run

1. Make sure `attendance_history_60000.csv` is in the same folder as the notebook.
2. Open `ai model.ipynb` in Jupyter (or run it as a script).
3. Run all cells top to bottom.

## Outputs

Running the notebook produces:
- `attendance_ai_predictions.csv` — per-student risk scores
- `attendance_calibration.csv` — how well predicted probabilities match reality
- `attendance_model_features.csv` — feature importance
- `attendance_baseline_comparison.csv` — baseline vs. model metrics
- `attendance_anomaly_report.csv` — flagged anomalies

## Limitations

- No explicit failed-QR-scan field is available in the data.
- No correction-request table is available for correction-volume analysis.
- Manual entries are flagged for review only, not automatically classified as fraud.
- Predictions are advisory: they never change attendance records automatically, and the core attendance system works without this service running.
