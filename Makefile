README.md: README.Rmd uw_covid_2022.csv
	R -e "knitr::knit('$<')"

uw_covid_2022.csv: scrape_data.py
	./scrape_data.py

clean:
	rm uw_covid_2022.csv README.md bar_plots-1.svg
