from src.visualization.exploration import exploration, get_dataframe
from src.models.pre_processing import pre_processing

############################################################################################################

df = exploration()

X_train, X_test, y_train, y_test, scaler = pre_processing(df)
