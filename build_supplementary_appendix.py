from __future__ import annotations

import csv
import json
from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


ROOT = Path("/workspace/scratch/e3addee252de")
AUDIT = ROOT / "outputs/final_dependency_audit_2026_11_01"
DUAL = ROOT / "outputs/dual_review_supplement_20261115/data/dual_review_supplement_data.json"
OUT = ROOT / "outputs/final_manuscript_2026_11_01"
OUT.mkdir(parents=True, exist_ok=True)
OUTFILE = OUT / "S1_Appendix_Integrated_Dependency_Adjusted_Evidence_Audit_FINAL.docx"

with (AUDIT / "reconciliation_data_final.json").open(encoding="utf-8-sig") as f:
    data = json.load(f)

with DUAL.open(encoding="utf-8") as f:
    dual = json.load(f)

with (AUDIT / "Final_Lineage_Crosswalk.csv").open(encoding="utf-8-sig", newline="") as f:
    lineage_rows = list(csv.DictReader(f))

claim_rows = data["claim_rows"]
summary = data["final_summary"]
dual_summary = dual["summary"]


DARK = "18324A"
TEAL = "2F6F68"
LIGHT_BLUE = "EAF2F8"
LIGHT_TEAL = "E8F3F1"
LIGHT_GRAY = "F2F2F2"
AMBER = "FFF2CC"
WHITE = "FFFFFF"
BLACK = "222222"


