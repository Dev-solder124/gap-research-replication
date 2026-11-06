"""
Master Replication Orchestrator
Executes all 11 econometric replication tests sequentially and verifies cross-test consistency.
"""

import sys
import os
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.test_01_descriptive_stats import run_test_1
from src.test_02_oos_threshold_convergence import run_test_2
from src.test_03_structural_breaks import run_test_3
from src.test_04_lpm_two_way_cluster import run_test_4
from src.test_05_wls_newey_west import run_test_5
from src.test_06_gap_size_bins import run_test_6
from src.test_07_event_study_cawr import run_test_7
from src.test_08_sector_did import run_test_8
from src.test_09_strata_analysis import run_test_9
from src.test_10_macro_horse_race import run_test_10
from src.test_11_granger_causality import run_test_11

def main():
    print("=" * 80)
    print("STARTING COMPLETE MANUSCRIPT REPLICATION PIPELINE")
    print("=" * 80)
    start_total = time.time()
    
    stages = [
        ("Test 1: Sample Partition & Descriptive Statistics (Table 3)", run_test_1),
        ("Test 2: 16-Quarter Walk-Forward OOS Convergence (Table 4, Figure 2)", run_test_2),
        ("Test 3: Structural Break Tests (Table 5, Figure 1)", run_test_3),
        ("Test 4: Two-Way Clustered LPM (Table 6)", run_test_4),
        ("Test 5: Daily WLS with Newey-West HAC (Table 7)", run_test_5),
        ("Test 6: Gap-Size Bin Win-Rate Analysis (Table 8, Figure 3)", run_test_6),
        ("Test 7: Event Study — CAWR (Table 9, Figure 4)", run_test_7),
        ("Test 8: Sector Difference-in-Differences (Table 10, Figure 5)", run_test_8),
        ("Test 9: Survivorship & Liquidity Strata (Table 11, Figure 7)", run_test_9),
        ("Test 10: Macro Horse Race (Table 12, Figure 8)", run_test_10),
        ("Test 11: Granger Causality (Figure 6, Table)", run_test_11),
    ]
    
    for name, func in stages:
        t0 = time.time()
        print(f"\n>>> Executing {name}...")
        func()
        print(f">>> Completed {name} in {time.time() - t0:.2f} seconds.")
        
    print("\n" + "=" * 80)
    print(f"ALL 11 REPLICATION TESTS COMPLETED IN {time.time() - start_total:.2f} SECONDS.")
    print("=" * 80)

if __name__ == '__main__':
    main()

