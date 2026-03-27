'src/pipeline.py'
import sys
import joblib
import mlflow
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder

from pathlib import Path
sys.path.append(str(Path().resolve()))

from config import settings as st
from src.load_data import load_data
from src.preprocess import split_features_target, make_column_transformer



mlflow.autolog()
# mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("Classifier for churn prediction2")
with mlflow.start_run(run_name='DecisionTreeClassifier1'):
    df = load_data()
    X, y = split_features_target(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=st.random_state)

    
    pipeline = Pipeline(
        steps=[
            ("column_tran", make_column_transformer(X_train)),
            ("model", tree.DecisionTreeClassifier(random_state=st.random_state))
        ]
    )
    le = LabelEncoder()
    y_train_enc = le.fit_transform(y_train)
    y_test_enc = le.transform(y_test)

    pipeline.fit(X_train, y_train_enc)
    y_pred = pipeline.predict(X_test)
    # Сохраняем весь пайплайн
    joblib.dump({
        'pipeline': pipeline,
        'label_encoder': le,
        'features_used': X_train.columns.tolist()
    }, filename=f'{st.model_path}')