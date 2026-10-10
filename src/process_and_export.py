"""
Script: process_and_export.py
Purpose: Clean raw medical records dataset, compute derived clinical analytics metrics,
         and export structured tables for Python visualization and Tableau dashboards.
"""

import os
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# 1. Load Data
candidate_paths = [
    'data/train_disease.csv',
    'data/Training.csv',
    'data/Training_raw.csv',
    'data/train.csv',
    'Training.csv'
]
raw_train_path = None
for p in candidate_paths:
    if os.path.exists(p):
        raw_train_path = p
        break

if raw_train_path is None:
    # Look for any CSV with >100 columns in data/
    for f in os.listdir('data'):
        if f.endswith('.csv') and 'long' not in f.lower() and 'summary' not in f.lower() and 'metric' not in f.lower():
            raw_train_path = os.path.join('data', f)
            break

if raw_train_path is None:
    raise FileNotFoundError("Could not find raw training dataset in data/ folder. Please place your downloaded CSV there.")

print(f"Loading raw dataset from: {raw_train_path}")
df = pd.read_csv(raw_train_path)

# Handle possible target column name ('prognosis' or 'Disease')
if 'Disease' in df.columns and 'prognosis' not in df.columns:
    df = df.rename(columns={'Disease': 'prognosis'})

# Drop redundant/empty artifacts
if 'Unnamed: 133' in df.columns:
    df = df.drop(columns=['Unnamed: 133'])

# Resolve duplicate fluid_overload columns
if 'fluid_overload' in df.columns and 'fluid_overload.1' in df.columns:
    df = df.drop(columns=['fluid_overload'])
    df = df.rename(columns={'fluid_overload.1': 'fluid_overload'})

# Clean column headers
clean_cols = {col: col.strip().replace(' ', '_').replace('__', '_') for col in df.columns}
df = df.rename(columns=clean_cols)

# Standardize disease names
disease_name_map = {
    'Diabetes ': 'Diabetes',
    'Peptic ulcer diseae': 'Peptic Ulcer Disease',
    'Osteoarthristis': 'Osteoarthritis',
    '(vertigo) Paroymsal  Positional Vertigo': 'Paroxysmal Positional Vertigo',
    'Dimorphic hemmorhoids(piles)': 'Hemorrhoids (Piles)',
    'hepatitis A': 'Hepatitis A',
    'GERD': 'GERD',
    'AIDS': 'AIDS',
    'Urinary tract infection': 'Urinary Tract Infection'
}
df['prognosis'] = df['prognosis'].str.strip().replace(disease_name_map)

# Map clinical domains (Hospital Departments)
domain_map = {
    # Hepato-Biliary & Digestive
    'Hepatitis A': 'Hepato-Biliary & Digestive',
    'Hepatitis B': 'Hepato-Biliary & Digestive',
    'Hepatitis C': 'Hepato-Biliary & Digestive',
    'Hepatitis D': 'Hepato-Biliary & Digestive',
    'Hepatitis E': 'Hepato-Biliary & Digestive',
    'Alcoholic hepatitis': 'Hepato-Biliary & Digestive',
    'Chronic cholestasis': 'Hepato-Biliary & Digestive',
    'Jaundice': 'Hepato-Biliary & Digestive',
    'GERD': 'Hepato-Biliary & Digestive',
    'Peptic Ulcer Disease': 'Hepato-Biliary & Digestive',
    'Gastroenteritis': 'Hepato-Biliary & Digestive',
    'Hemorrhoids (Piles)': 'Hepato-Biliary & Digestive',
    
    # Infectious Diseases
    'Malaria': 'Infectious Diseases',
    'Dengue': 'Infectious Diseases',
    'Typhoid': 'Infectious Diseases',
    'Chicken pox': 'Infectious Diseases',
    'Tuberculosis': 'Infectious Diseases',
    'Common Cold': 'Infectious Diseases',
    'Pneumonia': 'Infectious Diseases',
    'AIDS': 'Infectious Diseases',
    
    # Dermatology & Allergy
    'Fungal infection': 'Dermatology & Allergy',
    'Allergy': 'Dermatology & Allergy',
    'Drug Reaction': 'Dermatology & Allergy',
    'Acne': 'Dermatology & Allergy',
    'Psoriasis': 'Dermatology & Allergy',
    'Impetigo': 'Dermatology & Allergy',
    
    # Endocrinology & Metabolism
    'Diabetes': 'Endocrinology & Metabolism',
    'Hypothyroidism': 'Endocrinology & Metabolism',
    'Hyperthyroidism': 'Endocrinology & Metabolism',
    'Hypoglycemia': 'Endocrinology & Metabolism',
    
    # Cardiovascular & Renal
    'Hypertension': 'Cardiovascular & Renal',
    'Heart attack': 'Cardiovascular & Renal',
    'Varicose veins': 'Cardiovascular & Renal',
    'Urinary Tract Infection': 'Cardiovascular & Renal',
    'Bronchial Asthma': 'Cardiovascular & Renal', # Pulmonology/Cardiopulmonary
    
    # Neurology & Musculoskeletal
    'Cervical spondylosis': 'Neurology & Musculoskeletal',
    'Paralysis (brain hemorrhage)': 'Neurology & Musculoskeletal',
    'Migraine': 'Neurology & Musculoskeletal',
    'Paroxysmal Positional Vertigo': 'Neurology & Musculoskeletal',
    'Osteoarthritis': 'Neurology & Musculoskeletal',
    'Arthritis': 'Neurology & Musculoskeletal'
}

