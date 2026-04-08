'src/load_data.py'
# import sys
# from pathlib import Path
import os
import pandas as pd
import kagglehub
from kagglehub import KaggleDatasetAdapter

# sys.path.append(str(Path().resolve().parent))
from config import settings as st


def download_dataset(file_name, pandas_kwargs=None):
    dataset_path = 'shilongzhuang/telecom-customer-churn-by-maven-analytics'
    df = kagglehub.dataset_load(
        adapter=KaggleDatasetAdapter.PANDAS,
        handle=dataset_path,
        path = st.doc_file_path,
        pandas_kwargs=pandas_kwargs
    )
    df.to_csv(f"{st.data_local_path}{file_name}")
    return df

def load_data(descr=False):
    '''
    descr = False - загрузить датасет о оттоке клиентов
    descr = True - загрузить описание признаков, а не сам датасет с признаками
    '''
    file_name = st.file_name if not descr else st.doc_file_name
    path = st.data_local_path
    if os.path.exists(f"{path}{file_name}"):
        return pd.read_csv(f"{path}{file_name}", index_col=0)
    else:        
        return download_dataset(file_name, pandas_kwargs=({'encoding': 'cp1252'} if descr else None))

