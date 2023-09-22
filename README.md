# Optimise Battery Dispatch Behaviour

This project aims to develop algorithms using linear programming to optimise the dispatch behaviour of a battery based in Victoria. Maximise revenues by charging when electricity prices are low and discharge when prices are high.

## Project Contributor
- Haonan Zhong (867492)
- Zhi Hern Tom (1068268)
- Kaixin Yu (1118795)
- Lissy Xun (1074284)
- Jiabao Zhang (1118553)

## Project Stages
- Stage one: Maximise revenue while assume having perfect foresight of future spot prices
- Stage two: Maximise revenue without having perfect foresight of future spot prices

## Dependencies
- <img src="https://iconape.com/wp-content/files/zt/11663/png/python.png" width="15" height="15"/> Language: Python 3.8.8
- <img src="https://iconape.com/wp-content/files/zt/11663/png/python.png" width="15" height="15"/> Python Packages/Libraries: [pandas](https://pandas.pydata.org), [numpy](https://numpy.org), [matplotlib](https://matplotlib.org), [statsmodels](https://www.statsmodels.org/stable/index.html), [pyomo](http://www.pyomo.org), [pyutilib](https://github.com/PyUtilib/pyutilib), [glpk](https://www.gnu.org/software/glpk/), [logging](https://docs.python.org/3/library/logging.html)
- To install all the required packages and libraries, please locate the text file `requirements.txt`

## Directory
- `algorithms`: contains algorithms and notebook for this project
- `data`: contains data for this project
- `modelling`: contains model for spot price forecasting
- `result`: contains simulated dispatch results of the proposed battery
- `visualization`: contains basic visualization of the spot price

## Reference 
- [Sandia National Laboratories. (2018). About. Pyomo.](http://www.pyomo.org/about)
- [Sandia National Laboratories. (2017). Pyomo Documentation 6.1.2. Pyomo Documentation.](https://pyomo.readthedocs.io/en/stable/)
- [Sandia National Laboratories. (2016). Pyomo Tutorial. Pyomo Tutorial.](https://www.osti.gov/biblio/1376827)
- [Brent Austgen - UT Austin INFORMS. (2021). Pyomo Tutorial. YouTube.](https://www.youtube.com/watch?v=pxCogCylmKs&t=346s)
- [Free Software Foundation, Inc. (2012). GLPK - GNU Project - Free Software Foundation (FSF). GNU.](https://www.gnu.org/software/glpk/)
- [AEMO. (2021). National Electricity Market (NEM).](https://aemo.com.au/energy-systems/electricity/national-electricity-market-nem)
- [Brakels, R. (2021). How Does 5-Minute Settlement Help Batteries? Solar Quotes Blog.](https://www.solarquotes.com.au/blog/nem-5-minute-settlement/)
