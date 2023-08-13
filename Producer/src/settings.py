from pydantic import BaseSettings, Field
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    broker: str = Field("dev", env="KAFKA_BROKER")
    topic: str = Field(..., env="TOPIC")

    class Config:
        env_file = ".env"


settings = Settings()


