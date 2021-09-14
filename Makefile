README.md: README.Rmd
	R -e "knitr::knit('$<')"
