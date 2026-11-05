"""
Test 11: Granger Causality — Sign vs Magnitude of Oil Shock
Manuscript Reference: Figure 6, Section 4.9
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
import matplotlib.pyplot as plt
from src.data_loader import load_daily_clean

def format_stars(p_val):
    if p_val < 0.01: return "***"
    elif p_val < 0.05: return "**"
    elif p_val < 0.10: return "*"
    else: return ""

def granger_f_test(y_series, x_series, L):
    """
    Bivariate Granger causality F-test based on OLS SSR comparison:
    F = [(SSR_r - SSR_ur) / L] / [SSR_ur / (T - 2L - 1)]
    """
    T = len(y_series)
    y_lags = np.column_stack([y_series[L - i - 1 : T - i - 1] for i in range(L)])
    x_lags = np.column_stack([x_series[L - i - 1 : T - i - 1] for i in range(L)])
    y_target = y_series[L:]
    
    # Restricted model
    X_r = sm.add_constant(y_lags)
    res_r = sm.OLS(y_target, X_r).fit()
    ssr_r = res_r.ssr
    
    # Unrestricted model
    X_ur = sm.add_constant(np.column_stack([y_lags, x_lags]))
    res_ur = sm.OLS(y_target, X_ur).fit()
    ssr_ur = res_ur.ssr
    
    df_num = L
    df_denom = len(y_target) - 2 * L - 1
    
    F = ((ssr_r - ssr_ur) / df_num) / (ssr_ur / df_denom)
    p_val = 1.0 - stats.f.cdf(F, df_num, df_denom)
    return F, p_val

def run_test_11():
    print("Running Test 11: Granger Causality (Figure 6)...")
    daily = load_daily_clean()
    
    brent_path = os.path.join(BASE_DIR, 'data', 'macro', 'XBR_USD Historical Data.csv')
    brent = pd.read_csv(brent_path, encoding='utf-8-sig')
    brent['date'] = pd.to_datetime(brent['Date']).dt.strftime('%Y-%m-%d')
    brent = brent.sort_values('date').reset_index(drop=True)
    brent['R_brent'] = np.log(brent['Price'] / brent['Price'].shift(1))
    brent['abs_R_brent'] = brent['R_brent'].abs()
    brent['sigma_brent_20d'] = brent['R_brent'].rolling(20).std()

    df = daily.merge(brent[['date', 'R_brent', 'abs_R_brent', 'sigma_brent_20d']], on='date', how='inner')
    df = df.dropna(subset=['resolved_wr', 'R_brent', 'abs_R_brent', 'sigma_brent_20d']).reset_index(drop=True)
    
    lags = [1, 3, 5, 10]
    pairs = [
        ('R_brent → WR', df['resolved_wr'].values, df['R_brent'].values, 'Signed Brent Return → WR'),
        ('|R_brent| → WR', df['resolved_wr'].values, df['abs_R_brent'].values, '|Brent Return| (Magnitude) → WR'),
        ('σ_Brent(20d) → WR', df['resolved_wr'].values, df['sigma_brent_20d'].values, 'Brent Realized Volatility → WR'),
        ('WR → R_brent', df['R_brent'].values, df['resolved_wr'].values, 'WR → Signed Brent Return (Reverse)'),
        ('WR → |R_brent|', df['abs_R_brent'].values, df['resolved_wr'].values, 'WR → |Brent Return| (Reverse)')
    ]

    records = []
    plot_dict = {p[0]: [] for p in pairs}

    for short_label, y_vals, x_vals, full_desc in pairs:
        for lag in lags:
            F, p = granger_f_test(y_vals, x_vals, lag)
            stars = format_stars(p)
            records.append({
                'Causal Direction': full_desc,
                'Relationship': short_label,
                'Lag Order (L)': lag,
                'Granger F-Statistic': f"{F:.3f}{stars}",
                'p-value': f"{p:.4f}" if p >= 0.0001 else "< 0.0001",
                '_F': F,
                '_p': p
            })
            plot_dict[short_label].append(F)

    df_granger = pd.DataFrame(records)

    # Save CSV
    os.makedirs(os.path.join(BASE_DIR, 'output', 'tables'), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, 'output', 'figures'), exist_ok=True)
    
    csv_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_granger_causality.csv')
    df_granger.drop(columns=['_F', '_p']).to_csv(csv_path, index=False)

    # Generate Markdown Table
    md_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_granger_causality.md')
    md_lines = [
        "# Table: Bivariate Granger Causality Tests — Sign vs Magnitude vs Volatility",
        "",
        "Bivariate Granger causality F-tests evaluating whether oil price direction (R_brent), shock magnitude (|R_brent|), "
        "or realized volatility (σ_Brent 20d) predictive Granger-cause the daily strategy win rate (WR_t). "
        "Tested across lag orders L ∈ {1, 3, 5, 10}. Significance: * p < 0.10, ** p < 0.05, *** p < 0.01.",
        "",
        "| Relationship | Lag Order (L) | Granger F-Statistic | p-value |",
        "|:---|---:|---:|:---:|"
    ]
    for _, r in df_granger.iterrows():
        md_lines.append(f"| {r['Causal Direction']} | {r['Lag Order (L)']} | {r['Granger F-Statistic']} | {r['p-value']} |")
    md_lines.append("")
    
    with open(md_path, 'w') as f:
        f.write('\n'.join(md_lines))
    print(f"Granger causality table saved to {csv_path} and {md_path}")

    # --- Plot Figure 6: Grouped Bar Chart of Granger F-Statistics ---
    fig_path = os.path.join(BASE_DIR, 'output', 'figures', 'figure_06_granger_causality_f_stats.png')
    
    plt.figure(figsize=(11, 5.5), dpi=300)
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    x = np.arange(len(lags))
    width = 0.16
    
    colors = ['#aec7e8', '#ff7f0e', '#d62728', '#2ca02c', '#98df8a']
    
    for i, (short_label, _, _, full_desc) in enumerate(pairs):
        offset = (i - 2) * width
        plt.bar(x + offset, plot_dict[short_label], width, label=short_label, color=colors[i], alpha=0.9)

    # Reference 5% critical value line (F ~ 3.84 for L=1, F ~ 2.60 for L=3, etc.)
    plt.axhline(y=3.84, color='#555555', linestyle='--', linewidth=1.2, alpha=0.7, label='L=1 5% Critical Value (F=3.84)')
    
    plt.title('Figure 6: Bivariate Granger Causality F-Statistics: Sign vs Magnitude vs Volatility', fontsize=13, fontweight='bold', pad=12)
    plt.xlabel('Lag Order (L Days)', fontsize=11, labelpad=8)
    plt.ylabel('Granger Causality F-Statistic', fontsize=11, labelpad=8)
    plt.xticks(x, [f'Lag {l}' for l in lags], fontsize=10)
    plt.legend(frameon=True, loc='upper right', fontsize=9)
    plt.tight_layout()
    plt.savefig(fig_path, dpi=300)
    plt.close()
    
    print(f"Figure 6 saved to {fig_path}")
    return df_granger

if __name__ == '__main__':
    run_test_11()

