# Tableau Dashboard & Storyboard Implementation Guide
## Course: 23CSE353 — Data Visualization Case Study
### Topic: MED-04 — Symptoms to Disease: Understanding Patterns in Medical Records

---

## 1. Executive Context & The Action-Target-Purpose (ATP) Pitch (2-Minute Defense)

When presenting to your faculty evaluator, deliver this exact narrative:

* **ACTION (What decision are we supporting?):**
  We provide clinical triage leadership with empirical evidence to:
  1. Transition from exhausting 131-item static intake questionnaires to a dynamic, 2-stage branching triage protocol.
  2. Implement mandatory laboratory reflex testing safety stops for disease pairs exhibiting high symptom overlap ($\ge 60\%$ cosine similarity).
  3. Audit and correct synthetic data biases before deploying diagnostic AI tools in healthcare clinics.

* **TARGET (Who is the audience?):**
  **Health Analytics Director, Hospital Operations Committee, and Emergency Department Triage Protocol Leads.**

* **PURPOSE (Why does it matter?):**
  Triage intake bottlenecks cause emergency department delays and patient survey fatigue. Concurrently, deploying automated tools without understanding symptom specificity leads to catastrophic diagnostic errors when conditions share near-identical symptoms (e.g., Viral Hepatitis or Malaria vs. Typhoid).

---

## 2. Directory Audit: The Files in Your `data/` Folder

Your `d:\College\sem5\Data Viz\case_study\data\` directory contains the raw Kaggle files you downloaded, alongside the pipeline-generated tidy tables:

| File Name in `data/` | Origin | Dimensions | Primary Role in Tableau |
| :--- | :--- | :--- | :--- |
| **`train_disease.csv`** | **Raw Kaggle Download** | 4,920 rows $\times$ 134 cols | Your primary raw dataset. Contains 132 binary symptom flags + `prognosis` + dirty trailing column `Unnamed: 133`. |
| **`test_disease.csv`** | **Raw Kaggle Download** | 42 rows $\times$ 133 cols | Independent test split provided in the Kaggle benchmark. |
| **`Training_Cleaned.csv`** | Pipeline Output | 4,920 rows $\times$ 135 cols | Cleaned wide table with `patient_id`, standardized disease names, `clinical_domain`, and row-level `symptom_count`. |
| **`Disease_Symptoms_Long.csv`** | Pipeline Output | 36,648 rows $\times$ 8 cols | **Master Long Table:** Unpivoted / melted version. Allows instant drag-and-drop filtering by `symptom` without manually managing 131 wide columns. |
| **`Symptom_Profile_Metrics.csv`** | Pipeline Output | 131 rows $\times$ 8 cols | **Used for Sheet 1 & Sheet 4:** Pre-calculated prevalence, disease breadth, and specificity classes. |
| **`Disease_Summary.csv`** | Pipeline Output | 41 rows $\times$ 11 cols | **Used for Sheet 2:** Disease-level complexity, mean/min/max symptom loads, and domain groupings. |
| **`Disease_Pairwise_Similarity.csv`** | Pipeline Output | 820 rows $\times$ 7 cols | **Used for Sheet 3:** Precomputed pairwise cosine similarities and clinical ambiguity risk tiers. |
| **`Disease_Similarity_Matrix.csv`** | Pipeline Output | 41 rows $\times$ 42 cols | 41 $\times$ 41 symmetric matrix for full correlation/overlap heatmaps. |

---

## 3. How to Connect Tableau to Your Data

### Method A: Using the Prepared Tidy Tables (Recommended & Fastest)
In Tableau, analyzing wide datasets with 131 binary columns is notoriously tedious. Connecting directly to our prepared tables allows you to build stunning sheets in seconds:
1. Open **Tableau Desktop** or **Tableau Public**.
2. On the left sidebar under **Connect** $\rightarrow$ **To a File**, click **Text file**.
3. Navigate to: `d:\College\sem5\Data Viz\case_study\data\`.
4. Select the specific CSV for each sheet as detailed below (or add multiple connections).

---

### Method B: Directly from Raw `train_disease.csv` (If Faculty Asks to See Raw Data)
If your faculty asks: *"Can you show me how you pivoted the raw Kaggle dataset directly inside Tableau?"*:
1. Connect to `data/train_disease.csv`.
2. In the Data Source preview window:
   * Click on the column header `itching`, scroll to the right, hold **Shift**, and click on the last symptom column before `prognosis`.
   * Right-click any selected column header and select **Pivot**.
   * Tableau automatically converts the 131 columns into two fields:
     * `Pivot Field Names` $\rightarrow$ Rename to **`symptom`**.
     * `Pivot Field Values` $\rightarrow$ Rename to **`is_present`**.
   * Right-click `Unnamed: 133` and select **Hide** (to drop the ghost column).
   * Filter the data source to keep only `is_present = 1`.
*(Notice that this produces the exact same structure as our pre-generated `Disease_Symptoms_Long.csv`!)*

---

## 4. Step-by-Step Worksheet Construction

### 📊 Worksheet 1: The "Chameleon" Spectrum (Symptom Ubiquity & Specificity)
* **Objective:** Answer *Which symptoms span the most diseases vs. which are unique anchors?*
* **Data Source:** Connect to `data/Symptom_Profile_Metrics.csv`.
* **Step-by-Step Setup:**
  1. Drag **`symptom`** to **Rows**.
  2. Drag **`diseases_affected_count`** to **Columns**.
  3. Sort the bars: Click the sort icon on the axis or right-click `symptom` $\rightarrow$ **Sort** $\rightarrow$ Descending by field `diseases_affected_count`.
  4. Drag **`specificity_class`** onto **Color** on the Marks card.
     * Edit Colors:
       * `Universal Chameleon (Non-Specific)` ($\ge 10$ diseases): **Red / Crimson** (`#C0392B`)
       * `Moderate Specificity (Polyspecific)`: **Amber / Orange** (`#E67E22`)
       * `High Specificity (Oligospecific)`: **Steel Blue** (`#2980B9`)
       * `Monospecific (Pathognomonic)`: **Forest Green** (`#27AE60`)
  5. Add Labels: Drag **`patient_prevalence_pct`** onto **Label**.
  6. Filter to Top Symptoms: Drag `diseases_affected_count` to **Filters** $\rightarrow$ select Top 15 (or range at least 5).
  7. Add Reference Line: Right-click the horizontal axis $\rightarrow$ **Add Reference Line** $\rightarrow$ Constant value `10` $\rightarrow$ Label: *"Universal Chameleon Threshold"*.
