"""
Test 6: Gap-Size Bin Win-Rate Analysis
Manuscript Reference: Table 8, Figure 3, Section 4.4
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from src.data_loader import load_trades_clean

def format_stars(p_val):
    if p_val < 0.01: return "***"
    elif p_val < 0.05: return "**"
    elif p_val < 0.10: return "*"
    else: return ""

def run_test_6():
    print("Running Test 6: Gap-Size Bin Win-Rate Analysis (Table 8, Figure 3)...")
    trades = load_trades_clean(resolved_only=True)
    
    # 10 fixed bins
    bins = [0.0, 0.25, 0.50, 0.75, 1.00, 1.25, 1.50, 2.00, 2.50, 3.00, np.inf]
    labels = ['0.00–0.25', '0.25–0.50', '0.50–0.75', '0.75–1.00', '1.00–1.25',
              '1.25–1.50', '1.50–2.00', '2.00–2.50', '2.50–3.00', '3.00+']

    trades['bin'] = pd.cut(trades['gap_size_pct'], bins=bins, labels=labels, right=False)

    stable = trades[trades['regime'] == 'stable']
    post = trades[trades['regime'] == 'post_shock']

    records = []
    plot_data = []

    for b in labels:
        s_sub = stable[stable['bin'] == b]
        p_sub = post[post['bin'] == b]
        
        n_s = len(s_sub)
        n_p = len(p_sub)
        w_s = s_sub['is_win'].sum()
        w_p = p_sub['is_win'].sum()
        
        wr_s = (w_s / n_s) if n_s > 0 else np.nan
        wr_p = (w_p / n_p) if n_p > 0 else np.nan
        diff = (wr_s - wr_p) if (not np.isnan(wr_s) and not np.isnan(wr_p)) else np.nan
        
        # Pooled two-sample z-test for difference in proportions
        p_pool = (w_s + w_p) / (n_s + n_p)
        se_pool = np.sqrt(p_pool * (1.0 - p_pool) * (1.0 / n_s + 1.0 / n_p))
        z_stat = (wr_s - wr_p) / se_pool
        p_val = 2.0 * (1.0 - stats.norm.cdf(abs(z_stat)))
        stars = format_stars(p_val)
        
        records.append({
            'Gap Size Bin (%)': b,
            'Stable Trades (N_s)': n_s,
            'Stable Win Rate (%)': f"{wr_s * 100:.2f}%",
            'Post-Shock Trades (N_p)': n_p,
            'Post-Shock Win Rate (%)': f"{wr_p * 100:.2f}%",
            'Difference (pp)': f"{diff * 100:.2f}%",
            'z-Statistic': f"{z_stat:.2f}{stars}",
            'p-value': f"{p_val:.4f}" if p_val >= 0.0001 else "< 0.0001"
        })
        
        plot_data.append({
            'bin': b,
            'wr_s': wr_s * 100,
            'wr_p': wr_p * 100
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
        "Win rates by 10 fixed gap-size bins comparing Stable (2022-03-01 to 2026-02-28) and Post-Shock (≥ 2026-03-01) regimes. "
        "Two-sample pooled z-test evaluates the null hypothesis of equal win-rate proportions between regimes. "
        "Significance: * p < 0.10, ** p < 0.05, *** p < 0.01.",
        "",
        "| Gap Size Bin (%) | Stable Trades (N_s) | Stable Win Rate (%) | Post-Shock Trades (N_p) | Post-Shock Win Rate (%) | Difference (pp) | z-Statistic | p-value |",
        "|:---|---:|---:|---:|---:|---:|---:|:---:|"
    ]
    for _, r in df_table8.iterrows():
        md_lines.append(
            f"| {r['Gap Size Bin (%)']} | {r['Stable Trades (N_s)']:,} | {r['Stable Win Rate (%)']} | "
            f"{r['Post-Shock Trades (N_p)']:,} | {r['Post-Shock Win Rate (%)']} | {r['Difference (pp)']} | "
            f"{r['z-Statistic']} | {r['p-value']} |"
        )
    md_lines.append("")
    
    with open(md_path, 'w') as f:
        f.write('\n'.join(md_lines))
    print(f"Table 8 saved to {csv_path} and {md_path}")

    # --- Plot Figure 3: Side-by-Side Bar Chart ---
    df_plot = pd.DataFrame(plot_data)
    fig_path = os.path.join(BASE_DIR, 'output', 'figures', 'figure_03_gap_size_bins.png')
    
    plt.figure(figsize=(11, 5.5), dpi=300)
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    x = np.arange(len(df_plot))
    width = 0.38
    
    plt.bar(x - width/2, df_plot['wr_s'], width, label='Stable Regime (2022–2026)', color='#1f77b4', alpha=0.9, edgecolor='none')
    plt.bar(x + width/2, df_plot['wr_p'], width, label='Post-Shock Regime (2026)', color='#d62728', alpha=0.9, edgecolor='none')
    
    # 50% breakeven reference line
    plt.axhline(y=50.0, color='#555555', linestyle='--', linewidth=1.2, alpha=0.7, label='Breakeven Win Rate (50%)')
    
    plt.title('Figure 3: Resolved Trade Win Rate by Gap-Size Bin Across Regimes', fontsize=13, fontweight='bold', pad=12)
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

