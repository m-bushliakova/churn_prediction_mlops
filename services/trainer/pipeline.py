# 'src/pipeline.py'
# import sys
import joblib
import mlflow
import logging
from mlflow.tracking import MlflowClient
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.base import BaseEstimator
from sklearn.metrics import f1_score, classification_report, precision_score, recall_score
from datetime import datetime
# from pathlib import Path
# sys.path.append(str(Path().resolve()))

from config import settings as st
from load_data import load_data
from preprocess import split_features_target, make_column_transformer

logging.basicConfig(filename='train.log', level = logging.INFO)



models = [
    DecisionTreeClassifier(random_state=st.random_state),
    LogisticRegression(random_state=st.random_state, max_iter=1000),
    RandomForestClassifier(random_state=st.random_state)
]


def load_and_split_data():
    """Загружает данные и делит на train/val/test (60/20/20)"""
    df = load_data()
    X, y = split_features_target(df)

    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X, y, train_size=0.8, random_state=st.random_state)
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val, y_train_val, train_size=0.75, random_state=st.random_state)
    return X_train, X_val, X_test, y_train, y_val, y_test


def train_and_evaluate(X_train, X_val, y_train, y_val, model: BaseEstimator):
    """Обучает модель на train, считает метрики на val"""
    
    # mlflow.set_tracking_uri(st.ml_flow_tracking_uri)
    mlflow.set_experiment("Churn prediction")
    run_name = type(model).__name__ + str(datetime.now())
    with mlflow.start_run(run_name=run_name):
        le = LabelEncoder()
        y_train_enc = le.fit_transform(y_train)
        y_true = le.transform(y_val)
        
        pipeline = Pipeline([
            ("column_tran", make_column_transformer(X_train)),
            ("model", model)
        ])
        
        cv_scores = cross_val_score(
            pipeline, X_train, y_train_enc,
            cv=5, scoring='f1_weighted'
        )
        
        pipeline.fit(X_train, y_train_enc)
        y_pred = pipeline.predict(X_val)
        
        val_f1 = f1_score(y_true, y_pred, average='weighted')        
        report = classification_report(y_true, y_pred, output_dict=True)        
        val_precision = precision_score(y_true, y_pred, average='weighted')
        val_recall = recall_score(y_true, y_pred, average='weighted')        
        return val_f1, pipeline, le


def register_model(pipeline, val_score):
    """Регистрирует модель в MLflow Registry и продвигает в Production"""
    
    # mlflow.set_tracking_uri(st.ml_flow_tracking_uri)
    client = MlflowClient()
    with mlflow.start_run():
        mlflow.log_metric("final_f1_weighted", val_score)
        
        mlflow.sklearn.log_model(
            pipeline,
            "model",
            registered_model_name="churn_classifier"
        )
    
    latest_version = client.get_latest_versions("churn_classifier", stages=["None"])[0]
    logging.info(f"latest_version=={latest_version}")
    prod_models = client.get_latest_versions("churn_classifier", stages=["Production"])
    logging.info(f"prod_models: {prod_models}")
    if not prod_models:
        client.transition_model_version_stage(
            name="churn_classifier",
            version=latest_version.version,
            stage="Production"
        )
        logging.info(f"Модель версии {latest_version.version} отправлена в Production (F1: {val_score:.4f})")
        return True
    else:
        prod_version = prod_models[0]
        prod_run = mlflow.get_run(prod_version.run_id)
        prod_score = prod_run.data.metrics.get("final_f1_weighted", 0)
        
        if val_score > prod_score:
            client.transition_model_version_stage(
                name="churn_classifier",
                version=latest_version.version,
                stage="Production"
            )
            logging.info(f"Модель версии {latest_version.version} продвинута в Production")
            logging.info(f"   Новый F1: {val_score:.4f} > Старый: {prod_score:.4f}")
            return True
        else:
            logging.info(f"Модель не лучше текущей Production")
            logging.info(f"   Текущий F1: {prod_score:.4f} > Новый: {val_score:.4f}")
            return False


def make_experiments():
    """Эксперименты, выбор модели, регистрация"""
    
    X_train, X_val, X_test, y_train, y_val, y_test = load_and_split_data()
    
    results = []
    for model in models:
        model_name = model.__class__.__name__
        print(f"Обучение: {model_name}")
        
        val_score, pipeline, le = train_and_evaluate(
            X_train, X_val, y_train, y_val, model
        )
        
        results.append({
            'name': model_name,
            'score': val_score,
            'pipeline': pipeline,
            'le': le
        })
    
    best = max(results, key=lambda x: x['score'])
    logging.info(f"Лучшая модель: {best['name']} (F1-weighted: {best['score']:.4f})")
    
    registered = register_model(
        best['pipeline'], 
        best['score']
    )
    
    if registered:
        le = best['le']
        y_test_enc = le.transform(y_test)
        y_pred = best['pipeline'].predict(X_test)
        test_f1 = f1_score(y_test_enc, y_pred, average='weighted')
        logging.info(f"Финальная оценка на тесте: F1 score = {test_f1:.4f}")
        
        # mlflow.set_tracking_uri(st.ml_flow_tracking_uri)
        with mlflow.start_run(run_name="final_test_evaluation"):
            mlflow.log_metric("test_f1_weighted", test_f1)
            mlflow.log_param("model_name", best['name'])
    
    joblib.dump(best['pipeline'], filename=f'{st.model_path}')
        
    logging.info(f"Модель сохранена: {st.model_path}")


if __name__ == "__main__":
    mlflow.set_tracking_uri(st.ml_flow_tracking_uri)
    logging.info(f"MLflow tracking URI: {mlflow.get_tracking_uri()}")
    mlflow.autolog()
    make_experiments()
