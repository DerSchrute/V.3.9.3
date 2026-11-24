import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_element(name):
    return OxmlElement(name)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=180, right=180):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="CBD5E1", sz="4"):
    tblPr = table._tbl.tblPr
    tblBorders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:right w:val="none"/>'
        f'  <w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(tblBorders)

def add_callout(doc, title, steps, expected, tc_code, is_admin=False):
    # Callout table with left accent border
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    
    # Left border thick teal, no other borders
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:top w:val="none"/>'
        f'  <w:left w:val="single" w:sz="24" w:space="0" w:color="0D9488"/>'
        f'  <w:bottom w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=160)
    
    # Paragraph 1: Test Case ID & Title
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    run_id = p.add_run(f"[{tc_code}] ")
    run_id.bold = True
    run_id.font.name = "Segoe UI"
    run_id.font.size = Pt(11)
    run_id.font.color.rgb = RGBColor(15, 118, 110) # dark teal
    
    run_title = p.add_run(title)
    run_title.bold = True
    run_title.font.name = "Segoe UI"
    run_title.font.size = Pt(11)
    run_title.font.color.rgb = RGBColor(15, 23, 42)
    
    if is_admin:
        run_badge = p.add_run(" (Admin Role Only)")
        run_badge.italic = True
        run_badge.font.name = "Segoe UI"
        run_badge.font.size = Pt(9.5)
        run_badge.font.color.rgb = RGBColor(180, 83, 9) # amber
    
    # Steps
    p_steps_h = cell.add_paragraph()
    p_steps_h.paragraph_format.space_before = Pt(4)
    p_steps_h.paragraph_format.space_after = Pt(2)
    r_sh = p_steps_h.add_run("Execution Steps:")
    r_sh.bold = True
    r_sh.font.name = "Segoe UI"
    r_sh.font.size = Pt(9.5)
    r_sh.font.color.rgb = RGBColor(71, 85, 105)
    
    for idx, s in enumerate(steps, 1):
        p_step = cell.add_paragraph()
        p_step.paragraph_format.left_indent = Inches(0.2)
        p_step.paragraph_format.space_before = Pt(1)
        p_step.paragraph_format.space_after = Pt(1)
        rs_num = p_step.add_run(f"{idx}. ")
        rs_num.bold = True
        rs_num.font.name = "Segoe UI"
        rs_num.font.size = Pt(9.5)
        rs_num.font.color.rgb = RGBColor(15, 118, 110)
        
        rs_text = p_step.add_run(s)
        rs_text.font.name = "Segoe UI"
        rs_text.font.size = Pt(9.5)
        rs_text.font.color.rgb = RGBColor(51, 65, 85)
    
    # Expected Result
    p_exp = cell.add_paragraph()
    p_exp.paragraph_format.space_before = Pt(6)
    p_exp.paragraph_format.space_after = Pt(3)
    r_eh = p_exp.add_run("Expected Result / Success Criteria:\n")
    r_eh.bold = True
    r_eh.font.name = "Segoe UI"
    r_eh.font.size = Pt(9.5)
    r_eh.font.color.rgb = RGBColor(15, 118, 110)
    
    r_eb = p_exp.add_run(expected)
    r_eb.font.name = "Segoe UI"
    r_eb.font.size = Pt(9.5)
    r_eb.font.color.rgb = RGBColor(30, 41, 59)
    
    # Evaluation Checkboxes & Rating
    p_eval = cell.add_paragraph()
    p_eval.paragraph_format.space_before = Pt(6)
    p_eval.paragraph_format.space_after = Pt(2)
    
    r_res = p_eval.add_run("Tester Evaluation:   ")
    r_res.bold = True
    r_res.font.name = "Segoe UI"
    r_res.font.size = Pt(9.5)
    r_res.font.color.rgb = RGBColor(71, 85, 105)
    
    r_box1 = p_eval.add_run("☐ Pass      ☐ Fail              ")
    r_box1.bold = True
    r_box1.font.name = "Segoe UI"
    r_box1.font.size = Pt(9.5)
    r_box1.font.color.rgb = RGBColor(15, 23, 42)
    
    r_rate = p_eval.add_run("Ease / Experience Rating:  1  2  3  4  5\n")
    r_rate.bold = True
    r_rate.font.name = "Segoe UI"
    r_rate.font.size = Pt(9)
    r_rate.font.color.rgb = RGBColor(71, 85, 105)
    
    r_notes = p_eval.add_run("Tester Notes: ____________________________________________________________________")
    r_notes.font.name = "Segoe UI"
    r_notes.font.size = Pt(9)
    r_notes.font.color.rgb = RGBColor(100, 116, 139)
    
    # Spacer paragraph after table
    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_before = Pt(2)
    p_space.paragraph_format.space_after = Pt(4)

