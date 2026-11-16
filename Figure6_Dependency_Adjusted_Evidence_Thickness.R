# Figure 6: Dependency-adjusted evidence thickness
# Locked results from the final dual-review evidence audit (2026-11-01)
# Outputs: 600-dpi PNG, 600-dpi LZW TIFF, vector PDF, and optional SVG

required_packages <- c("ggplot2", "patchwork")
missing_packages <- required_packages[
  !vapply(required_packages, requireNamespace, logical(1), quietly = TRUE)
]

if (length(missing_packages) > 0) {
  install.packages(missing_packages)
}

library(ggplot2)
library(patchwork)

# Remove any previously constructed version of Figure 6 from the current
# RStudio session. This prevents an old annotated object from being reprinted.
old_figure_objects <- intersect(
  c("pA", "pB", "pC", "figure6"),
  ls(envir = .GlobalEnv)
)
if (length(old_figure_objects) > 0) {
  rm(list = old_figure_objects, envir = .GlobalEnv)
}

# -----------------------------------------------------------------------------
# 1. Locked data
# -----------------------------------------------------------------------------

claim_data <- data.frame(
  claim = c(
    "GPX4/xCT · platinum · TNBC",
    "GPX4/xCT · anthracycline · mixed",
    "GPX4/xCT · anthracycline · TNBC",
    "GPX4/xCT · taxane · TNBC",
    "Iron/ferritinophagy · anthracycline · mixed",
    "Iron/ferritinophagy · anthracycline · TNBC",
    "GPX4/xCT · anthracycline · luminal",
    "GPX4/xCT · multidrug · mixed",
    "Iron/ferritinophagy · taxane · TNBC"
  ),
  nominal = c(7, 6, 3, 3, 3, 3, 2, 2, 2),
  independent = c(5, 4, 3, 3, 2, 3, 2, 2, 2),
  stringsAsFactors = FALSE
)

# Preserve the intended top-to-bottom order.
claim_data$claim <- factor(
  claim_data$claim,
  levels = rev(claim_data$claim)
)

level_data <- data.frame(
  level = factor(c("E1", "E2", "E3", "E4"),
                 levels = c("E1", "E2", "E3", "E4")),
  n = c(11, 0, 2, 7)
)

# -----------------------------------------------------------------------------
# 2. Publication palette and shared theme
# -----------------------------------------------------------------------------

navy     <- "#173B5E"
blue     <- "#2A5D84"
teal     <- "#34776C"
gold     <- "#E5A62F"
gray     <- "#A5A7AA"
lightbar <- "#D9E1E6"
lightbox <- "#EFF3F5"
darkgray <- "#4C5157"
gridgray <- "#E3E6E8"

base_family <- "sans"

theme_publication <- theme_minimal(base_family = base_family, base_size = 10.5) +
  theme(
    plot.title = element_text(
      face = "bold", size = 13.0, colour = "#111111",
      margin = margin(b = 8)
    ),
    axis.title = element_text(colour = "#111111"),
    axis.text = element_text(colour = "#111111"),
    panel.grid.minor = element_blank(),
    panel.grid.major = element_line(colour = gridgray, linewidth = 0.45),
    plot.margin = margin(8, 10, 8, 10)
  )

# -----------------------------------------------------------------------------
# 3. Panel A: eligibility and adjudication
# -----------------------------------------------------------------------------

