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

Your `d:\College\sem5\Data Viz\case_study\data\` directory contains your downloaded Kaggle files and the pipeline-generated tidy tables:

| File Name in `data/` | Origin | Dimensions | Primary Role in Tableau |
| :--- | :--- | :--- | :--- |
| **`train_disease.csv`** | **Raw Kaggle Download** | 4,920 rows $\times$ 134 cols | Your primary raw dataset (132 symptom flags + `prognosis` + `Unnamed: 133`). |
| **`test_disease.csv`** | **Raw Kaggle Download** | 42 rows $\times$ 133 cols | Independent test split provided in the Kaggle benchmark. |
| **`Training_Cleaned.csv`** | Pipeline Output | 4,920 rows $\times$ 135 cols | Cleaned wide table with `patient_id`, standardized disease names, `clinical_domain`, and `symptom_count`. |
| **`Disease_Symptoms_Long.csv`** | Pipeline Output | 36,648 rows $\times$ 8 cols | Master unpivoted long format (used for multi-filter general exploration). |
| **`Symptom_Profile_Metrics.csv`** | Pipeline Output | 131 rows $\times$ 8 cols | **Used for Sheet 1 & Sheet 4:** Pre-calculated prevalence, ubiquity, and specificity classes. |
| **`Disease_Summary.csv`** | Pipeline Output | 41 rows $\times$ 11 cols | **Used for Sheet 2:** Disease-level complexity, active symptom counts, and clinical domain mappings. |
| **`Disease_Pairwise_Similarity.csv`** | Pipeline Output | 820 rows $\times$ 7 cols | **Used for Sheet 3:** Precomputed pairwise cosine similarities and clinical ambiguity risk tiers. |
| **`Disease_Similarity_Matrix.csv`** | Pipeline Output | 41 rows $\times$ 42 cols | 41 $\times$ 41 symmetric matrix for full correlation/overlap heatmaps. |

---

## 3. Ultra-Detailed Step-by-Step Worksheet Construction

---

### 📊 Worksheet 1: The "Chameleon" Spectrum (Symptom Ubiquity & Specificity)

* **Objective:** Answer *Which symptoms span the most diseases (chameleons) vs. which are unique anchors?*
* **Active Data Source:** Click on **`Symptom_Profile_Metrics`** in the top-left Data pane.

#### Exact Click-by-Click Steps:
1. **Put Symptoms on Rows:**
   * In the left sidebar under Tables, click **`symptom`** and drag it onto the **Rows** shelf at the top.
2. **Put Disease Count on Columns:**
   * From the left sidebar, click **`diseases_affected_count`** and drag it onto the **Columns** shelf.
3. **Sort Descending:**
   * Look at the top toolbar (just under the main menu). Click the **Sort Descending** button (an icon with horizontal bars and an arrow pointing down from longest to shortest).
   * *(Alternatively: Right-click `symptom` on Rows $\rightarrow$ **Sort** $\rightarrow$ Sort By: **Field** $\rightarrow$ Field Name: `diseases_affected_count` $\rightarrow$ Sort Order: **Descending** $\rightarrow$ close popup).*
4. **Color by Specificity:**
   * Drag **`specificity_class`** from the left sidebar onto **Color** on the Marks card.
   * *To set the colors:* Click **Color** on the Marks card $\rightarrow$ click **Edit Colors...**:
     * `Universal Chameleon (Non-Specific)` $\rightarrow$ Red / Crimson
     * `Moderate Specificity (Polyspecific)` $\rightarrow$ Orange / Amber
     * `High Specificity (Oligospecific)` $\rightarrow$ Blue
     * `Monospecific (Pathognomonic)` $\rightarrow$ Forest Green
     * Click **OK**.
5. **Add Prevalence Labels:**
   * Drag **`patient_prevalence_pct`** from the left sidebar onto **Label** on the Marks card so each bar displays its percentage.
6. **Filter to Top 15 Symptoms:**
   * Drag **`symptom`** from the left sidebar onto the **Filters** shelf.
   * In the popup dialog, click on the **Top** tab at the top.
   * Select **By field** $\rightarrow$ leave it on **Top** $\rightarrow$ type **`15`** $\rightarrow$ choose by **`diseases_affected_count`** $\rightarrow$ **Sum**.
   * Click **OK**.
7. **Add the Chameleon Cutoff Line at 10:**
   * In the top-left corner (next to the word *Data*), click the **`Analytics`** tab.
   * Under "Custom", click and drag **Constant Line** onto your chart $\rightarrow$ drop it on **Table $\rightarrow$ SUM(diseases_affected_count)**.
   * A small box appears on the bottom axis: type **`10`** and hit **Enter**!
   * Right-click the line $\rightarrow$ **Edit...** $\rightarrow$ Next to **Label**, select **Custom** $\rightarrow$ type `Universal Chameleon Cutoff (10)` $\rightarrow$ click **OK**.
8. **Rename the Tab:** Double-click the tab at the bottom and name it `Sheet 1 - Chameleon Spectrum`.

---

### 📊 Worksheet 2: Patient Symptom Burden by Clinical Domain

* **Objective:** Answer *How does patient symptom burden vary across conditions and clinical specialties?*
* **Active Data Source:** Click on **`Disease_Summary`** in the top-left Data pane.

#### Exact Click-by-Click Steps:
1. **Put Diseases on Rows:**
   * Drag **`Prognosis`** from the left sidebar onto the **Rows** shelf.
2. **Put Symptom Count on Columns:**
   * Drag **`Active Symptoms Count`** from the left sidebar onto the **Columns** shelf.
   * *(Note: If `CNT(Disease_Summary)` is already on Columns, drag it off into blank space to delete it).*
3. **Sort the Bars:**
   * In the top toolbar, click the **Sort Ascending** button (icon with bars getting longer from top to bottom) so the shortest bars are at the top and the longest at the bottom.
4. **Color by Clinical Domain:**
   * Drag **`Clinical Domain`** from the left sidebar onto **Color** on the Marks card.
   * *Domain colors:*
     * Infectious Diseases: Red (`#E74C3C`)
     * Hepato-Biliary & Digestive: Orange (`#F39C12`)
     * Dermatology & Allergy: Purple (`#9B59B6`)
     * Endocrinology & Metabolism: Green (`#2ECC71`)
     * Cardiovascular & Renal: Dark Slate (`#34495E`)
     * Neurology & Musculoskeletal: Blue (`#3498DB`)
