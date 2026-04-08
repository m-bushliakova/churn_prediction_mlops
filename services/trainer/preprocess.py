'src/preprocess.py'
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

def split_features_target(df):
    exclude = ['Customer ID', 'Churn Category', 'Churn Reason']
    target = 'Customer Status'

    X = df.drop(columns=[col for col in exclude] + [target])
    y = df[target]
    return X, y

def make_column_transformer(X_train):

    cat_col = [col for col in X_train.columns if X_train[col].dtype == 'object']
    num_col = [col for col in X_train.columns if X_train[col].dtype != 'object']
    ct = ColumnTransformer(
        transformers=[
            ("small_category", OneHotEncoder(min_frequency=20, max_categories=20, handle_unknown='infrequent_if_exist'), cat_col),
            ("numeric",  Pipeline(
                                steps=[("missing", SimpleImputer(strategy='median')),
                                ("standardize", StandardScaler())]),
                                num_col)
        ]
    )
    return ct