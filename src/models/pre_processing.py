import pandas as pd

from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

############################################################################################################

def pre_processing(df):
    
    df = df[df["RainTomorrow"].notna()] # TODO : remove ?? on ne garde que les lignes où la cible n'est pas nulle
    
    # Gestion des variables binaires
    df["RainToday"] = df["RainToday"].map({"No":0, "Yes":1})
    df["RainTomorrow"] = df["RainTomorrow"].map({"No":0, "Yes":1})

    # Séparation des features et de la cible
    X = df.drop("RainTomorrow", axis=1)
    y = df["RainTomorrow"]

    # Variables numériques et catégorielles
    num_cols = X.select_dtypes(include="number").columns
    cat_cols = X.select_dtypes(include="object").columns
    cat_cols = cat_cols.drop("Location", errors="ignore") # TODO : remove si on décide de ne pas faire la gestion des NaN par Location

    # Gestion des valeurs nulles pour les variables numériques : médiane par Location
    for col in num_cols:
        X[col] = X.groupby("Location")[col].transform(
            lambda x: x.fillna(x.median())
        )
        X[col] = X[col].fillna(X[col].median()) # certains groupes Location peuvent être entièrement nuls pour une variable

    # Gestion des valeurs nulles pour les variables catégorielles : mode par Location
    for col in cat_cols:
        X[col] = X.groupby("Location")[col].transform(
            lambda x: x.fillna(x.mode().iloc[0] if not x.mode().empty else pd.NA)
        )

    # Gestion des valeurs nulles pour Location : mode global # TODO : remove si on décide de ne pas faire la gestion des NaN par Location
    if X["Location"].isna().any():
        X["Location"] = X["Location"].fillna(X["Location"].mode().iloc[0])

    # Encodage des variables catégorielles
    X = pd.get_dummies(X, columns=X.select_dtypes(include="object").columns, drop_first=True)
    
    # Séparation train / test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y # stratify pour garder la même proportion de classes dans le train et le test, important pour le ré-équilibrage avec SMOTE
    )

    # Standardisation des features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Ré-équilibrage de la cible avec SMOTE 
    smote = SMOTE(random_state=42)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train_scaled, y_train)

    return X_train_resampled, X_test_scaled, y_train_resampled, y_test, scaler
