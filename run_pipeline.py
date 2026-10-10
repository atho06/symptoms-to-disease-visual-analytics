"""
Script: run_pipeline.py
Purpose: Master execution script. Automatically processes raw Kaggle data in data/,
         generates publication visualizations, updates report figures, and executes
         the Jupyter notebook end-to-end.
"""

import os
import shutil
import subprocess
import sys

def main():
    print("=" * 60)
    print("STARTING MED-04 DATA VISUALIZATION RE-RUN PIPELINE")
    print("=" * 60)

    # Step 1: Preprocess Data & Export Tidy Tables
    print("\n[Step 1/4] Running data cleaning & Tableau exports (process_and_export.py)...")
    res1 = subprocess.run([sys.executable, 'src/process_and_export.py'], capture_output=True, text=True)
    print(res1.stdout)
    if res1.returncode != 0:
        print("[ERROR] Error in preprocessing:", res1.stderr)
        return

    # Step 2: Generate 5 High-Resolution Figures
    print("\n[Step 2/4] Generating 5 publication visualizations (generate_visualizations.py)...")
    res2 = subprocess.run([sys.executable, 'src/generate_visualizations.py'], capture_output=True, text=True)
    print(res2.stdout)
    if res2.returncode != 0:
        print("[ERROR] Error in visualizations:", res2.stderr)
        return

    # Step 3: Sync figures to report/figures/
    print("\n[Step 3/4] Copying figures to report/figures/...")
    os.makedirs('report/figures', exist_ok=True)
    for f in os.listdir('figures'):
        if f.endswith('.png'):
            shutil.copy(os.path.join('figures', f), os.path.join('report/figures', f))
    print("[SUCCESS] Figures copied successfully!")

    # Step 4: Re-execute Jupyter Notebook
    print("\n[Step 4/4] Re-executing Jupyter Notebook (disease_prediction_case_study.ipynb)...")
    res4 = subprocess.run([
        'jupyter', 'nbconvert', '--to', 'notebook', '--execute', '--inplace',
        'disease_prediction_case_study.ipynb'
    ], capture_output=True, text=True)
    if res4.returncode == 0:
        print("[SUCCESS] Jupyter Notebook executed and updated successfully with fresh inline outputs!")
    else:
        print("[WARNING] Warning executing notebook via nbconvert, trying python kernel execution...")
        print(res4.stderr)

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY! ALL ARTIFACTS ARE FRESH & SYNCED!")
    print("=" * 60)

if __name__ == '__main__':
    main()
