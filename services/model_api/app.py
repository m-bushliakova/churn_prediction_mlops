'app.py'
import joblib
import mlflow
import asyncio
import socket
import logging
import pandas as pd
from fastapi import FastAPI, HTTPException, BackgroundTasks
from contextlib import asynccontextmanager
from sklearn.pipeline import Pipeline


from config import settings as st
from shema import InputClient


def is_mlflow_server_running():
    host, port = st.ml_flow_host, st.ml_flow_port
    timeout = 2
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False
    

class MLService:
    
    def __init__(self):
        self.pipeline: Pipeline = None
        self.features_used = None

    async def load_model(self):             
        try:
            loop = asyncio.get_event_loop()
            try:
                if is_mlflow_server_running():
                    mlflow.set_tracking_uri(f"{st.ml_flow_tracking_uri}")
                    self.pipeline = await asyncio.wait_for(
                        loop.run_in_executor(
                            None, 
                            mlflow.sklearn.load_model, 
                            st.prodaction_model_path),
                        timeout=10)                                
                    self.features_used = self.pipeline.named_steps["column_tran"].feature_names_in_
                    logging.info("ml flow prod model loaded")
                else:
                    raise Exception("Ml flow server not running")
            
            except Exception as mlflow_ex:
                logging.error(
                    f'Unable to load prodation model from ml flow : {str(mlflow_ex)}, loading local model...')
                self.pipeline = joblib.load(st.local_model_path)
                self.features_used = self.pipeline.named_steps["column_tran"].feature_names_in_
                logging.info("local model loaded")
            logging.info(f"Features: {str(self.features_used)}")
        except Exception as ex:
            logging.exception(f'Load pipeline failed : {str(ex)}')
    
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

@app.get("/")
async def root():
    
    return {
        "service": "Churn Prediction API",
        "status": f"running {"with" if is_mlflow_server_running() else "without"} Ml flow"
    }

@app.post(path=('/predict'))
async def predict(input_data: InputClient, background_tasks: BackgroundTasks):
    try:
        pred, df_dict = await model_servise.predict(input_data)
        pred = int(pred[0])
        background_tasks.add_task(log_request, df_dict, pred)
        return {'class_ind': pred}
    except Exception as ex:
        logging.exception('Prediction failed')
        raise HTTPException(status_code=500, detail=f'Prediction failed, {str(ex)}')


@app.get("/health")
async def health():
    if model_servise and model_servise.pipeline:
        return {"status": "healthy", "model_loaded": True}
    return {"status": "unhealthy", "model_loaded": False}


@app.post("/reload")
async def reload_model():
    await model_servise.load_model()
    return {"message": "Model reloaded"}

def log_request(data: dict, prediction: int):
    logging.info(f"data: {data} | prediction: {prediction}") 

