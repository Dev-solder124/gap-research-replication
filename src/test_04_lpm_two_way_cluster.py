"""
Test 4: Two-Way Clustered Linear Probability Model
Manuscript Reference: Table 6, Section 4.2
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy import stats
from src.data_loader import load_trades_clean

def two_way_cluster_ols(y, X, cluster_day, cluster_stock):
    """
    Two-way clustering by trading day and stock symbol (Cameron, Gelbach, and Miller 2011).
    V_2way = V_day + V_stock - V_White
    """
    model = sm.OLS(y, X).fit()
    params = model.params
    cov_day = model.get_robustcov_results(cov_type='cluster', groups=cluster_day).cov_params()
    cov_stock = model.get_robustcov_results(cov_type='cluster', groups=cluster_stock).cov_params()
    cov_white = model.get_robustcov_results(cov_type='HC0').cov_params()
    
    cov_2way = cov_day + cov_stock - cov_white
    # Ensure positive semidefinite diagonal
    diag = np.diag(cov_2way)
    diag = np.where(diag > 0, diag, np.diag(cov_day))
    se_2way = np.sqrt(diag)
    
    t_stats = params / se_2way
    p_vals = 2 * (1 - stats.norm.cdf(np.abs(t_stats)))
    return params, se_2way, t_stats, p_vals

def format_stars(p_val):
    if p_val < 0.01: return "***"
    elif p_val < 0.05: return "**"
    elif p_val < 0.10: return "*"
    else: return ""

def run_test_4():
    print("Running Test 4: Two-Way Clustered Linear Probability Model (Table 6)...")
    trades = load_trades_clean(resolved_only=True)
    stable_trades = trades[trades['regime'] == 'stable'].copy()
    
    subsample_defs = [
        ('Full Sample (All 1,116 Days)', 'full_sample'),
        ('January 2026 Alone (Pre-Shock Month 1)', 'month_2026-01'),
        ('February 2026 Alone (Pre-Shock Month 2)', 'month_2026-02'),
        ('March 2026 Alone (Acute Shock Month 3)', 'month_2026-03'),
        ('April 2026 Alone (Shock Month 4)', 'month_2026-04'),
        ('May 2026 Alone (Shock Month 5)', 'month_2026-05'),
        ('Full Post-Shock Window (≥ 2026-03-01)', 'post_shock_all')
    ]
    
    records = []
    
    for label, kind in subsample_defs:
        if kind == 'full_sample':
            y = trades['is_win'].values
            post = (trades['regime'] == 'post_shock').astype(float).values
            pre = (trades['regime'] == 'pre_stable').astype(float).values
            X = sm.add_constant(np.column_stack([post, pre]))
            cluster_day = trades['date'].values
            cluster_stock = trades['symbol'].values
            
            p, se, t, pvals = two_way_cluster_ols(y, X, cluster_day, cluster_stock)
            beta1 = p[1]
            se1 = se[1]
            t1 = t[1]
            pval1 = pvals[1]
            n_trades = len(trades)
            n_days = trades['date'].nunique()
            
        elif kind.startswith('month_'):
            month_str = kind.replace('month_', '')
            m_trades = trades[trades['date'].str.startswith(month_str)].copy()
            # Baseline: stable regime excluding the month if it fell in stable
            base_trades = stable_trades[~stable_trades['date'].str.startswith(month_str)].copy()
            sub = pd.concat([base_trades, m_trades]).reset_index(drop=True)
            sub['is_target'] = (sub['date'].str.startswith(month_str)).astype(float)
            
            y = sub['is_win'].values
            X = sm.add_constant(sub['is_target'].values)
            cluster_day = sub['date'].values
            cluster_stock = sub['symbol'].values
            
            p, se, t, pvals = two_way_cluster_ols(y, X, cluster_day, cluster_stock)
            beta1 = p[1]
            se1 = se[1]
            t1 = t[1]
            pval1 = pvals[1]
            n_trades = len(m_trades)
            n_days = m_trades['date'].nunique()
            
        elif kind == 'post_shock_all':
            post_trades = trades[trades['regime'] == 'post_shock'].copy()
            sub = pd.concat([stable_trades, post_trades]).reset_index(drop=True)
            sub['is_post'] = (sub['regime'] == 'post_shock').astype(float)
            
            y = sub['is_win'].values
            X = sm.add_constant(sub['is_post'].values)
            cluster_day = sub['date'].values
            cluster_stock = sub['symbol'].values
            
            p, se, t, pvals = two_way_cluster_ols(y, X, cluster_day, cluster_stock)
            beta1 = p[1]
            se1 = se[1]
            t1 = t[1]
            pval1 = pvals[1]
            n_trades = len(post_trades)
            n_days = post_trades['date'].nunique()

        stars = format_stars(pval1)
        records.append({
            'Sub-Sample': label,
            'PostShock Indicator (β₁)': f"{beta1 * 100:.2f}%{stars}",
            'Two-Way SE (%)': f"{se1 * 100:.2f}%",
            't-Statistic': f"{t1:.2f}",
            'p-value': f"{pval1:.4f}" if pval1 >= 0.0001 else "< 0.0001",
            'Resolved Trades': n_trades,
            'Trading Days': n_days,
            '_raw_beta': beta1,
            '_raw_se': se1,
            '_raw_t': t1,
            '_raw_p': pval1
        })

    df_table6 = pd.DataFrame(records)
    
    # Save CSV
    os.makedirs(os.path.join(BASE_DIR, 'output', 'tables'), exist_ok=True)
    csv_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_06_lpm_two_way_cluster.csv')
    df_table6.drop(columns=['_raw_beta', '_raw_se', '_raw_t', '_raw_p']).to_csv(csv_path, index=False)
    
    # Generate Markdown Table
    md_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_06_lpm_two_way_cluster.md')
    md_lines = [
        "# Table 6: Two-Way Clustered Linear Probability Model",
        "",
        "Linear Probability Model (LPM) of trade win outcome (1 = target hit, 0 = stop-loss hit). "
        "Standard errors are two-way clustered by trading day and stock symbol following Cameron, Gelbach, and Miller (2011). "
        "Stable regime (2022-03-01 to 2026-02-28) is the omitted baseline. Significance: * p < 0.10, ** p < 0.05, *** p < 0.01.",
        "",
        "| Sub-Sample | PostShock Indicator (β₁) | Two-Way SE (%) | t-Statistic | p-value | Resolved Trades | Trading Days |",
        "|:---|---:|---:|---:|:---:|---:|---:|"
    ]
    for _, r in df_table6.iterrows():
        md_lines.append(
            f"| {r['Sub-Sample']} | {r['PostShock Indicator (β₁)']} | {r['Two-Way SE (%)']} | {r['t-Statistic']} | {r['p-value']} | {r['Resolved Trades']:,} | {r['Trading Days']:,} |"
        )
    md_lines.append("")
    
    with open(md_path, 'w') as f:
        f.write('\n'.join(md_lines))
    print(f"Table 6 saved to {csv_path} and {md_path}")
    return df_table6

if __name__ == '__main__':
    run_test_4()

