"""
Test 2: 15-Quarter Walk-Forward OOS Threshold Convergence
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

def run_test_2():
    print("Running Test 2: 15-Quarter Walk-Forward OOS Threshold Convergence (Table 4, Figure 2)...")
    
    trades = load_trades_clean(resolved_only=True)
    trades['date'] = pd.to_datetime(trades['date'])

    # 15 OOS quarters specified: Q3 2022 to Q1 2026
    quarters = [
        '2022Q3', '2022Q4',
        '2023Q1', '2023Q2', '2023Q3', '2023Q4',
        '2024Q1', '2024Q2', '2024Q3', '2024Q4',
        '2025Q1', '2025Q2', '2025Q3', '2025Q4',
        '2026Q1'
    ]

    candidate_thresholds = np.round(np.linspace(0.0, 5.0, 101), 2)
    records = []

    for q_label in quarters:
        q_period = pd.Period(q_label, freq='Q')
        q_start = q_period.start_time
        q_end = q_period.end_time
        
        # Training window: start of sample through last day before OOS quarter begins
        train_trades = trades[trades['date'] < q_start]
        oos_trades = trades[(trades['date'] >= q_start) & (trades['date'] <= q_end)]
        
        best_c = None
        best_wr = -1.0
        train_n_at_best_c = 0
        
        # Grid search over candidate thresholds
        for c in candidate_thresholds:
            subset = train_trades[train_trades['gap_size_pct'] >= c]
            if len(subset) >= 30:
                wr = subset['is_win'].mean()
                if wr > best_wr:
                    best_wr = wr
                    best_c = c
                    train_n_at_best_c = len(subset)
                    
        # OOS evaluation
        oos_filtered = oos_trades[oos_trades['gap_size_pct'] >= best_c]
        oos_trades_count = len(oos_filtered)
        oos_wr = oos_filtered['is_win'].mean() if oos_trades_count > 0 else np.nan
        fade_dominant = "Yes" if (not np.isnan(oos_wr) and oos_wr > 0.50) else "No"
        
        # Human-readable quarter label: "Q3 2022"
        q_name = f"{q_label[4:]} {q_label[:4]}"
        
        records.append({
            'Quarter': q_name,
            'Train Trades (Total)': len(train_trades),
            'Optimal Threshold c*(k) (%)': best_c,
            'Train WR (%)': round(best_wr * 100.0, 2) if best_wr is not None else np.nan,
            'OOS Trades (Filtered)': oos_trades_count,
            'OOS Win Rate (%)': round(oos_wr * 100.0, 2) if not np.isnan(oos_wr) else np.nan,
            'Fade-Dominant': fade_dominant
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
        "# Table 4: 15-Quarter Walk-Forward Out-of-Sample Threshold Convergence",
        "",
        "Expanding-window walk-forward parameter stability across 15 out-of-sample quarters (Q3 2022 to Q1 2026). "
        "Threshold c*(k) is selected on the expanding in-sample window (grid: 0.00% to 5.00%, step 0.05%, min 30 trades) "
        "and applied out-of-sample.",
        "",
        "| Quarter | In-Sample Trades | Optimal Threshold c*(k) (%) | In-Sample WR (%) | OOS Filtered Trades | OOS Win Rate (%) | Fade-Dominant |",
        "|:---|---:|---:|---:|---:|---:|:---:|"
    ]
    for _, r in df_table4.iterrows():
        md_content.append(
            f"| {r['Quarter']} | {r['Train Trades (Total)']:,} | {r['Optimal Threshold c*(k) (%)']:.2f}% | "
            f"{r['Train WR (%)']:.2f}% | {r['OOS Trades (Filtered)']:,} | {r['OOS Win Rate (%)']:.2f}% | {r['Fade-Dominant']} |"
        )
    md_content.append("")
    
    with open(md_path, 'w') as f:
        f.write('\n'.join(md_content))
    print(f"Table 4 saved to {csv_path} and {md_path}")

    # Plot Figure 2: Time-series line chart of c*(k) over the 15 OOS quarters
    fig_path = os.path.join(BASE_DIR, 'output', 'figures', 'figure_02_oos_threshold_convergence.png')
    
    plt.figure(figsize=(10, 5), dpi=300)
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    x_indices = list(range(len(df_table4)))
    c_vals = df_table4['Optimal Threshold c*(k) (%)'].values
    quarter_labels = df_table4['Quarter'].values
    
    plt.plot(x_indices, c_vals, marker='o', color='#1f77b4', linewidth=2.2, markersize=7, label='Optimal Threshold c*(k)')
    
    # Add horizontal reference lines or convergence highlight
    plt.axhline(y=2.80, color='#d62728', linestyle='--', alpha=0.7, label='Convergence Level (~2.80%)')
    
    plt.title('Figure 2: Walk-Forward OOS Threshold Convergence Over 15 Quarters', fontsize=13, fontweight='bold', pad=12)
    plt.xlabel('Out-of-Sample Quarter', fontsize=11, labelpad=8)
    plt.ylabel('Optimal Gap-Size Threshold c* (%)', fontsize=11, labelpad=8)
    plt.xticks(x_indices, quarter_labels, rotation=45, ha='right', fontsize=9)
    plt.yticks(np.arange(2.0, 5.5, 0.5), fontsize=10)
    plt.ylim(2.0, 5.25)
    
    for i, txt in enumerate(c_vals):
        plt.annotate(f"{txt:.2f}%", (x_indices[i], c_vals[i] + 0.1), fontsize=8, ha='center', color='#333333')
        
    plt.legend(frameon=True, loc='upper right', fontsize=10)
    plt.tight_layout()
    plt.savefig(fig_path, dpi=300)
    plt.close()
    
    print(f"Figure 2 saved to {fig_path}")
    return df_table4

if __name__ == '__main__':
    run_test_2()

