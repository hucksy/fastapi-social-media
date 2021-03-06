from pydantic import BaseSettings


class EnvSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    EXPIRE_TIME_MIN: int
    DATABASE_TYPE: str
    DATABASE_USER: str
    DATABASE_HOST: str
    DATABASE_NAME: str
    DATABASE_PASSWORD: str
    DATABASE_PORT: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


env_settings = EnvSettings()
