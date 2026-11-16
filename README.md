# Reproducibility environment

Run the following commands on the original analysis computer and save the output in this folder:

```r
sessionInfo()
installed.packages()[, c("Package", "Version")]
getwd()
```

Save `sessionInfo()` as `R_sessionInfo.txt` and the package table as `R_package_versions.csv`. Remove the local working-directory line before public release if it contains a username.

Also record the installed versions of VOSviewer, CiteSpace, RStudio, Java, Python, and the operating system in `software_versions.md`.

