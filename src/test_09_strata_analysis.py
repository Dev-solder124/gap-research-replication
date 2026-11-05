"""
Test 9: Survivorship and Liquidity Strata
Manuscript Reference: Table 11, Figure 7, Section 4.7
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
from src.data_loader import load_trades_clean, load_subuniverse_symbols

def format_stars(p_val):
    if p_val < 0.01: return "***"
    elif p_val < 0.05: return "**"
    elif p_val < 0.10: return "*"
    else: return ""

def two_way_cluster_ols(y, X, cluster_day, cluster_stock):
    model = sm.OLS(y, X).fit()
    params = model.params
    cov_day = model.get_robustcov_results(cov_type='cluster', groups=cluster_day).cov_params()
    cov_stock = model.get_robustcov_results(cov_type='cluster', groups=cluster_stock).cov_params()
    cov_white = model.get_robustcov_results(cov_type='HC0').cov_params()
    cov_2way = cov_day + cov_stock - cov_white
    diag = np.diag(cov_2way)
    diag = np.where(diag > 0, diag, np.diag(cov_day))
    se_2way = np.sqrt(diag)
    t_stats = params / se_2way
    p_vals = 2 * (1 - stats.norm.cdf(np.abs(t_stats)))
    return params, se_2way, t_stats, p_vals

def run_test_9():
    print("Running Test 9: Survivorship and Liquidity Strata (Table 11, Figure 7)...")
    trades = load_trades_clean(resolved_only=True)
    all_trades = load_trades_clean(resolved_only=False)
    sub_univs = load_subuniverse_symbols()
    
    # Ex-ante 2022 turnover proxy: trade counts in first 60 trading days
    u_dates = sorted(all_trades['date'].unique())
    first_60 = set(u_dates[:60])
    counts_60 = all_trades[all_trades['date'].isin(first_60)].groupby('symbol_root').size()
    
    all_symbols = sorted(all_trades['symbol_root'].unique())
    s_series = pd.Series(0, index=all_symbols)
    s_series.update(counts_60)
    q_labels = ['Liquidity Q4 (lowest)', 'Liquidity Q3', 'Liquidity Q2', 'Liquidity Q1 (highest)']
    s_quartiles = pd.qcut(s_series.rank(method='first'), q=4, labels=q_labels)

    strata_definitions = [
        ('Full 480 Universe', set(all_symbols)),
        ('Nifty 50 Sub-universe', set([s.replace('_1M', '') for s in sub_univs['nifty50_symbols']])),
        ('Midcap 50 Sub-universe', set([s.replace('_1M', '') for s in sub_univs['midcap50_symbols']])),
        ('Smallcap 50 Sub-universe', set([s.replace('_1M', '') for s in sub_univs['smcap50_symbols']])),
        ('Liquidity Q1 (highest)', set(s_quartiles[s_quartiles == 'Liquidity Q1 (highest)'].index)),
        ('Liquidity Q2', set(s_quartiles[s_quartiles == 'Liquidity Q2'].index)),
        ('Liquidity Q3', set(s_quartiles[s_quartiles == 'Liquidity Q3'].index)),
        ('Liquidity Q4 (lowest)', set(s_quartiles[s_quartiles == 'Liquidity Q4 (lowest)'].index))
    ]

    records = []
    forest_plot_data = []

    for name, syms in strata_definitions:
        sub = trades[trades['symbol_root'].isin(syms)].copy()
        y = sub['is_win'].values
        post = (sub['regime'] == 'post_shock').astype(float).values
        pre = (sub['regime'] == 'pre_stable').astype(float).values
        X = sm.add_constant(np.column_stack([post, pre]))
        
        p, se, t, pvals = two_way_cluster_ols(y, X, sub['date'].values, sub['symbol'].values)
        beta1, se1, t1, pval1 = p[1], se[1], t[1], pvals[1]
        
        n_stable = len(sub[sub['regime'] == 'stable'])
        n_post = len(sub[sub['regime'] == 'post_shock'])
        n_syms = sub['symbol_root'].nunique()
        stars = format_stars(pval1)
        
        records.append({
            'Stratum': name,
            'PostShock Indicator (β₁)': f"{beta1 * 100:.2f}%{stars}",
            'Two-Way SE (%)': f"{se1 * 100:.2f}%",
            't-Statistic': f"{t1:.2f}",
            'p-value': f"{pval1:.4f}" if pval1 >= 0.0001 else "< 0.0001",
            'N Resolved (Stable)': n_stable,
            'N Resolved (Post-Shock)': n_post,
            'Number of Symbols': n_syms
        })
        
        forest_plot_data.append({
            'name': name,
            'beta': beta1 * 100.0,
            'se': se1 * 100.0,
            'ci_lower': (beta1 - 1.96 * se1) * 100.0,
            'ci_upper': (beta1 + 1.96 * se1) * 100.0
        })

    df_table11 = pd.DataFrame(records)

    # Save CSV
    os.makedirs(os.path.join(BASE_DIR, 'output', 'tables'), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, 'output', 'figures'), exist_ok=True)
    
    csv_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_11_strata_analysis.csv')
    df_table11.to_csv(csv_path, index=False)

    # Generate Markdown Table
    md_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_11_strata_analysis.md')
    md_lines = [
        "# Table 11: Survivorship and Liquidity Strata LPM Estimations",
        "",
        "Linear Probability Model (LPM) of trade win outcome across 8 sub-universe and ex-ante liquidity strata. "
        "Standard errors are two-way clustered by trading day and stock symbol. Significance: * p < 0.10, ** p < 0.05, *** p < 0.01.",
        "",
        "| Stratum | PostShock Indicator (β₁) | Two-Way SE (%) | t-Statistic | p-value | N Resolved (Stable) | N Resolved (Post-Shock) | Number of Symbols |",
        "|:---|---:|---:|---:|:---:|---:|---:|---:|"
    ]
    for _, r in df_table11.iterrows():
        md_lines.append(
            f"| {r['Stratum']} | {r['PostShock Indicator (β₁)']} | {r['Two-Way SE (%)']} | {r['t-Statistic']} | "
            f"{r['p-value']} | {r['N Resolved (Stable)']:,} | {r['N Resolved (Post-Shock)']:,} | {r['Number of Symbols']:,} |"
        )
    md_lines.append("")
    
    with open(md_path, 'w') as f:
        f.write('\n'.join(md_lines))
    print(f"Table 11 saved to {csv_path} and {md_path}")

    # --- Plot Figure 7: Forest Plot ---
    df_forest = pd.DataFrame(forest_plot_data).iloc[::-1].reset_index(drop=True)
    fig_path = os.path.join(BASE_DIR, 'output', 'figures', 'figure_07_strata_forest_plot.png')
    
    plt.figure(figsize=(10, 6), dpi=300)
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    y_pos = np.arange(len(df_forest))
    
    plt.errorbar(
        df_forest['beta'], y_pos, 
        xerr=1.96 * df_forest['se'], 
        fmt='o', color='#1f77b4', ecolor='#1f77b4', elinewidth=2.0, capsize=4, markersize=7,
        label='Post-Shock β₁ (95% CI)'
    )
    
    plt.axvline(x=0, color='#333333', linestyle='--', linewidth=1.0, alpha=0.7)
    plt.axvline(x=df_forest.loc[df_forest['name'] == 'Full 480 Universe', 'beta'].values[0], color='#d62728', linestyle=':', linewidth=1.2, label='Full 480 Benchmark (-8.15%)')
    
    plt.yticks(y_pos, df_forest['name'], fontsize=10)
    plt.xlabel('Post-Shock Treatment Effect on Win Rate (Percentage Points)', fontsize=11, labelpad=8)
    plt.title('Figure 7: Post-Shock Win-Rate Contraction Across Strata (Forest Plot)', fontsize=13, fontweight='bold', pad=12)
    plt.legend(frameon=True, loc='lower left', fontsize=10)
    plt.tight_layout()
    plt.savefig(fig_path, dpi=300)
    plt.close()
    
    print(f"Figure 7 saved to {fig_path}")
    return df_table11

if __name__ == '__main__':
    run_test_9()

