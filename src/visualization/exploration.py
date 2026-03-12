import pandas as pd

from src.config import HOME_PATH

def exploration():

    df = get_dataframe()
    df_numeric = df.select_dtypes(include='number')
    
    print("\nDimensions du dataset :", df.shape)

    print("\nTypes de variables :")
    print(df.dtypes)

    print("\nStatistiques descriptives :")
    print(df_numeric.describe())

    print("\nValeurs manquantes :")
    print(df.isnull().sum())
    
    print("\nDistribution de Location :")
    print(df["Location"].value_counts(normalize=True))

    print("\nDistribution de RainToday :")
    print(df["RainToday"].value_counts(normalize=True))

    print("\nDistribution de RainTomorrow :")
    print(df["RainTomorrow"].value_counts(normalize=True))
    
    return df
    
def get_dataframe():
    
    df = pd.read_csv(HOME_PATH + "/data/raw/weatherAUS.csv")

    df["Date"] = pd.to_datetime(df["Date"])
    df["year"] = df["Date"].dt.year
    df["month"] = df["Date"].dt.month
    df["day"] = df["Date"].dt.day
    
    df = df.drop("Date", axis=1)
    
    return df