* **Defense Narrative ("Explain Your Choices"):**
  * *Why this graph?* Horizontal bar chart permits clear label reading without text rotation.
  * *Why this colour?* Crimson warns of high diagnostic ambiguity; Forest green identifies pathognomonic anchors.
  * *Why this aggregation?* Distinct disease count (`COUNTD(prognosis)`).
  * *What should the reader notice?* Fatigue and vomiting appear in 17 diseases each (~41.5% of conditions), while 80 symptoms are entirely unique to a single disease.

---

### 📊 Worksheet 2: Patient Symptom Burden by Clinical Domain
* **Objective:** Answer *How does patient symptom burden vary across conditions and clinical specialties?*
* **Data Source:** Connect to `data/Training_Cleaned.csv` (or `data/Disease_Summary.csv`).
* **Step-by-Step Setup:**
  1. Drag **`prognosis`** to **Rows**.
  2. Drag **`symptom_count`** to **Columns**.
  3. Right-click `prognosis` on Rows $\rightarrow$ **Sort** $\rightarrow$ Sort by Field `symptom_count` $\rightarrow$ Aggregation: **Median** (or Average), Ascending.
  4. Drag **`clinical_domain`** onto **Color** on the Marks card.
     * Colors for the 6 domains:
       * *Infectious Diseases:* Red (`#E74C3C`)
       * *Hepato-Biliary & Digestive:* Orange (`#F39C12`)
       * *Dermatology & Allergy:* Purple (`#9B59B6`)
       * *Endocrinology & Metabolism:* Green (`#2ECC71`)
       * *Cardiovascular & Renal:* Dark Slate (`#34495E`)
       * *Neurology & Musculoskeletal:* Blue (`#3498DB`)
  5. If using `Training_Cleaned.csv`: Change Marks type to **Circle**, and in the Analytics pane, drag **Box Plot** onto the view.
  6. Add Annotations:
     * Right-click near Common Cold / Tuberculosis $\rightarrow$ **Annotate** $\rightarrow$ **Point** $\rightarrow$ *"High Burden: 14 to 17 symptoms"*.
     * Right-click near Heart Attack / UTI $\rightarrow$ **Annotate** $\rightarrow$ **Point** $\rightarrow$ *"Low Burden: 4 symptoms"*.
