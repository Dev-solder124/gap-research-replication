"""
Test 6: Gap-Size Bin Win-Rate Analysis
Day-Clustered Linear Probability Models & Resolved vs. Nominal Win Rates
Manuscript Reference: Table 8, Figure 3, Section 4.4
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from src.data_loader import load_trades_clean

def format_stars(p_val):
    if p_val < 0.01: return "***"
    elif p_val < 0.05: return "**"
    elif p_val < 0.10: return "*"
    else: return ""

def run_test_6():
    print("Running Test 6: Gap-Size Bin Win-Rate Analysis (Table 8, Figure 3)...")
    trades = load_trades_clean(resolved_only=False)
    
    # 10 fixed bins
    bins = [0.0, 0.25, 0.50, 0.75, 1.00, 1.25, 1.50, 2.00, 2.50, 3.00, np.inf]
    labels = ['0.00–0.25', '0.25–0.50', '0.50–0.75', '0.75–1.00', '1.00–1.25',
              '1.25–1.50', '1.50–2.00', '2.00–2.50', '2.50–3.00', '3.00+']

    trades['bin'] = pd.cut(trades['gap_size_pct'], bins=bins, labels=labels, right=False)
    sub_all = trades[trades['regime'].isin(['stable', 'post_shock'])].copy()
    sub_all['post_shock'] = (sub_all['regime'] == 'post_shock').astype(float)
    sub_all['win_nominal'] = (sub_all['status'] == 'TARGET').astype(float)

    records = []
    plot_data = []

    for b in labels:
        b_all = sub_all[sub_all['bin'] == b].copy()
        b_res = b_all[b_all['status'].isin(['TARGET', 'STOP_LOSS'])].copy()
        b_res['win_resolved'] = (b_res['status'] == 'TARGET').astype(float)
        
        # Trade counts
        n_stable_total = len(b_all[b_all['regime'] == 'stable'])
        n_post_total = len(b_all[b_all['regime'] == 'post_shock'])
        
        n_stable_res = len(b_res[b_res['regime'] == 'stable'])
        n_post_res = len(b_res[b_res['regime'] == 'post_shock'])
        
        # Nominal Win Rates
        nom_wr_stable = b_all[b_all['regime'] == 'stable']['win_nominal'].mean() if n_stable_total > 0 else np.nan
        nom_wr_post = b_all[b_all['regime'] == 'post_shock']['win_nominal'].mean() if n_post_total > 0 else np.nan
        
        # Resolved Win Rates
        res_wr_stable = b_res[b_res['regime'] == 'stable']['win_resolved'].mean() if n_stable_res > 0 else np.nan
        res_wr_post = b_res[b_res['regime'] == 'post_shock']['win_resolved'].mean() if n_post_res > 0 else np.nan
        
        # Day-clustered LPM for Resolved Win Rate:
        # win_resolved = alpha + beta * post_shock + e, clustered by date
        X_res = sm.add_constant(b_res['post_shock'])
        res_model = sm.OLS(b_res['win_resolved'], X_res).fit(cov_type='cluster', cov_kwds={'groups': b_res['date']})
        diff_res = res_model.params['post_shock']
        se_res = res_model.bse['post_shock']
        t_res = res_model.tvalues['post_shock']
        p_res = res_model.pvalues['post_shock']
        stars_res = format_stars(p_res)
        
        # Day-clustered LPM for Nominal Win Rate:
        X_nom = sm.add_constant(b_all['post_shock'])
        nom_model = sm.OLS(b_all['win_nominal'], X_nom).fit(cov_type='cluster', cov_kwds={'groups': b_all['date']})
        diff_nom = nom_model.params['post_shock']
        se_nom = nom_model.bse['post_shock']
        t_nom = nom_model.tvalues['post_shock']
        p_nom = nom_model.pvalues['post_shock']
        stars_nom = format_stars(p_nom)

        records.append({
            'Gap Size Bin (%)': b,
            'Stable Total N': n_stable_total,
            'Stable Resolved N': n_stable_res,
            'Post Total N': n_post_total,
            'Post Resolved N': n_post_res,
            'Stable Resolved WR (%)': f"{res_wr_stable * 100:.2f}%",
            'Post Resolved WR (%)': f"{res_wr_post * 100:.2f}%",
            'Resolved Diff (pp)': f"{diff_res * 100:.2f}%{stars_res}",
            'Resolved Day-Clustered SE': f"{se_res * 100:.2f}%",
            'Resolved t-Stat': f"{t_res:.2f}",
            'Resolved p-value': f"{p_res:.4f}" if p_res >= 0.0001 else "< 0.0001",
            'Stable Nominal WR (%)': f"{nom_wr_stable * 100:.2f}%",
            'Post Nominal WR (%)': f"{nom_wr_post * 100:.2f}%",
            'Nominal Diff (pp)': f"{diff_nom * 100:.2f}%{stars_nom}",
            'Nominal Day-Clustered SE': f"{se_nom * 100:.2f}%",
            'Nominal t-Stat': f"{t_nom:.2f}",
            'Nominal p-value': f"{p_nom:.4f}" if p_nom >= 0.0001 else "< 0.0001"
        })

        plot_data.append({
            'bin': b,
            'res_s': res_wr_stable * 100.0,
            'res_p': res_wr_post * 100.0,
            'nom_s': nom_wr_stable * 100.0,
            'nom_p': nom_wr_post * 100.0
        })

    df_table8 = pd.DataFrame(records)

    # Save CSV
    os.makedirs(os.path.join(BASE_DIR, 'output', 'tables'), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, 'output', 'figures'), exist_ok=True)
    
    csv_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_08_gap_size_bins.csv')
    df_table8.to_csv(csv_path, index=False)

    # Generate Markdown Table
    md_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_08_gap_size_bins.md')
    md_lines = [
        "# Table 8: Gap-Size Bin Win-Rate Analysis and Structural Comparison",
        "",
        "Win rates across 10 fixed gap-size bins comparing Stable (2022-03-01 to 2026-02-28) and Post-Shock (≥ 2026-03-01) regimes. "
        "Differences are evaluated via day-clustered Linear Probability Models (LPM) clustering by trading session date to account for cross-sectional dependence. "
        "Both Resolved Win Rate (TARGET / (TARGET + STOP_LOSS)) and Nominal Win Rate (TARGET / ALL) are reported. "
        "Significance: * p < 0.10, ** p < 0.05, *** p < 0.01.",
        "",
        "| Gap Size Bin (%) | Stable Resolved WR | Post Resolved WR | Resolved Diff (Day-Clustered SE) | Resolved t-Stat (p-val) | Stable Nominal WR | Post Nominal WR | Nominal Diff (Day-Clustered SE) |",
        "|:---|---:|---:|---:|---:|---:|---:|---:|"
    ]
    for _, r in df_table8.iterrows():
        md_lines.append(
            f"| {r['Gap Size Bin (%)']} | {r['Stable Resolved WR (%)']} | {r['Post Resolved WR (%)']} | "
            f"{r['Resolved Diff (pp)']} ({r['Resolved Day-Clustered SE']}) | {r['Resolved t-Stat']} ({r['Resolved p-value']}) | "
            f"{r['Stable Nominal WR (%)']} | {r['Post Nominal WR (%)']} | {r['Nominal Diff (pp)']} ({r['Nominal Day-Clustered SE']}) |"
        )
    md_lines.append("")
    
    with open(md_path, 'w') as f:
        f.write('\n'.join(md_lines))
    print(f"Table 8 saved to {csv_path} and {md_path}")

    # Plot Figure 3: Side-by-Side Bar Chart for Resolved Win Rates
    df_plot = pd.DataFrame(plot_data)
    fig_path = os.path.join(BASE_DIR, 'output', 'figures', 'figure_03_gap_size_bins.png')
    
    plt.figure(figsize=(11, 5.5), dpi=300)
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    x = np.arange(len(df_plot))
    width = 0.38
    
    plt.bar(x - width/2, df_plot['res_s'], width, label='Stable Regime: Resolved WR', color='#1f77b4', alpha=0.9)
    plt.bar(x + width/2, df_plot['res_p'], width, label='Post-Shock Regime: Resolved WR', color='#d62728', alpha=0.9)
    
    plt.axhline(y=50.0, color='#555555', linestyle='--', linewidth=1.2, alpha=0.7, label='50% Breakeven Barrier')
    
    plt.title('Figure 3: Resolved Win Rate by Gap-Size Bin Across Regimes (Day-Clustered Inference)', fontsize=13, fontweight='bold', pad=12)
    plt.xlabel('Overnight Gap Size Range (% of Entry Price)', fontsize=11, labelpad=8)
    plt.ylabel('Resolved Win Rate (%)', fontsize=11, labelpad=8)
    plt.xticks(x, df_plot['bin'], rotation=30, ha='right', fontsize=9)
    plt.yticks(np.arange(20, 75, 10), fontsize=10)
    plt.ylim(20, 72)
    plt.legend(frameon=True, loc='upper left', fontsize=10)
    plt.tight_layout()
    plt.savefig(fig_path, dpi=300)
    plt.close()
    
    print(f"Figure 3 saved to {fig_path}")
    return df_table8

if __name__ == '__main__':
    run_test_6()
