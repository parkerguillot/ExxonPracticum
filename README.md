# ExxonPracticum
This github is designed as a repository for code as well as information regarding the 
entire process of scraping websites and generating topic models.

This github has separate branches for each section of the process. The main purpose behind 
this repository is to allow the user to view the analysis process on a step-by-step basis 
and then replicate the process on their own system, thus allowing them to perform 
their own analysis in the future.  

# Requirements
Before checking the other branches, We highly recommend looking into the requirements text file.
This file lists all of the required Python packages and versions we used to comlete this analysis.
These packages need to be imported into a user's system before performing this analysis.

# Data Collection
This branch contains code related to scraping text from public blog websites and
pipelining those data points to a database. This process was performed in using 
xpath locators from each individual website. 
One important note is that a user would need to adjust any file path references
in the code to match the file path from their own system. 
Additionally, if a user would like to add new websites to the analysis,
he or she must determine the proper xpath locators for each item on the new website.

# NLP & Data Visualization
This branch contains the code related to the topic modeling process of the scraped web data.
All of the data visualization done as part of this process was performed in a single
Jupyter notebook.

# Topic Modeling
