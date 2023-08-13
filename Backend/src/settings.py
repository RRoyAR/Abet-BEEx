from pydantic import BaseSettings, Field
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    broker: str = Field("dev", env="KAFKA_BROKER")
    topic: str = Field(..., env="TOPIC")
    redis_url: str = Field(..., env="REDIS_URL")
    redis_port: str = Field(..., env="REDIS_PORT")
    redis_password: str = Field(..., env="REDIS_PORT")
    group_id: str = Field(..., env="GROUP_ID")


    class Config:
        env_file = ".env"


settings = Settings()


