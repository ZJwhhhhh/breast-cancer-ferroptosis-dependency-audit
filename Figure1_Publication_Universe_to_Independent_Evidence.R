# Figure 1. From publication universe to independent evidence units
# Standalone, publication-quality flow diagram using base R grid graphics.
# Outputs: 600-dpi PNG, 600-dpi LZW TIFF, vector PDF, and vector SVG.

library(grid)

# -----------------------------------------------------------------------------
# 1. Output settings
# -----------------------------------------------------------------------------

output_directory <- file.path(getwd(), "Figure1_R_output")
dir.create(output_directory, recursive = TRUE, showWarnings = FALSE)

fig_width  <- 12.0
fig_height <- 7.4

png_file <- file.path(
  output_directory,
  "Figure_1_Publication_Universe_to_Independent_Evidence_600dpi.png"
)
tiff_file <- file.path(
  output_directory,
  "Figure_1_Publication_Universe_to_Independent_Evidence_600dpi.tiff"
)
pdf_file <- file.path(
  output_directory,
  "Figure_1_Publication_Universe_to_Independent_Evidence_VECTOR.pdf"
)
svg_file <- file.path(
  output_directory,
  "Figure_1_Publication_Universe_to_Independent_Evidence_VECTOR.svg"
)

# -----------------------------------------------------------------------------
# 2. Palette
# -----------------------------------------------------------------------------

navy       <- "#102F49"
blue       <- "#225C78"
teal       <- "#276F64"
orange     <- "#B96D2E"
light_gray <- "#E9ECEA"
mid_gray   <- "#7C827E"
dark_gray  <- "#30383D"
line_gray  <- "#6D7478"
paper      <- "#FCFCF9"
white      <- "#FFFFFF"

base_family <- "sans"

# -----------------------------------------------------------------------------
# 3. Reusable grobs
# -----------------------------------------------------------------------------

node_grob <- function(
  x, y, width, height, fill,
  number, title, subtitle,
  number_colour = white,
  title_colour = white,
  subtitle_colour = "#DCE5E8",
  border_colour = NA
) {
  grobTree(
    roundrectGrob(
      x = unit(x, "npc"), y = unit(y, "npc"),
      width = unit(width, "npc"), height = unit(height, "npc"),
      r = unit(0.10, "inches"),
      gp = gpar(
        fill = fill, col = border_colour,
        lwd = if (is.na(border_colour)) 0 else 1.2
      )
    ),
    textGrob(
      number,
      x = unit(x, "npc"), y = unit(y + height * 0.23, "npc"),
      gp = gpar(
        fontfamily = base_family, fontface = "bold",
        fontsize = 22, col = number_colour
      )
    ),
    textGrob(
      title,
      x = unit(x, "npc"), y = unit(y - height * 0.02, "npc"),
      gp = gpar(
        fontfamily = base_family, fontface = "bold",
        fontsize = 11.2, col = title_colour
      )
    ),
    textGrob(
      subtitle,
      x = unit(x, "npc"), y = unit(y - height * 0.30, "npc"),
      gp = gpar(
        fontfamily = base_family,
        fontsize = 8.4, col = subtitle_colour
      )
    )
  )
}

source_card_grob <- function(x, y, width, height) {
  grobTree(
    roundrectGrob(
      x = unit(x, "npc"), y = unit(y, "npc"),
      width = unit(width, "npc"), height = unit(height, "npc"),
      r = unit(0.10, "inches"),
      gp = gpar(fill = light_gray, col = mid_gray, lwd = 1.2)
    ),
    textGrob(
      "44-study review table",
      x = unit(x, "npc"), y = unit(y + 0.020, "npc"),
      gp = gpar(
        fontfamily = base_family, fontface = "bold",
        fontsize = 12.2, col = dark_gray
      )
    ),
    textGrob(
      "32 overlapped the 118-Article corpus",
      x = unit(x, "npc"), y = unit(y - 0.026, "npc"),
      gp = gpar(
        fontfamily = base_family,
        fontsize = 8.9, col = line_gray
      )
    )
  )
}

arrow_grob <- function(
  x0, y0, x1, y1,
  colour = line_gray,
  linewidth = 1.25,
  arrow_size = 0.105
) {
  segmentsGrob(
    x0 = unit(x0, "npc"), y0 = unit(y0, "npc"),
    x1 = unit(x1, "npc"), y1 = unit(y1, "npc"),
    arrow = arrow(
      length = unit(arrow_size, "inches"),
      type = "closed"
    ),
    gp = gpar(col = colour, lwd = linewidth, lineend = "round")
  )
}

# -----------------------------------------------------------------------------
# 4. Complete figure grob
# -----------------------------------------------------------------------------

