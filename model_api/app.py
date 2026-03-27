'app.py'
import joblib
import asyncio
import logging
import pandas as pd
from fastapi import FastAPI, HTTPException, BackgroundTasks
from contextlib import asynccontextmanager
from sklearn.pipeline import Pipeline

from config import settings as st
from shema import InputClient

class MLService:
    
    def __init__(self, model_path = st.model_path):
        self.model_path = model_path
        self.pipeline: Pipeline = None
        self.features_used = None

    async def load_model(self):             
        try:
            loop = asyncio.get_event_loop()
            model_data = await loop.run_in_executor(None, joblib.load, f'{st.model_path}')
            self.pipeline = model_data['pipeline']
            self.features_used = model_data['features_used']
        except Exception as ex:
            logging.exception('Load pipeline failed')
    
    def prepare_data(self, input_data: InputClient):
        data = input_data.model_dump().items()
        name_info = dict(InputClient.model_fields.items())
        df_dict = {name_info[name].title : [value] for name, value in data}
        df = pd.DataFrame(df_dict, columns=self.features_used)
        return df, df_dict

    async def predict(self, input_data: InputClient):
        df, df_dict = self.prepare_data(input_data)
        loop = asyncio.get_event_loop()
        pred = await loop.run_in_executor(None, self.pipeline.predict, df)
        return pred, df_dict

model_servise = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model_servise
    model_servise = MLService()
    await model_servise.load_model()
    yield
    
logging.basicConfig(filename='api.log', level = logging.INFO)
app = FastAPI(lifespan=lifespan)

@app.post(path=('/predict'))
async def predict(input_data: InputClient, background_tasks: BackgroundTasks):
    try:
        pred, df_dict = await model_servise.predict(input_data)
        background_tasks.add_task(log_request, df_dict, pred)
        return {'class_ind': int(pred[0])}
    except Exception as ex:
        logging.exception('Prediction failed')
        return HTTPException(status_code=500, detail='Predictionfailed')


def log_request(data: dict, prediction: int):
    logging.info(f"data: {data} | prediction: {prediction}") 

