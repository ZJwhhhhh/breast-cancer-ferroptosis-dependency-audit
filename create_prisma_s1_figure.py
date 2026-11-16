#!/usr/bin/env python3
"""Create a publication-ready modified PRISMA flow for the evidence audit."""

from pathlib import Path
import textwrap

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


ROOT = Path("/workspace/scratch/e3addee252de")
OUT = ROOT / "outputs/integrated_submission_20261115/Supporting_Information"
OUT.mkdir(parents=True, exist_ok=True)

NAVY = "#173B57"
BLUE = "#2B6387"
TEAL = "#2F7B70"
ORANGE = "#E9A72C"
PALE = "#F5F7F8"
GRAY = "#6B7280"
INK = "#18212A"


def wrap(text: str, width: int) -> str:
    return "\n".join(textwrap.wrap(text, width=width, break_long_words=False))


def box(ax, x, y, w, h, text, *, edge=NAVY, fill="white", fontsize=8.2,
        bold=False, text_color=INK, radius=0.012, lw=1.25):
    wrap_width = max(14, int(w * 128))
    text = "\n".join(
        wrapped
        for line in text.split("\n")
        for wrapped in (textwrap.wrap(line, width=wrap_width, break_long_words=False) or [""])
    )
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.008,rounding_size={radius}",
        linewidth=lw, edgecolor=edge, facecolor=fill,
    )
    ax.add_patch(patch)
    ax.text(
        x + w / 2, y + h / 2, text,
        ha="center", va="center", fontsize=fontsize, color=text_color,
        fontweight="bold" if bold else "normal", linespacing=1.15,
    )
    return patch


def arrow(ax, x1, y1, x2, y2, *, color=GRAY, lw=1.3):
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=11,
        linewidth=lw, color=color, shrinkA=3, shrinkB=3,
        connectionstyle="arc3,rad=0",
    ))


fig, ax = plt.subplots(figsize=(11.4, 8.5))
fig.patch.set_facecolor("white")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

ax.text(
    0.5, 0.975,
    "Modified PRISMA 2020 flow: corpus formation and evidence-audit eligibility",
    ha="center", va="top", fontsize=13.4, fontweight="bold", color=INK,
)
ax.text(
    0.5, 0.943,
    "Structural mapping and the strict acquired-resistance audit use distinct denominators",
    ha="center", va="top", fontsize=8.6, color=GRAY,
)

box(ax, 0.05, 0.868, 0.54, 0.042,
    "Identification and screening via Web of Science Core Collection",
    edge=ORANGE, fill=ORANGE, fontsize=9.3, bold=True, text_color="white", radius=0.008)
box(ax, 0.64, 0.868, 0.31, 0.042,
    "Identification via other methods",
    edge=ORANGE, fill=ORANGE, fontsize=9.3, bold=True, text_color="white", radius=0.008)

# Database pathway
box(ax, 0.06, 0.790, 0.28, 0.072,
    "Records identified from Web of Science Core Collection\n(n = 442)")
box(ax, 0.39, 0.790, 0.19, 0.072,
    "Removed before screening\nDuplicates (n = 0)\nOther reasons (n = 0)",
    edge=GRAY, fill=PALE, fontsize=7.5)

box(ax, 0.06, 0.670, 0.28, 0.072, "Records screened\n(n = 442)")
box(ax, 0.39, 0.670, 0.19, 0.072,
    "Excluded after title/abstract and scope screening\n(n = 307)",
    edge=GRAY, fill=PALE, fontsize=7.6)

box(ax, 0.06, 0.550, 0.28, 0.072,
    "Publications retained for structural mapping\n(n = 135)",
    edge=BLUE, fill="#EAF2F7")
box(ax, 0.39, 0.550, 0.19, 0.072,
    "Reviews retained for structural mapping only\n(n = 17)",
    edge=GRAY, fill=PALE, fontsize=7.6)

