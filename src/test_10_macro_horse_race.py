"""
Test 10: Macro Horse Race — Sequential WLS Models
Manuscript Reference: Table 12, Figure 8, Section 4.8
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
from src.data_loader import load_daily_clean, load_trades_clean

def format_stars(p_val):
    if p_val < 0.01: return "***"
    elif p_val < 0.05: return "**"
    elif p_val < 0.10: return "*"
    else: return ""

def run_test_10():
    print("Running Test 10: Macro Horse Race (Table 12, Figure 8)...")
    daily = load_daily_clean()

    # Load Macro Series
    # 1. Brent Crude
    brent_path = os.path.join(BASE_DIR, 'data', 'macro', 'XBR_USD Historical Data.csv')
    brent = pd.read_csv(brent_path, encoding='utf-8-sig')
    brent['date'] = pd.to_datetime(brent['Date']).dt.strftime('%Y-%m-%d')
    brent = brent.sort_values('date').reset_index(drop=True)
    brent['R_brent'] = np.log(brent['Price'] / brent['Price'].shift(1))
    brent['abs_R_brent'] = brent['R_brent'].abs()
    brent['sigma_brent_20d'] = brent['R_brent'].rolling(20).std()

    # 2. India VIX
    vix_path = os.path.join(BASE_DIR, 'data', 'macro', 'India VIX Historical Data.csv')
    vix = pd.read_csv(vix_path, encoding='utf-8-sig')
    vix['date'] = pd.to_datetime(vix['Date']).dt.strftime('%Y-%m-%d')
    vix = vix.sort_values('date').reset_index(drop=True)
    vix['vix'] = vix['Price']

    # 3. Nifty 500
    n500_path = os.path.join(BASE_DIR, 'data', 'macro', 'Nifty 500 Historical Data.csv')
    n500 = pd.read_csv(n500_path, encoding='utf-8-sig')
    n500['date'] = pd.to_datetime(n500['Date']).dt.strftime('%Y-%m-%d')
    n500 = n500.sort_values('date').reset_index(drop=True)
    p_num = n500['Price'].astype(str).str.replace(',', '').astype(float)
    n500['R_nifty500'] = np.log(p_num / p_num.shift(1))
    n500['abs_R_nifty500'] = n500['R_nifty500'].abs()

    # 4. USD/INR
    usdinr_path = os.path.join(BASE_DIR, 'data', 'macro', 'INR_USD Historical Data.csv')
    usdinr = pd.read_csv(usdinr_path, encoding='utf-8-sig')
    usdinr['date'] = pd.to_datetime(usdinr['Date']).dt.strftime('%Y-%m-%d')
    usdinr = usdinr.sort_values('date').reset_index(drop=True)
    usdinr['usd_inr_chg'] = np.log(usdinr['Price'] / usdinr['Price'].shift(1))

    # 5. NSE Volume / Turnover
    vol_path = os.path.join(BASE_DIR, 'data', 'macro', 'NSE_Volume_Jan2022_to_May2026.csv')
    nse_vol = pd.read_csv(vol_path, encoding='utf-8-sig')
    nse_vol['date'] = pd.to_datetime(nse_vol['Date'], dayfirst=True).dt.strftime('%Y-%m-%d')
    nse_vol = nse_vol.sort_values('date').reset_index(drop=True)
    to_crore = nse_vol['Turnover_Rs_Crore'].replace(0, np.nan)
    nse_vol['ln_turnover'] = np.log(to_crore)

    # 6. FII Net Flows
    fii_path = os.path.join(BASE_DIR, 'data', 'macro', 'fii_dii_cash_2025_to_present.csv')
    fii = pd.read_csv(fii_path, encoding='utf-8-sig')
    fii['date'] = pd.to_datetime(fii['Date']).dt.strftime('%Y-%m-%d')
    fii = fii.sort_values('date').reset_index(drop=True)
    fii['fii_net'] = fii['FII_Net']

    # 7. Opening Bar Range (Microstructure)
    bar_path = os.path.join(BASE_DIR, 'data', 'microstructure', 'opening_bar_ranges.pkl')
    bar_df = pd.read_pickle(bar_path)
    bar_df['range'] = (bar_df['bar0_high'] - bar_df['bar0_low']) / bar_df['bar0_open']
    bar_df['date_str'] = bar_df['date'].astype(str)
    daily_bar_range = bar_df.groupby('date_str')['range'].mean().reset_index()
    daily_bar_range.columns = ['date', 'mean_bar0_range']

    # 8. Sweet Spot Share
    trades = load_trades_clean(resolved_only=True)
    trades['is_sweet_spot'] = trades['gap_size_pct'].between(0.50, 2.00)
    daily_sweet = trades.groupby('date')['is_sweet_spot'].mean().reset_index()
    daily_sweet.columns = ['date', 'sweet_spot_share']

    # Merging panel
    df = daily.copy()
    df['post_shock'] = (df['regime'] == 'post_shock').astype(float)
    df = df.merge(vix[['date', 'vix']], on='date', how='left')
    df = df.merge(n500[['date', 'R_nifty500', 'abs_R_nifty500']], on='date', how='left')
    df = df.merge(usdinr[['date', 'usd_inr_chg']], on='date', how='left')
    df = df.merge(nse_vol[['date', 'ln_turnover']], on='date', how='left')
    df = df.merge(fii[['date', 'fii_net']], on='date', how='left')
    df = df.merge(daily_bar_range[['date', 'mean_bar0_range']], on='date', how='left')
    df = df.merge(daily_sweet[['date', 'sweet_spot_share']], on='date', how='left')
    df = df.merge(brent[['date', 'R_brent', 'abs_R_brent', 'sigma_brent_20d']], on='date', how='left')

    models = [
        ('Model 1', ['post_shock']),
        ('Model 2', ['post_shock', 'vix', 'R_nifty500', 'abs_R_nifty500']),
        ('Model 3', ['post_shock', 'vix', 'R_nifty500', 'abs_R_nifty500', 'usd_inr_chg', 'ln_turnover']),
        ('Model 4', ['post_shock', 'vix', 'R_nifty500', 'abs_R_nifty500', 'usd_inr_chg', 'ln_turnover', 'mean_bar0_range', 'sweet_spot_share']),
        ('Model 5', ['post_shock', 'vix', 'R_nifty500', 'abs_R_nifty500', 'usd_inr_chg', 'ln_turnover', 'mean_bar0_range', 'sweet_spot_share', 'sigma_brent_20d', 'abs_R_brent']),
        ('Model 6', ['post_shock', 'vix', 'R_nifty500', 'abs_R_nifty500', 'usd_inr_chg', 'ln_turnover', 'mean_bar0_range', 'sweet_spot_share', 'sigma_brent_20d', 'abs_R_brent', 'fii_net'])
    ]

    all_variables = [
        ('const', 'Constant (α)'),
        ('post_shock', 'PostShock Indicator (β₁)'),
        ('vix', 'India VIX'),
        ('R_nifty500', 'Nifty 500 Return'),
        ('abs_R_nifty500', '|Nifty 500 Return|'),
        ('usd_inr_chg', 'Δ USD/INR'),
        ('ln_turnover', 'ln(NSE Turnover)'),
        ('mean_bar0_range', 'Mean Opening Bar Range'),
        ('sweet_spot_share', 'Sweet Spot Share'),
        ('sigma_brent_20d', 'Brent 20d Volatility'),
        ('abs_R_brent', '|Brent Return|'),
        ('fii_net', 'FII Net Flow (Rs Cr)')
    ]

    model_results = {}
    fig8_data = []

    for m_label, v_list in models:
        sub = df.dropna(subset=v_list + ['resolved_wr', 'n_resolved']).copy()
        X = sm.add_constant(sub[v_list])
        res = sm.WLS(sub['resolved_wr'], X, weights=sub['n_resolved']).fit(cov_type='HAC', cov_kwds={'maxlags': 5})
        
        post_b = res.params['post_shock']
        post_se = res.bse['post_shock']
        fig8_data.append({
            'model': m_label,
            'x_label': f"{m_label}\n(N={len(sub):,})",
            'beta': post_b * 100.0,
            'se': post_se * 100.0,
            'ci_lower': (post_b - 1.96 * post_se) * 100.0,
            'ci_upper': (post_b + 1.96 * post_se) * 100.0
        })
        
        col_dict = {}
        for var_name, var_disp in all_variables:
            if var_name in res.params:
                coef = res.params[var_name]
                se = res.bse[var_name]
                pval = res.pvalues[var_name]
                stars = format_stars(pval)
                if var_name == 'fii_net':
                    col_dict[var_disp] = f"{coef:.2e}{stars} ({se:.2e})"
                elif var_name in ['const', 'post_shock']:
                    col_dict[var_disp] = f"{coef * 100:.2f}%{stars} ({se * 100:.2f}%)"
                else:
                    col_dict[var_disp] = f"{coef:.4f}{stars} ({se:.4f})"
            else:
                col_dict[var_disp] = "—"
                
        col_dict['Weighted R²'] = f"{res.rsquared:.4f}"
        col_dict['Observations (N)'] = f"{len(sub):,}"
        model_results[m_label] = col_dict

    df_table12 = pd.DataFrame(model_results)
    df_table12.index.name = 'Variable'
    df_table12 = df_table12.reset_index()

    # Save CSV
    os.makedirs(os.path.join(BASE_DIR, 'output', 'tables'), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, 'output', 'figures'), exist_ok=True)
    
    csv_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_12_macro_horse_race.csv')
    df_table12.to_csv(csv_path, index=False)

    # Generate Markdown Table
    md_path = os.path.join(BASE_DIR, 'output', 'tables', 'table_12_macro_horse_race.md')
    md_lines = [
        "# Table 12: Macro Horse Race — Sequential WLS Models",
        "",
        "Sequential Weighted Least Squares (WLS) regressions of daily resolved win rate (WR_t). "
        "Models 1–5 cover the full 2022–2026 sample; Model 6 evaluates the 2025–2026 sub-sample with direct FII net flows. "
        "Weights: daily resolved trade count (n_resolved). Standard errors: Newey-West HAC (lag = 5) reported in parentheses. "
        "Significance: * p < 0.10, ** p < 0.05, *** p < 0.01.",
        "",
        "| Variable | Model 1 | Model 2 | Model 3 | Model 4 | Model 5 | Model 6 |",
        "|:---|---:|---:|---:|---:|---:|---:|"
    ]
    for _, r in df_table12.iterrows():
        md_lines.append(
            f"| {r['Variable']} | {r['Model 1']} | {r['Model 2']} | {r['Model 3']} | {r['Model 4']} | {r['Model 5']} | {r['Model 6']} |"
        )
    md_lines.append("")
    
    with open(md_path, 'w') as f:
        f.write('\n'.join(md_lines))
    print(f"Table 12 saved to {csv_path} and {md_path}")

    # --- Plot Figure 8: Horse Race Coefficient Path ---
    df_fig8 = pd.DataFrame(fig8_data)
    fig_path = os.path.join(BASE_DIR, 'output', 'figures', 'figure_08_macro_horse_race_coefficients.png')
    
    plt.figure(figsize=(10, 5), dpi=300)
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    x = np.arange(len(df_fig8))
    plt.errorbar(
        x, df_fig8['beta'], 
        yerr=1.96 * df_fig8['se'], 
        fmt='-o', color='#1f77b4', ecolor='#1f77b4', elinewidth=2.0, capsize=5, markersize=7, linewidth=2.0,
        label='PostShock β₁ (95% CI)'
    )
    plt.axhline(y=0, color='#d62728', linestyle='--', linewidth=1.2, alpha=0.8, label='Zero Effect Threshold')
    
    plt.xticks(x, df_fig8['x_label'], fontsize=9.5)
    plt.ylabel('PostShock Effect on Daily Win Rate (pp)', fontsize=11, labelpad=8)
    plt.xlabel('Sequential Macro Control Model', fontsize=11, labelpad=8)
    plt.title('Figure 8: Post-Shock Indicator Attenuation in Macro Horse Race', fontsize=13, fontweight='bold', pad=12)
    plt.legend(frameon=True, loc='lower right', fontsize=10)
    plt.tight_layout()
    plt.savefig(fig_path, dpi=300)
    plt.close()
    
    print(f"Figure 8 saved to {fig_path}")
    return df_table12

if __name__ == '__main__':
    run_test_10()

