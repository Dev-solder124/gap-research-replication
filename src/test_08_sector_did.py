"""
Test 8: Sector Difference-in-Differences — Energy Transmission Specifications
Manuscript Reference: Table 10, Figure 5, Section 4.6
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
from src.data_loader import load_trades_clean, load_sector_map

def format_stars(p_val):
    if p_val < 0.01: return "***"
    elif p_val < 0.05: return "**"
    elif p_val < 0.10: return "*"
    else: return ""

def run_test_8():
    print("Running Test 8: Sector Difference-in-Differences (Table 10, Figure 5)...")
    trades = load_trades_clean(resolved_only=True)
    sector_map = load_sector_map()
    trades['sector'] = trades['symbol_root'].map(sector_map)
    
    # 1. Three distinct mutually exclusive industry groups from SECTOR_MAP.py:
    downstream_target = {'Auto', 'Automobile', 'Cement', 'Cement & Cement Products', 'Chemicals', 'Power', 'Fertilisers', 'Fertilisers & Pesticides'}
    upstream_target = {'Oil & Gas', 'Metals'}
    defensive_target = {'FMCG', 'Consumer Goods', 'Healthcare', 'Healthcare Services', 'Pharma', 'IT'}

    trades['is_downstream'] = trades['sector'].isin(downstream_target)
    trades['is_upstream'] = trades['sector'].isin(upstream_target)
    trades['is_defensive'] = trades['sector'].isin(defensive_target)
    
    # Load Brent crude futures data
    brent_path = os.path.join(BASE_DIR, 'data', 'macro', 'XBR_USD Historical Data.csv')
    brent = pd.read_csv(brent_path, encoding='utf-8-sig')
    brent['date'] = pd.to_datetime(brent['Date']).dt.strftime('%Y-%m-%d')
    brent = brent.sort_values('date').reset_index(drop=True)
    brent['R_brent'] = np.log(brent['Price'] / brent['Price'].shift(1))
    brent['sigma_brent_20d'] = brent['R_brent'].rolling(20).std()

    table10_rows = []

    # --- Spec 1A: Downstream Consumers vs. Clean Defensives (Acute March 2026 vs. Stable Baseline) ---
    sub_1a = trades[trades['is_downstream'] | trades['is_defensive']].copy()
    pre_1a = sub_1a[sub_1a['regime'] == 'stable'].copy()
    post_1a = sub_1a[sub_1a['date'].str.startswith('2026-03')].copy()
    df_1a = pd.concat([pre_1a, post_1a]).reset_index(drop=True)
    df_1a['post'] = (df_1a['date'].str.startswith('2026-03')).astype(float)
    df_1a['treat'] = df_1a['is_downstream'].astype(float)
    df_1a['post_x_treat'] = df_1a['post'] * df_1a['treat']

    X_1a = sm.add_constant(df_1a[['post', 'treat', 'post_x_treat']])
    m_1a = sm.OLS(df_1a['is_win'], X_1a).fit(cov_type='cluster', cov_kwds={'groups': df_1a['date']})
    b3_1a, se_1a, t_1a, p_1a = m_1a.params['post_x_treat'], m_1a.bse['post_x_treat'], m_1a.tvalues['post_x_treat'], m_1a.pvalues['post_x_treat']
    
    table10_rows.append({
        'Specification': 'Spec 1A: Downstream Consumers vs. Defensives (Acute Mar 2026)',
        'DiD Parameter': 'β₃ (PostShock × Downstream)',
        'DiD Coefficient': f"{b3_1a * 100:.2f}%{format_stars(p_1a)}",
        'Day-Clustered SE': f"{se_1a * 100:.2f}%",
        't-Statistic': f"{t_1a:.2f}",
        'p-value': f"{p_1a:.4f}",
        'Resolved Trades (N)': len(df_1a),
        'Trading Days': df_1a['date'].nunique()
    })

    # --- Spec 1B: Downstream Consumers vs. Clean Defensives (Full Post-Shock Mar–Jul 2026 vs. Stable Baseline) ---
    post_1b = sub_1a[sub_1a['regime'] == 'post_shock'].copy()
    df_1b = pd.concat([pre_1a, post_1b]).reset_index(drop=True)
    df_1b['post'] = (df_1b['regime'] == 'post_shock').astype(float)
    df_1b['treat'] = df_1b['is_downstream'].astype(float)
    df_1b['post_x_treat'] = df_1b['post'] * df_1b['treat']

    X_1b = sm.add_constant(df_1b[['post', 'treat', 'post_x_treat']])
    m_1b = sm.OLS(df_1b['is_win'], X_1b).fit(cov_type='cluster', cov_kwds={'groups': df_1b['date']})
    b3_1b, se_1b, t_1b, p_1b = m_1b.params['post_x_treat'], m_1b.bse['post_x_treat'], m_1b.tvalues['post_x_treat'], m_1b.pvalues['post_x_treat']

    table10_rows.append({
        'Specification': 'Spec 1B: Downstream Consumers vs. Defensives (Extended Mar–Jul 2026)',
        'DiD Parameter': 'β₃ (PostShock × Downstream)',
        'DiD Coefficient': f"{b3_1b * 100:.2f}%{format_stars(p_1b)}",
        'Day-Clustered SE': f"{se_1b * 100:.2f}%",
        't-Statistic': f"{t_1b:.2f}",
        'p-value': f"{p_1b:.4f}",
        'Resolved Trades (N)': len(df_1b),
        'Trading Days': df_1b['date'].nunique()
    })

    # --- Spec 1C: Upstream Producers vs. Clean Defensives (Acute March 2026 vs. Stable Baseline) ---
    sub_1c = trades[trades['is_upstream'] | trades['is_defensive']].copy()
    pre_1c = sub_1c[sub_1c['regime'] == 'stable'].copy()
    post_1c = sub_1c[sub_1c['date'].str.startswith('2026-03')].copy()
    df_1c = pd.concat([pre_1c, post_1c]).reset_index(drop=True)
    df_1c['post'] = (df_1c['date'].str.startswith('2026-03')).astype(float)
    df_1c['treat'] = df_1c['is_upstream'].astype(float)
    df_1c['post_x_treat'] = df_1c['post'] * df_1c['treat']

    X_1c = sm.add_constant(df_1c[['post', 'treat', 'post_x_treat']])
    m_1c = sm.OLS(df_1c['is_win'], X_1c).fit(cov_type='cluster', cov_kwds={'groups': df_1c['date']})
    b3_1c, se_1c, t_1c, p_1c = m_1c.params['post_x_treat'], m_1c.bse['post_x_treat'], m_1c.tvalues['post_x_treat'], m_1c.pvalues['post_x_treat']

    table10_rows.append({
        'Specification': 'Spec 1C: Upstream Producers vs. Defensives (Acute Mar 2026)',
        'DiD Parameter': 'β₃ (PostShock × Upstream)',
        'DiD Coefficient': f"{b3_1c * 100:.2f}%{format_stars(p_1c)}",
        'Day-Clustered SE': f"{se_1c * 100:.2f}%",
        't-Statistic': f"{t_1c:.2f}",
        'p-value': f"{p_1c:.4f}",
        'Resolved Trades (N)': len(df_1c),
        'Trading Days': df_1c['date'].nunique()
    })

    # --- Spec 2: Naive Binary DiD pooling Upstream + Downstream together against all other sectors ---
    df_2 = trades[trades['regime'].isin(['stable', 'post_shock'])].copy()
    df_2['post'] = (df_2['regime'] == 'post_shock').astype(float)
    df_2['treat'] = (df_2['is_upstream'] | df_2['is_downstream']).astype(float)
    df_2['post_x_treat'] = df_2['post'] * df_2['treat']
    
    X_2 = sm.add_constant(df_2[['post', 'treat', 'post_x_treat']])
    m_2 = sm.OLS(df_2['is_win'], X_2).fit(cov_type='cluster', cov_kwds={'groups': df_2['date']})
    b3_2, se_2, t_2, p_2 = m_2.params['post_x_treat'], m_2.bse['post_x_treat'], m_2.tvalues['post_x_treat'], m_2.pvalues['post_x_treat']

    table10_rows.append({
        'Specification': 'Spec 2: Naive Binary DiD (Pooled Upstream + Downstream vs. Others)',
        'DiD Parameter': 'β₃ (PostShock × EnergySector)',
        'DiD Coefficient': f"{b3_2 * 100:.2f}%{format_stars(p_2)}",
        'Day-Clustered SE': f"{se_2 * 100:.2f}%",
        't-Statistic': f"{t_2:.2f}",
        'p-value': f"{p_2:.4f}",
        'Resolved Trades (N)': len(df_2),
        'Trading Days': df_2['date'].nunique()
    })

    # --- Spec 2A: Pre-Shock Brent Beta Quartile Dummy across all 480 stocks ---
    trades_brent = trades.merge(brent[['date', 'R_brent']], on='date', how='left')
    stable_tb = trades_brent[trades_brent['regime'] == 'stable'].copy()
    stock_betas = {}
    for sym, group in stable_tb.groupby('symbol_root'):
        daily_stock = group.groupby('date').agg({'result_pct': 'mean', 'R_brent': 'first'}).dropna()
        if len(daily_stock) >= 30:
            cov = np.cov(daily_stock['result_pct'], daily_stock['R_brent'])[0, 1]
            var = np.var(daily_stock['R_brent'], ddof=1)
            stock_betas[sym] = (cov / var) if var > 0 else 0
            
    beta_series = pd.Series(stock_betas)
    q75 = beta_series.quantile(0.75)
    high_beta_stocks = set(beta_series[beta_series >= q75].index)
    
    df_2a = trades[trades['regime'].isin(['stable', 'post_shock'])].copy()
    df_2a['high_beta'] = df_2a['symbol_root'].isin(high_beta_stocks).astype(float)
    df_2a['post'] = (df_2a['regime'] == 'post_shock').astype(float)
    df_2a['post_x_high_beta'] = df_2a['post'] * df_2a['high_beta']
    
    X_2a = sm.add_constant(df_2a[['post', 'high_beta', 'post_x_high_beta']])
    m_2a = sm.OLS(df_2a['is_win'], X_2a).fit(cov_type='cluster', cov_kwds={'groups': df_2a['date']})
    b3_2a, se_2a, t_2a, p_2a = m_2a.params['post_x_high_beta'], m_2a.bse['post_x_high_beta'], m_2a.tvalues['post_x_high_beta'], m_2a.pvalues['post_x_high_beta']

    table10_rows.append({
        'Specification': 'Spec 2A: Pre-Shock Brent Beta Quartile Dummy (All 480 Stocks)',
        'DiD Parameter': 'β₃ (PostShock × HighBrentBeta)',
        'DiD Coefficient': f"{b3_2a * 100:.2f}%{format_stars(p_2a)}",
        'Day-Clustered SE': f"{se_2a * 100:.2f}%",
        't-Statistic': f"{t_2a:.2f}",
        'p-value': f"{p_2a:.4f}",
        'Resolved Trades (N)': len(df_2a),
        'Trading Days': df_2a['date'].nunique()
    })

    # --- Spec 3A: Continuous Brent Volatility × Downstream Consumers (vs. Clean Defensives) ---
    df_3a = trades[trades['is_downstream'] | trades['is_defensive']].merge(
        brent[['date', 'sigma_brent_20d']], on='date', how='inner'
    ).dropna(subset=['sigma_brent_20d']).copy()

    df_3a['treat'] = df_3a['is_downstream'].astype(float)
    df_3a['vol_x_treat'] = df_3a['sigma_brent_20d'] * df_3a['treat']

    X_3a = sm.add_constant(df_3a[['sigma_brent_20d', 'treat', 'vol_x_treat']])
    m_3a = sm.OLS(df_3a['is_win'], X_3a).fit(cov_type='cluster', cov_kwds={'groups': df_3a['date']})
    b3_3a, se_3a, t_3a, p_3a = m_3a.params['vol_x_treat'], m_3a.bse['vol_x_treat'], m_3a.tvalues['vol_x_treat'], m_3a.pvalues['vol_x_treat']

    table10_rows.append({
        'Specification': 'Spec 3A: Continuous Brent Volatility × Downstream Consumers',
        'DiD Parameter': 'β₃ (σ_Brent × Downstream)',
        'DiD Coefficient': f"{b3_3a:.4f}{format_stars(p_3a)}",
        'Day-Clustered SE': f"{se_3a:.4f}",
        't-Statistic': f"{t_3a:.2f}",
        'p-value': f"{p_3a:.4f}",
        'Resolved Trades (N)': len(df_3a),
        'Trading Days': df_3a['date'].nunique()
    })

    df_table10 = pd.DataFrame(table10_rows)

    # Save CSV
    os.makedirs(os.path.join(BASE_DIR, 'output', 'tables'), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, 'output', 'figures'), exist_ok=True)
    
    csv_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_10_sector_did.csv')
    df_table10.to_csv(csv_path, index=False)

    # Generate Markdown Table
    md_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_10_sector_did.md')
    md_lines = [
        "# Table 10: Sector Difference-in-Differences Estimations",
        "",
        "Difference-in-Differences (DiD) specifications evaluating energy transmission across Downstream Consumers, Upstream Producers, and Clean Defensives. "
        "Standard errors are clustered by trading session date. Significance: * p < 0.10, ** p < 0.05, *** p < 0.01.",
        "",
        "| Specification | DiD Parameter | DiD Coefficient | Day-Clustered SE | t-Statistic | p-value | Resolved Trades (N) | Trading Days |",
        "|:---|:---|---:|---:|---:|:---:|---:|---:|"
    ]
    for _, r in df_table10.iterrows():
        md_lines.append(
            f"| {r['Specification']} | {r['DiD Parameter']} | {r['DiD Coefficient']} | "
            f"{r['Day-Clustered SE']} | {r['t-Statistic']} | {r['p-value']} | "
            f"{r['Resolved Trades (N)']:,} | {r['Trading Days']:,} |"
        )
    md_lines.append("")
    
    with open(md_path, 'w') as f:
        f.write('\n'.join(md_lines))
    print(f"Table 10 saved to {csv_path} and {md_path}")

    # Plot Figure 5: Downstream vs Upstream vs Defensive Daily Win Rates
    down_daily = trades[trades['is_downstream']].groupby('date')['is_win'].mean() * 100.0
    up_daily = trades[trades['is_upstream']].groupby('date')['is_win'].mean() * 100.0
    def_daily = trades[trades['is_defensive']].groupby('date')['is_win'].mean() * 100.0
    
    plot_df = pd.DataFrame({'Downstream': down_daily, 'Upstream': up_daily, 'Defensive': def_daily}).dropna().reset_index()
    plot_df['date_dt'] = pd.to_datetime(plot_df['date'])
    plot_df = plot_df.sort_values('date_dt')
    
    plot_df['Downstream_20d'] = plot_df['Downstream'].rolling(20).mean()
    plot_df['Upstream_20d'] = plot_df['Upstream'].rolling(20).mean()
    plot_df['Defensive_20d'] = plot_df['Defensive'].rolling(20).mean()
    
    fig_path = os.path.join(BASE_DIR, 'output', 'figures', 'figure_05_sector_did_trajectories.png')
    
    plt.figure(figsize=(11, 5.5), dpi=300)
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    plt.plot(plot_df['date_dt'], plot_df['Downstream_20d'], color='#d62728', linewidth=2.0, label='Downstream Consumers (20-Day MA)')
    plt.plot(plot_df['date_dt'], plot_df['Upstream_20d'], color='#ff7f0e', linewidth=1.8, linestyle='--', label='Upstream Producers (20-Day MA)')
    plt.plot(plot_df['date_dt'], plot_df['Defensive_20d'], color='#1f77b4', linewidth=2.0, label='Clean Defensives (20-Day MA)')
    
    plt.axvline(x=pd.to_datetime('2026-03-04'), color='#2ca02c', linestyle=':', linewidth=1.8, label='Event Date (2026-03-04)')
    plt.axhline(y=50.0, color='#333333', linestyle='--', linewidth=1.0, alpha=0.7, label='50% Breakeven Barrier')
    
    plt.title('Figure 5: Daily Win Rates for Downstream, Upstream, and Defensive Sectors', fontsize=13, fontweight='bold', pad=12)
    plt.xlabel('Calendar Date', fontsize=11, labelpad=8)
    plt.ylabel('Resolved Win Rate (%, 20-Day Moving Average)', fontsize=11, labelpad=8)
    plt.legend(frameon=True, loc='lower left', fontsize=9.5)
    plt.tight_layout()
    plt.savefig(fig_path, dpi=300)
    plt.close()
    
    print(f"Figure 5 saved to {fig_path}")
    return df_table10

if __name__ == '__main__':
    run_test_8()