def build_testing_docx(output_path):
    doc = Document()
    
    # Configure page geometry (Standard Letter, 0.75 in margins for maximum executive layout)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)
        
        # Header
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hr = hp.add_run("AQUACAST Decision-Support System | UAT & Usability Protocol v1.0")
        hr.font.name = "Segoe UI"
        hr.font.size = Pt(8.5)
        hr.font.color.rgb = RGBColor(148, 163, 184)
        
        # Footer
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        fr = fp.add_run("Confidential — Municipal Water Intelligence Research & Stakeholder Evaluation")
        fr.font.name = "Segoe UI"
        fr.font.size = Pt(8.5)
        fr.font.color.rgb = RGBColor(148, 163, 184)

    # Document Header / Eyebrow
    p_eyebrow = doc.add_paragraph()
    p_eyebrow.paragraph_format.space_before = Pt(0)
    p_eyebrow.paragraph_format.space_after = Pt(2)
    r_eye = p_eyebrow.add_run("SYSTEM VERIFICATION & USER ACCEPTANCE TESTING PROTOCOL")
    r_eye.bold = True
    r_eye.font.name = "Segoe UI"
    r_eye.font.size = Pt(10)
    r_eye.font.color.rgb = RGBColor(13, 148, 136) # Teal
    
    # Main Document Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run("AQUACAST Usability & Performance Testing Guide")
    r_title.bold = True
    r_title.font.name = "Segoe UI"
    r_title.font.size = Pt(22)
    r_title.font.color.rgb = RGBColor(15, 23, 42)
    
    # Subtitle
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(14)
    r_sub = p_sub.add_run("Standardized Evaluation Questions, Test Procedures, Expected Results, and System Usability Scale (SUS) Scorecard for Testing Personnel.")
    r_sub.font.name = "Segoe UI"
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = RGBColor(71, 85, 105)

    # Metadata & Control Table
    meta_table = doc.add_table(rows=6, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False
    set_table_borders(meta_table)
    
    col_widths = [Inches(2.0), Inches(4.5)]
    meta_data = [
        ("System Under Test", "AQUACAST — Water Intelligence & Forecasting Decision-Support System (v3.9.6)"),
        ("Document Classification", "User Acceptance Testing (UAT) & Standardized Usability Protocol"),
        ("Evaluation Dataset", "72-Month Multi-Year Group (Jan 2021 – Dec 2026), 4,464 Synthetic Readings"),
        ("Target Test Audience", "Municipal Water District Staff, QA Testers, System Evaluators, Research Reviewers"),
        ("Test Environment", "Modern Web Browser (Chrome / Edge / Firefox) with JavaScript Enabled"),
        ("Key Evaluation Focus", "Typography/Dark Mode, Multi-Year Filtering, Plain-Language Forecasts, SUS Score")
    ]
    
    for row_idx, (k, v) in enumerate(meta_data):
        row = meta_table.rows[row_idx]
        
        c0 = row.cells[0]
        c0.width = col_widths[0]
        set_cell_background(c0, "F1F5F9")
        set_cell_margins(c0, top=80, bottom=80, left=120, right=120)
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_before = Pt(0)
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(k)
        r0.bold = True
        r0.font.name = "Segoe UI"
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = RGBColor(30, 41, 59)
        
        c1 = row.cells[1]
        c1.width = col_widths[1]
        set_cell_background(c1, "FFFFFF" if row_idx % 2 == 0 else "F8FAFC")
        set_cell_margins(c1, top=80, bottom=80, left=120, right=120)
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(0)
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(v)
        r1.font.name = "Segoe UI"
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Tester Information Form
    p_tinfo_h = doc.add_paragraph()
    p_tinfo_h.paragraph_format.space_before = Pt(8)
    p_tinfo_h.paragraph_format.space_after = Pt(4)
    r_tih = p_tinfo_h.add_run("Evaluator Sign-In Details")
    r_tih.bold = True
    r_tih.font.name = "Segoe UI"
    r_tih.font.size = Pt(13)
    r_tih.font.color.rgb = RGBColor(15, 118, 110)

    tinfo_table = doc.add_table(rows=3, cols=2)
    tinfo_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tinfo_table)
    
    tinfo_fields = [
        ("Tester Name:", "Organization / Designation:"),
        ("Date of Evaluation:", "Evaluation Start & End Time:"),
        ("Browser & Version:", "Operating System & Resolution:")
    ]
    for row_idx, (f1, f2) in enumerate(tinfo_fields):
        row = tinfo_table.rows[row_idx]
        for col_idx, field in enumerate([f1, f2]):
            cell = row.cells[col_idx]
            cell.width = Inches(3.25)
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            rf = p.add_run(f"{field} ")
            rf.bold = True
            rf.font.name = "Segoe UI"
            rf.font.size = Pt(9)
            rf.font.color.rgb = RGBColor(71, 85, 105)
            
            ru = p.add_run("____________________________________")
            ru.font.name = "Segoe UI"
            ru.font.size = Pt(9)
            ru.font.color.rgb = RGBColor(148, 163, 184)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Section 1: Objectives & Guidelines
    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after = Pt(4)
    r_h1 = h1.add_run("1. Testing Objectives & Evaluation Methodology")
    r_h1.bold = True
    r_h1.font.name = "Segoe UI"
    r_h1.font.size = Pt(14)
    r_h1.font.color.rgb = RGBColor(15, 118, 110)

    p_obj = doc.add_paragraph()
    p_obj.paragraph_format.space_after = Pt(4)
    r_obj = p_obj.add_run(
        "This evaluation protocol is structured to provide empirical validation of the AQUACAST decision-support prototype. "
        "Evaluators should follow the test cases sequentially and grade both functional accuracy (Pass/Fail) and usability quality (1 to 5 Likert scale)."
    )
    r_obj.font.name = "Segoe UI"
    r_obj.font.size = Pt(10)
    r_obj.font.color.rgb = RGBColor(51, 65, 85)

    objectives = [
        ("Functional Integrity: ", "Verify that navigation, dynamic filters, statistical models, CSV processing, and tariff cost calculations execute without console errors or UI dead ends."),
        ("Visual & Ergonomic Appeal: ", "Evaluate the modernized typographic hierarchy, enlarged page headings, contrast legibility, and complete Dark Mode support across all UI elements and charts."),
        ("Decision-Support Correlation: ", "Assess whether plain-language forecasts, anomaly review threads, and budget reports translate complex municipal water data into actionable operational decisions."),
        ("Multi-Year Stress Test: ", "Validate application speed, table responsiveness, and backtest plots when handling the comprehensive 6-year (2021–2026, 4,464 records) historical series.")
    ]
    for bold_txt, norm_txt in objectives:
        p_item = doc.add_paragraph()
        p_item.paragraph_format.left_indent = Inches(0.25)
        p_item.paragraph_format.space_before = Pt(1)
        p_item.paragraph_format.space_after = Pt(2)
        rb = p_item.add_run(f"• {bold_txt}")
        rb.bold = True
        rb.font.name = "Segoe UI"
        rb.font.size = Pt(9.5)
        rb.font.color.rgb = RGBColor(15, 23, 42)
        rn = p_item.add_run(norm_txt)
        rn.font.name = "Segoe UI"
        rn.font.size = Pt(9.5)
        rn.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Section 2: Demo Credentials
    h2 = doc.add_paragraph()
    h2.paragraph_format.space_before = Pt(12)
    h2.paragraph_format.space_after = Pt(4)
    r_h2 = h2.add_run("2. Test Roles & Access Credentials")
    r_h2.bold = True
    r_h2.font.name = "Segoe UI"
    r_h2.font.size = Pt(14)
    r_h2.font.color.rgb = RGBColor(15, 118, 110)

    cred_table = doc.add_table(rows=5, cols=4)
    cred_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(cred_table)
    
    headers = ["Role", "Username", "Password", "Permissions & Access Scope"]
    widths = [Inches(1.5), Inches(1.1), Inches(1.1), Inches(2.8)]
    
    hdr_row = cred_table.rows[0]
    for c_idx, title in enumerate(headers):
        c = hdr_row.cells[c_idx]
        c.width = widths[c_idx]
        set_cell_background(c, "0F766E")
        set_cell_margins(c, top=80, bottom=80, left=100, right=100)
        p = c.paragraphs[0]
        r = p.add_run(title)
        r.bold = True
        r.font.name = "Segoe UI"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    creds_data = [
        ("System Administrator", "admin", "admin123", "Full unrestricted access: Tariff settings, Model Evaluation sandbox, CSV import/restore, Broadcast composer."),
        ("Station (Negros Occ.)", "bagocity", "station123", "Scoped strictly to Bago City (NO-01): Station Forecast Guide, Anomaly discussion, Contact admin."),
        ("Station (Negros Or.)", "dumaguetecity", "station123", "Scoped strictly to Dumaguete City (NOR-10): Station Forecast Guide, Anomaly discussion."),
        ("Station (Siquijor)", "enriquevillanueva", "station123", "Scoped strictly to Enrique Villanueva (SIQ-01): Station-level views.")
    ]
    for r_idx, (r_name, u_name, p_name, perm) in enumerate(creds_data, 1):
        row = cred_table.rows[r_idx]
        fill = "FFFFFF" if r_idx % 2 == 1 else "F8FAFC"
        for col_idx, text_val in enumerate([r_name, u_name, p_name, perm]):
            c = row.cells[col_idx]
            c.width = widths[col_idx]
            set_cell_background(c, fill)
            set_cell_margins(c, top=80, bottom=80, left=100, right=100)
            p = c.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(text_val)
            r.font.name = "Segoe UI"
            r.font.size = Pt(9)
            if col_idx in [1, 2]:
                r.bold = True
                r.font.color.rgb = RGBColor(15, 118, 110)
            else:
                r.font.color.rgb = RGBColor(30, 41, 59)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Modules Section
    def add_module_heading(num, title):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(6)
        r = h.add_run(f"Module {num}: {title}")
        r.bold = True
        r.font.name = "Segoe UI"
        r.font.size = Pt(13)
        r.font.color.rgb = RGBColor(15, 23, 42)
        return h

    # Module 1
    add_module_heading(1, "Authentication & Role-Based Access Control")
    add_callout(
        doc,
        title="Role-Based Sign-In & Workspace Isolation",
        steps=[
            "Open the sign-in screen and verify client-side prototype demonstration notice.",
            "Sign in as station user 'bagocity' with password 'station123'. Inspect sidebar navigation and active station badge.",
            "Confirm that administrator-only tabs (Admin settings, Tariff settings, Model Evaluation) are hidden.",
            "Sign out via Account menu and sign in as 'admin' with 'admin123'. Confirm full administration suite appears."
        ],
        expected="Station accounts are restricted strictly to station-level operational views. Administrator account displays provincial overview, model evaluation, tariff settings, and broadcast notification tools.",
        tc_code="TC-AUTH-01"
    )

    # Module 2
    add_module_heading(2, "Typography, Visual Appeal & Dark Mode Consistency")
    add_callout(
        doc,
        title="Section Headings & Visual Hierarchy",
        steps=[
            "Navigate to Forecasting, Dashboard, and Consumption records.",
            "Inspect the topbar section title (e.g., 'Forecasting'), page h1 heading ('Forecasting workspace'), and teal eyebrow pills.",
            "Check that font sizes follow clear visual hierarchy (22px topbar title, 32-44px h1 heading, 38px key metrics)."
        ],
        expected="Headings are crisp, modern, and prominent. Topbar title provides immediate spatial awareness. Eyebrow pills render neatly in teal with uppercase tracking.",
        tc_code="TC-UI-01"
    )
    add_callout(
        doc,
        title="Dark Mode Toggle & Global Element Styling",
        steps=[
            "Click the 🌙 icon in the topbar or select Dark Mode in the Account menu.",
            "Observe the color changes across cards, table rows, dropdowns, inputs, buttons, and text.",
            "Navigate through all sections in Dark Mode to ensure zero low-contrast or illegible elements."
        ],
        expected="Background smoothly transitions to deep slate/navy (#0b131d / #141f2c). All text inverts to clean off-white (#e2e8f0) and muted slate (#94a3b8); no black text on dark surfaces. Topbar icon toggles to ☀️.",
        tc_code="TC-UI-02"
    )
    add_callout(
        doc,
        title="Dark Mode Canvas & SVG Chart Adaptation",
        steps=[
            "View charts on Dashboard and Forecasting workspace.",
            "Toggle between Light and Dark mode while observing chart grids, ticks, and series lines.",
            "Verify that SVG charts in Model Evaluation also adapt dynamically without browser reload."
        ],
        expected="Chart grid lines adapt to subtle slate (#26384a), axis typography remains crisp, and data series (teal actuals, orange/blue forecasts) maintain high contrast.",
        tc_code="TC-UI-03"
    )

    # Module 3
    add_module_heading(3, "Executive Dashboard & Timeframe Scaling")
    add_callout(
        doc,
        title="Metric Summaries & Period Dropdown Scaling",
        steps=[
            "On Dashboard, review summary metrics: Total consumption, Average per period, Records represented, and Items flagged.",
            "Change the Reporting Period dropdown from 4 to 6, 12, 24, and 36 periods.",
            "Observe metric recalculation speed and horizontal axis scaling on the Trend Visualization chart."
        ],
        expected="Aggregations compute instantaneously. Key metrics display in bold 38px numerals with unit indicators (m³). Trend chart adapts horizontal timeline cleanly.",
        tc_code="TC-DASH-01"
    )
    add_callout(
        doc,
        title="Review Queue Direct Case Navigation",
        steps=[
            "Locate the Review Queue card on the Dashboard.",
            "Click 'View all →' or 'Open anomaly monitoring'."
        ],
        expected="Smoothly redirects to the Anomaly monitoring workspace with active exception flags loaded and focused.",
        tc_code="TC-DASH-02"
    )

    # Module 4
    add_module_heading(4, "Consumption Records Explorer (2021–2026)")
    add_callout(
        doc,
        title="Multi-Year Data Scope & Filtering Responsiveness",
        steps=[
            "Open Consumption records and inspect total record counter (4,464 records across 62 stations).",
            "Filter by Year: '2023', Month: 'October', and Station: 'Bago City'.",
            "Test sorting options: 'Newest period first', 'Highest consumption', and 'Station A–Z'. Click 'Reset filters'."
        ],
        expected="Filtering and sorting execute instantly without browser stutter. Record counter reflects exact match count. Status pills indicate Normal or Flagged.",
        tc_code="TC-REC-01"
    )
    add_callout(
        doc,
        title="Manual Anomaly Flagging Workflow",
        steps=[
            "In the records table, find an unflagged station reading and click 'Flag reading'.",
            "Enter a reason (e.g., 'Unusual surge during off-peak season') and submit the form."
        ],
        expected="Status badge immediately updates to 'Flagged' in red/orange. The reading is added to the Anomaly monitoring queue with the logged reason and timestamp.",
        tc_code="TC-REC-02"
    )

    # Module 5
    add_module_heading(5, "Drag-and-Drop CSV Import & Dataset History")
    add_callout(
        doc,
        title="CSV File Validation & Staging Preview",
        steps=[
            "As 'admin', navigate to the Import panel in Consumption records.",
            "Drag and drop 'AQUACAST_2021_2026_mock_consumption_import.csv' into the dropzone.",
            "Review the validation summary (records parsed, updated, format checks) and confirmation modal.",
            "Click 'Review and import' to execute the update."
        ],
        expected="File is parsed locally with instant validation. Modal confirms that a recoverable snapshot was automatically generated prior to data replacement.",
        tc_code="TC-IMP-01",
        is_admin=True
    )
    add_callout(
        doc,
        title="History Card Layout & 'Overview' Button Sizing",
        steps=[
            "Scroll down to 'Consumption Records activity & dataset history'.",
            "Locate the newly created import snapshot entry.",
            "Inspect the 'Overview' button on the right edge of the card.",
            "Click 'Overview' to view snapshot records and search bar, then click 'Close overview'."
        ],
        expected="The 'Overview' button is neatly contained within the card container. It does NOT stretch across the screen, wrap awkwardly, or cause horizontal scrolling. Clicking toggles version details seamlessly.",
        tc_code="TC-IMP-02"
    )

    # Module 6
    add_module_heading(6, "Forecasting Workspace & Plain-Language Guide")
    add_callout(
        doc,
        title="Station Plain-Language Forecast Presentation",
        steps=[
            "Log in as station user 'bagocity' and navigate to Forecasting workspace.",
            "Inspect 'Understanding your station's forecast' card deck."
        ],
        expected="Presents three clear cards: (1) Water-use pattern with trend comparison, (2) Next month's estimated demand (m³), and (3) Typical past difference (error margin). Avoids complex statistical jargon.",
        tc_code="TC-FCST-01"
    )
    add_callout(
        doc,
        title="Candidate Forecasting Model Research Lab",
        steps=[
            "As 'admin', expand the One-Month-Ahead Research Lab in Forecasting.",
            "Compare candidate models: Naïve, Moving Average, SES, Drift, and Linear Trend."
        ],
        expected="Displays side-by-side MAE, RMSE, and MASE benchmark metrics. Chart visualizes actual historical readings against candidate predictions.",
        tc_code="TC-FCST-02",
        is_admin=True
    )

    # Module 7
    add_module_heading(7, "Model Evaluation Sandbox & Accuracy Dashboard")
    add_callout(
        doc,
        title="Rolling-Origin Backtesting on Multi-Year History",
        steps=[
            "Go to Admin settings -> Model evaluation.",
            "Click 'Load fictional sample' and select station 'Bago City (NO-01)'.",
            "Examine the rolling-origin backtest on the full 2021–2026 timeline."
        ],
        expected="Backtesting calculates over 66 holdout test months (excluding the 6-month burn-in). SVG plot graphs actual polyline (teal) against forecast polyline (orange dashed) with exact MAE/RMSE readouts.",
        tc_code="TC-EVAL-01",
        is_admin=True
    )

    # Module 8
    add_module_heading(8, "Anomaly Monitoring & Investigation Workflow")
    add_callout(
        doc,
        title="Regional Anomaly Organization & Filtering",
        steps=[
            "Open Anomaly monitoring workspace.",
            "Filter flags by region: Negros Occidental, Negros Oriental, and Siquijor.",
            "Toggle between 'Active flags', 'For review', and 'Archived flags'."
        ],
        expected="Anomalies are presented with non-accusatory operational framing ('A flag is not a conclusion'). Shows baseline median, percentage deviation, and trigger classification.",
        tc_code="TC-ANOM-01"
    )
    add_callout(
        doc,
        title="Collaborative Station Investigation Thread",
        steps=[
            "As 'admin', select an open flag, click 'Request info', and type an inquiry.",
            "Log in as target station ('bagocity'), check notification bell, and reply to the inquiry.",
            "Log back in as 'admin' and verify the conversation thread."
        ],
        expected="Full bidirectional chronological discussion thread displays with sender badges, timestamps, and attached monthly consumption figures.",
        tc_code="TC-ANOM-02"
    )

    # Module 9
    add_module_heading(9, "Utility Tariff Settings & Budget Reporting")
    add_callout(
        doc,
        title="Tariff Structure Reconfiguration & Cost Reporting",
        steps=[
            "As 'admin', open Admin settings -> Tariff settings.",
            "Change Bago City's classification to Commercial/Industrial (2-inch meter) with Effective Date 2021-01-01 and save.",
            "Navigate to Reports, select Yearly Report for Year 2024, and click 'Print report ↗'."
        ],
        expected="Tariff tiers apply correctly. Yearly report calculates monthly consumption and billing totals accurately. Print preview provides clean, uncluttered output.",
        tc_code="TC-REP-01"
    )

    # Module 10
    add_module_heading(10, "Administrative Communications Suite")
    add_callout(
        doc,
        title="Broadcast Notification Publisher",
        steps=[
            "Click the floating notification creator button (envelope icon, bottom right).",
            "Compose an announcement, select Recipient: 'Negros Occidental', Priority: 'Important', and publish.",
            "Verify receipt in 'bagocity' inbox, and verify that 'dumaguetecity' does NOT receive it."
        ],
        expected="Broadcast is targeted strictly to selected regional stations. Recipient station displays unread counter on topbar bell icon; non-target stations remain unaffected.",
        tc_code="TC-NOTIF-01",
        is_admin=True
    )

    # Section: SUS Usability Scale
    doc.add_page_break()
    h_sus = doc.add_paragraph()
    h_sus.paragraph_format.space_before = Pt(8)
    h_sus.paragraph_format.space_after = Pt(4)
    r_hsus = h_sus.add_run("Standardized Usability Scale (SUS) Scorecard")
    r_hsus.bold = True
    r_hsus.font.name = "Segoe UI"
    r_hsus.font.size = Pt(14)
    r_hsus.font.color.rgb = RGBColor(15, 118, 110)

    p_sus_desc = doc.add_paragraph()
    p_sus_desc.paragraph_format.space_after = Pt(8)
    r_sd = p_sus_desc.add_run(
        "Please rate the following 10 standardized statements regarding your overall experience using AQUACAST. "
        "Select exactly one rating per item: 1 = Strongly Disagree (SD), 2 = Disagree (D), 3 = Neutral (N), 4 = Agree (A), 5 = Strongly Agree (SA)."
    )
    r_sd.font.name = "Segoe UI"
    r_sd.font.size = Pt(9.5)
    r_sd.font.color.rgb = RGBColor(71, 85, 105)

    sus_questions = [
        "1. I think that I would like to use this system frequently for water demand monitoring.",
        "2. I found the system unnecessarily complex.",
        "3. I thought the system was easy to use and navigate.",
        "4. I think that I would need the support of a technical person to be able to use this system.",
        "5. I found the various functions in this system were well integrated.",
        "6. I thought there was too much inconsistency in typography or layouts.",
        "7. I would imagine that most municipal water officers would learn to use this system very quickly.",
        "8. I found the system very cumbersome to use.",
        "9. I felt very confident navigating the records, forecasts, and anomaly queues.",
        "10. I needed to learn a lot of things before I could get going with this system."
    ]

    sus_table = doc.add_table(rows=11, cols=6)
    sus_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(sus_table)
    
    sus_widths = [Inches(3.8), Inches(0.54), Inches(0.54), Inches(0.54), Inches(0.54), Inches(0.54)]
    
    # Header
    s_hdr = sus_table.rows[0]
    s_hdr_titles = ["Usability Metric Statement", "1 (SD)", "2 (D)", "3 (N)", "4 (A)", "5 (SA)"]
    for i, t in enumerate(s_hdr_titles):
        c = s_hdr.cells[i]
        c.width = sus_widths[i]
        set_cell_background(c, "0F766E")
        set_cell_margins(c, top=80, bottom=80, left=60, right=60)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i > 0 else WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(t)
        r.bold = True
        r.font.name = "Segoe UI"
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for q_idx, q_text in enumerate(sus_questions, 1):
        row = sus_table.rows[q_idx]
        fill = "FFFFFF" if q_idx % 2 == 1 else "F8FAFC"
        
        # Question text
        c0 = row.cells[0]
        c0.width = sus_widths[0]
        set_cell_background(c0, fill)
        set_cell_margins(c0, top=70, bottom=70, left=80, right=80)
        p0 = c0.paragraphs[0]
        r0 = p0.add_run(q_text)
        r0.font.name = "Segoe UI"
        r0.font.size = Pt(8.5)
        r0.font.color.rgb = RGBColor(30, 41, 59)
        
        # 5 Rating columns
        for c_idx in range(1, 6):
            c = row.cells[c_idx]
            c.width = sus_widths[c_idx]
            set_cell_background(c, fill)
            set_cell_margins(c, top=70, bottom=70, left=40, right=40)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run("☐")
            r.font.name = "Segoe UI"
            r.font.size = Pt(11)
            r.font.color.rgb = RGBColor(148, 163, 184)

    # SUS Calculation formula callout
    p_sus_calc = doc.add_paragraph()
    p_sus_calc.paragraph_format.space_before = Pt(8)
    p_sus_calc.paragraph_format.space_after = Pt(12)
    r_sc = p_sus_calc.add_run(
        "SUS Scoring Standard: Odd Items (1, 3, 5, 7, 9) Score = Scale Position - 1. "
        "Even Items (2, 4, 6, 8, 10) Score = 5 - Scale Position. Total SUS Score = (Sum of All Item Scores) × 2.5 (Yields 0 to 100 Scale; >68 is Above Average, >80.3 is Grade A Excellence)."
    )
    r_sc.italic = True
    r_sc.font.name = "Segoe UI"
    r_sc.font.size = Pt(8.5)
    r_sc.font.color.rgb = RGBColor(100, 116, 139)

    # Section: Qualitative Feedback & Final Sign-Off
    h_sign = doc.add_paragraph()
    h_sign.paragraph_format.space_before = Pt(10)
    h_sign.paragraph_format.space_after = Pt(4)
    r_hsign = h_sign.add_run("Qualitative Feedback & Evaluator Sign-Off")
    r_hsign.bold = True
    r_hsign.font.name = "Segoe UI"
    r_hsign.font.size = Pt(14)
    r_hsign.font.color.rgb = RGBColor(15, 118, 110)

    # Prompt 1
    p_q1 = doc.add_paragraph()
    p_q1.paragraph_format.space_before = Pt(4)
    p_q1.paragraph_format.space_after = Pt(2)
    rq1 = p_q1.add_run("1. Key System Strengths & Well-Executed Features:")
    rq1.bold = True
    rq1.font.name = "Segoe UI"
    rq1.font.size = Pt(9.5)
    rq1.font.color.rgb = RGBColor(15, 23, 42)
    
    p_l1 = doc.add_paragraph()
    p_l1.paragraph_format.space_before = Pt(0)
    p_l1.paragraph_format.space_after = Pt(8)
    rl1 = p_l1.add_run(
        "___________________________________________________________________________________________________\n"
        "___________________________________________________________________________________________________"
    )
    rl1.font.color.rgb = RGBColor(203, 213, 225)

    # Prompt 2
    p_q2 = doc.add_paragraph()
    p_q2.paragraph_format.space_before = Pt(4)
    p_q2.paragraph_format.space_after = Pt(2)
    rq2 = p_q2.add_run("2. Recommended UI Enhancements or Workflow Revisions:")
    rq2.bold = True
    rq2.font.name = "Segoe UI"
    rq2.font.size = Pt(9.5)
    rq2.font.color.rgb = RGBColor(15, 23, 42)
    
    p_l2 = doc.add_paragraph()
    p_l2.paragraph_format.space_before = Pt(0)
    p_l2.paragraph_format.space_after = Pt(8)
    rl2 = p_l2.add_run(
        "___________________________________________________________________________________________________\n"
        "___________________________________________________________________________________________________"
    )
    rl2.font.color.rgb = RGBColor(203, 213, 225)

    # Pilot Recommendation
    p_rec = doc.add_paragraph()
    p_rec.paragraph_format.space_before = Pt(4)
    p_rec.paragraph_format.space_after = Pt(4)
    r_rc = p_rec.add_run("3. Final Stakeholder Deployment Recommendation:")
    r_rc.bold = True
    r_rc.font.name = "Segoe UI"
    r_rc.font.size = Pt(9.5)
    r_rc.font.color.rgb = RGBColor(15, 23, 42)

    recs = [
        ("☐ Approved for Pilot Deployment: ", "Meets functional requirements, provides actionable forecasting intelligence, and displays clean usability."),
        ("☐ Conditionally Approved with Minor Revisions: ", "Core capabilities operate reliably; minor visual adjustments or wording improvements recommended prior to field rollout."),
        ("☐ Not Approved / Major Rework Required: ", "Requires architectural revisions, missing key operational controls, or exhibits significant workflow friction.")
    ]
    for b_txt, n_txt in recs:
        p_r = doc.add_paragraph()
        p_r.paragraph_format.left_indent = Inches(0.2)
        p_r.paragraph_format.space_before = Pt(1)
        p_r.paragraph_format.space_after = Pt(2)
        rb = p_r.add_run(b_txt)
        rb.bold = True
        rb.font.name = "Segoe UI"
        rb.font.size = Pt(9)
        rb.font.color.rgb = RGBColor(15, 118, 110)
        rn = p_r.add_run(n_txt)
        rn.font.name = "Segoe UI"
        rn.font.size = Pt(9)
        rn.font.color.rgb = RGBColor(51, 65, 85)

    # Signature Block
    doc.add_paragraph().paragraph_format.space_after = Pt(8)
    sig_table = doc.add_table(rows=1, cols=2)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(sig_table)
    
    c_sig1 = sig_table.rows[0].cells[0]
    c_sig1.width = Inches(3.25)
    set_cell_margins(c_sig1, top=100, bottom=100, left=100, right=100)
    p_s1 = c_sig1.paragraphs[0]
    p_s1.paragraph_format.space_after = Pt(0)
    rs1 = p_s1.add_run("Evaluator Signature: ________________________________\nName: __________________________________________")
    rs1.font.name = "Segoe UI"
    rs1.font.size = Pt(9.5)
    rs1.font.color.rgb = RGBColor(71, 85, 105)

    c_sig2 = sig_table.rows[0].cells[1]
    c_sig2.width = Inches(3.25)
    set_cell_margins(c_sig2, top=100, bottom=100, left=100, right=100)
    p_s2 = c_sig2.paragraphs[0]
    p_s2.paragraph_format.space_after = Pt(0)
    rs2 = p_s2.add_run("Date of Sign-Off: _________________________________\nCalculated SUS Score: ________ / 100")
    rs2.font.name = "Segoe UI"
    rs2.font.size = Pt(9.5)
    rs2.font.color.rgb = RGBColor(71, 85, 105)

    # Save document
    doc.save(output_path)
    print(f"Successfully generated DOCX at {output_path}")

if __name__ == "__main__":
    out1 = r"c:\Users\Administrator\Downloads\AQUACAST\V.3.9.3\docs\AQUACAST_System_Evaluation_and_Testing_Guide.docx"
    out2 = r"c:\Users\Administrator\Downloads\AQUACAST\V.3.9.3\AQUACAST_System_Evaluation_and_Testing_Guide.docx"
    build_testing_docx(out1)
    build_testing_docx(out2)
