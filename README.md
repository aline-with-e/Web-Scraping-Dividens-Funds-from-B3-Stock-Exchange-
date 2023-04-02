# Web-Scraping-Dividens-Funds-from-B3-Stock-Exchange-
This code was built using Python and R to web scrape dividends from Funds from B3 stock exchange. The script in a jupyter notebook.

The main purpose of this code was  automate my daily tasks. 

In order to use it, you will need a csv file containing the links of the annoucements you want to scrape just like the SAMPLE_COTISTAS file I have attached on this project. 

How does it work? 
Well, the code loops through each link, opening the annoucement, taking a screenshot and saving on your current directory as pdf. (using webshot library from R) 
Next, it will read each PDF and extract the tables on it. (Tabula package Python)
Finally, I did a little bit of Data Cleaning and Data Modelling using Pandas. 

This my first web scrapping project. If you have any suggestions how it could be improved I would love to hear! Thanks and I hope it helps you somehow :) Aline. 