5. **Add Numbers on the Bars:**
   * Drag **`Active Symptoms Count`** from the left sidebar onto **Label** on the Marks card.
6. **Rename the Tab:** Double-click the tab at the bottom and name it `Sheet 2 - Symptom Burden`.

---

### 📊 Worksheet 3: Diagnostic Ambiguity & High-Risk Disease Pairs

* **Objective:** Answer *Which disease pairs share severe symptom profile similarity ($\ge 60\%$), creating triage misdirection risks?*
* **Active Data Source:** Click on **`Disease_Pairwise_Similarity`** in the top-left Data pane.

#### Exact Click-by-Click Steps:
1. **Create the Combined Disease Pair Field:**
   * Right-click any blank space in the left Data sidebar $\rightarrow$ click **Create Calculated Field...**
   * In the title box at the top, name it: `Disease Pair`
   * In the formula box, type:
     ```tableau
     [disease_a] + "  ↔  " + [disease_b]
     ```
     *(Type only the text above — do NOT include backticks or markdown code fences).*
   * Make sure it says **"The calculation is valid"** at the bottom left $\rightarrow$ click **OK**.
2. **Put Disease Pair on Rows:**
   * Drag **`Disease Pair`** from the left sidebar onto the **Rows** shelf.
3. **Put Similarity on Columns:**
   * Drag **`cosine_similarity`** from the left sidebar onto the **Columns** shelf.
4. **Filter to High and Moderate Ambiguity:**
   * Drag **`risk_tier`** from the left sidebar onto the **Filters** shelf.
   * In the checkbox popup that opens, check **both**:
     * `High Ambiguity (>=0.60)`
     * `Moderate Ambiguity (0.40-0.59)`
   * Click **OK**.
5. **Sort Descending:**
   * Click the **Sort Descending** button on the top toolbar (so the highest similarity pairs like Hepatitis D ↔ E are at the very top).
