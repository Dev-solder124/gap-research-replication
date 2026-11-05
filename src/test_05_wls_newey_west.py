"""
Test 5: Daily WLS with Newey-West HAC
Manuscript Reference: Table 7, Section 4.3
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import pandas as pd
import numpy as np
import statsmodels.api as sm
from src.data_loader import load_daily_clean

def format_stars(p_val):
    if p_val < 0.01: return "***"
    elif p_val < 0.05: return "**"
    elif p_val < 0.10: return "*"
    else: return ""

def run_test_5():
    print("Running Test 5: Daily WLS with Newey-West HAC (Table 7)...")
    daily = load_daily_clean()
    
    y = daily['resolved_wr'].values
    post = (daily['regime'] == 'post_shock').astype(float).values
    pre = (daily['regime'] == 'pre_stable').astype(float).values
    weights = daily['n_resolved'].values
    
    # Specification 1: As specified in TESTS.md: WR_t = alpha + beta_1 * PostShock_t + eps_t
    X_spec1 = sm.add_constant(post)
    model1 = sm.WLS(y, X_spec1, weights=weights)
    
    # Specification 2: With Pre-Stable control (matching trade-level LPM baseline)
    X_spec2 = sm.add_constant(np.column_stack([post, pre]))
    model2 = sm.WLS(y, X_spec2, weights=weights)
    
    lags = [5, 10, 20]
    records = []
    
    for lag in lags:
        res1 = model1.fit(cov_type='HAC', cov_kwds={'maxlags': lag})
        beta1_1 = res1.params[1]
        se1_1 = res1.bse[1]
        t1_1 = res1.tvalues[1]
        p1_1 = res1.pvalues[1]
        r2_1 = res1.rsquared
        stars1 = format_stars(p1_1)
        
        res2 = model2.fit(cov_type='HAC', cov_kwds={'maxlags': lag})
        beta1_2 = res2.params[1]
        se1_2 = res2.bse[1]
        t1_2 = res2.tvalues[1]
        p1_2 = res2.pvalues[1]
        r2_2 = res2.rsquared
        stars2 = format_stars(p1_2)
        
        records.append({
            'HAC Lag': f"Lag = {lag}",
            'PostShock β₁ (%)': f"{beta1_1 * 100:.2f}%{stars1}",
            'Newey-West SE (%)': f"{se1_1 * 100:.2f}%",
            't-Statistic': f"{t1_1:.2f}",
            'p-value': f"{p1_1:.4e}",
            'Weighted R²': f"{r2_1:.4f}",
            'PostShock β₁ (Pre-Stable Controlled)': f"{beta1_2 * 100:.2f}%{stars2}",
            'SE (Pre-Controlled)': f"{se1_2 * 100:.2f}%",
            't-Stat (Pre-Controlled)': f"{t1_2:.2f}",
            'N Observations': len(daily)
        })

    df_table7 = pd.DataFrame(records)
    
    # Save CSV
    os.makedirs(os.path.join(BASE_DIR, 'output', 'tables'), exist_ok=True)
    csv_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_07_wls_newey_west.csv')
    df_table7.to_csv(csv_path, index=False)
    
    # Generate Markdown Table
    md_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_07_wls_newey_west.md')
    md_lines = [
        "# Table 7: Daily WLS with Newey-West HAC Standard Errors",
        "",
        "Weighted Least Squares (WLS) regression of daily resolved win rate (WR_t) on PostShock indicator across 1,116 trading sessions. "
        "Weights: daily count of resolved trades (n_resolved). Standard errors: Newey-West HAC with lags = 5, 10, and 20. "
        "Significance: * p < 0.10, ** p < 0.05, *** p < 0.01.",
        "",
        "| HAC Lag | PostShock β₁ (%) | Newey-West SE (%) | t-Statistic | p-value | Weighted R² | β₁ (Pre-Stable Controlled) | SE (Pre-Controlled) |",
        "|:---|---:|---:|---:|:---:|---:|---:|---:|"
    ]
    for _, r in df_table7.iterrows():
        md_lines.append(
            f"| {r['HAC Lag']} | {r['PostShock β₁ (%)']} | {r['Newey-West SE (%)']} | {r['t-Statistic']} | {r['p-value']} | {r['Weighted R²']} | {r['PostShock β₁ (Pre-Stable Controlled)']} | {r['SE (Pre-Controlled)']} |"
        )
    md_lines.append("")
    
    with open(md_path, 'w') as f:
        f.write('\n'.join(md_lines))
        
    print(f"Table 7 saved to {csv_path} and {md_path}")
    return df_table7

if __name__ == '__main__':
    run_test_5()

