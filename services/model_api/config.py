'model_api/config.py'
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):

    local_model_path: str = Field(alias='LOCAL_MODEL_PATH')
    prodaction_model_path: str = Field(alias='PRODACTION_MODEL_PATH')
    ml_flow_tracking_uri: str = Field(alias='MLFLOW_TRACKING_URI')
    ml_flow_host: str = Field(alias="MLFLOW_HOST")
    ml_flow_port: str = Field(alias="MLFLOW_PORT")
    random_state: int = 22

    model_config = SettingsConfigDict(
        env_file = '.env',
        env_file_encoding = 'utf-8',
        extra = 'ignore'
    )

settings = Settings()