6. **Color by Within-Specialty vs. Cross-Specialty:**
   * Drag **`same_domain`** from the left sidebar onto **Color** on the Marks card.
   * Click **Color** on the Marks card $\rightarrow$ **Edit Colors...**:
     * `True` (Confusion within the same department, e.g. Viral Hepatitis): **Crimson / Red**
     * `False` (Confusion across different departments, e.g. Malaria ↔ Typhoid): **Purple / Violet**
     * Click **OK**.
7. **Add Percentage Labels:**
   * Drag **`cosine_similarity`** from the left sidebar onto **Label** on the Marks card.
   * *To format it as a percentage (e.g. 83.0%):*
     * Right-click the `SUM(cosine_similarity)` pill on the Marks card (the one with the small `T` icon next to it) $\rightarrow$ click **Format...**
     * On the left pane under "Default", click the **Numbers** dropdown $\rightarrow$ choose **Percentage** $\rightarrow$ set Decimal places to `1`.
8. **Add the 60% Safety Threshold Line:**
   * Click the **`Analytics`** tab at the top-left (next to *Data*).
   * Under "Custom", drag **Constant Line** onto your chart $\rightarrow$ drop it on **Table $\rightarrow$ SUM(cosine_similarity)**.
   * A small yellow box appears on the bottom axis: type **`0.6`** and press **Enter**!
   * Right-click that line on your chart $\rightarrow$ click **Edit...**
   * Next to **Label**, choose **Custom** from the dropdown $\rightarrow$ in the text box type:  
     `High Ambiguity Risk Cutoff (60%)`
   * Click **OK**.
9. **Rename the Tab:** Double-click the tab at the bottom and name it `Sheet 3 - Ambiguity Pairs`.

---

### 📊 Worksheet 4: Feature Imbalance & Pareto 80/20 Curve

* **Objective:** Answer *Where does the dataset exhibit structural feature imbalance (the Pareto 80/20 rule)?*
* **Active Data Source:** Click the **New Worksheet** icon at the bottom. In the top-left Data pane, click **`Symptom_Profile_Metrics`**.

#### Exact Click-by-Click Steps:
1. **Put Symptoms on Columns:**
   * Drag **`symptom`** from the left sidebar onto the **Columns** shelf.
2. **Put Frequency on Rows:**
   * Drag **`patient_frequency`** from the left sidebar onto the **Rows** shelf.
3. **Sort Descending:**
   * Click the **Sort Descending** button on the top toolbar (so the highest frequency symptoms like fatigue and vomiting are on the left).
4. **Create the Second Measure (Cumulative Percentage Line):**
   * Drag **`patient_frequency`** from the left sidebar onto the **Rows** shelf a **SECOND** time (you will now see two green `SUM(patient_frequency)` pills on Rows).
   * Right-click the **second** `SUM(patient_frequency)` pill on Rows $\rightarrow$ hover over **Quick Table Calculation** $\rightarrow$ click **Running Total**.
   * Right-click that **same second pill** again $\rightarrow$ click **Edit Table Calculation...**:
     * In the popup, check the box that says **Perform secondary calculation**.
     * Next to **Secondary Calculation Type**, select **Percent of Total**.
     * Close the popup window (click `X`).
5. **Combine into a Dual Axis:**
   * Right-click that second pill on Rows $\rightarrow$ click **Dual Axis**.
   * Notice that your chart now has two axes: Left axis has counts (0 to 2000), right axis has percentages (0% to 100%).
6. **Assign Chart Types (Marks Card):**
   * Look at the Marks card area. You will see three tabs: `All`, `SUM(patient_frequency)`, and `SUM(patient_frequency) (2)`.
   * Click on the **`SUM(patient_frequency)`** tab $\rightarrow$ change the dropdown from Automatic to **Bar** $\rightarrow$ click **Color** and select Dark Slate / Navy Blue.
   * Click on the **`SUM(patient_frequency) (2)`** tab $\rightarrow$ change the dropdown from Automatic to **Line** $\rightarrow$ click **Color** and select Vivid Orange (`#E67E22`).