pA <- ggplot() +
  annotate(
    "rect", xmin = 0.35, xmax = 1.45, ymin = 1.10, ymax = 1.52,
    fill = navy, colour = NA
  ) +
  annotate(
    "rect", xmin = 1.85, xmax = 2.95, ymin = 1.10, ymax = 1.52,
    fill = teal, colour = NA
  ) +
  annotate(
    "rect", xmin = 3.35, xmax = 4.45, ymin = 1.10, ymax = 1.52,
    fill = gray, colour = NA
  ) +
  annotate(
    "segment", x = 1.48, xend = 1.80, y = 1.31, yend = 1.31,
    colour = darkgray, linewidth = 0.7,
    arrow = grid::arrow(length = grid::unit(0.13, "inches"), type = "closed")
  ) +
  annotate(
    "segment", x = 2.98, xend = 3.30, y = 1.31, yend = 1.31,
    colour = darkgray, linewidth = 0.7,
    arrow = grid::arrow(length = grid::unit(0.13, "inches"), type = "closed")
  ) +
  annotate(
    "text", x = c(0.90, 2.40, 3.90), y = 1.31,
    label = c("63", "42", "21"),
    colour = "white", size = 6.4, fontface = "bold", family = base_family
  ) +
  annotate(
    "text", x = c(0.90, 2.40, 3.90), y = 0.96,
    label = c("candidate reports", "strict reports", "context / excluded"),
    colour = darkgray, size = 3.15, fontface = "bold", family = base_family
  ) +
  annotate(
    "text", x = 0.35, y = 0.66,
    label = "Independent eligibility review",
    hjust = 0, colour = navy, size = 3.45, fontface = "bold",
    family = base_family
  ) +
  annotate(
    "text", x = 0.35, y = 0.39,
    label = "62 coded  •  45 exact agreements (72.6%)  •  kappa = 0.411",
    hjust = 0, colour = darkgray, size = 3.05, family = base_family
  ) +
  coord_cartesian(xlim = c(0.20, 4.60), ylim = c(0.18, 1.62), clip = "off") +
  labs(title = "A  Eligibility and adjudication") +
  theme_void(base_family = base_family, base_size = 10.5) +
  theme(
    plot.title = element_text(
      face = "bold", size = 12.5, colour = "#111111",
      margin = margin(b = 8)
    ),
    plot.margin = margin(5, 10, 5, 10)
  )

# -----------------------------------------------------------------------------
# 4. Panel B: nominal strict reports versus independent units
# -----------------------------------------------------------------------------

pB <- ggplot(claim_data, aes(y = claim)) +
  geom_col(
    aes(x = nominal, fill = "Nominal strict reports"),
    width = 0.68, colour = NA
  ) +
  geom_col(
    aes(x = independent, fill = "Independent units (primary)"),
    width = 0.40, colour = NA
  ) +
  geom_text(
    aes(x = nominal, label = ifelse(nominal == independent, "", nominal)),
    hjust = -0.35, size = 3.20, colour = darkgray,
    family = base_family
  ) +
  geom_text(
    aes(x = independent, label = independent),
    hjust = 1.20, size = 3.20, colour = "white", fontface = "bold",
    family = base_family
  ) +
  scale_x_continuous(
    limits = c(0, 8.10), breaks = 0:8,
    expand = expansion(mult = c(0, 0.01))
  ) +
  scale_fill_manual(
    name = NULL,
    values = c(
      "Nominal strict reports" = lightbar,
      "Independent units (primary)" = blue
    ),
    breaks = c("Nominal strict reports", "Independent units (primary)")
  ) +
  labs(
    title = "B  Nominal reports versus independent units",
    x = NULL, y = NULL,
    caption = "Eleven additional claims were singletons (1 report = 1 independent unit each)."
  ) +
  theme_publication +
  theme(
    panel.grid.major.y = element_blank(),
    axis.ticks.y = element_blank(),
    axis.text.y = element_text(size = 8.6, margin = margin(r = 6)),
    axis.text.x = element_text(size = 9.0),
    legend.position = "bottom",
    legend.direction = "horizontal",
    legend.justification = "left",
    legend.box.just = "left",
    legend.text = element_text(size = 8.2),
    legend.key.height = grid::unit(0.30, "cm"),
    legend.key.width = grid::unit(0.50, "cm"),
    legend.margin = margin(0, 0, 0, 0),
    legend.box.margin = margin(-3, 0, -2, 0),
    plot.caption = element_text(
      hjust = 0, size = 8.2, colour = darkgray,
      margin = margin(t = 5)
    ),
    plot.margin = margin(6, 14, 4, 10)
  )

# -----------------------------------------------------------------------------
# 5. Panel C: evidence levels
# -----------------------------------------------------------------------------

level_data$label_y <- ifelse(level_data$n == 0, 0.35, level_data$n + 0.35)

pC <- ggplot(level_data, aes(x = level, y = n, fill = level)) +
  geom_col(width = 0.63, colour = NA) +
  geom_text(
    aes(y = label_y, label = n),
    fontface = "bold", size = 4.6, family = base_family
  ) +
  scale_fill_manual(
    values = c(E1 = gold, E2 = gray, E3 = blue, E4 = teal),
    guide = "none"
  ) +
  scale_y_continuous(
    limits = c(0, 13.2), breaks = seq(0, 12, by = 2),
    expand = expansion(mult = c(0, 0))
  ) +
  labs(
    title = "C  Evidence level after dependency correction",
    x = NULL, y = "Claims (n = 20)"
  ) +
  theme_publication +
  theme(
    panel.grid.major.x = element_blank(),
    axis.text.x = element_text(size = 10.0),
    axis.text.y = element_text(size = 9.0),
    plot.margin = margin(6, 14, 2, 10)
  )