figure1 <- grobTree(
  # Background
  rectGrob(gp = gpar(fill = paper, col = NA)),

  # Main title and subtitle
  textGrob(
    "From publication universe to independent evidence units",
    x = unit(0.5, "npc"), y = unit(0.952, "npc"),
    gp = gpar(
      fontfamily = base_family, fontface = "bold",
      fontsize = 22, col = "#111111"
    )
  ),
  textGrob(
    paste0(
      "Structural maps define the field; source adjudication and provenance ",
      "define evidence thickness"
    ),
    x = unit(0.5, "npc"), y = unit(0.913, "npc"),
    gp = gpar(
      fontfamily = base_family,
      fontsize = 10.6, col = line_gray
    )
  ),

  # Section labels
  textGrob(
    "STRUCTURAL CONTEXT",
    x = unit(0.075, "npc"), y = unit(0.812, "npc"),
    just = c("left", "centre"),
    gp = gpar(
      fontfamily = base_family, fontface = "bold",
      fontsize = 11.5, col = dark_gray
    )
  ),
  textGrob(
    "PRIMARY EVIDENCE AUDIT",
    x = unit(0.075, "npc"), y = unit(0.495, "npc"),
    just = c("left", "centre"),
    gp = gpar(
      fontfamily = base_family, fontface = "bold",
      fontsize = 11.5, col = teal
    )
  ),

  # Connectors are drawn before nodes so that they remain behind boxes.
  arrow_grob(0.267, 0.690, 0.293, 0.690),
  arrow_grob(0.487, 0.690, 0.513, 0.690),
  arrow_grob(0.297, 0.340, 0.317, 0.340),
  arrow_grob(0.543, 0.340, 0.577, 0.340),
  arrow_grob(0.783, 0.340, 0.807, 0.340),

  # Two source streams converge on the 63-report audit set.
  arrow_grob(
    0.610, 0.604, 0.205, 0.426,
    colour = teal, linewidth = 1.45, arrow_size = 0.115
  ),
  arrow_grob(
    0.860, 0.620, 0.235, 0.426,
    colour = mid_gray, linewidth = 1.20, arrow_size = 0.105
  ),

  # Structural context nodes
  node_grob(
    x = 0.170, y = 0.690, width = 0.190, height = 0.160,
    fill = navy,
    number = "442",
    title = "records screened",
    subtitle = "Web of Science universe"
  ),
  node_grob(
    x = 0.390, y = 0.690, width = 0.190, height = 0.160,
    fill = blue,
    number = "135",
    title = "mapped publications",
    subtitle = "118 Articles + 17 Reviews"
  ),
  node_grob(
    x = 0.610, y = 0.690, width = 0.190, height = 0.160,
    fill = teal,
    number = "118",
    title = "primary Articles",
    subtitle = "experimental literature"
  ),
  source_card_grob(
    x = 0.860, y = 0.690,
    width = 0.220, height = 0.125
  ),

  # Primary evidence audit nodes
  node_grob(
    x = 0.190, y = 0.340, width = 0.210, height = 0.165,
    fill = navy,
    number = "63",
    title = "unique candidates",
    subtitle = "DOI reconciliation + prescreening"
  ),
  node_grob(
    x = 0.430, y = 0.340, width = 0.220, height = 0.165,
    fill = teal,
    number = "42",
    title = "strict acquired resistance",
    subtitle = "21 context / excluded"
  ),
  node_grob(
    x = 0.680, y = 0.340, width = 0.200, height = 0.165,
    fill = blue,
    number = "20",
    title = "claim units",
    subtitle = "mechanism × drug × subtype"
  ),
  node_grob(
    x = 0.900, y = 0.340, width = 0.180, height = 0.165,
    fill = orange,
    number = "37",
    title = "independent units",
    subtitle = "39 in split-unresolved sensitivity"
  ),

  # Interpretive note
  textGrob(
    paste0(
      "The 37-unit result is the sum of claim-specific maximum team–model matchings;\n",
      "it is not a count of 37 unique laboratories."
    ),
    x = unit(0.5, "npc"), y = unit(0.125, "npc"),
    gp = gpar(
      fontfamily = base_family,
      fontsize = 9.8, col = dark_gray,
      lineheight = 1.05
    )
  )
)

# -----------------------------------------------------------------------------
# 5. Drawing and export helpers
# -----------------------------------------------------------------------------

draw_figure1 <- function() {
  grid.newpage()
  grid.draw(figure1)
}

# Vector PDF
if (capabilities("cairo")) {
  grDevices::cairo_pdf(
    filename = pdf_file,
    width = fig_width, height = fig_height,
    family = base_family, bg = paper
  )
} else {
  grDevices::pdf(
    file = pdf_file,
    width = fig_width, height = fig_height,
    family = base_family, bg = paper,
    useDingbats = FALSE
  )
}
draw_figure1()
grDevices::dev.off()

# 600-dpi PNG
if (requireNamespace("ragg", quietly = TRUE)) {
  ragg::agg_png(
    filename = png_file,
    width = fig_width, height = fig_height,
    units = "in", res = 600,
    background = paper
  )
} else {
  grDevices::png(
    filename = png_file,
    width = fig_width, height = fig_height,
    units = "in", res = 600,
    bg = paper
  )
}
draw_figure1()
grDevices::dev.off()

# 600-dpi LZW TIFF
grDevices::tiff(
  filename = tiff_file,
  width = fig_width, height = fig_height,
  units = "in", res = 600,
  compression = "lzw", bg = paper
)
draw_figure1()
grDevices::dev.off()

# Vector SVG, when supported by the local R installation.
if (capabilities("cairo")) {
  grDevices::svg(
    filename = svg_file,
    width = fig_width, height = fig_height,
    family = base_family, bg = paper
  )
  draw_figure1()
  grDevices::dev.off()
}

# Preview in the RStudio plot device.
draw_figure1()

cat("\nFigure 1 files saved to:\n", normalizePath(output_directory), "\n")
cat("PNG :", png_file, "\n")
cat("TIFF:", tiff_file, "\n")
cat("PDF :", pdf_file, "\n")
if (file.exists(svg_file)) cat("SVG :", svg_file, "\n")

