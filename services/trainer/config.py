from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):

    # db_username: str = Field(alias='DB_USERNAME')
    # db_pw: str = Field(alias='DB_PASSWORD')
    # db_hostname: str = Field(alias='DB_HOSTNAME')
    # db_port: str = Field(alias='DB_PORT')
    # db_name: str = Field(alias='DB_NAME')
    file_name: str = 'telecom_customer_churn.csv'
    doc_file_name: str = 'telecom_data_dictionary.csv'
    data_local_path: str = 'data/'
    ml_flow_tracking_uri: str = Field(alias='MLFLOW_TRACKING_URI')

    model_path: str = 'models/model.pkl'
    model_api_reload_url: str = Field(alias="MODEL_API_RELOAD_URL")
    random_state: int = 22

    model_config = SettingsConfigDict(
        env_file = '.env',
        env_file_encoding = 'utf-8',
        extra = 'ignore'
    )

settings = Settings()