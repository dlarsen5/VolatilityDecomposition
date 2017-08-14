# Volatility Decomposition

Asset prices are usually modeled as a continuous diffusion process with random jumps. By decomposing a asset's
price variance into continuous and jump components, better risk management and asset allocation can be achieved.

In order to compute price variations, returns are first calculated and normalized by taking the logarithm of
price t and t-1:

(../Volatility Decomposition/Equation Images/Log Returns.png)

By recording a price time series at short time intervals (minute intervals used), the variation of an asset's price is
measured by looking at the sums of products of returns calculated over very small time periods, also known as Quadratic
Variation:

(../Volatility Decomposition/Equation Images/Quadratic Variation.png)

Realized variation (RV) is the also the sum of squared returns, which yields a similar measure of price variation:

(../Volatility Decomposition/Equation Images/Realized Variation.png)

As referenced in Barndorff-Nielsen, Bipower Variation (BV) is the sum of the product of absolute time series returns:

(../Volatility Decomposition/Equation Images/Bipower Variation.png)

BV differs from RV in that as sampling frequency increases, price jumps will not affect BV since at least one
of the returns will will shrink to zero as the sampling interval shrinks to zero.

The implication from this fact about BV is that the jump component of variance can be measured non-parametrically by
the difference between RV and BV, with the logarithm of RV and BV delivering more stable results
(Huang and Tauchen (2005)).

By comparing the continuous variation (BV) to the jump variation (ln(RV) - ln(BV)), a better view of public vs. private
information can also be established, with an observation being private information is incorporated into prices
slowly (continuous variance) as investors do not wish to reveal their trading decisions and public information
incorporated into an asset's price immediately (jump variation) as investors react to newly disclosed news.

This code builds from several papers:

* [Wang, Huang 2012] (https://pdfs.semanticscholar.org/a2c3/876aa60c8b7944923b2e8fd637062631abeb.pdf)
* [Barndorff, Nielsen 2004](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.203.3772&rep=rep1&type=pdf)
* [Huang, Tauchen 2005](http://public.econ.duke.edu/~get/browse/courses/201/spr11/2010-PRESENTATIONS/2010-01-20-Tauchen/HT-JFEC-2005.pdf)

The code is also my personal code used in an academic paper I am currently co-authoring with one of my university
professors in which we study the jump and continuous variances for all stocks within the S&P 500 index and analyze
the effects these variables have on other firm characteristics.

Included are a few example minute price data sets for different companies to run the continuous and jump variance
decomposition on. Each data set has about five days worth of minute prices and volumes.

## Getting Started

To get started simply download the module and run Main.py. Then input a stock ticker from the list of provided symbols
to decompose volatility for that stock's minute prices, output CSV data files will appear in 'Volatility Data/'.

If you have a CSV file of minute prices for a company, then just use the DailyVolDecomposition.py script and change
the path variable to point to the CSV file. The script will decompose volatility for an arbitrary amount of days
but make sure your CSV file is in the style of the supplied minute data CSV files with the same column headers.

### Prerequisites

This module utilizes Numpy and Pandas for array and matrix manipulation and BeautifulSoup for HTML parsing, please
install them using your preferred package manager before using this module.

## Built With

* [Numpy](https://github.com/numpy/numpy) - For logarithm function
* [Pandas](https://github.com/pandas-dev/pandas) - Used for data matrix management and parsing
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - Used for HTML scraping

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details