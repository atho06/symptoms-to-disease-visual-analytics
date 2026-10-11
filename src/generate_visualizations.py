"""
Script: generate_visualizations.py
Purpose: Generate 5 high-resolution publication-quality visualization figures 
         answering the 5 analytical research questions for the MED-04 case study.
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Set aesthetic style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10

os.makedirs('figures', exist_ok=True)

# Load processed data
df_clean = pd.read_csv('data/Training_Cleaned.csv')
df_symptom_metrics = pd.read_csv('data/Symptom_Profile_Metrics.csv')
df_pairwise = pd.read_csv('data/Disease_Pairwise_Similarity.csv')
df_disease_summary = pd.read_csv('data/Disease_Summary.csv')
df_sim_matrix = pd.read_csv('data/Disease_Similarity_Matrix.csv', index_col=0)

# ==============================================================================
# FIGURE 1: Question 1 - Symptom Ubiquity vs Specificity Spectrum
# ==============================================================================
print("Generating Figure 1: Symptom Ubiquity vs Specificity Spectrum...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), gridspec_kw={'width_ratios': [1.8, 1.2]})

# Panel A: Top 15 Ubiquitous Chameleon Symptoms
top_15_symp = df_symptom_metrics.head(15).sort_values(by='diseases_affected_count', ascending=True)
colors = ['#c0392b' if c >= 10 else '#e67e22' if c >= 7 else '#2980b9' for c in top_15_symp['diseases_affected_count']]

bars = ax1.barh(top_15_symp['symptom'].str.replace('_', ' ').str.title(), 
                top_15_symp['diseases_affected_count'], 
                color=colors, height=0.65, edgecolor='black', linewidth=0.8)

ax1.set_xlabel('Number of Diseases Manifesting Symptom (out of 41)', labelpad=10)
ax1.set_title('A. The "Chameleon" Spectrum: Symptoms With Broadest Disease Span', pad=15)
ax1.set_xlim(0, 20)
ax1.axvline(10, color='#c0392b', linestyle='--', linewidth=1.5, alpha=0.7, label='Universal Chameleon Threshold (>=10 Diseases)')

# Data callout labels
for bar, prev in zip(bars, top_15_symp['patient_prevalence_pct']):
    width = bar.get_width()
    ax1.text(width + 0.3, bar.get_y() + bar.get_height()/2, 
             f"{int(width)} diseases ({prev}% cohort)", 
             va='center', ha='left', fontsize=9, fontweight='bold', color='#2c3e50')

ax1.legend(loc='lower right', frameon=True, facecolor='#f8f9fa')
ax1.grid(axis='x', linestyle=':', alpha=0.6)

# Panel B: Specificity Spectrum Categorical Distribution
spec_counts = df_symptom_metrics['specificity_class'].value_counts()
spec_order = ['Monospecific (Pathognomonic)', 'High Specificity (Oligospecific)', 
              'Moderate Specificity (Polyspecific)', 'Universal Chameleon (Non-Specific)']
spec_counts = spec_counts.reindex(spec_order)
donut_colors = ['#27ae60', '#2980b9', '#f39c12', '#c0392b']

wedges, texts, autotexts = ax2.pie(
    spec_counts, 
    labels=[f"{c.split(' ')[0]}\n({n} symptoms)" for c, n in zip(spec_order, spec_counts)],
    autopct='%1.1f%%',
    startangle=140,
    colors=donut_colors,
    wedgeprops=dict(width=0.45, edgecolor='black', linewidth=1.2),
    pctdistance=0.75,
    textprops={'fontsize': 9, 'fontweight': 'bold'}
)
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')

ax2.set_title('B. Diagnostic Specificity Partition (131 Symptoms)', pad=15)
# Add center circle text
ax2.text(0, 0, f"131 Total\nSymptoms\n\n61.1%\nUnique", ha='center', va='center', fontsize=11, fontweight='bold', color='#2c3e50')

plt.tight_layout()
plt.savefig('figures/fig1_symptom_ubiquity_specificity.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved figures/fig1_symptom_ubiquity_specificity.png")

# ==============================================================================
# FIGURE 2: Question 2 - Disease Complexity & Patient Symptom Burden
# ==============================================================================
print("Generating Figure 2: Disease Complexity & Patient Symptom Burden...")
fig, ax = plt.subplots(figsize=(15, 10))

# Sort diseases by median symptom burden
order = df_disease_summary.sort_values(by='mean_symptom_load', ascending=True)['prognosis'].tolist()

# Define clinical domain palette
domain_colors = {
    'Infectious Diseases': '#e74c3c',
    'Hepato-Biliary & Digestive': '#f39c12',
    'Dermatology & Allergy': '#9b59b6',
    'Endocrinology & Metabolism': '#2ecc71',
    'Cardiovascular & Renal': '#34495e',
    'Neurology & Musculoskeletal': '#3498db'
}

# Map prognosis to domain color
palette_list = [domain_colors.get(df_disease_summary.set_index('prognosis').loc[d, 'clinical_domain'], '#95a5a6') for d in order]

sns.boxplot(
    data=df_clean,
    y='prognosis',
    x='symptom_count',
    order=order,
    palette=palette_list,
    fliersize=0,
    boxprops=dict(alpha=0.8, edgecolor='black', linewidth=1),
    whiskerprops=dict(color='black', linewidth=1),
    medianprops=dict(color='yellow', linewidth=2.5),
    ax=ax
)

# Overlay strip plot for discrete patient variations
sns.stripplot(
    data=df_clean.sample(1500, random_state=42), # jittered subsample for crisp readability
    y='prognosis',
    x='symptom_count',
    order=order,
    color='black',
    alpha=0.25,
    size=3,
    jitter=0.2,
    ax=ax
)

ax.set_title('Patient Symptom Burden Distribution Across 41 Medical Conditions', pad=15)
ax.set_xlabel('Number of Co-Manifesting Symptoms (Patient Symptom Burden)', labelpad=10)
ax.set_ylabel('Clinical Prognosis (Ordered by Mean Symptom Burden)', labelpad=10)
ax.set_xlim(2, 19)

# Annotate Extreme Ends
ax.annotate('Highest Burden:\nCommon Cold (17 symp)\nTuberculosis (16 symp)\nDengue (14 symp)', 
            xy=(17, 39), xytext=(14, 30),
            arrowprops=dict(facecolor='#c0392b', shrink=0.05, width=1.5, headwidth=8),
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#fadbd8', edgecolor='#c0392b', alpha=0.9),
            fontweight='bold', fontsize=9)

ax.annotate('Lowest Burden:\nHeart Attack, UTI,\nParalysis, Gastro (4 symp)', 
            xy=(4, 1), xytext=(8, 5),
            arrowprops=dict(facecolor='#2980b9', shrink=0.05, width=1.5, headwidth=8),
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#d4e6f1', edgecolor='#2980b9', alpha=0.9),
            fontweight='bold', fontsize=9)

# Custom legend for clinical domains
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=c, edgecolor='black', label=dom) for dom, c in domain_colors.items()]
legend_elements.append(plt.Line2D([0], [0], color='yellow', lw=3, label='Median Load'))
ax.legend(handles=legend_elements, loc='lower right', frameon=True, facecolor='#ffffff', title='Clinical Specialty Domain')

plt.tight_layout()
plt.savefig('figures/fig2_disease_complexity_burden.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved figures/fig2_disease_complexity_burden.png")

# ==============================================================================
# FIGURE 3: Question 3 - Disease Pairwise Similarity & Diagnostic Ambiguity
# ==============================================================================
print("Generating Figure 3: Disease Pairwise Similarity & Ambiguity...")
fig = plt.figure(figsize=(18, 9))
gs = fig.add_gridspec(1, 2, width_ratios=[1.3, 1.0])

# Panel A: Clustered Heatmap
ax_heat = fig.add_subplot(gs[0])
# Reorder correlation matrix by hierarchical clustering
from scipy.cluster.hierarchy import linkage, leaves_list
from scipy.spatial.distance import pdist

dist_condensed = pdist(df_sim_matrix.values, metric='euclidean')
linkage_mat = linkage(dist_condensed, method='ward')
order_idx = leaves_list(linkage_mat)
ordered_diseases = [df_sim_matrix.index[i] for i in order_idx]
clustered_sim = df_sim_matrix.loc[ordered_diseases, ordered_diseases]

sns.heatmap(
    clustered_sim,
    cmap='YlOrRd',
    vmin=0.0,
    vmax=0.85,
    cbar_kws={'label': 'Cosine Similarity (Symptom Overlap)'},
    xticklabels=False, # cleaner view for 41 labels
    yticklabels=True,
    ax=ax_heat
)
ax_heat.set_title('A. Clustered Disease Symptom Overlap Topology (41x41)', pad=15)
ax_heat.set_ylabel('Condition (Hierarchically Clustered)')

# Panel B: Top 12 High-Risk Diagnostic Confusion Pairs
ax_bar = fig.add_subplot(gs[1])
top_pairs = df_pairwise.head(12).sort_values(by='cosine_similarity', ascending=True)

pair_labels = [f"{r['disease_a']}  ↔  {r['disease_b']}" for _, r in top_pairs.iterrows()]

# Color by clinical domain (both domains represent intra-domain specialty confusion)
domain_pair_colors = {
    'Hepato-Biliary & Digestive': '#c0392b',
    'Infectious Diseases': '#2980b9'
}
pair_colors = [domain_pair_colors.get(r['domain_a'], '#7f8c8d') for _, r in top_pairs.iterrows()]

bars = ax_bar.barh(pair_labels, top_pairs['cosine_similarity'], color=pair_colors, height=0.6, edgecolor='black', linewidth=0.8)
ax_bar.set_xlim(0, 1.15)
ax_bar.set_ylim(-2.2, 11.8)
ax_bar.set_xlabel('Cosine Similarity Score', labelpad=10)
ax_bar.set_title('B. Top 12 Clinically Ambiguous Disease Pairs (High Triage Misdirection Risk)', pad=15)
ax_bar.axvline(0.60, color='#e74c3c', linestyle='--', linewidth=1.5, label='High Ambiguity Threshold (>= 0.60)')

for bar in bars:
    w = bar.get_width()
    ax_bar.text(w + 0.02, bar.get_y() + bar.get_height()/2, f"{w*100:.1f}%", va='center', ha='left', fontsize=9, fontweight='bold', color='#2c3e50')

legend_handles = [
    Patch(facecolor='#c0392b', edgecolor='black', label='Hepato-Biliary Ambiguity (Hepatitis variants, Jaundice)'),
    Patch(facecolor='#2980b9', edgecolor='black', label='Infectious Diseases Ambiguity (Pneumonia ↔ TB, Malaria ↔ Typhoid)'),
    plt.Line2D([0], [0], color='#e74c3c', linestyle='--', lw=1.5, label='High Ambiguity Threshold (0.60)')
]
# Positioned at lower right within expanded y-limits so no bars or labels are covered
ax_bar.legend(handles=legend_handles, loc='lower right', frameon=True, facecolor='#f8f9fa', fontsize=8.5)

plt.tight_layout()
plt.savefig('figures/fig3_disease_similarity_confusion.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved figures/fig3_disease_similarity_confusion.png")

# ==============================================================================
# FIGURE 4: Question 4 - Dataset Structural Imbalance & Synthetic Artifacts
# ==============================================================================
print("Generating Figure 4: Dataset Imbalance & Pareto Distribution...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Panel A: Disease Cohort Distribution (Uniform Synthetic Balance)
disease_counts = df_clean['prognosis'].value_counts()
ax1.bar(range(len(disease_counts)), disease_counts.values, color='#3498db', edgecolor='black', alpha=0.85, width=0.8)
ax1.set_title('A. Perfectly Uniform Disease Representation (Synthetic Balance)', pad=15)
ax1.set_xlabel('41 Distinct Clinical Conditions (Ranked)', labelpad=10)
ax1.set_ylabel('Number of Patient Records', labelpad=10)
ax1.set_ylim(0, 160)
ax1.axhline(120, color='#e74c3c', linestyle='--', linewidth=2, label='Fixed Quota: 120 Cases per Disease')
ax1.text(20, 130, 'Synthetic Artifact: Exactly 120 records per disease\n(Real-world epidemiology is heavily non-uniform)', 
         ha='center', va='center', bbox=dict(boxstyle='round', facecolor='#fadbd8', edgecolor='#e74c3c'), fontweight='bold', fontsize=9)
ax1.legend(loc='lower right', frameon=True)

# Panel B: Symptom Long-Tail Pareto Distribution
symp_freq_sorted = df_symptom_metrics.sort_values(by='patient_frequency', ascending=False).reset_index(drop=True)
total_mentions = symp_freq_sorted['patient_frequency'].sum()
symp_freq_sorted['cum_pct'] = (symp_freq_sorted['patient_frequency'].cumsum() / total_mentions) * 100

ax2_twin = ax2.twinx()
# Bar plot for frequency
ax2.bar(range(len(symp_freq_sorted)), symp_freq_sorted['patient_frequency'], color='#34495e', width=1.0, alpha=0.7, label='Symptom Occurrences')
# Line plot for cumulative %
ax2_twin.plot(range(len(symp_freq_sorted)), symp_freq_sorted['cum_pct'], color='#e67e22', linewidth=2.5, label='Cumulative Prevalence (%)')
ax2_twin.axhline(80, color='#e74c3c', linestyle=':', linewidth=1.5, label='80% Pareto Cutoff')
ax2_twin.axhline(50, color='#2980b9', linestyle=':', linewidth=1.2, alpha=0.7)

# Exact threshold counts (1-indexed count: index + 1)
idx_50 = (symp_freq_sorted['cum_pct'] >= 50).idxmax() + 1   # 20 symptoms
idx_80 = (symp_freq_sorted['cum_pct'] >= 80).idxmax() + 1   # 66 symptoms
ax2.axvline(idx_80, color='#e74c3c', linestyle='--', linewidth=1.5)
ax2.axvline(idx_50, color='#2980b9', linestyle='--', linewidth=1.2, alpha=0.7)

ax2.set_title('B. Symptom Long-Tail & Pareto Inequity (Heavily Imbalanced Features)', pad=15)
ax2.set_xlabel('131 Symptom Features (Ranked by Occurrence)', labelpad=10)
ax2.set_ylabel('Total Patient Occurrences in Cohort', labelpad=10)
ax2_twin.set_ylabel('Cumulative Percentage (%)', labelpad=10, color='#e67e22')
ax2_twin.set_ylim(0, 105)

ax2.text(idx_80 + 4, 1150, 
         f'Pareto Principle in Action:\n• Top {idx_50} symptoms (15.3%) account for 50.7% of all mentions\n• Top {idx_80} symptoms (50.4%) account for 80.0% of all mentions\n• Remaining {131-idx_80} symptoms form the sparse tail (20.0%)',
         bbox=dict(boxstyle='round', facecolor='#fef9e7', edgecolor='#f39c12'), fontweight='bold', fontsize=8.5)

# Reconciled data audit callout pointing to the true sparse tail
ax2.annotate('Data Audit Reconciliation:\nRaw "fluid_overload" had 0 mentions\n(due to duplicate header bug);\nreconciled to 114 cases during audit.',
             xy=(118, 114), xytext=(72, 450),
             arrowprops=dict(facecolor='#c0392b', shrink=0.05, width=1.5, headwidth=7),
             bbox=dict(boxstyle='round', facecolor='#fadbd8', edgecolor='#c0392b'), fontweight='bold', fontsize=8)

lines1, labels1 = ax2.get_legend_handles_labels()
lines2, labels2 = ax2_twin.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, loc='center right', frameon=True, facecolor='#ffffff', fontsize=8.5)

plt.tight_layout()
plt.savefig('figures/fig4_dataset_imbalance_pareto.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved figures/fig4_dataset_imbalance_pareto.png")

# ==============================================================================
# FIGURE 5: Question 5 - Symptom Co-occurrence & Syndromic Clusters
# ==============================================================================
print("Generating Figure 5: Symptom Co-occurrence & Syndromic Clusters...")
# Select top 22 most prevalent symptoms to inspect interaction patterns
top_symps = df_symptom_metrics.head(22)['symptom'].tolist()

corr_matrix = df_clean[top_symps].corr()
corr_matrix.columns = [c.replace('_', ' ').title() for c in top_symps]
corr_matrix.index = [c.replace('_', ' ').title() for c in top_symps]

fig, ax = plt.subplots(figsize=(13, 11))

# Mask the upper triangle for clean visual inspection
mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)

sns.heatmap(
    corr_matrix,
    mask=mask,
    cmap='icefire',
    center=0,
    vmin=-0.25,
    vmax=0.85,
    annot=True,
    fmt='.2f',
    annot_kws={'size': 7.5, 'weight': 'bold'},
    cbar_kws={'label': 'Pearson Correlation (Co-occurrence Coupling)', 'shrink': 0.8},
    linewidths=0.5,
    linecolor='white',
    ax=ax
)

ax.set_title('Co-occurrence Matrix of Top 22 Clinical Symptoms: Identifying Syndrome Archetypes', pad=15)

# Annotate syndrome blocks
ax.text(12, 5, 'Hepato-Biliary Syndrome:\nYellowish Skin + Yellow Eyes +\nAbdominal Pain + Dark Urine\n(r = 0.53 to 0.73)',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#fef9e7', edgecolor='#f39c12'), fontsize=9, fontweight='bold')

ax.text(15, 15, 'Systemic Febrile Syndrome:\nHigh Fever + Chills +\nHeadache + Malaise\n(r = 0.24 to 0.54)',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#fadbd8', edgecolor='#c0392b'), fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('figures/fig5_symptom_cooccurrence_clusters.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved figures/fig5_symptom_cooccurrence_clusters.png")

print("\n--- ALL 5 FIGURES GENERATED IN HIGHEST QUALITY ---")
