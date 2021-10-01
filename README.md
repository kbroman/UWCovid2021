## UW-Madison COVID data, Fall 2021

Plot of data from the [UW-Madison COVID
dashboard](https://covidresponse.wisc.edu/dashboard/) from Fall, 2021,
scraped into [`uw_covid_2021.csv`](uw_covid_2021.csv) using a python
script based on the
[gist](https://gist.github.com/dgfitch/b6ca1cc61b4795e698cefdf672a90f23)
from [Dan Fitch](https://github.com/dgfitch).

Here, just calculating and plotting the test positivity;
the curves are 7-day running averages.
The shaded regions are pointwise 95% confidence intervals on the 7-day
running averages.
The source is in [`README.Rmd`](README.Rmd).









![plot of chunk bar_plots](bar_plots-1.svg)