# -----------------------------------------------------------------------------
# 6. Assemble the three panels
# -----------------------------------------------------------------------------

figure6 <- (pA / pB / pC) +
  plot_layout(heights = c(1.60, 2.35, 1.15)) +
  plot_annotation(
    title = "Dependency-adjusted evidence thickness",
    subtitle = paste0(
      "Strict eligibility is separated from team-model independence ",
      "and translational alignment."
    ),
    caption = paste0(
      "Primary estimate: 37 claim-specific independent units from 42 strict reports (88.1%).\n",
      "Sensitivity upper bound after splitting unresolved models: 39 (92.9%).\n",
      "Sums across claim cells; not counts of unique laboratories."
    ),
    theme = theme(
      plot.title = element_text(
        family = base_family, face = "bold", size = 18.5,
        colour = "#111111", hjust = 0,
        margin = margin(b = 4)
      ),
      plot.subtitle = element_text(
        family = base_family, size = 10.5,
        colour = darkgray, hjust = 0,
        margin = margin(b = 14)
      ),
      plot.caption = element_text(
        family = base_family, size = 8.7,
        colour = darkgray, hjust = 0,
        lineheight = 1.05,
        margin = margin(t = 10)
      ),
      plot.margin = margin(18, 18, 14, 18)
    )
  )

# -----------------------------------------------------------------------------
# 7. Export: real raster resolution plus vector PDF
# -----------------------------------------------------------------------------

output_directory <- file.path(getwd(), "Figure6_R_output")
dir.create(output_directory, recursive = TRUE, showWarnings = FALSE)

# Fixed landscape dimensions. Keeping one pair of dimensions for every output
# guarantees that PNG, TIFF, PDF, and SVG retain the same layout.
fig_width  <- 11.5
fig_height <- 9.0

png_file <- file.path(
  output_directory,
    "Figure_6_FINAL_LANDSCAPE_600dpi.png"
)
tiff_file <- file.path(
  output_directory,
    "Figure_6_FINAL_LANDSCAPE_600dpi.tiff"
)
pdf_file <- file.path(
  output_directory,
    "Figure_6_FINAL_LANDSCAPE_VECTOR.pdf"
)

# If ragg is installed, it gives especially clean anti-aliased PNG text.
if (requireNamespace("ragg", quietly = TRUE)) {
  ggsave(
    png_file, figure6,
    device = ragg::agg_png,
    width = fig_width, height = fig_height, units = "in",
    dpi = 600, background = "white", limitsize = FALSE
  )
} else {
  ggsave(
    png_file, figure6,
    device = "png",
    width = fig_width, height = fig_height, units = "in",
    dpi = 600, bg = "white", limitsize = FALSE
  )
}

ggsave(
  tiff_file, figure6,
  device = "tiff",
  width = fig_width, height = fig_height, units = "in",
  dpi = 600, compression = "lzw",
  bg = "white", limitsize = FALSE
)

pdf_device <- if (capabilities("cairo")) grDevices::cairo_pdf else grDevices::pdf
ggsave(
  pdf_file, figure6,
  device = pdf_device,
  width = fig_width, height = fig_height, units = "in",
  bg = "white", limitsize = FALSE
)

# Optional SVG. Install svglite only if the target journal requests SVG.
if (requireNamespace("svglite", quietly = TRUE)) {
  svg_file <- file.path(
    output_directory,
    "Figure_6_FINAL_LANDSCAPE_VECTOR.svg"
  )
  ggsave(
    svg_file, figure6,
    device = svglite::svglite,
    width = fig_width, height = fig_height, units = "in",
    bg = "white", limitsize = FALSE
  )
}

print(figure6)
cat("\nFigure 6 files saved to:\n", normalizePath(output_directory), "\n")
cat("PNG :", png_file, "\n")
cat("TIFF:", tiff_file, "\n")
cat("PDF :", pdf_file, "\n")

