README.md: README.Rmd uw_covid_2021.csv
	R -e "knitr::knit('$<')"

uw_covid_2021.csv:
	./scrape_data.py