symptom_cols = [c for c in df.columns if c != 'prognosis']

# Create copy with patient metadata
df_clean = df.copy()
df_clean.insert(0, 'patient_id', [f'PAT_{i+1:04d}' for i in range(len(df))])
df_clean.insert(2, 'clinical_domain', df_clean['prognosis'].map(domain_map))
df_clean['symptom_count'] = df_clean[symptom_cols].sum(axis=1)

# Export cleaned wide dataset
df_clean.to_csv('data/Training_Cleaned.csv', index=False)
print("Saved data/Training_Cleaned.csv (shape: {})".format(df_clean.shape))

# 2. Symptom Profile Metrics (Ubiquity, Specificity, Coverage)
total_patients = len(df_clean)
symptom_totals = df_clean[symptom_cols].sum()

disease_has_symp = (df_clean.groupby('prognosis')[symptom_cols].max() > 0)
disease_symp_count = disease_has_symp.sum(axis=0)

symptom_metrics = []
for symp in symptom_cols:
    freq = int(symptom_totals[symp])
    d_count = int(disease_symp_count[symp])
    prev_pct = round((freq / total_patients) * 100, 2)
    
    # Associated diseases list
    assoc_diseases = disease_has_symp.index[disease_has_symp[symp]].tolist()
    assoc_str = "; ".join(assoc_diseases[:3]) + (f" (+{len(assoc_diseases)-3} more)" if len(assoc_diseases) > 3 else "")
    
    # Specificity Classification
    if d_count == 1:
        spec_class = "Monospecific (Pathognomonic)"
        spec_score = 1.0
    elif d_count <= 4:
        spec_class = "High Specificity (Oligospecific)"
        spec_score = 0.75
    elif d_count <= 9:
        spec_class = "Moderate Specificity (Polyspecific)"
        spec_score = 0.40
    else:
        spec_class = "Universal Chameleon (Non-Specific)"
        spec_score = 0.10
        
    symptom_metrics.append({
        'symptom': symp,
        'patient_frequency': freq,
        'patient_prevalence_pct': prev_pct,
        'diseases_affected_count': d_count,
        'disease_breadth_pct': round((d_count / 41) * 100, 2),
        'specificity_class': spec_class,
        'specificity_score': spec_score,
        'primary_diseases': assoc_str
    })

df_symptom_metrics = pd.DataFrame(symptom_metrics)
df_symptom_metrics = df_symptom_metrics.sort_values(by='diseases_affected_count', ascending=False)
df_symptom_metrics.to_csv('data/Symptom_Profile_Metrics.csv', index=False)
print("Saved data/Symptom_Profile_Metrics.csv (count: {})".format(len(df_symptom_metrics)))

