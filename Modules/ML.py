import re
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import argparse
import warnings
warnings.filterwarnings("ignore")


def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("path_df_featured", help="Path the df_featured")
    args = parser.parse_args()
    
    df_featured = pd.read_csv(args.path_df_featured)
    X = df_featured[['contains_number','contains_currency','contains_symbols','font-weight','font-size']]
    y = df_featured['class']
    X['font-size'] = X['font-size'].apply(lambda x: float(re.findall(r"[-+]?\d*\.\d+|\d+", str(x))[0]) if len(re.findall(r"[-+]?\d*\.\d+|\d+", str(x)))>0 else 15)
    X['font-weight'] = X['font-weight'].fillna(value = 500)
    y = y.replace({"title":0,"description":1,"price":2})

    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = 0.2)

    rfc = RandomForestClassifier()
    rfc.fit(X_train,y_train)
    print("Test Accuracy Score For Random Forest: ", rfc.score(X_test,y_test))

    lr = LogisticRegression()
    lr.fit(X_train,y_train)
    print("Test Accuracy Score for Logistic regression: ", lr.score(X_test,y_test))
    
if __name__ == "__main__":
    main()