"""
Test 7: Event Study — Cumulative Abnormal Win Rate (CAWR)
Manuscript Reference: Table 9, Figure 4, Section 4.5
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
from src.data_loader import load_daily_clean

def format_stars(p_val):
    if p_val < 0.01: return "***"
    elif p_val < 0.05: return "**"
    elif p_val < 0.10: return "*"
    else: return ""

def run_test_7():
    print("Running Test 7: Event Study — CAWR (Table 9, Figure 4)...")
    daily = load_daily_clean()
    daily['date_dt'] = pd.to_datetime(daily['date'])
    
    # 1. Estimation window: 2022-03-15 to 2025-07-31
    est_win = daily[(daily['date_dt'] >= '2022-03-15') & (daily['date_dt'] <= '2025-07-31')]
    mu = est_win['resolved_wr'].mean()
    sigma = est_win['resolved_wr'].std()
    
    # 2. Event date: 2026-03-04
    event_date = '2026-03-04'
    event_matches = daily[daily['date'] == event_date]
    assert len(event_matches) == 1, f"Event date {event_date} not found uniquely in daily data."
    event_idx = event_matches.index[0]
    
    daily['event_rel_day'] = daily.index - event_idx
    daily['AWR'] = daily['resolved_wr'] - mu
    
    # Windows to evaluate
    windows = [
        ('Pre-event Placebo', -10, -1),
        ('Short post-shock', 1, 5),
        ('Medium post-shock', 1, 10),
        ('Long post-shock', 1, 20),
        ('Extended post-shock', 1, 40)
    ]
    
    records = []
    for label, a, b in windows:
        sub = daily[(daily['event_rel_day'] >= a) & (daily['event_rel_day'] <= b)]
        L = b - a + 1
        cawr = sub['AWR'].sum()
        cawr_pp = cawr * 100.0
        se = sigma * np.sqrt(L)
        se_pp = se * 100.0
        t_stat = cawr / se
        p_val = 2.0 * (1.0 - stats.norm.cdf(abs(t_stat)))
        stars = format_stars(p_val)
        
        records.append({
            'Window Label': label,
            'Event-Relative Days': f"[{a:+d}, {b:+d}]",
            'Window Length (L)': L,
            'CAWR (pp)': f"{cawr_pp:+.2f}{stars}",
            'Standard Error (pp)': f"{se_pp:.2f}",
            't-Statistic': f"{t_stat:.2f}",
            'p-value': f"{p_val:.4f}" if p_val >= 0.0001 else "< 0.0001"
        })
        
    df_table9 = pd.DataFrame(records)
    
    # Save CSV
    os.makedirs(os.path.join(BASE_DIR, 'output', 'tables'), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, 'output', 'figures'), exist_ok=True)
    
    csv_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_09_event_study_cawr.csv')
    df_table9.to_csv(csv_path, index=False)
    
    # Generate Markdown Table
    md_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_09_event_study_cawr.md')
    md_lines = [
        "# Table 9: Event Study — Cumulative Abnormal Win Rate (CAWR)",
        "",
        "Cumulative Abnormal Win Rate (CAWR) around the March 4, 2026 structural break event date. "
        f"Benchmark parameters estimated on 2022-03-15 to 2025-07-31 (N = {len(est_win)} days): "
        f"benchmark mean μ = {mu * 100:.2f}%, daily volatility σ = {sigma * 100:.2f}%. "
        "Standard errors are computed as SE(CAWR) = σ × √L. Significance: * p < 0.10, ** p < 0.05, *** p < 0.01.",
        "",
        "| Window Label | Event-Relative Days | Window Length (L) | CAWR (pp) | Standard Error (pp) | t-Statistic | p-value |",
        "|:---|:---:|---:|---:|---:|---:|:---:|"
    ]
    for _, r in df_table9.iterrows():
        md_lines.append(
            f"| {r['Window Label']} | {r['Event-Relative Days']} | {r['Window Length (L)']} | "
            f"{r['CAWR (pp)']} | {r['Standard Error (pp)']} | {r['t-Statistic']} | {r['p-value']} |"
        )
    md_lines.append("")
    
    with open(md_path, 'w') as f:
        f.write('\n'.join(md_lines))
    print(f"Table 9 saved to {csv_path} and {md_path}")
    
    # --- 3. Plot Figure 4: CAWR Trajectory with 95% Confidence Bands ---
    window_df = daily[(daily['event_rel_day'] >= -10) & (daily['event_rel_day'] <= 40)].sort_values('event_rel_day').copy()
    
    cawr_path = []
    cum_days_list = []
    for d in window_df['event_rel_day']:
        if d < 0:
            # Pre-event cumulation backward from Day 0 over [d, -1]
            cawr = daily[(daily['event_rel_day'] >= d) & (daily['event_rel_day'] <= -1)]['AWR'].sum() * 100.0
            k = abs(d)
        elif d == 0:
            # Day 0 reference origin
            cawr = 0.0
            k = 0
        else:
            # Post-event cumulation forward from Day 0 over [1, d]
            cawr = daily[(daily['event_rel_day'] >= 1) & (daily['event_rel_day'] <= d)]['AWR'].sum() * 100.0
            k = d
        cawr_path.append(cawr)
        cum_days_list.append(k)
        
    window_df['CAWR_path'] = cawr_path
    window_df['cum_days'] = cum_days_list
    window_df['ci_upper'] = 1.96 * (sigma * 100.0) * np.sqrt(window_df['cum_days'])
    window_df['ci_lower'] = -1.96 * (sigma * 100.0) * np.sqrt(window_df['cum_days'])
    
    fig_path = os.path.join(BASE_DIR, 'output', 'figures', 'figure_04_cawr_trajectory.png')
    
    plt.figure(figsize=(11, 5.5), dpi=300)
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    days_x = window_df['event_rel_day'].values
    cawr_y = window_df['CAWR_path'].values
    ci_up = window_df['ci_upper'].values
    ci_lo = window_df['ci_lower'].values
    
    plt.plot(days_x, cawr_y, color='#d62728', linewidth=2.2, label='CAWR (Day 0 origin: cumulated over [d, -1] and [1, d])')
    plt.plot(days_x, ci_up, color='#7f7f7f', linestyle='--', linewidth=1.2, label='95% Confidence Band (±1.96 × σ × √|k|)')
    plt.plot(days_x, ci_lo, color='#7f7f7f', linestyle='--', linewidth=1.2)
    plt.fill_between(days_x, ci_lo, ci_up, color='#7f7f7f', alpha=0.15)
    
    plt.axvline(x=0, color='#1f77b4', linestyle='-', linewidth=1.8, label='Event Date (Day 0: 2026-03-04)')
    plt.axhline(y=0, color='#333333', linestyle=':', linewidth=1.0)
    
    plt.title('Figure 4: Cumulative Abnormal Win Rate (CAWR) Trajectory [-10, +40 Days]', fontsize=13, fontweight='bold', pad=12)
    plt.xlabel('Event-Relative Trading Days (Day 0 = 2026-03-04)', fontsize=11, labelpad=8)
    plt.ylabel('CAWR (Percentage Points)', fontsize=11, labelpad=8)
    plt.xticks(np.arange(-10, 45, 5), fontsize=10)
    plt.legend(frameon=True, loc='lower left', fontsize=9.5)
    plt.tight_layout()
    plt.savefig(fig_path, dpi=300)
    plt.close()
    
    print(f"Figure 4 saved to {fig_path}")
    return df_table9

if __name__ == '__main__':
    run_test_7()