def shade(cell, fill: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_width(cell, width_inches: float) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_w = tc_pr.find(qn("w:tcW"))
    if tc_w is None:
        tc_w = OxmlElement("w:tcW")
        tc_pr.append(tc_w)
    tc_w.set(qn("w:w"), str(int(width_inches * 1440)))
    tc_w.set(qn("w:type"), "dxa")


def set_repeat_table_header(row) -> None:
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def keep_row_together(row) -> None:
    tr_pr = row._tr.get_or_add_trPr()
    cant_split = OxmlElement("w:cantSplit")
    tr_pr.append(cant_split)


def set_cell_text(cell, text: str, *, bold=False, color=BLACK, size=8.0, align=None) -> None:
    cell.text = ""
    p = cell.paragraphs[0]
    if align is not None:
        p.alignment = align
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    r = p.add_run(str(text))
    r.bold = bold
    r.font.name = "Arial"
    r.font.size = Pt(size)
    r.font.color.rgb = RGBColor.from_string(color)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER


def add_table(doc: Document, headers, rows, widths, *, font_size=8.0, center_cols=(), header_fill=DARK):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.style = "Table Grid"
    hdr = table.rows[0]
    set_repeat_table_header(hdr)
    keep_row_together(hdr)
    for i, (h, w) in enumerate(zip(headers, widths)):
        set_cell_width(hdr.cells[i], w)
        shade(hdr.cells[i], header_fill)
        set_cell_text(hdr.cells[i], h, bold=True, color=WHITE, size=font_size, align=WD_ALIGN_PARAGRAPH.CENTER)
    for ridx, row_data in enumerate(rows):
        row = table.add_row()
        keep_row_together(row)
        if ridx % 2:
            for c in row.cells:
                shade(c, LIGHT_BLUE)
        for i, (value, w) in enumerate(zip(row_data, widths)):
            set_cell_width(row.cells[i], w)
            align = WD_ALIGN_PARAGRAPH.CENTER if i in center_cols else WD_ALIGN_PARAGRAPH.LEFT
            set_cell_text(row.cells[i], value, size=font_size, align=align)
    return table


def add_heading(doc: Document, text: str, level=1):
    p = doc.add_paragraph(style=f"Heading {level}")
    p.paragraph_format.space_before = Pt(12 if level == 1 else 8)
    p.paragraph_format.space_after = Pt(5)
    r = p.add_run(text)
    return p


def add_body(doc: Document, text: str):
    p = doc.add_paragraph(style="Body Text")
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = 1.08
    p.add_run(text)
    return p


def add_label_value(doc: Document, label: str, value: str):
    p = doc.add_paragraph(style="Body Text")
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(label + "  ")
    r.bold = True
    p.add_run(value)
    return p


doc = Document()
section = doc.sections[0]
section.orientation = WD_ORIENT.LANDSCAPE
section.page_width = Inches(11)
section.page_height = Inches(8.5)
section.top_margin = Inches(0.48)
section.bottom_margin = Inches(0.48)
section.left_margin = Inches(0.45)
section.right_margin = Inches(0.45)
section.header_distance = Inches(0.22)
section.footer_distance = Inches(0.22)

styles = doc.styles
styles["Normal"].font.name = "Arial"
styles["Normal"].font.size = Pt(9)
styles["Body Text"].font.name = "Arial"
styles["Body Text"].font.size = Pt(9.5)
for level, size, color in [(1, 15, DARK), (2, 12, TEAL), (3, 10.5, DARK)]:
    s = styles[f"Heading {level}"]
    s.font.name = "Arial"
    s.font.size = Pt(size)
    s.font.bold = True
    s.font.color.rgb = RGBColor.from_string(color)

footer = section.footer.paragraphs[0]
footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = footer.add_run("Supplementary appendix | Dependency-adjusted evidence audit | ")
run.font.name = "Arial"
run.font.size = Pt(8)
field = OxmlElement("w:fldSimple")
field.set(qn("w:instr"), "PAGE")
footer._p.append(field)

# Title page
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(48)
r = p.add_run("S1 Appendix")
r.font.name = "Arial"
r.font.size = Pt(24)
r.bold = True
r.font.color.rgb = RGBColor.from_string(DARK)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Dependency-Adjusted Evidence Thickness in Breast Cancer Ferroptosis Research")
r.font.name = "Arial"
r.font.size = Pt(19)
r.bold = True
r.font.color.rgb = RGBColor.from_string(TEAL)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("A meta-research audit of cytotoxic chemotherapy resistance")
r.font.name = "Arial"
r.font.size = Pt(13)
r.italic = True

doc.add_paragraph()
add_label_value(doc, "Purpose", "Document the full evidential chain from independent eligibility review and source adjudication to claim-specific team-model dependency correction.")
add_label_value(doc, "Locked corpus", f"{summary['candidate_reports']} candidate reports; {summary['strict_reports']} strict acquired-resistance reports; {summary['claim_units']} mechanism–drug–subtype claims.")
add_label_value(doc, "Primary result", f"{summary['independent_units_primary']} claim-specific independent team–model units ({100*summary['global_primary_retention_fraction']:.1f}% of {summary['strict_reports']} nominal strict reports).")
add_label_value(doc, "Deterministic sensitivity", f"{summary['independent_units_sensitivity']} units ({100*summary['global_sensitivity_retention_fraction']:.1f}%) after splitting unresolved model labels by report.")
add_label_value(doc, "Version", "Integrated submission version, 15 November 2026.")

doc.add_page_break()

add_heading(doc, "S1. Reader's guide and analysis hierarchy", 1)
add_body(doc, "This study separates three questions that are often conflated. Bibliometric maps describe visibility, themes, temporal evolution, and citation structure. The 10 × 3 cross-layer analysis tests whether research fronts preferentially draw on distinct intellectual bases. Neither establishes experimental replication. The primary audit therefore returns to the source reports and asks how many mutually independent team–model units support each mechanism–drug–subtype claim after eligibility and provenance correction.")

hierarchy_rows = [
    ("Stage 1", "Structural context", "VOSviewer, CiteSpace, Bibliometrix", "Where the field is growing and how concepts/collaborations are organized", "Not evidence of independent validation"),
    ("Stage 2", "Cross-layer structure", "10 × 3 fractional matrix; 3,600 permutations", "Whether research fronts segregate across co-cited knowledge bases", "Citation sharing is not experimental replication"),
    ("Stage 3", "Primary evidence audit", "Dual review, source adjudication, canonical team/model crosswalk, claim-specific maximum matching", "How much independent evidence remains", "Primary inferential layer"),
]
add_table(doc, ["Stage", "Role", "Method", "Question answered", "Interpretive boundary"], hierarchy_rows,
          [0.65, 1.35, 2.15, 3.0, 2.7], font_size=8.3, center_cols=(0,))

add_heading(doc, "S2. Operational definitions", 1)
definitions = [
    ("Primary claim unit", "Mechanism class × cytotoxic drug/class × breast-cancer subtype × acquired-resistance context."),
    ("Strict acquired resistance", "Resistance documented after prior cytotoxic exposure; a drug-selected derivative compared with its parental counterpart and resistance quantified; or post-treatment residual/relapsed clinical material explicitly tied to the claim."),
    ("Context-only report", "Intrinsic sensitivity, short-term exposure, ordinary sensitization, non-cytotoxic therapy resistance, or an incompletely specified tolerance state that does not meet the strict numerator."),
    ("Team lineage", "Canonical laboratory/programme grouping based on senior/corresponding authors, affiliations, shared authorship, and explicit continuity."),
    ("Model/provenance lineage", "Canonical resistant derivative, clinical cohort, PDX/PDO, or other experimental source defined by parent, drug, derivation/source, and provenance."),
    ("Primary provenance rule", "Unresolved identical parent-cell/drug families are merged across reports; this prevents unsupported claims of model independence."),
    ("Independent team–model unit", "One edge retained in the maximum matching of the claim-specific team-by-model bipartite graph; no retained pair shares a team or model lineage."),
    ("Deterministic sensitivity", "Only unresolved model labels are split by report; documented team and model links remain unchanged. This is an upper-bound scenario, not a confidence interval."),
    ("T0", "In vitro only; no aligned resistant-model in vivo or clinical support."),
    ("T1", "In vivo evidence that does not establish an aligned acquired-resistant model."),
    ("T2", "Aligned resistant-model in vivo support."),
    ("T3", "Patient-derived or clinical resistance material aligned to the claim."),
    ("E1", "One independent team–model support unit."),
    ("E2", "At least two independent units but no aligned T2/T3 support."),
    ("E3", "At least two independent units with one aligned T2/T3 unit."),
    ("E4", "E3 plus at least two mutually independent aligned T2/T3 units."),
]
add_table(doc, ["Field", "Operational definition"], definitions, [2.2, 7.9], font_size=8.5)

doc.add_page_break()
add_heading(doc, "S3. Dual-review and reconciliation audit", 1)
add_body(doc, "The targeted audit contained 63 deduplicated candidate reports after reconciliation of the 118-Article Web of Science corpus with the external 44-study evidence table. Reviewer 1 completed the primary eligibility assessment. Reviewer 2 independently coded 62 reports as Yes, No, or Unclear using the same operational rule; 33 were checked at full-text level. W93 was withheld from Reviewer 2 classification because its retraction or availability status was uncertain and was handled as a separate publisher-status exception.")
add_body(doc, "Reviewer labels are anonymous in the public data file. Public bibliographic identifiers are retained because they are required to reproduce the eligibility decisions.")

add_heading(doc, "S3.1 Prespecified eligibility rule", 2)
add_body(doc, "A report entered the strict denominator only when the source record supported all applicable elements below:")
for item in [
    "The experimental or clinical context represented acquired resistance to a cytotoxic chemotherapy, rather than lower drug sensitivity in an unselected parental model.",
    "The resistant material was a drug-selected derivative or stable resistant lineage, or clinical material explicitly described as resistant, relapsed, progressing, non-responsive, or post-treatment residual disease.",
    "The selecting drug or drug class aligned with the resistance claim; cross-resistance was not assumed when the selecting and tested drugs differed.",
    "The ferroptosis mechanism or ferroptosis-directed perturbation was evaluated in, or explicitly linked to, the acquired-resistant state.",
]:
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(2)
    p.add_run(item)
add_body(doc, "Reports were excluded when they contained only parental-model sensitivity, transient tolerance or persister states without a separately documented stable lineage, non-cytotoxic resistance, a drug-context mismatch, or an insufficient link between ferroptosis and the acquired-resistant state.")

add_heading(doc, "Supplementary Table S1. Prespecified operational decision structure", 2)
add_table(
    doc,
    ["Decision", "Operational meaning", "Consequence"],
    [
        ("Yes", "Strict acquired cytotoxic-resistance evidence was supported by the source record.", "Report enters the nominal strict denominator."),
        ("No", "One or more strict criteria were not met.", "Report receives one mutually exclusive exclusion code."),
        ("Unclear", "Available information was insufficient for Reviewer 2 to make a stable Yes/No call.", "Record is escalated to source adjudication."),
        ("Not coded", "Used only for the W93 publisher-status exception.", "Record is excluded from the agreement denominator and adjudicated separately."),
    ],
    [1.0, 4.7, 4.4],
    font_size=8.2,
    center_cols=(0,),
    header_fill=TEAL,
)

add_heading(doc, "S3.2 Agreement before adjudication", 2)
add_body(doc, "Exact agreement required the same Yes or No classification before adjudication. Reviewer 2 Unclear classifications counted as nonagreements. Because Reviewer 1 made no Unclear assignments, Cohen's kappa was treated as a secondary chance-corrected diagnostic rather than a measure of evidence strength.")
add_body(doc, "Among the 62 jointly coded reports, 45 were exact agreements (72.6%) and 17 were nonagreements (27.4%). The nonagreements comprised 11 opposite binary calls and six Reviewer 2 Unclear calls. Expected agreement was 53.5%; Cohen's kappa was 0.411.")
add_body(doc, "Observed agreement = (36 Yes/Yes + 9 No/No) / 62 = 0.7258. Expected agreement = [(41 × 44) + (21 × 12) + (0 × 6)] / 62² = 0.5349. Kappa = (0.7258 - 0.5349) / (1 - 0.5349) = 0.4105.")

coverage_rows = [
    ("Candidate reports", "63", "Deduplicated records entering the targeted audit"),
    ("Jointly coded", "62 (98.4%)", "W93 was handled as a source-verification exception"),
    ("Reviewer 2 full-text checks", "33/62 (53.2%)", "Other calls used available abstracts or metadata and could be escalated"),
    ("Exact agreement", "45/62 (72.6%)", "36 Yes/Yes plus 9 No/No"),
    ("Nonagreement", "17/62 (27.4%)", "11 binary disagreements plus 6 Unclear classifications"),
    ("Expected agreement", "53.5%", "Expectation from the marginal decision distributions"),
    ("Cohen's kappa", "0.411", "Secondary pre-adjudication agreement diagnostic"),
]
add_heading(doc, "Supplementary Table S2. Review coverage and pre-adjudication agreement", 2)
add_table(doc, ["Measure", "Value", "Interpretation"], coverage_rows, [2.7, 1.5, 5.9], font_size=8.0, center_cols=(1,))

cross_rows = [
    ("Reviewer 1 Yes", 36, 3, 2, 41),
    ("Reviewer 1 No", 8, 9, 4, 21),
    ("Column total", 44, 12, 6, 62),
]
add_heading(doc, "Supplementary Table S3. Reviewer cross-tabulation before adjudication", 2)
add_table(doc, ["Reviewer 1", "Reviewer 2 Yes", "Reviewer 2 No", "Reviewer 2 Unclear", "Row total"], cross_rows, [2.3, 1.8, 1.8, 2.2, 1.5], font_size=8.2, center_cols=(1,2,3,4), header_fill=TEAL)

add_heading(doc, "S3.3 Source adjudication", 2)
add_body(doc, "All 17 pre-adjudication nonagreements were resolved against the same operational rule using the primary article, methods, supplementary material, or other source-level evidence as required. W93 underwent publisher-status and full-text verification outside the agreement denominator. Publisher verification identified an active version of record with no retraction notice, and the full text documented MDA-MB-231/DOX and MDA-MB-468/DOX derivatives generated by escalating doxorubicin exposure over 10 months.")
add_body(doc, "Adjudication changed six individual memberships: R39, R66, and R74 entered the strict set, whereas R42, R60, and R61 left it. The equal three-in/three-out exchange left the final total unchanged but altered the composition of the evidence base.")

def adjudication_effect(row):
    rid = row["Audit_ID"]
    if rid in dual_summary["changed_into_strict_set"]:
        return "Entered"
    if rid in dual_summary["changed_out_of_strict_set"]:
        return "Left"
    if rid == "W93":
        return "Exception -> Yes"
    return f"Retained {row['Final_adjudicated_status']}"

adjudication_rows = []
for row in dual["adjudication_log"]:
    adjudication_rows.append((
        row["Audit_ID"],
        row["Reviewer_1_decision"],
        row["Reviewer_2_decision"],
        row["Reviewer_2_source_depth"].replace("Abstract or metadata", "Abstract/metadata"),
        row["Final_adjudicated_status"],
        adjudication_effect(row),
        row["Adjudication_basis"],
        row["DOI"],
    ))
add_heading(doc, "Supplementary Table S4. Nonagreements and the W93 source-verification exception", 2)
add_table(
    doc,
    ["ID", "R1", "R2", "R2 source", "Final", "Effect", "Source-adjudicated basis", "DOI"],
    adjudication_rows,
    [0.45, 0.42, 0.55, 0.85, 0.50, 0.85, 5.1, 1.4],
    font_size=6.7,
    center_cols=(0,1,2,4,5),
    header_fill=TEAL,
)

add_heading(doc, "S3.4 Final denominator and exclusion taxonomy", 2)
add_body(doc, "After source adjudication, 42 reports formed the nominal strict acquired-resistance denominator and 21 were excluded. Every excluded report received one mutually exclusive category. Eligibility was resolved before claim assignment and before correction for shared team or model lineage.")
changed_basis = {
    "R39": "Post-doxorubicin resistant or early-relapse clinical material was linked to the ferroptosis mechanism.",
    "R66": "Post-paclitaxel resistant clinical material was linked to CD24/STT3-mediated ferroptosis suppression.",
    "R74": "Clinical non-response after carboplatin-paclitaxel therapy was linked to the THEM6-FDFT1 mechanism.",
    "R42": "Parental models only; no acquired-resistant lineage or resistant clinical material was documented.",
    "R60": "Parental tumor models only; no acquired-resistant derivative or resistant clinical material was documented.",
    "R61": "A resistant line was mentioned, but causal linkage to acquired resistance and lineage provenance were unresolved.",
}
by_id = {r["Audit_ID"]: r for r in dual["adjudication_log"]}
changed_rows = []
for rid in dual_summary["changed_into_strict_set"]:
    row = by_id[rid]
    changed_rows.append((rid, f"{row['Reviewer_1_decision']} -> {row['Final_adjudicated_status']}", "Entered strict set", changed_basis[rid]))
for rid in dual_summary["changed_out_of_strict_set"]:
    row = by_id[rid]
    changed_rows.append((rid, f"{row['Reviewer_1_decision']} -> {row['Final_adjudicated_status']}", "Left strict set", changed_basis[rid]))
add_heading(doc, "Supplementary Table S5. Reports whose membership changed after adjudication", 2)
add_table(doc, ["ID", "Decision change", "Effect", "Source-adjudicated basis"], changed_rows, [0.7, 1.6, 1.6, 6.2], font_size=8.0, center_cols=(0,1,2))

exclusion_rows = []
for code, definition in dual["exclusion_categories"].items():
    ids = [r["Audit_ID"] for r in dual["final_excluded"] if r["Exclusion_code"] == code]
    exclusion_rows.append((code, dual_summary["exclusion_category_counts"][code], definition, ", ".join(ids)))
add_heading(doc, "Supplementary Table S6. Mutually exclusive final exclusion categories", 2)
add_table(doc, ["Code", "n", "Definition", "Audit IDs"], exclusion_rows, [0.65, 0.45, 5.6, 3.4], font_size=8.0, center_cols=(0,1), header_fill=TEAL)

add_body(doc, "The dual-review stage establishes which reports belong in the experimental audit; it does not establish independent replication. The 42 strict reports were subsequently assigned to 20 mechanism-drug-subtype claim cells and corrected for shared team and model lineages. The complete 63-record decisions and adjudication log are provided in S1 Data.")

add_heading(doc, "S4. Claim-level dependency correction", 1)
add_body(doc, "The 42 strict reports were assigned to 20 mechanism-drug-subtype claim cells. Within each claim, maximum bipartite matching retained the largest set of report contributions that shared neither a canonical team lineage nor a canonical model/provenance lineage. The conservative primary analysis yielded 37 claim-specific independent units; splitting only unresolved model labels by report yielded an upper bound of 39.")
add_heading(doc, "Supplementary Table S7. Complete claim-level evidence matrix", 2)
add_body(doc, "Retention equals primary independent units divided by nominal strict reports within a claim. T2/T3 units are counted after the same team–model matching constraint. Evidence levels are claim-level summaries, not effect-size grades.")
s1_rows = []
for r in claim_rows:
    s1_rows.append((
        r["Claim_ID"], r["Mechanism"], r["Drug_class"], r["Subtype"], r["Strict_reports"],
        r["Distinct_teams"], r["Conservative_model_lineages"], r["Independent_units_primary"],
        f"{100*r['Primary_retention_fraction']:.1f}%", r["Aligned_T2_T3_units_primary"], r["Evidence_level_primary"]
    ))
add_table(doc,
          ["ID", "Mechanism", "Drug", "Subtype", "Reports", "Teams", "Models", "Independent", "Retained", "T2/T3", "Level"],
          s1_rows, [0.42, 1.55, 0.85, 1.15, 0.62, 0.55, 0.6, 0.72, 0.68, 0.55, 0.52],
          font_size=7.6, center_cols=(0,4,5,6,7,8,9,10))

add_heading(doc, "S4.1 Interpretation of the claim matrix", 2)
add_body(doc, "Seven claims reached E4, two reached E3, and eleven remained E1; none was E2. The global dependency correction was numerically modest (42 nominal strict reports to 37 conservative independent units), but the claim distribution was highly fragmented. Eleven of twenty claims were single-lineage observations. The most defensible conclusions therefore concern the small set of multi-report claims with cross-team, cross-model, and aligned T2/T3 support, not a field-wide assertion that ferroptosis reverses all forms of breast-cancer chemoresistance.")

add_heading(doc, "S5. Canonical lineages and final evidence distribution", 1)
add_heading(doc, "Supplementary Table S8. Report-level canonical lineage crosswalk", 2)
add_body(doc, "Each row is one strict acquired-resistance report after source adjudication. Canonical labels are analytic identifiers rather than claims that the original authors used identical nomenclature. ‘Unresolved’ provenance is deliberately merged in the primary analysis and split only in the deterministic sensitivity analysis.")
s2_rows = []
for r in lineage_rows:
    title = r["Title"]
    if len(title) > 90:
        title = title[:87].rstrip() + "…"
    claim = f"{r['Final_mechanism']} | {r['Final_drug']} | {r['Final_subtype']}"
    provenance = r.get("Model_provenance_status", "")
    s2_rows.append((r["Audit_ID"], r["DOI"], title, r["Final_team"], r["Final_models"], r["Final_tier"], claim, provenance))
add_table(doc,
          ["Audit", "DOI", "Report", "Canonical team", "Canonical model/provenance", "Tier", "Claim", "Provenance status"],
          s2_rows, [0.45, 1.25, 2.05, 1.35, 1.65, 0.42, 1.75, 1.12],
          font_size=6.9, center_cols=(0,5))

add_heading(doc, "Supplementary Table S9. Final evidence distribution", 2)
dist_rows = [
    ("Translation tier", "T0 / T1 / T2 / T3", f"{summary['tier_counts']['T0']} / {summary['tier_counts']['T1']} / {summary['tier_counts']['T2']} / {summary['tier_counts']['T3']}"),
    ("Mechanism", "GPX4/xCT/redox; iron/ferritinophagy; other target; microenvironment; FSP1", "25; 11; 4; 1; 1"),
    ("Drug class", "Anthracycline; platinum; taxane; multidrug", "20; 11; 7; 4"),
    ("Subtype", "TNBC; mixed/unspecified; luminal/ER-positive", "21; 15; 6"),
    ("Evidence level", "E1 / E2 / E3 / E4", "11 / 0 / 2 / 7 claims"),
]
add_table(doc, ["Dimension", "Categories", "Counts"], dist_rows, [1.5, 6.7, 1.9], font_size=8.6, center_cols=(2,))

add_heading(doc, "S6. Reproducibility package", 1)
add_heading(doc, "Supplementary Table S10. Locked implementation and file locations", 2)
check_rows = [
    ("Candidate denominator", "63 deduplicated reports", "S1 Data: Overview and Record decisions"),
    ("Eligibility decisions", "Independent review for 62 reports; W93 exception documented", "S1 Data: Record decisions and Adjudication log"),
    ("Agreement calculation", "45/62 exact agreements; kappa 0.411", "S1 Data: formula-driven Overview"),
    ("Canonical lineage lock", "42 strict reports; 38 teams; 45 conservative model/provenance lineages", "S2 Data: Lineage crosswalk"),
    ("Claim denominator", "20 mechanism-drug-subtype units", "S2 Data: Claim evidence"),
    ("Primary dependency correction", "Claim-specific maximum bipartite matching", "S4 Data: Final claim evidence table"),
    ("Provenance sensitivity", "Unresolved model labels split by report only", "S3 Data: Final lineage crosswalk"),
    ("Machine-readable summary", "Counts, distributions, and rules", "S5 Data: JSON summary"),
    ("Record flow", "442 mapped records; 63 reconciled candidates; 42 strict reports", "S1 Fig: modified PRISMA 2020 flow"),
    ("Visual synthesis", "Eligibility, fragmentation, retention, and claim levels", "Main Figure 6: TIFF and PDF"),
]
add_table(doc, ["Audit element", "Locked implementation", "Location"], check_rows, [2.35, 4.9, 2.85], font_size=8.4)

add_heading(doc, "S6.1 Files supplied with the submission package", 2)
files = [
    "S1 Appendix: S1_Appendix_Integrated_Dependency_Adjusted_Evidence_Audit_FINAL.pdf — integrated methods, eligibility adjudication, lineage audit, claim matrix, and interpretation boundaries.",
    "S1 Data: S1_Data_Dual_Reviewer_Eligibility_and_Adjudication.xlsx — all 63 record-level decisions, the 18-record adjudication log, the 42 strict inclusions, the 21 exclusions, and the operational codebook.",
    "S2 Data: Dependency_Adjusted_Evidence_Audit_Final.xlsx — complete human-readable dependency audit and source reconciliation workbook.",
    "S3 Data: Final_Lineage_Crosswalk.csv — report-level canonical team and model/provenance assignments.",
    "S4 Data: Final_Claim_Evidence_Table.csv — complete 20-claim dependency-adjusted evidence matrix.",
    "S5 Data: Final_Dependency_Audit_Summary.json — machine-readable locked counts and analysis rules.",
    "S1 Fig: S1_Fig_Modified_PRISMA_2020_Flow.tiff — modified PRISMA 2020 flow separating the structural-mapping corpus from the strict evidence-audit denominator; vector PDF is also supplied.",
    "Main Figure 6: Figure_6_Dependency_Adjusted_Evidence_Thickness_FINAL.tiff — publication-resolution evidence-thickness figure; PDF is supplied for vector review.",
    "Code repository — versioned scripts for reconciliation, agreement calculation, lineage matching, sensitivity analysis, and figure regeneration.",
]
for item in files:
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(2)
    p.add_run(item)

add_heading(doc, "S7. Interpretive guardrails", 1)
guardrails = [
    "A shared cited reference demonstrates common intellectual infrastructure, not independent experimental validation.",
    "A common parental cell line does not prove model dependence; a named derivative also does not prove independence without derivation or source information.",
    "The primary estimate is deliberately conservative where provenance is unresolved; the sensitivity estimate is an upper bound, not a probabilistic interval.",
    "Evidence levels describe replication breadth and aligned translational support, not therapeutic effect magnitude, clinical efficacy, or certainty of benefit.",
    "Singleton E1 claims remain hypothesis-generating even when their individual experiments are technically strong.",
]
for item in guardrails:
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(2)
    p.add_run(item)

# Keep metadata lean and reproducible.
props = doc.core_properties
props.title = "Supplementary Appendix: Dependency-Adjusted Evidence Audit"
props.subject = "Breast cancer ferroptosis and cytotoxic chemotherapy resistance"
props.author = ""
props.last_modified_by = ""
props.keywords = "ferroptosis; breast cancer; acquired resistance; dependency-adjusted evidence; meta-research"

doc.save(OUTFILE)
print(OUTFILE)
