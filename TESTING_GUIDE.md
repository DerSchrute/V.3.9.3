# AQUACAST — Usability & Performance Testing Protocol
**System Verification, User Acceptance Testing (UAT), and Development Alignment Guide**

---

## Document Control & Metadata

| Field | Detail |
| :--- | :--- |
| **System Name** | AQUACAST (Water Intelligence & Forecasting Decision-Support System) |
| **Document Type** | User Acceptance Testing (UAT) & Performance Evaluation Protocol |
| **Document Version** | 1.0 (Corresponds to AQUACAST v3.9.6) |
| **Effective Date** | November 2026 |
| **Target Audience** | System Testers, Municipal Water Officers, Academic Reviewers, QA Evaluators |
| **Evaluation Scope** | UI/UX Usability, Dark Mode Consistency, Multi-Year Forecasting (2021–2026), Anomaly Workflow, and Tariff Reporting |

### Tester Information (To be filled by Evaluator)
* **Tester Name:** __________________________________________________
* **Organization / Role:** ___________________________________________
* **Date of Testing:** ____________________ | **Time:** ______________
* **Browser & OS:** _________________________________________________
* **Display Resolution / Device:** ___________________________________

---

## Table of Contents
1. [Testing Objectives & Guidelines](#1-testing-objectives--guidelines)
2. [Test Environment & Credentials](#2-test-environment--credentials)
3. [Module 1: Authentication & Access Control](#module-1-authentication--access-control)
4. [Module 2: Typography, Visual Appeal & Dark Mode](#module-2-typography-visual-appeal--dark-mode)
5. [Module 3: Executive Dashboard & Monitoring](#module-3-executive-dashboard--monitoring)
6. [Module 4: Consumption Records Explorer & Filtering (2021–2026)](#module-4-consumption-records-explorer--filtering-20212026)
7. [Module 5: Drag-and-Drop CSV Import & Dataset History](#module-5-drag-and-drop-csv-import--dataset-history)
8. [Module 6: Forecasting Workspace & Plain-Language Guide](#module-6-forecasting-workspace--plain-language-guide)
9. [Module 7: Model Evaluation Sandbox & Accuracy Dashboard](#module-7-model-evaluation-sandbox--accuracy-dashboard)
10. [Module 8: Anomaly Monitoring & Investigation Thread](#module-8-anomaly-monitoring--investigation-thread)
11. [Module 9: Utility Tariff Settings & Budget Reporting](#module-9-utility-tariff-settings--budget-reporting)
12. [Module 10: Administrative Communications Suite](#module-10-administrative-communications-suite)
13. [Standardized Usability Scorecard (SUS)](#standardized-usability-scorecard-sus)
14. [Qualitative Feedback & Final Sign-Off](#qualitative-feedback--final-sign-off)

---

## 1. Testing Objectives & Guidelines

### Primary Objectives
1. **Verify Functional Readiness:** Ensure every navigation route, filter, calculation, and model evaluation executes accurately without console errors.
2. **Evaluate Usability & Visual Appeal:** Confirm that font sizing hierarchy, contrast, section titles, and Dark Mode provide an intuitive and comfortable operational experience.
3. **Assess Decision-Support Value:** Determine whether plain-language forecasts, anomaly investigation threads, and budget reports correlate with real-world public administration workflows.
4. **Validate Multi-Year Integrity:** Test responsiveness and stability across the 6-year ($72$-month, $4,464$-record) synthetic dataset spanning 2021 through 2026.

### Evaluator Instructions
* Complete each test case sequentially.
* Record whether the observed behavior matches the **Expected Result** ([X] Pass / [ ] Fail).
* Provide constructive notes if any layout, formatting, or performance unexpected behavior occurs.

---

## 2. Test Environment & Credentials

Serve the application locally (`http://localhost:8000`) or open in a modern browser. Ensure JavaScript is enabled.

| Role | Username | Demo Password | Scope / Permissions |
| :--- | :--- | :--- | :--- |
| **System Administrator** | `admin` | `admin123` | Unrestricted provincial view, Tariff configuration, Model Evaluation sandbox, Notification broadcast composer, CSV import/restore. |
| **Station User (Negros Occ.)** | `bagocity` | `station123` | Scoped strictly to Bago City (`NO-01`), Station Forecast Guide, Contact Administration channel. |
| **Station User (Negros Or.)** | `dumaguetecity` | `station123` | Scoped strictly to Dumaguete City (`NOR-10`), Station Forecast Guide, anomaly correspondence. |
| **Station User (Siquijor)** | `enriquevillanueva`| `station123` | Scoped strictly to Enrique Villanueva (`SIQ-01`). |

---

## Module 1: Authentication & Access Control

### Test Case `TC-AUTH-01`: Role-Based Sign-In & Workspace Isolation
* **Objective:** Verify role-specific page views and security messaging.
* **Steps:**
  1. Navigate to the login screen.
  2. Sign in as `bagocity` with password `station123`.
  3. Observe sidebar navigation items, topbar station indicator, and available pages.
  4. Sign out via Account menu and sign in as `admin` with `admin123`.
* **Expected Result:**
  * Demonstrates client-side prototype authentication disclaimer.
  * Station user sees **Dashboard**, **Records**, **Forecast**, **Anomalies**, **Reports**, and **Contact administration** (admin-only tools are hidden).
  * Administrator sees all management sections, admin tabs, and notification action button.
* **Evaluation:**
  * Status: `[ ] Pass  [ ] Fail`
  * Rating (1–5): `____` | Notes: `________________________________________________`

---

## Module 2: Typography, Visual Appeal & Dark Mode

### Test Case `TC-UI-01`: Section Headings & Visual Hierarchy
* **Objective:** Ensure page titles, topbar labels, and eyebrows are visually prominent and balanced.
* **Steps:**
  1. Navigate to **Forecasting**, **Dashboard**, and **Consumption records**.
  2. Inspect the topbar title (e.g., *Forecasting*), the main `h1` heading (e.g., *Forecasting workspace*), and the eyebrow badge (e.g., `PREDICTIVE ANALYTICS`).
* **Expected Result:**
  * Topbar active section title is bold, crisp ($22\text{px}$), and serves as an unambiguous location indicator.
  * Page `h1` titles are large ($32\text{px} - 44\text{px}$), elegant, and rendered in modern system typography.
  * Eyebrows render as clean teal pill badges with uppercase tracking.
* **Evaluation:**
  * Status: `[ ] Pass  [ ] Fail`
  * Rating (1–5): `____` | Notes: `________________________________________________`

### Test Case `TC-UI-02`: Dark Mode Toggle & Comprehensive Element Styling
* **Objective:** Verify seamless dark mode switching and total readability.
* **Steps:**
  1. Click the 🌙 icon in the topbar (or select *Dark mode* under Appearance in Account menu).
  2. Inspect text, metric numbers, cards, table rows, dropdowns, and buttons.
  3. Navigate across all sections in Dark Mode.
* **Expected Result:**
  * Background transitions to deep navy/slate (`#0b131d` / `#141f2c`).
  * All fonts, subtitles, and labels invert to high-contrast off-white (`#e2e8f0` / `#ffffff`) and light slate (`#94a3b8`); no black or dark gray text on dark surfaces.
  * The topbar toggle icon toggles to ☀️.
* **Evaluation:**
  * Status: `[ ] Pass  [ ] Fail`
  * Rating (1–5): `____` | Notes: `________________________________________________`

### Test Case `TC-UI-03`: Dark Mode Chart Adaptation
* **Objective:** Confirm canvas and SVG charts dynamically theme without reload.
* **Steps:**
  1. On Dashboard and Forecasting, toggle between Light and Dark mode while watching charts.
* **Expected Result:**
  * Grid lines change from faint gray to subtle dark borders (`#26384a`).
  * Axis labels and ticks remain fully legible.
  * Data series lines (teal actuals, blue/orange predictions) maintain high contrast.
* **Evaluation:**
  * Status: `[ ] Pass  [ ] Fail`
  * Rating (1–5): `____` | Notes: `________________________________________________`

---

## Module 3: Executive Dashboard & Monitoring

### Test Case `TC-DASH-01`: Metric Summary & Period Selection
* **Objective:** Validate summary card aggregations and dynamic timeframe scaling.
* **Steps:**
  1. On the **Dashboard**, review: *Total recorded consumption*, *Average per period*, *Records represented*, and *Items flagged for review*.
  2. Switch the Reporting Period selector between *Last 4*, *Last 6*, *Last 12*, *Last 24*, and *Last 36 periods*.
* **Expected Result:**
  * Metrics recalculate instantaneously.
  * Values display in bold $38\text{px}$ numerals with appropriate unit captions ($m^3$).
  * The Trend Visualization chart scales the horizontal time axis smoothly.
* **Evaluation:**
  * Status: `[ ] Pass  [ ] Fail`
  * Rating (1–5): `____` | Notes: `________________________________________________`

### Test Case `TC-DASH-02`: Review Queue Navigation
* **Objective:** Verify direct workflow connection between Dashboard review queue and anomaly cases.
* **Steps:**
  1. Click *"View all →"* or *"Open anomaly monitoring"* inside the Review Queue card.
* **Expected Result:**
  * Directly navigates to the **Anomaly monitoring** section with active exception cases filtered.
* **Evaluation:**
  * Status: `[ ] Pass  [ ] Fail`

---

## Module 4: Consumption Records Explorer & Filtering (2021–2026)

### Test Case `TC-REC-01`: Multi-Year Data Scope & Filtering Speed
* **Objective:** Test responsiveness across 4,464 records spanning 6 full years (2021–2026).
* **Steps:**
  1. Open **Consumption records**.
  2. Select Year: `2023`, Month: `October`, and Station: `Bago City`.
  3. Clear filters using *"Reset filters"*.
  4. Test sorting by: *Newest period first*, *Highest consumption*, and *Station A–Z*.
* **Expected Result:**
  * Filters update instantly without page lag or stutter.
  * Record counter accurately states total matching entries.
  * Status pills indicate *Normal* or *Flagged*.
* **Evaluation:**
  * Status: `[ ] Pass  [ ] Fail`
  * Rating (1–5): `____` | Notes: `________________________________________________`

### Test Case `TC-REC-02`: Manual Anomaly Flagging Workflow
* **Objective:** Ensure station readings can be flagged by authorized personnel for investigation.
* **Steps:**
  1. In the records table, locate any unflagged reading and click *"Flag reading"*.
  2. Provide a reason (e.g., *"Meter maintenance audit required"*) and submit.
* **Expected Result:**
  * Modal opens with context metadata.
  * After submission, status pill updates to *Flagged*, and an anomaly case is logged in the Anomaly queue.
* **Evaluation:**
  * Status: `[ ] Pass  [ ] Fail`

---

## Module 5: Drag-and-Drop CSV Import & Dataset History

### Test Case `TC-IMP-01`: Drag-and-Drop CSV Validation & Preview
* **Objective:** *(Admin only)* Test CSV parsing, schema checking, and staging preview.
* **Steps:**
  1. As `admin`, go to the Import panel in **Consumption records**.
  2. Drag and drop [`AQUACAST_2021_2026_mock_consumption_import.csv`](file:///c:/Users/Administrator/Downloads/AQUACAST/V.3.9.3/sample-data/AQUACAST_2021_2026_mock_consumption_import.csv).
  3. Inspect the validation summary and change preview table.
  4. Click *"Review and import"* and confirm in the confirmation modal.
* **Expected Result:**
  * File is accepted, validated locally (no cloud transfer), and summary displays rows to be updated.
  * Confirmation modal emphasizes that existing numbers will be replaced and a recoverable snapshot saved.
* **Evaluation:**
  * Status: `[ ] Pass  [ ] Fail`
  * Rating (1–5): `____` | Notes: `________________________________________________`

### Test Case `TC-IMP-02`: History Card Layout & "Overview" Button Sizing
* **Objective:** Confirm that the "Overview" button fits properly within the history card box without layout overflow.
* **Steps:**
  1. Scroll down to **Consumption Records activity & dataset history**.
  2. Inspect the newly logged import snapshot entry.
  3. Observe the **"Overview"** button on the right side of the card.
  4. Click **"Overview"** to review snapshot records, then click *"Close overview"*.
* **Expected Result:**
  * **Layout Check:** The "Overview" button is neatly contained **inside** the card border. It does **not** stretch across the screen, overlap neighboring text, or cause a horizontal page scrollbar.
  * Clicking "Overview" toggles the dataset inspection panel with version details and search.
* **Evaluation:**
  * Status: `[ ] Pass  [ ] Fail`
  * Rating (1–5): `____` | Notes: `________________________________________________`

---

## Module 6: Forecasting Workspace & Plain-Language Guide

### Test Case `TC-FCST-01`: Station Plain-Language Forecast Guide
* **Objective:** *(Station User)* Verify actionable, jargon-free forecast presentation.
* **Steps:**
  1. Log in as `bagocity` and navigate to **Forecasting**.
  2. Inspect *"Understanding your station's forecast"*.
* **Expected Result:**
  * Displays 3 plain cards:
    1. *Water-use pattern:* General trend (increasing, decreasing, steady) comparing earliest to latest sample months.
    2. *Next month's estimate:* Projected $m^3$ demand.
    3. *Typical past difference:* Historical average error margin ($m^3$).
  * Context explains why the model was selected and advises operational vigilance.
* **Evaluation:**
  * Status: `[ ] Pass  [ ] Fail`
  * Rating (1–5): `____` | Notes: `________________________________________________`

### Test Case `TC-FCST-02`: One-Month-Ahead Research Lab
* **Objective:** *(Admin only)* Inspect candidate forecasting models.
* **Steps:**
  1. As `admin`, expand the One-Month-Ahead Research Lab.
  2. Switch between candidate models: *Naïve*, *Moving Average*, *SES*, *Drift*, *Linear Trend*.
* **Expected Result:**
  * Table compares MAE, RMSE, MASE across identical walk-forward periods.
  * Backtest chart graphs actual readings against model predictions.
* **Evaluation:**
  * Status: `[ ] Pass  [ ] Fail`

---

## Module 7: Model Evaluation Sandbox & Accuracy Dashboard

### Test Case `TC-EVAL-01`: Rolling-Origin Backtesting on Multi-Year History
* **Objective:** Verify mathematical integrity and walk-forward holdouts.
* **Steps:**
  1. In **Admin settings** $\rightarrow$ **Model evaluation**, click *"Load fictional sample"*.
  2. Select Station: `Bago City (NO-01)`.
  3. Switch between models and review the Accuracy Dashboard.
* **Expected Result:**
  * Evaluates on 66 test months (2021–2026 minus 6-month initial training window).
  * Backtested SVG plot displays actual polyline (teal) vs forecast polyline (orange dashed).
  * Error metrics display MAE, RMSE, and Naïve baseline MAE.
* **Evaluation:**
  * Status: `[ ] Pass  [ ] Fail`
  * Rating (1–5): `____` | Notes: `________________________________________________`

---

## Module 8: Anomaly Monitoring & Investigation Thread

### Test Case `TC-ANOM-01`: Exception Organization & Regional Filtering
* **Objective:** Validate regional categorization and non-accusatory framing.
* **Steps:**
  1. Open **Anomaly monitoring**.
  2. Filter by *Negros Occidental*, *Negros Oriental*, and *Siquijor*.
  3. Toggle between *Active flags*, *For review*, and *Archived flags*.
* **Expected Result:**
  * Clear disclaimers reinforce: *"A flag is not a conclusion — unusual consumption can have legitimate causes."*
  * Cases display station baseline median and recorded trigger reasons.
* **Evaluation:**
  * Status: `[ ] Pass  [ ] Fail`

### Test Case `TC-ANOM-02`: Collaborative Investigation Simulation
* **Objective:** Test end-to-end communication between Admin and Station regarding an anomaly.
* **Steps:**
  1. As `admin`, click *"Request info"* on an open flag, enter a query, and send.
  2. Sign in as the target station (e.g. `bagocity`), check notification bell, and reply.
  3. Sign back in as `admin` and open the flag thread.
* **Expected Result:**
  * Thread displays chronological message exchanges with sender badge, timestamp, and attached evidence table.
* **Evaluation:**
  * Status: `[ ] Pass  [ ] Fail`
  * Rating (1–5): `____` | Notes: `________________________________________________`

---

## Module 9: Utility Tariff Settings & Budget Reporting

### Test Case `TC-REP-01`: Tariff Reconfiguration & Cost Recalculation
* **Objective:** Verify BACIWA tariff table application by meter size and customer class.
* **Steps:**
  1. As `admin`, go to **Admin settings** $\rightarrow$ **Tariff settings**.
  2. For Bago City, change Classification to *Commercial/Industrial* and Connection size to *2 inches* with Effective Date `2021-01-01`. Save.
  3. Open **Reports**, choose View: *Yearly report*, Year: `2024`.
* **Expected Result:**
  * Tariff preview calculates minimum charge and tiered charges accurately.
  * Yearly report breaks down consumption and recalculated estimated costs month-by-month.
  * Clicking *"Print report ↗"* opens a clean, uncluttered print preview.
* **Evaluation:**
  * Status: `[ ] Pass  [ ] Fail`
  * Rating (1–5): `____` | Notes: `________________________________________________`

---

## Module 10: Administrative Communications Suite

### Test Case `TC-NOTIF-01`: Broadcast Notification Composer
* **Objective:** *(Admin only)* Test announcement publishing and station targeting.
* **Steps:**
  1. Click the floating notification creator button (envelope icon at lower right).
  2. Compose an announcement, select Recipients: *Negros Occidental*, set Priority: *Important*, and publish.
  3. Sign in as `bagocity` (should receive notification) and `dumaguetecity` (should NOT receive it).
* **Expected Result:**
  * Rich-text formatting (bold, lists, headings) functions cleanly.
  * Station bell displays unread notification badge; Dumaguete City remains untouched.
* **Evaluation:**
  * Status: `[ ] Pass  [ ] Fail`

---

## Standardized Usability Scorecard (SUS)

Please rate the following statements on a scale of **1 (Strongly Disagree)** to **5 (Strongly Agree)**:

| # | Usability Metric Statement | 1 (SD) | 2 (D) | 3 (N) | 4 (A) | 5 (SA) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **1** | I think that I would like to use this system frequently for water demand monitoring. | [ ] | [ ] | [ ] | [ ] | [ ] |
| **2** | I found the system unnecessarily complex. | [ ] | [ ] | [ ] | [ ] | [ ] |
| **3** | I thought the system was easy to use and navigate. | [ ] | [ ] | [ ] | [ ] | [ ] |
| **4** | I think that I would need technical support to be able to use this system. | [ ] | [ ] | [ ] | [ ] | [ ] |
| **5** | I found the various functions in this system were well integrated. | [ ] | [ ] | [ ] | [ ] | [ ] |
| **6** | I thought there was too much inconsistency in typography or layouts. | [ ] | [ ] | [ ] | [ ] | [ ] |
| **7** | I would imagine that most municipal water officers would learn to use this system very quickly. | [ ] | [ ] | [ ] | [ ] | [ ] |
| **8** | I found the system very cumbersome to use. | [ ] | [ ] | [ ] | [ ] | [ ] |
| **9** | I felt very confident navigating the records, forecasts, and anomaly queues. | [ ] | [ ] | [ ] | [ ] | [ ] |
| **10**| I needed to learn a lot of things before I could get going with this system. | [ ] | [ ] | [ ] | [ ] | [ ] |

---

## Qualitative Feedback & Final Sign-Off

### 1. Key Strengths
*What aspects of the interface, speed, or features performed best during your evaluation?*
> _____________________________________________________________________________________
> _____________________________________________________________________________________

### 2. Suggested Improvements
*Did you notice any visual flaws, confusing terminology, or missing operational capabilities?*
> _____________________________________________________________________________________
> _____________________________________________________________________________________

### 3. Pilot Deployment Recommendation
*Do you consider this system aligned with provincial public water utility management requirements?*
* [ ] **Approved:** Ready for research stakeholder presentation and pilot evaluation.
* [ ] **Minor Revisions Needed:** Meets core objectives but requires minor UI or wording adjustments.
* [ ] **Not Approved:** Requires fundamental architectural or workflow modifications.

---

**Evaluator Signature:** ___________________________________  
**Date:** ________________________
