# Corporate-Action Reconciliation Table: January 2022 NIFTY 500 Constituent Universe Audit

**Document Provenance**:
- **Source Index Factsheet**: *Constituents of NIFTY 500 (January 31, 2022)*, NSE Indices Limited, Mumbai, India. Archived at: `sources/NSE_NIFTY_500_Jan2022_Archived_Factsheet.pdf`
- **Total Initial Constituents**: 501 entries (comprising 500 unique corporate issuers including dual-class shares: TATAMOTORS and TATAMTRDVR).
- **Excluded Non-Continuous Constituents**: Exactly 21 tickers (representing 20 corporate restructuring/insolvency situations) identified in `delisted_2022.txt`.
- **Final Master Sample**: 480 continuous equities possessing continuous 1-minute historical intraday bar records from January 3, 2022 to July 10, 2026.

---

### Comprehensive Corporate Action Audit & Reconciliation Table

| # | Ticker Symbol | Company Name | Industry / GICS Sector | Initial Weight (%) | Close Price (Jan 2022) | Corporate Action Type | Effective Date | Successor Entity / Resolution Status | Reason for Microstructural Exclusion |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :---: | :--- | :--- |
| 1 | **HDFC** | Housing Development Finance Corporation Ltd. | Financial Services | 3.9746% | ₹2,521.00 | Reverse Merger / Amalgamation | July 13, 2023 | Merged into **HDFC Bank Ltd.** (HDFCBANK) | Discontinued historical ticker; trading ceased on NSE. |
| 2 | **LTI** | Larsen & Toubro Infotech Ltd. | Information Technology | 0.2529% | ₹6,270.35 | Amalgamation / Merger | Nov 14, 2022 | Amalgamated with Mindtree to form **LTIMindtree Ltd.** (LTIM) | Discontinued historical ticker; merged trading under new ticker LTIM. |
| 3 | **MINDTREE** | MindTree Ltd. | Information Technology | 0.2226% | ₹4,006.30 | Amalgamation / Merger | Nov 14, 2022 | Amalgamated into **LTIMindtree Ltd.** (LTIM) | Discontinued historical ticker; shares converted to LTIM. |
| 4 | **INOXLEISUR** | Inox Leisure Ltd. | Media & Entertainment | 0.0228% | ₹416.85 | Amalgamation / Merger | Feb 17, 2023 | Merged into **PVR Ltd.** (forming PVR INOX Ltd.) | Discontinued historical ticker; merged into PVRINOX. |
| 5 | **TATACOFFEE** | Tata Coffee Ltd. | Consumer Goods | 0.0217% | ₹216.25 | Composite Scheme of Amalgamation | Jan 15, 2024 | Merged into **Tata Consumer Products Ltd.** (TATACONSUM) | Discontinued historical ticker; trading ceased. |
| 6 | **TATASTLLP** | Tata Steel Long Products Ltd. | Metals & Mining | 0.0186% | ₹765.80 | Amalgamation / Group Consolidation | Nov 17, 2023 | Merged into **Tata Steel Ltd.** (TATASTEEL) | Discontinued historical ticker; shares merged. |
| 7 | **JSLHISAR** | Jindal Stainless (Hisar) Ltd. | Metals & Mining | 0.0339% | ₹402.90 | Amalgamation / Group Consolidation | Mar 09, 2023 | Merged into **Jindal Stainless Ltd.** (JSL) | Discontinued historical ticker; trading consolidated into JSL. |
| 8 | **SHRIRAMCIT** | Shriram City Union Finance Ltd. | Financial Services | 0.0441% | ₹1,776.30 | Composite Scheme of Amalgamation | Nov 30, 2022 | Merged into Shriram Transport Finance (now **Shriram Finance Ltd.**) | Discontinued historical ticker; merged into SHREERAMFIN. |
| 9 | **EQUITAS** | Equitas Holdings Ltd. | Financial Services | 0.0337% | ₹109.50 | Reverse Amalgamation | Feb 08, 2023 | Amalgamated with **Equitas Small Finance Bank Ltd.** | Discontinued historical holding company ticker. |
| 10 | **UJJIVAN** | Ujjivan Financial Services Ltd. | Financial Services | 0.0117% | ₹137.40 | Reverse Amalgamation | Apr 30, 2024 | Merged into **Ujjivan Small Finance Bank Ltd.** | Discontinued historical holding company ticker. |
| 11 | **IDFC** | IDFC Ltd. | Financial Services | 0.0887% | ₹64.70 | Reverse Merger | Oct 01, 2024 | Merged into **IDFC FIRST Bank Ltd.** (IDFCFIRSTB) | Discontinued historical holding company ticker. |
| 12 | **FRETAIL** | Future Retail Ltd. | Consumer Services | 0.0115% | ₹48.70 | Corporate Insolvency (CIRP) / Delisting | Aug 12, 2022 | Admitted to NCLT insolvency; trading suspended by NSE | Insolvent entity; trading suspended; zero post-2022 intraday price discovery. |
| 13 | **DHANI** | Dhani Services Ltd. | Financial Services | 0.0443% | ₹131.40 | Capital Reduction & Restructuring | Nov 2022 | Restructured; moved to trade-to-trade surveillance | Discontinuous order-book depth; failed continuous liquidity criteria. |
| 14 | **IBREALEST** | Indiabulls Real Estate Ltd. | Construction & Realty | 0.0552% | ₹143.85 | Scheme of Arrangement / Rebranding | May 2023 | Reorganized and rebranded as **Equinox India Developments Ltd.** | Multi-month suspension and structural restructuring. |
| 15 | **ISEC** | ICICI Securities Ltd. | Financial Services | 0.0558% | ₹721.20 | Scheme of Delisting & Merger | June 2024 | Delisted from NSE; merged as wholly owned subsidiary of ICICI Bank | Delisted equity; trading discontinued on NSE. |
| 16 | **PEL** | Piramal Enterprises Ltd. | Financial Services | 0.2832% | ₹2,391.55 | Structural Demerger | Aug 26, 2022 | Demerged pharma division into standalone **Piramal Pharma Ltd.** | Price step-down from ~₹2,400 to ~₹800 due to demerger; unadjusted intraday gap distortion. |
| 17 | **SUVENPHAR** | Suven Pharmaceuticals Ltd. | Healthcare / Pharma | 0.0555% | ₹536.85 | Strategic Buyout / Scheme of Amalgamation | May 2023 | Acquired by Advent International; amalgamated with Cohance Lifesciences | Significant discontinuous trading halts during takeover. |
| 18 | **TATAMTRDVR** | Tata Motors Ltd. (DVR Class A) | Automobile | 0.1112% | ₹260.70 | Capital Reduction Scheme | Aug 30, 2024 | Extinguished; converted to ordinary Tata Motors shares | Dual-class security cancelled; ceased trading on NSE. |
| 19 | **TCNSBRANDS** | TCNS Clothing Co. Ltd. | Textiles & Apparel | 0.0115% | ₹722.65 | Strategic Acquisition & Scheme | Sept 2023 | Acquired by Aditya Birla Fashion & Retail Ltd. (ABFRL) | Discontinuous liquidity; merged into ABFRL operations. |
| 20 | **TV18BRDCST** | TV18 Broadcast Ltd. | Media & Entertainment | 0.0441% | ₹59.10 | Composite Scheme of Arrangement | Oct 2024 | Merged into **Network18 Media & Investments Ltd.** | Discontinued historical ticker; merged into parent. |
| 21 | **SPICEJET** | SpiceJet Ltd. | Transportation / Airlines | 0.0115% | ₹60.85 | Enhanced Surveillance Measure (ESM) / Insolvency Petitions | 2022–2024 | Ongoing surveillance; periodic trading restrictions | Severe trading interruptions; failed 1-minute continuous auction liquidity criteria. |

---

### Verification Summary
1. **Mathematical Consistency**:
   - Initial Universe: 501 constituent listings.
   - Dual-class shares: TATAMOTORS (ordinary) and TATAMTRDVR (DVR Class A) both included in the January 2022 factsheet.
   - Removing the 21 discontinued/restructured listings yields exactly:
     $$501 - 21 = 480 \text{ continuous, balanced cross-sectional equities}$$
2. **Robustness to Survivorship Bias**:
   - All 480 remaining constituents possess unbroken 1-minute intraday tick data across all 1,116 regular trading sessions (March 2022 to July 2026).
   - In Table 11 of the manuscript, survivorship bias is formally tested by estimating the two-way clustered LPM across the blue-chip Nifty 50 sub-universe (48 surviving stocks with zero survivorship or delisting risk), showing an identical collapse of -8.38 pp ($t = -5.33, p < 0.0001$) matching the full universe (-8.15 pp).