# 3. Disease Pairwise Similarity Matrix
disease_profiles = df_clean.groupby('prognosis')[symptom_cols].mean()
sim_matrix = cosine_similarity(disease_profiles)
df_sim = pd.DataFrame(sim_matrix, index=disease_profiles.index, columns=disease_profiles.index)
df_sim.to_csv('data/Disease_Similarity_Matrix.csv')
print("Saved data/Disease_Similarity_Matrix.csv (shape: {})".format(df_sim.shape))

# Pairwise Long format for Tableau heatmaps & rankings
pairwise_records = []
diseases_list = disease_profiles.index.tolist()
for i in range(len(diseases_list)):
    for j in range(i + 1, len(diseases_list)):
        d1 = diseases_list[i]
        d2 = diseases_list[j]
        score = df_sim.loc[d1, d2]
        c1 = domain_map.get(d1, 'Other')
        c2 = domain_map.get(d2, 'Other')
        pairwise_records.append({
            'disease_a': d1,
            'domain_a': c1,
            'disease_b': d2,
            'domain_b': c2,
            'same_domain': (c1 == c2),
            'cosine_similarity': round(score, 4),
            'risk_tier': 'High Ambiguity (>=0.60)' if score >= 0.60 else ('Moderate Ambiguity (0.40-0.59)' if score >= 0.40 else 'Distinct (<0.40)')
        })

df_pairwise = pd.DataFrame(pairwise_records).sort_values(by='cosine_similarity', ascending=False)
df_pairwise.to_csv('data/Disease_Pairwise_Similarity.csv', index=False)
print("Saved data/Disease_Pairwise_Similarity.csv (pairs: {})".format(len(df_pairwise)))

# 4. Disease Summary Table
disease_summary = []
for d in diseases_list:
    subset = df_clean[df_clean['prognosis'] == d]
    domain = domain_map.get(d, 'Other')
    unique_patterns = subset[symptom_cols].drop_duplicates().shape[0]
    active_symp_count = (subset[symptom_cols].max() > 0).sum()
    s_counts = subset['symptom_count']
    
    # Top similar counterpart
    sim_row = df_sim.loc[d].drop(d)
    top_counterpart = sim_row.idxmax()
    top_counterpart_score = round(sim_row.max(), 4)
    
    disease_summary.append({
        'prognosis': d,
        'clinical_domain': domain,
        'total_cases': len(subset),
        'unique_symptom_patterns': unique_patterns,
        'active_symptoms_count': int(active_symp_count),
        'mean_symptom_load': round(s_counts.mean(), 2),
        'min_symptom_load': int(s_counts.min()),
        'max_symptom_load': int(s_counts.max()),
        'std_symptom_load': round(s_counts.std(), 2),
        'most_similar_disease': top_counterpart,
        'max_similarity_score': top_counterpart_score
    })

df_disease_summary = pd.DataFrame(disease_summary).sort_values(by='mean_symptom_load', ascending=False)
df_disease_summary.to_csv('data/Disease_Summary.csv', index=False)
print("Saved data/Disease_Summary.csv (count: {})".format(len(df_disease_summary)))

# 5. Long Format for Tableau
# Melt wide matrix to long format (keeping Present == 1 records to keep file lightweight and high-performance in Tableau)
df_long_present = df_clean.melt(
    id_vars=['patient_id', 'prognosis', 'clinical_domain', 'symptom_count'],
    value_vars=symptom_cols,
    var_name='symptom',
    value_name='is_present'
)
df_long_present = df_long_present[df_long_present['is_present'] == 1].copy()

# Add symptom metadata
symp_lookup = df_symptom_metrics.set_index('symptom')
df_long_present['specificity_class'] = df_long_present['symptom'].map(symp_lookup['specificity_class'])
df_long_present['diseases_affected_count'] = df_long_present['symptom'].map(symp_lookup['diseases_affected_count'])

df_long_present.to_csv('data/Disease_Symptoms_Long.csv', index=False)
print("Saved data/Disease_Symptoms_Long.csv (active records: {})".format(len(df_long_present)))

print("\n--- ALL PREPROCESSING COMPLETED SUCCESSFULLY ---")
