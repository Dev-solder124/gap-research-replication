"""
Audit Bundle Generator
Compiles README, DATA_DICTIONARY, TESTS, all src/*.py, output/tables/*.md, and output/tables/*.csv
into a single consolidated markdown document: audit_bundle.md
"""

import os
import glob

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def generate_bundle():
    files_order = [
        'README.md',
        'DATA_DICTIONARY.md',
        'TESTS.md'
    ]
    files_order += sorted(glob.glob('src/*.py'))
    files_order += sorted(glob.glob('output/tables/*.md'))
    files_order += sorted(glob.glob('output/tables/*.csv'))
    
    # Exclude the builder itself if in src/
    files_order = [f for f in files_order if 'build_audit_bundle.py' not in f]

    bundle_lines = [
        "# Complete Replication Audit Bundle",
        "",
        "> **Manuscript**: Opening Gap Reversals in Indian Equities: Strategy Persistence, Structural Breaks, and Macro Sensitivities",
        "> **Master Sample**: 1,116 Regular Trading Sessions (January 2022 through July 2026)",
        "> **Global Sample Cleaning**: Three Diwali Muhurat sessions purged (2022-10-24, 2023-11-12, 2024-11-01)",
        f"> **Bundled Scope**: {len(files_order)} files (Documentation, Source Code, Output Markdown Tables, Output CSVs)",
        "",
        "---",
        "",
        "## Table of Contents",
        ""
    ]

    for idx, fpath in enumerate(files_order, 1):
        anchor = fpath.lower().replace('/', '-').replace('.', '-').replace('_', '-')
        bundle_lines.append(f"{idx}. [{fpath}](#file-{anchor})")

    bundle_lines.extend(["", "---", ""])

    for fpath in files_order:
        anchor = fpath.lower().replace('/', '-').replace('.', '-').replace('_', '-')
        bundle_lines.append(f"## File: `{fpath}` <a id=\"file-{anchor}\"></a>")
        bundle_lines.append("")
        
        full_path = os.path.join(BASE_DIR, fpath)
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            
        if fpath.endswith('.py'):
            bundle_lines.append("```python")
            bundle_lines.append(content)
            bundle_lines.append("```")
        elif fpath.endswith('.csv'):
            bundle_lines.append("```csv")
            bundle_lines.append(content)
            bundle_lines.append("```")
        else:
            # Markdown documentation & tables: insert directly for native rendering
            bundle_lines.append(content)
            
        bundle_lines.extend(["", "---", ""])

    out_path = os.path.join(BASE_DIR, 'audit_bundle.md')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(bundle_lines))

    print(f"audit_bundle.md generated at {out_path} ({len(bundle_lines)} lines, {os.path.getsize(out_path):,} bytes)")

if __name__ == '__main__':
    generate_bundle()

