"""
Test 8: Sector Difference-in-Differences — 4 Specifications
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
    
    # Classify sectors
    defensive_sectors = {'FMCG', 'Healthcare', 'Pharma', 'IT'}
    downstream_sectors = {'Oil & Gas', 'Chemicals'}
    paint_transport_tickers = {'ASIANPAINT', 'BERGEPAINT', 'KANSAINER', 'INDIGOPNTS', 'INDIGO', 'CONCOR', 'BLUEDART'}

    trades['is_defensive'] = trades['sector'].isin(defensive_sectors)
    trades['is_downstream'] = trades['sector'].isin(downstream_sectors) | trades['symbol_root'].isin(paint_transport_tickers)
    
    # Load Brent crude data for Specs 2A and 3A
    brent_path = os.path.join(BASE_DIR, 'data', 'macro', 'XBR_USD Historical Data.csv')
    brent = pd.read_csv(brent_path, encoding='utf-8-sig')
    brent['date'] = pd.to_datetime(brent['Date']).dt.strftime('%Y-%m-%d')
    brent = brent.sort_values('date').reset_index(drop=True)
    brent['R_brent'] = np.log(brent['Price'] / brent['Price'].shift(1))
    brent['sigma_brent_20d'] = brent['R_brent'].rolling(20).std()

    table10_rows = []

    # --- Specification 1A: Downstream vs Defensives, Acute March 2026 ---
    sub_1a = trades[trades['is_defensive'] | trades['is_downstream']].copy()
    pre_1a = sub_1a[sub_1a['regime'] == 'stable'].copy()
    post_1a = sub_1a[sub_1a['date'].str.startswith('2026-03')].copy()
    df_1a = pd.concat([pre_1a, post_1a]).reset_index(drop=True)
    df_1a['post'] = (df_1a['date'].str.startswith('2026-03')).astype(float)
    df_1a['downstream'] = df_1a['is_downstream'].astype(float)
    df_1a['post_x_downstream'] = df_1a['post'] * df_1a['downstream']

    X_1a = sm.add_constant(df_1a[['post', 'downstream', 'post_x_downstream']])
    m_1a = sm.OLS(df_1a['is_win'], X_1a).fit(cov_type='cluster', cov_kwds={'groups': df_1a['date']})
    b3_1a, se_1a, t_1a, p_1a = m_1a.params['post_x_downstream'], m_1a.bse['post_x_downstream'], m_1a.tvalues['post_x_downstream'], m_1a.pvalues['post_x_downstream']
    
    table10_rows.append({
        'Specification': 'Spec 1A: Downstream vs Defensives (Acute Mar 2026)',
        'DiD Parameter': 'β₃ (PostShock × Downstream)',
        'DiD Coefficient': f"{b3_1a * 100:.2f}%{format_stars(p_1a)}",
        'Day-Clustered SE': f"{se_1a * 100:.2f}%",
        't-Statistic': f"{t_1a:.2f}",
        'p-value': f"{p_1a:.4f}",
        'Resolved Trades (N)': len(df_1a),
        'Trading Days': df_1a['date'].nunique()
    })

    # --- Specification 1B: Downstream vs Defensives, Extended March–July 2026 ---
    post_1b = sub_1a[sub_1a['regime'] == 'post_shock'].copy()
    df_1b = pd.concat([pre_1a, post_1b]).reset_index(drop=True)
    df_1b['post'] = (df_1b['regime'] == 'post_shock').astype(float)
    df_1b['downstream'] = df_1b['is_downstream'].astype(float)
    df_1b['post_x_downstream'] = df_1b['post'] * df_1b['downstream']

    X_1b = sm.add_constant(df_1b[['post', 'downstream', 'post_x_downstream']])
    m_1b = sm.OLS(df_1b['is_win'], X_1b).fit(cov_type='cluster', cov_kwds={'groups': df_1b['date']})
    b3_1b, se_1b, t_1b, p_1b = m_1b.params['post_x_downstream'], m_1b.bse['post_x_downstream'], m_1b.tvalues['post_x_downstream'], m_1b.pvalues['post_x_downstream']

    table10_rows.append({
        'Specification': 'Spec 1B: Downstream vs Defensives (Extended Mar–Jul 2026)',
        'DiD Parameter': 'β₃ (PostShock × Downstream)',
        'DiD Coefficient': f"{b3_1b * 100:.2f}%{format_stars(p_1b)}",
        'Day-Clustered SE': f"{se_1b * 100:.2f}%",
        't-Statistic': f"{t_1b:.2f}",
        'p-value': f"{p_1b:.4f}",
        'Resolved Trades (N)': len(df_1b),
        'Trading Days': df_1b['date'].nunique()
    })

    # --- Specification 2: Naive Binary DiD (Pooled, All Sectors) ---
    df_2 = trades[trades['regime'].isin(['stable', 'post_shock'])].copy()
    df_2['post'] = (df_2['regime'] == 'post_shock').astype(float)
    X_2 = sm.add_constant(df_2['post'])
    m_2 = sm.OLS(df_2['is_win'], X_2).fit(cov_type='cluster', cov_kwds={'groups': df_2['date']})
    b1_2, se_2, t_2, p_2 = m_2.params['post'], m_2.bse['post'], m_2.tvalues['post'], m_2.pvalues['post']

    table10_rows.append({
        'Specification': 'Spec 2: Naive Binary DiD (Pooled All Sectors)',
        'DiD Parameter': 'β₁ (PostShock)',
        'DiD Coefficient': f"{b1_2 * 100:.2f}%{format_stars(p_2)}",
        'Day-Clustered SE': f"{se_2 * 100:.2f}%",
        't-Statistic': f"{t_2:.2f}",
        'p-value': f"{p_2:.4f}" if p_2 >= 0.0001 else "< 0.0001",
        'Resolved Trades (N)': len(df_2),
        'Trading Days': df_2['date'].nunique()
    })

    # --- Specification 2A: Pre-Shock Brent Beta Quartile Dummy ---
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
        'Specification': 'Spec 2A: Pre-Shock Brent Beta Quartile Dummy',
        'DiD Parameter': 'β₃ (PostShock × HighBrentBeta)',
        'DiD Coefficient': f"{b3_2a * 100:.2f}%{format_stars(p_2a)}",
        'Day-Clustered SE': f"{se_2a * 100:.2f}%",
        't-Statistic': f"{t_2a:.2f}",
        'p-value': f"{p_2a:.4f}",
        'Resolved Trades (N)': len(df_2a),
        'Trading Days': df_2a['date'].nunique()
    })

    # --- Specification 3A: Continuous Brent Volatility × Downstream Interaction ---
    df_3a = trades[(trades['is_defensive'] | trades['is_downstream'])].merge(
        brent[['date', 'sigma_brent_20d']], on='date', how='inner'
    ).dropna(subset=['sigma_brent_20d']).copy()

    df_3a['downstream'] = df_3a['is_downstream'].astype(float)
    df_3a['vol_x_downstream'] = df_3a['sigma_brent_20d'] * df_3a['downstream']

    X_3a = sm.add_constant(df_3a[['sigma_brent_20d', 'downstream', 'vol_x_downstream']])
    m_3a = sm.OLS(df_3a['is_win'], X_3a).fit(cov_type='cluster', cov_kwds={'groups': df_3a['date']})
    b3_3a, se_3a, t_3a, p_3a = m_3a.params['vol_x_downstream'], m_3a.bse['vol_x_downstream'], m_3a.tvalues['vol_x_downstream'], m_3a.pvalues['vol_x_downstream']

    table10_rows.append({
        'Specification': 'Spec 3A: Continuous Brent Volatility × Downstream',
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
        "Difference-in-Differences (DiD) specifications evaluating sector vulnerabilities across Downstream and Defensive industries. "
        "Standard errors are clustered by trading day. Significance: * p < 0.10, ** p < 0.05, *** p < 0.01.",
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

    # --- Plot Figure 5: Downstream vs Defensive Daily Win Rates ---
    daily_sec = trades.groupby(['date', 'is_downstream', 'is_defensive']).agg(
        wins=('is_win', 'sum'),
        total=('is_win', 'count')
    ).reset_index()
    
    down_daily = trades[trades['is_downstream']].groupby('date')['is_win'].mean() * 100.0
    def_daily = trades[trades['is_defensive']].groupby('date')['is_win'].mean() * 100.0
    
    plot_df = pd.DataFrame({'Downstream': down_daily, 'Defensive': def_daily}).dropna().reset_index()
    plot_df['date_dt'] = pd.to_datetime(plot_df['date'])
    plot_df = plot_df.sort_values('date_dt')
    
    # 20-day rolling averages for visual clarity
    plot_df['Downstream_20d'] = plot_df['Downstream'].rolling(20).mean()
    plot_df['Defensive_20d'] = plot_df['Defensive'].rolling(20).mean()
    
    fig_path = os.path.join(BASE_DIR, 'output', 'figures', 'figure_05_sector_did_trajectories.png')
    
    plt.figure(figsize=(11, 5.5), dpi=300)
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    plt.plot(plot_df['date_dt'], plot_df['Downstream_20d'], color='#d62728', linewidth=2.0, label='Downstream Oil-Sensitive (20-Day MA)')
    plt.plot(plot_df['date_dt'], plot_df['Defensive_20d'], color='#1f77b4', linewidth=2.0, label='Defensive Oil-Insensitive (20-Day MA)')
    
    plt.axvline(x=pd.to_datetime('2026-03-04'), color='#2ca02c', linestyle=':', linewidth=1.8, label='Event Date (2026-03-04)')
    plt.axhline(y=50.0, color='#333333', linestyle='--', linewidth=1.0, alpha=0.7, label='50% Breakeven')
    
    plt.title('Figure 5: Daily Win Rates for Downstream vs Defensive Sectors Over Time', fontsize=13, fontweight='bold', pad=12)
    plt.xlabel('Calendar Date', fontsize=11, labelpad=8)
    plt.ylabel('Resolved Win Rate (%, 20-Day Moving Average)', fontsize=11, labelpad=8)
    plt.legend(frameon=True, loc='lower left', fontsize=10)
    plt.tight_layout()
    plt.savefig(fig_path, dpi=300)
    plt.close()
    
    print(f"Figure 5 saved to {fig_path}")
    return df_table10

if __name__ == '__main__':
    run_test_8()

