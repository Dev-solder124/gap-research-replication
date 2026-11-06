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
        
        # Day-clustered SE for Stable Resolved WR
        b_res_s = b_res[b_res['regime'] == 'stable']
        if len(b_res_s) > 0:
            m_s_res = sm.OLS(b_res_s['win_resolved'], np.ones(len(b_res_s))).fit(cov_type='cluster', cov_kwds={'groups': b_res_s['date']})
            se_res_s = m_s_res.bse.iloc[0]
        else:
            se_res_s = 0.0

        # Day-clustered SE for Post-Shock Resolved WR
        b_res_p = b_res[b_res['regime'] == 'post_shock']
        if len(b_res_p) > 0:
            m_p_res = sm.OLS(b_res_p['win_resolved'], np.ones(len(b_res_p))).fit(cov_type='cluster', cov_kwds={'groups': b_res_p['date']})
            se_res_p = m_p_res.bse.iloc[0]
        else:
            se_res_p = 0.0

        # Day-clustered SE for Stable Nominal WR
        b_all_s = b_all[b_all['regime'] == 'stable']
        if len(b_all_s) > 0:
            m_s_nom = sm.OLS(b_all_s['win_nominal'], np.ones(len(b_all_s))).fit(cov_type='cluster', cov_kwds={'groups': b_all_s['date']})
            se_nom_s = m_s_nom.bse.iloc[0]
        else:
            se_nom_s = 0.0

        # Day-clustered SE for Post-Shock Nominal WR
        b_all_p = b_all[b_all['regime'] == 'post_shock']
        if len(b_all_p) > 0:
            m_p_nom = sm.OLS(b_all_p['win_nominal'], np.ones(len(b_all_p))).fit(cov_type='cluster', cov_kwds={'groups': b_all_p['date']})
            se_nom_p = m_p_nom.bse.iloc[0]
        else:
            se_nom_p = 0.0

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
            'res_s_se': se_res_s * 100.0,
            'res_p': res_wr_post * 100.0,
            'res_p_se': se_res_p * 100.0,
            'nom_s': nom_wr_stable * 100.0,
            'nom_s_se': se_nom_s * 100.0,
            'nom_p': nom_wr_post * 100.0,
            'nom_p_se': se_nom_p * 100.0
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

    # Plot Figure 3: 2-Panel Stacked Bar Chart (Panel A: Resolved WR, Panel B: Nominal WR)
    df_plot = pd.DataFrame(plot_data)
    fig_path = os.path.join(BASE_DIR, 'output', 'figures', 'figure_03_gap_size_bins.png')
    
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8.5), sharex=True, dpi=300)
    
    x = np.arange(len(df_plot))
    width = 0.38
    
    # --- Panel A: Resolved Win Rates with Day-Clustered 95% CI ---
    ax1.bar(
        x - width/2, df_plot['res_s'], width, 
        yerr=1.96 * df_plot['res_s_se'], capsize=3, 
        label='Stable Regime: Resolved WR', color='#1f77b4', alpha=0.9
    )
    ax1.bar(
        x + width/2, df_plot['res_p'], width, 
        yerr=1.96 * df_plot['res_p_se'], capsize=3, 
        label='Post-Shock Regime: Resolved WR', color='#d62728', alpha=0.9
    )
    ax1.axhline(y=50.0, color='#555555', linestyle='--', linewidth=1.2, alpha=0.7, label='50.0% Breakeven Barrier')
    ax1.set_ylabel('Resolved Win Rate (%)', fontsize=11, labelpad=8)
    ax1.set_title('Panel A: Resolved Win Rate by Gap-Size Bin (Day-Clustered 95% CI)', fontsize=12, fontweight='bold', pad=8)
    ax1.legend(frameon=True, loc='upper left', fontsize=9.5)
    ax1.set_ylim(15, 80)
    
    # --- Panel B: Nominal Win Rates with Day-Clustered 95% CI ---
    ax2.bar(
        x - width/2, df_plot['nom_s'], width, 
        yerr=1.96 * df_plot['nom_s_se'], capsize=3, 
        label='Stable Regime: Nominal WR', color='#1f77b4', alpha=0.9
    )
    ax2.bar(
        x + width/2, df_plot['nom_p'], width, 
        yerr=1.96 * df_plot['nom_p_se'], capsize=3, 
        label='Post-Shock Regime: Nominal WR', color='#d62728', alpha=0.9
    )
    ax2.axhline(y=50.0, color='#555555', linestyle='--', linewidth=1.2, alpha=0.7, label='50.0% Breakeven Barrier')
    ax2.set_ylabel('Nominal Win Rate (%)', fontsize=11, labelpad=8)
    ax2.set_xlabel('Overnight Gap Size Range (% of Entry Price)', fontsize=11, labelpad=8)
    ax2.set_title('Panel B: Nominal Win Rate by Gap-Size Bin (Day-Clustered 95% CI)', fontsize=12, fontweight='bold', pad=8)
    ax2.set_xticks(x)
    ax2.set_xticklabels(df_plot['bin'], rotation=30, ha='right', fontsize=9.5)
    ax2.legend(frameon=True, loc='upper right', fontsize=9.5)
    ax2.set_ylim(10, 70)
    
    plt.tight_layout()
    plt.savefig(fig_path, dpi=300)
    plt.close()
    
    print(f"Figure 3 saved to {fig_path}")
    return df_table8

if __name__ == '__main__':
    run_test_6()