7. **Add the 80% Pareto Reference Line:**
   * Click the **`Analytics`** tab at the top-left (next to *Data*).
   * Drag **Constant Line** onto your chart $\rightarrow$ drop it on the **right-hand percentage axis** (`SUM(patient_frequency) (2)`).
   * In the small box, type **`0.8`** (or `80%`) and hit **Enter**!
   * Right-click the line $\rightarrow$ **Edit...** $\rightarrow$ Label: **Custom** $\rightarrow$ type `80% Pareto Cutoff` $\rightarrow$ click **OK**.
8. **Rename the Tab:** Double-click the tab at the bottom and name it `Sheet 4 - Pareto Imbalance`.

---

## 4. Dashboard Assembly & Interactivity (Putting It All Together)

### Exact Click-by-Click Steps:
1. **Create New Dashboard:**
   * At the bottom of your screen, click the **New Dashboard** icon (the small grid icon with a plus sign next to the new worksheet icon).
2. **Set Dashboard Size:**
   * In the left pane under **Size**, click the dropdown (currently *Fixed size*) $\rightarrow$ choose **Generic Desktop (1366 $\times$ 768)** or set to **Automatic**.
3. **Show Title:**
   * At the bottom of the left pane, check the box: **Show dashboard title**.
   * Double-click the title box at the top of your dashboard $\rightarrow$ type:
     ```text
     Clinical Informatics & Triage Decision Dashboard
     Course: 23CSE353 — Data Visualization | Topic: MED-04 Symptoms to Disease
     ```
   * Click **OK**.
4. **Arrange the 4 Sheets in a 2 $\times$ 2 Grid:**
   * From the left pane under Sheets:
     * Drag **`Sheet 1 - Chameleon Spectrum`** into the top-left area.
     * Drag **`Sheet 3 - Ambiguity Pairs`** to the top-right area (next to Sheet 1).
     * Drag **`Sheet 2 - Symptom Burden`** to the bottom-left area.
     * Drag **`Sheet 4 - Pareto Imbalance`** to the bottom-right area.
5. **Add 1-Click Interactivity ("Use as Filter"):**
   * Click on **`Sheet 2 - Symptom Burden`** on your dashboard so its gray outline appears.
   * Look at the small toolbar in the top-right corner of Sheet 2's border. Click the small **Funnel icon ("Use as Filter")**.
   * *Test it:* Click on any bar in Sheet 2 (for example, *Hepatitis D* or *Malaria*) $\rightarrow$ notice how Sheet 1 and Sheet 3 automatically filter to highlight only the symptoms and confusion pairs for that condition!
   * Click the bar again to unselect.

---

## 5. Defense Cheat Sheet: Answering Faculty Questions

| Evaluator Question | Recommended Student Response |
| :--- | :--- |
| **"Where did you get your data and what files are in your folder?"** | "We downloaded the official Kaggle benchmark (`train_disease.csv` and `test_disease.csv`). We audited the 4,920 records and uncovered a trailing ghost column (`Unnamed: 133`) and a duplicate header bug (`fluid_overload`). To enable scalable visual analysis in Tableau without managing 131 wide columns, we developed an automated pipeline that produced clean, unpivoted tidy tables." |
| **"Why not just drag all 131 columns into Tableau directly?"** | "Wide binary datasets force manual selection of 131 measures. Unpivoting the dataset into long format (`Disease_Symptoms_Long.csv`) is the industry-standard data modeling practice for Tableau, enabling dynamic filtering by symptom, disease, and clinical specialty." |
| **"Why did you choose these specific 4 charts?"** | "Each chart answers a distinct operational question: Sheet 1 dictates triage questionnaire branching; Sheet 2 dictates consultation time allocation; Sheet 3 sets safety rails for laboratory reflex testing; and Sheet 4 audits feature imbalance and data sampling bias." |
| **"What is the single most important clinical insight from your dashboard?"** | "Symptom overlap is severe among conditions like Hepatitis D and E (83% overlap) and Malaria and Typhoid (63.6%). Symptom-only screening cannot differentiate these conditions. Our dashboard establishes an empirical threshold ($\ge 60\%$) where the triage system must enforce mandatory laboratory reflex orders rather than relying on subjective screening." |

---
*Guide prepared for Course 23CSE353 — Data Visualization Case Study.*
