# Automate Scraping E-commerce Websites using Machine Learning

## I. Motivation
The classic way to scrape a website is to detect where the interesting elements are in the html page and then save the path towards these elements, the variable name, the class id,... to be able to retrive their contents or their characteristics automatically for future times. However, each website has its own path and naming, this way each time you have a new website you need to do it manually the first time. Morever, the same website could be updated and the references you picked up before to reach your elements could change. This is where you need to think about something more general that does not depend on the specificities of the website.

In this project, we are intersted in extracting from an E-Commerce websites the product's title, the product's description and the product's price. The steps considered during our work are as follow:

    1. Build a dataframe with examples of E-commerce websites and then annotate them by picking up manually for each wesbite the CSS Selector for the title, the description and the price. Also, we saved the pages locally to be able to open them afterwards (The saving was done using an Add-in called Save Page WE).
    Due to the tight schedule, the dataframe contains only about 60 different websites. We could add more to the dataframe: example of websites that we could consider stores for football teams (PSG store, FCB store,....), E-sport and gaming stores, Print on demande stores,...

    And then last, verify with a Python Script that the annotation is fine.

    2. Feature engineering by extracting all the useful properties abou the three elements whether from the CSS style such as the font-size, the position, number of words, percentage of capital letters, presence in header,....

    The feature engineering done here could be extended with more ideas.

    3.  Build baselines that are based whether on if-conditions or on the metadata stucture of the html page. 

    4. Build a Machine Learning Model to be evaluate the quality of the feature engineering done by measuring how well we are able to seperate the the classes title, description and price.

## II. Tools used:
<br />

![alt text](imgs/techno.png)

## III. Steps in details

### 1. Constructing the dataframe:

An intial dataframe strucutre is stored in excel file called df_annotated. This dataframe is done manually for each new website. For pages from the same website, there is no need to do it more than one time, since the CSS selector for the same element is the same.

|URL_Live  	| Title | Description | Price |URL_Parent |
|-----------|------------|---------|------|-----------|
| The product's live url| 	Title CSS selector| Description CSS selector| Price CSS selector| The home page

When doing the annotation for a product page, we download the page locally. We make sure that we download not just the html but the css too, so that the page would look exactly like the live one without losing any element and importantly the three elements we need. We tried saving the pages with Python, but the methods we tried didn't save the page correctly (we are not sure if there is a clean way to do it with Python).

The pages are saved in a folder called pages, each page is named with a number that is linked to the dataframe: the file page_{i}.html corresponds to the row i+2 in the excel file.

We then link the initial dataframe with the folder pages by adding a column towards the file with a relative path.

URL_Live  	| Title | Description | Price |URL_Parent | URL_Local |
|-----------|------------|---------|------|-----------| ----------|
| The product's live url| 	Title CSS selector| Description CSS selector| Price CSS selector| The home page | path to local html page

And the last, we make a verification that the annoation is well done and we can access the elements. Sometimes, some element can't be reached even if the CSS selector is well copied, but there is some attributes taking hidden as property that makes it invisble to the Selenium driver.

### 2. Feature engineering:

Feature engineering is used to access important characteristics of each element (Title, description, price...) that might play a role in distinguishing between them. Feature engineering is a set of multiple functions that takes as an input the previous constructed dataframe, and outputs a new dataframe where each line is an element and the columns are the newly built features. 

The features chosen are of two types:

    . CSS properties: can be accessed by first reading the element from the html page using Selenium web scraping library and the correct css properties method. We chose first a limited number of css properties that seems to characterize the Title, Description and Price elements. These properties include font properties (size, style...) and position of the elements in the page.
    
    . Mined metadata information: Using regular expressions, we can extract meaningful features like Number of words, Number of characters, Percentage of capitalized words.

A class column is added to the dataframe, so that we have explanatory variables in the form of engineered features and a target variable corresponding to the class (Title, description, price). This dataframe can then be used for machine learning purposes.

Further work to improve this dataframe is to add new elements that differ from the initial 3 classes.

### 3. The Baselines:

We managed to create two baselines:

    1. Baseline 1: we extract the information from the metadata that is a part in the header. The results on the 60 websites are as follow:
        100% availabity for the title, 98.2% availabity for the description and 40.4% for the price.
    The metadata content is not the same content displayed on the webpage for instance we can find that the title are not exactly the same, however they contains the same information. Same for the description.

    2. Baseline 2: we look for the element having key words related to one of the three elements in their CSS selector, Xpath, class name... For instance, for the title we can look for "title", "h1".... The results on the 60 websites are as follow:
        91% for the title
        90% for the price
        We didn't get finish the same idea with the decription

### 4. A try-out to using Machine Learning with the data:

Supervized classification models were tested on the output of the feature engineering pipeline. The scikit-learn library was used for this task.
    
    . The features were first correctly pre-processed (mainly encoding strings into proper floats)
    . A test sample was derived from the dataframe. (20%)
    Models such as Random Forest and Logistic regression were fitted on the train part.
    . The default accuracy metric was used to evaluate the models. (rate of correct responses)
    . Accuracy attains 90% on the test set

Although this simple approach seems to give interesting results in terms of separation between the 3 main classes, the sample used was low and additional data might be needed to assert the efficiency of the models. 

The objective is to have at least an additional class called "other" that contains any element that differs from the 3 main classes, this will be important to have the model used for prediction on elements on any web page. 






