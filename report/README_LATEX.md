# How to Compile the LaTeX Case Study Report

This directory contains the complete, publication-grade academic report formatted according to institutional requirements for **23CSE353 - Data Visualization**.

---

## Files in this Directory:
* `case_study_report.tex` — Main LaTeX document.
* `references.bib` — BibTeX bibliography citations.
* `figures/` — High-resolution (300 DPI) figures embedded in the report:
  * `fig1_symptom_ubiquity_specificity.png`
  * `fig2_disease_complexity_burden.png`
  * `fig3_disease_similarity_confusion.png`
  * `fig4_dataset_imbalance_pareto.png`
  * `fig5_symptom_cooccurrence_clusters.png`
* `CASE_STUDY_REPORT.md` — Complete rendered Markdown version of the report for instant offline reading.

---

## 1-Minute Compilation on Overleaf (Recommended):
1. Open [Overleaf.com](https://www.overleaf.com) and log in.
2. Click **New Project** $\rightarrow$ **Upload Project**.
3. Upload this entire `report/` folder (or zip the `report/` folder and upload it).
4. Set compiler to **pdfLaTeX** (default).
5. Click **Recompile** — your PDF report will generate instantly with all embedded figures, tables, and formatted citations!

---

## Local Compilation via TeX Live / MiKTeX / VS Code:
If you have LaTeX installed locally:
```bash
pdflatex case_study_report.tex
bibtex case_study_report
pdflatex case_study_report.tex
pdflatex case_study_report.tex
```