* **Defense Narrative ("Explain Your Choices"):**
  * *Why this graph?* Boxplot / dot-distribution illustrates both central tendency and patient variations across all 41 conditions.
  * *Why this colour?* Six distinct hues represent hospital clinical specialty departments.
  * *Why this aggregation?* Row-level sum of active symptoms per patient encounter, aggregated by Mean/Median per disease.
  * *What should the reader notice?* A dramatic 4-fold disparity: Common Cold (17), TB (16), and Dengue (14) represent high-burden multi-system infections; Heart Attack, UTI, and Paralysis present with strictly 4 symptoms.

---

### 📊 Worksheet 3: Diagnostic Ambiguity & High-Risk Disease Pairs
* **Objective:** Answer *Which disease pairs share severe symptom profile similarity, creating critical misdirection risks?*
* **Data Source:** Connect to `data/Disease_Pairwise_Similarity.csv`.
* **Step-by-Step Setup:**
  1. Create a combined label: In Tableau, create a **Calculated Field** named `Disease Pair`:
     ```tableau
     [disease_a] + "  ↔  " + [disease_b]
     ```
  2. Drag **`Disease Pair`** to **Rows**.
  3. Drag **`cosine_similarity`** to **Columns**.
  4. Filter to High & Moderate Risk: Drag **`risk_tier`** to **Filters** $\rightarrow$ check `High Ambiguity (>=0.60)` and `Moderate Ambiguity (0.40-0.59)`.
  5. Sort: Sort `Disease Pair` descending by `cosine_similarity`.
  6. Color by Specialty: Drag **`same_domain`** onto **Color**:
     * `True` (Intra-domain confusion, e.g. Viral Hepatitis): **Crimson** (`#C0392B`)
     * `False` (Cross-domain confusion, e.g. Malaria vs. Typhoid): **Violet / Purple** (`#8E44AD`)
  7. Add Label: Drag `cosine_similarity` onto **Label** $\rightarrow$ Format as Percentage with 1 decimal place (`0.0%`).
  8. Add Safety Line: Add a Reference Line on the X-axis at `0.60` $\rightarrow$ Label: *"High Ambiguity Risk Cutoff (60%)"*.
* **Defense Narrative ("Explain Your Choices"):**
  * *Why this graph?* Horizontal ranked bar isolates the top dangerous confusion pairs where symptom screening alone fails.
  * *Why this colour?* Distinguishes within-specialty confusion from cross-specialty overlap.
  * *Why this aggregation?* Pairwise Cosine Similarity computed across 131-dimensional binary symptom vectors.
  * *What should the reader notice?* Hepatitis D & E have 83.0% overlap; Hepatitis D & A have 79.8%; Pneumonia & TB share 66.7%; Malaria & Typhoid share 63.6%. These pairs mandate automated laboratory reflex testing.

---

### 📊 Worksheet 4: Feature Imbalance & Pareto 80/20 Curve
* **Objective:** Answer *Where does the dataset exhibit structural feature imbalance?*
* **Data Source:** Connect to `data/Symptom_Profile_Metrics.csv`.
* **Step-by-Step Setup:**
  1. Drag **`symptom`** to **Columns**.
  2. Drag **`patient_frequency`** to **Rows**.
  3. Sort `symptom` descending by `patient_frequency`.
  4. Create Cumulative Percentage: Drag `patient_frequency` to **Rows** a second time (you now have two rows).
     * Right-click the second `patient_frequency` pill on Rows $\rightarrow$ **Quick Table Calculation** $\rightarrow$ **Running Total**.
     * Right-click it again $\rightarrow$ **Edit Table Calculation** $\rightarrow$ Check **Perform secondary calculation** $\rightarrow$ Secondary Calculation Type: **Percent of Total**.
     * Change its Marks type to **Line** (Color: Vivid Orange `#E67E22`).
     * Change the first Marks card to **Bar** (Color: Navy Slate `#34495E`).
     * Right-click the second pill on Rows $\rightarrow$ Select **Dual Axis**.
     * Right-click the right axis $\rightarrow$ Select **Synchronize Axis** (or set scale 0 to 100%).
  5. Add Reference Line: Right-click the right percentage axis $\rightarrow$ **Add Reference Line** $\rightarrow$ Constant value `80%` (or `0.80`) $\rightarrow$ Label: *"80% Pareto Cutoff"*.
