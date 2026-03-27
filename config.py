from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):

    db_username: str = Field(alias='DB_USERNAME')
    db_pw: str = Field(alias='DB_PASSWORD')
    db_hostname: str = Field(alias='DB_HOSTNAME')
    db_port: str = Field(alias='DB_PORT')
    db_name: str = Field(alias='DB_NAME')
    file_name: str = 'telecom_customer_churn.csv'
    doc_file_name: str = 'telecom_data_dictionary.csv'
    data_local_path: str = 'data/'

    # model_path: str = 'model/model.pkl'
    random_state: int = 22

    model_config = SettingsConfigDict(
        env_file = '.env',
        env_file_encoding = 'utf-8',
        extra = 'ignore'
    )

settings = Settings()