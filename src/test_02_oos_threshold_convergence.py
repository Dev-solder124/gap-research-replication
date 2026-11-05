"""
Test 2: 15-Quarter Walk-Forward OOS Threshold Convergence
First-Crossing Breakeven Estimator
Manuscript Reference: Table 4, Figure 2, Section 3.5
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.data_loader import load_trades_clean

def estimate_first_crossing_threshold(train_df, bin_edges, bin_midpoints, min_trades=30):
    """
    Non-parametric first-crossing cutoff of the 50.0% directional breakeven barrier.
    Partitions trades with gap_size_pct in [0.0, 5.0] into 20 equal-width bins (width=0.25%).
    Computes resolved win rate (TARGET / (TARGET + STOP_LOSS)) in each bin with n_j >= min_trades.
    Finds first adjacent pair of bins (j, j+1) where wr_j < 0.50 and wr_{j+1} >= 0.50,
    and linearly interpolates at wr = 0.50.
    """
    t = train_df[(train_df['gap_size_pct'] >= 0.0) & (train_df['gap_size_pct'] <= 5.0)].copy()
    t_res = t[t['status'].isin(['TARGET', 'STOP_LOSS'])].copy()
    
    t_res['bin_idx'] = np.digitize(t_res['gap_size_pct'], bin_edges) - 1
    t_res['bin_idx'] = np.clip(t_res['bin_idx'], 0, 19)
    
    valid_bins = []
    for j in range(20):
        sub = t_res[t_res['bin_idx'] == j]
        n_j = len(sub)
        if n_j >= min_trades:
            wr_j = (sub['status'] == 'TARGET').mean()
            valid_bins.append((j, bin_midpoints[j], wr_j, n_j))
            
    if not valid_bins:
        return np.nan
        
    if valid_bins[0][2] >= 0.50:
        return valid_bins[0][1]
        
    for idx in range(len(valid_bins) - 1):
        j1, m1, wr1, n1 = valid_bins[idx]
        j2, m2, wr2, n2 = valid_bins[idx + 1]
        if j2 == j1 + 1 and wr1 < 0.50 and wr2 >= 0.50:
            c_star = m1 + (0.50 - wr1) / (wr2 - wr1) * (m2 - m1)
            return c_star
            
    return np.nan

def run_test_2():
    print("Running Test 2: 15-Quarter Walk-Forward OOS Threshold Convergence (Table 4, Figure 2)...")
    trades = load_trades_clean(resolved_only=False)
    trades['date'] = pd.to_datetime(trades['date'])

    quarters = [
        '2022Q3', '2022Q4',
        '2023Q1', '2023Q2', '2023Q3', '2023Q4',
        '2024Q1', '2024Q2', '2024Q3', '2024Q4',
        '2025Q1', '2025Q2', '2025Q3', '2025Q4',
        '2026Q1'
    ]

    bin_edges = np.linspace(0.0, 5.0, 21)
    bin_midpoints = 0.5 * (bin_edges[:-1] + bin_edges[1:])

    records = []

    for q_label in quarters:
        qp = pd.Period(q_label, freq='Q')
        train_trades = trades[trades['date'] < qp.start_time]
        oos_trades = trades[(trades['date'] >= qp.start_time) & (trades['date'] <= qp.end_time)]
        
        c_star = estimate_first_crossing_threshold(train_trades, bin_edges, bin_midpoints, min_trades=30)
        
        # In-sample summary
        train_res = train_trades[train_trades['status'].isin(['TARGET', 'STOP_LOSS'])]
        train_res_wr = (train_res['status'] == 'TARGET').mean() if len(train_res) > 0 else np.nan
        train_nom_wr = (train_trades['status'] == 'TARGET').mean() if len(train_trades) > 0 else np.nan
        
        # Out-of-sample unfiltered
        oos_res = oos_trades[oos_trades['status'].isin(['TARGET', 'STOP_LOSS'])]
        unf_res_wr = (oos_res['status'] == 'TARGET').mean() if len(oos_res) > 0 else np.nan
        unf_nom_wr = (oos_trades['status'] == 'TARGET').mean() if len(oos_trades) > 0 else np.nan
        
        # Out-of-sample filtered: gap_size_pct >= c_star
        if not np.isnan(c_star):
            fil_oos = oos_trades[oos_trades['gap_size_pct'] >= c_star]
            fil_tot = len(fil_oos)
            fil_res = fil_oos[fil_oos['status'].isin(['TARGET', 'STOP_LOSS'])]
            fil_res_n = len(fil_res)
            fil_res_wr = (fil_res['status'] == 'TARGET').mean() if fil_res_n > 0 else np.nan
            fil_nom_wr = (fil_oos['status'] == 'TARGET').mean() if fil_tot > 0 else np.nan
            fade_dominant = "Yes" if (not np.isnan(fil_res_wr) and fil_res_wr > 0.50) else "No"
        else:
            fil_tot = 0
            fil_res_n = 0
            fil_res_wr = np.nan
            fil_nom_wr = np.nan
            fade_dominant = "No"

        q_name = f"{q_label[4:]} {q_label[:4]}"
        
        records.append({
            'Quarter': q_name,
            'In-Sample Total Trades': len(train_trades),
            'In-Sample Resolved Trades': len(train_res),
            'First-Crossing Cutoff c*(k) (%)': c_star,
            'OOS Unfiltered Trades': len(oos_trades),
            'OOS Unfiltered Resolved WR (%)': round(unf_res_wr * 100.0, 2) if not np.isnan(unf_res_wr) else np.nan,
            'OOS Unfiltered Nominal WR (%)': round(unf_nom_wr * 100.0, 2) if not np.isnan(unf_nom_wr) else np.nan,
            'OOS Filtered Total Trades': fil_tot,
            'OOS Filtered Resolved Trades': fil_res_n,
            'OOS Filtered Resolved WR (%)': round(fil_res_wr * 100.0, 2) if not np.isnan(fil_res_wr) else np.nan,
            'OOS Filtered Nominal WR (%)': round(fil_nom_wr * 100.0, 2) if not np.isnan(fil_nom_wr) else np.nan,
            'Fade-Dominant (>50% WR)': fade_dominant
        })

    df_table4 = pd.DataFrame(records)

    # Save CSV
    os.makedirs(os.path.join(BASE_DIR, 'output', 'tables'), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, 'output', 'figures'), exist_ok=True)
    
    csv_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_04_oos_threshold_convergence.csv')
    df_table4.to_csv(csv_path, index=False)

    # Generate Markdown Table
    md_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_04_oos_threshold_convergence.md')
    md_content = [
        "# Table 4: 15-Quarter Walk-Forward OOS Threshold Convergence",
        "",
        "First-crossing breakeven threshold estimator c*(k) across 15 out-of-sample quarters (Q3 2022 to Q1 2026). "
        "Estimated via linear interpolation between adjacent 0.25% bins at the 50.0% resolved win-rate barrier on the expanding training window. "
        "Both Resolved Win Rate (TARGET / (TARGET + STOP_LOSS)) and Nominal Win Rate (TARGET / ALL) are reported.",
        "",
        "| Quarter | In-Sample Resolved | Cutoff c*(k) (%) | OOS Filtered Resolved | OOS Filtered Resolved WR (%) | OOS Filtered Nominal WR (%) | Fade-Dominant (>50%) |",
        "|:---|---:|---:|---:|---:|---:|:---:|"
    ]
    for _, r in df_table4.iterrows():
        md_content.append(
            f"| {r['Quarter']} | {r['In-Sample Resolved Trades']:,} | {r['First-Crossing Cutoff c*(k) (%)']:.3f}% | "
            f"{r['OOS Filtered Resolved Trades']:,} | {r['OOS Filtered Resolved WR (%)']:.2f}% | "
            f"{r['OOS Filtered Nominal WR (%)']:.2f}% | {r['Fade-Dominant (>50% WR)']} |"
        )
    md_content.append("")
    
    with open(md_path, 'w') as f:
        f.write('\n'.join(md_content))
    print(f"Table 4 saved to {csv_path} and {md_path}")

    # Plot Figure 2: Time-series line chart of c*(k)
    fig_path = os.path.join(BASE_DIR, 'output', 'figures', 'figure_02_oos_threshold_convergence.png')
    
    plt.figure(figsize=(10, 5), dpi=300)
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    x_indices = list(range(len(df_table4)))
    c_vals = df_table4['First-Crossing Cutoff c*(k) (%)'].values
    quarter_labels = df_table4['Quarter'].values
    
    plt.plot(x_indices, c_vals, marker='o', color='#1f77b4', linewidth=2.2, markersize=7, label='First-Crossing Breakeven Threshold c*(k)')
    
    # Convergence reference line around ~0.37%
    mean_stable_c = np.mean(c_vals[4:]) # from 2023Q3 onward
    plt.axhline(y=mean_stable_c, color='#d62728', linestyle='--', alpha=0.7, label=f'Convergence Level (~{mean_stable_c:.2f}%)')
    
    plt.title('Figure 2: Walk-Forward OOS First-Crossing Breakeven Threshold Convergence', fontsize=13, fontweight='bold', pad=12)
    plt.xlabel('Out-of-Sample Quarter', fontsize=11, labelpad=8)
    plt.ylabel('Breakeven Cutoff c* (%)', fontsize=11, labelpad=8)
    plt.xticks(x_indices, quarter_labels, rotation=45, ha='right', fontsize=9)
    plt.yticks(np.arange(0.2, 0.8, 0.1), fontsize=10)
    plt.ylim(0.25, 0.75)
    
    for i, txt in enumerate(c_vals):
        plt.annotate(f"{txt:.2f}%", (x_indices[i], c_vals[i] + 0.025), fontsize=8, ha='center', color='#333333')
        
    plt.legend(frameon=True, loc='upper right', fontsize=10)
    plt.tight_layout()
    plt.savefig(fig_path, dpi=300)
    plt.close()
    
    print(f"Figure 2 saved to {fig_path}")
    return df_table4

if __name__ == '__main__':
    run_test_2()