* **Defense Narrative ("Explain Your Choices"):**
  * *Why this graph?* Dual-axis Pareto chart visually demonstrates the 80/20 rule of symptom prevalence.
  * *Why this colour?* Neutral navy for frequency bars; high-contrast orange for the cumulative curve.
  * *What should the reader notice?* Just 28 out of 131 symptoms account for 50% of all symptom occurrences, while the remaining symptoms form an ultra-sparse long tail.

---

## 5. Dashboard Assembly & Storyboard Architecture

### Layout Specification:
1. **Size:** Set dashboard size to **Fixed Size** $\rightarrow$ **1920 $\times$ 1080** (or Automatic).
2. **Top Banner (Header & KPIs):**
   * Text Object:
     * **Title:** Clinical Informatics & Triage Decision Dashboard
     * **Subtitle:** *Course: 23CSE353 — Data Visualization | Topic: MED-04 Symptoms to Disease*
   * 4 KPI Text Cards (Top Strip):
     * Card 1: **41** Total Clinical Conditions
     * Card 2: **131** Active Symptom Features
     * Card 3: **61.1%** Pathognomonic Anchors (80 Single-Disease Symptoms)
     * Card 4: **12** Critical Confusion Pairs ($\ge 60\%$ Overlap)
3. **Main 2 $\times$ 2 Grid Layout:**
   * **Top-Left:** Worksheet 1 (Symptom Ubiquity & Specificity Spectrum)
   * **Top-Right:** Worksheet 3 (Diagnostic Ambiguity & High-Risk Disease Pairs)
   * **Bottom-Left:** Worksheet 2 (Patient Symptom Burden by Domain)
   * **Bottom-Right:** Worksheet 4 (Feature Imbalance & Pareto 80/20 Curve)
4. **Interactive Dashboard Actions:**
   * In Tableau menu: **Dashboard** $\rightarrow$ **Actions...** $\rightarrow$ **Add Action** $\rightarrow$ **Filter**:
     * *Source Sheet:* Worksheet 2 (Domain Boxplot)
     * *Target Sheets:* Worksheet 1, Worksheet 3
     * *Run action on:* **Select**
     * *Clearing selection will:* **Show all values**
   * *Result:* Clicking on any Clinical Domain (e.g., *Hepato-Biliary*) automatically filters the dashboard to show only the symptoms and confusion pairs within that specialty!

---

## 6. Faculty Evaluation Defense Cheat Sheet

| Evaluator Question | Recommended Student Response |
| :--- | :--- |
| **"Where did you get your data and what files are in your folder?"** | "We downloaded the official Kaggle benchmark (`train_disease.csv` and `test_disease.csv`). We audited the 4,920 records and uncovered a trailing ghost column (`Unnamed: 133`) and a duplicate header bug (`fluid_overload`). To enable scalable visual analysis in Tableau without managing 131 wide columns, we developed an automated pipeline that produced clean, unpivoted tidy tables." |
| **"Why not just drag all 131 columns into Tableau directly?"** | "Wide binary datasets force manual selection of 131 measures. Unpivoting the dataset into long format (`Disease_Symptoms_Long.csv`) is the industry-standard data modeling practice for Tableau, enabling dynamic filtering by symptom, disease, and clinical specialty." |
| **"Why did you choose these specific 4 charts?"** | "Each chart answers a distinct operational question: Sheet 1 dictates triage questionnaire branching; Sheet 2 dictates consultation time allocation; Sheet 3 sets safety rails for laboratory reflex testing; and Sheet 4 audits feature imbalance and data sampling bias." |
| **"What is the single most important clinical insight from your dashboard?"** | "Symptom overlap is severe among conditions like Hepatitis D and E (83% overlap) and Malaria and Typhoid (63.6%). Symptom-only screening cannot differentiate these conditions. Our dashboard establishes an empirical threshold ($\ge 60\%$) where the triage system must enforce mandatory laboratory reflex orders rather than relying on subjective screening." |

---
*Guide prepared for Course 23CSE353 — Data Visualization Case Study.*