box(ax, 0.06, 0.430, 0.28, 0.072,
    "Original Articles entering evidence-audit prescreening\n(n = 118)",
    edge=TEAL, fill="#E8F3F0")
box(ax, 0.39, 0.430, 0.19, 0.072,
    "Not meeting targeted evidence-candidate criteria\n(n = 67)",
    edge=GRAY, fill=PALE, fontsize=7.6)

box(ax, 0.06, 0.310, 0.28, 0.072,
    "Candidate reports from the Web of Science Article corpus\n(n = 51)",
    edge=NAVY, fill="#EAF0F5")

# Other-source pathway
box(ax, 0.655, 0.790, 0.28, 0.072,
    "Published 2026 systematic-review evidence table\n(n = 44)")
box(ax, 0.655, 0.670, 0.28, 0.072,
    "Reports cross-matched against the Web of Science Article corpus by DOI\n(n = 44)",
    fontsize=7.7)
box(ax, 0.655, 0.550, 0.28, 0.072,
    "Reports overlapping the Web of Science Article corpus\n(n = 32)",
    edge=GRAY, fill=PALE)
box(ax, 0.655, 0.430, 0.28, 0.072,
    "Additional unique reports outside the Web of Science corpus\n(n = 12)",
    edge=TEAL, fill="#E8F3F0")

# Merge and final eligibility
box(ax, 0.37, 0.225, 0.27, 0.076,
    "Reconciled unique candidate reports\n51 + 12 = 63",
    edge=NAVY, fill=NAVY, fontsize=9.1, bold=True, text_color="white")
box(ax, 0.225, 0.090, 0.25, 0.082,
    "Strict acquired-resistance reports included\n(n = 42)",
    edge=TEAL, fill=TEAL, fontsize=8.8, bold=True, text_color="white")
box(ax, 0.525, 0.090, 0.25, 0.082,
    "Context-only or claim-mismatched reports excluded\n(n = 21)",
    edge=GRAY, fill="#A7A9AC", fontsize=8.4, bold=True, text_color="white")

# Arrows: database pathway
arrow(ax, 0.20, 0.790, 0.20, 0.742)
arrow(ax, 0.20, 0.670, 0.20, 0.622)
arrow(ax, 0.20, 0.550, 0.20, 0.502)
arrow(ax, 0.20, 0.430, 0.20, 0.382)
arrow(ax, 0.34, 0.826, 0.39, 0.826)
arrow(ax, 0.34, 0.706, 0.39, 0.706)
arrow(ax, 0.34, 0.586, 0.39, 0.586)
arrow(ax, 0.34, 0.466, 0.39, 0.466)

# Arrows: other pathway
arrow(ax, 0.795, 0.790, 0.795, 0.742)
arrow(ax, 0.795, 0.670, 0.795, 0.622)
arrow(ax, 0.795, 0.550, 0.795, 0.502)

# Merge arrows and final split
arrow(ax, 0.34, 0.346, 0.43, 0.301)
arrow(ax, 0.655, 0.466, 0.60, 0.301)
arrow(ax, 0.505, 0.225, 0.355, 0.172)
arrow(ax, 0.505, 0.225, 0.645, 0.172)

ax.text(
    0.5, 0.038,
    "The 42-report denominator is the locked strict-eligibility set used for team–model dependency correction.",
    ha="center", va="center", fontsize=7.6, color=GRAY,
)

base = OUT / "S1_Fig_Modified_PRISMA_2020_Flow"
fig.savefig(base.with_suffix(".pdf"), bbox_inches="tight", facecolor="white")
fig.savefig(base.with_suffix(".png"), dpi=600, bbox_inches="tight", facecolor="white")
fig.savefig(base.with_suffix(".tiff"), dpi=600, bbox_inches="tight", facecolor="white",
            pil_kwargs={"compression": "tiff_lzw"})
plt.close(fig)
print(base)
