import pandas as pd

summary = [
    {
        "rule_id": "DQ01",
        "rule_name": "Primary Key Uniqueness",
        "status": "PASS",
        "failures": 0
    },
    {
        "rule_id": "DQ03",
        "rule_name": "Foreign Key Integrity",
        "status": "FAIL",
        "failures": 304
    },
    {
        "rule_id": "DQ04",
        "rule_name": "Balance Sheet Equation",
        "status": "PASS",
        "failures": 0
    },
    {
        "rule_id": "DQ05",
        "rule_name": "OPM Validation",
        "status": "REVIEW",
        "failures": 234
    }
]

df = pd.DataFrame(summary)

df.to_csv(
    "outputs/validation_summary.csv",
    index=False
)

print(df)