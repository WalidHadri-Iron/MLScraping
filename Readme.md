# Automate Scraping E-commerce Websites using Machine Learning

## Motivation
The classic way to scrape a website is to detect where the interesting elements are in the html page and then save the path towards these elements, the variable name, the class id,... to be able to retrive their contents or their characteristics automatically for future times. However, each website has its own path and naming, this way each time you have a new website you need to do it manually the first time. Morever, the same website could be updated and the references you picked up before to reach your elements could change. This is where you need to think about something more general that does not depend on the specificities of the website.

In this project, we are intersted in extracting from an E-Commerce websites the product's title, the product's description and the product's price. The steps considered during our work are as follow:

    1. Build a dataframe with examples of E-commerce websites and then annotate them by picking up manually for each wesbite the CSS Selector for the title, the description and the price. Also, we saved the pages locally to be able to open them afterwards (The saving was done using an Add-in called Save Page WE).
    Due to the tight schedule, the dataframe contains only about 60 different websites. We could add more to the dataframe: example of websites that we could consider stores for football teams (PSG store, FCB store,....), E-sport and gaming stores, Print on demande stores,...

    And then last, verify with a Python Script that the annotation is fine.

    2. Feature engineering by extracting all the useful properties abou the three elements whether from the CSS style such as the font-size, the position, number of words, percentage of capital letters, presence in header,....

    The feature engineering done here could be extended with more ideas.

    3.  Build baselines that are based whether on if-conditions or on the metadata stucture of the html page. 

    4. Build a Machine Learning Model to be evaluate the quality of the feature engineering done by measuring how well we are able to seperate the the classes title, description and price.




