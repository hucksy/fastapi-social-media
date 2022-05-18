from pydantic import BaseSettings


class EnvSettings(BaseSettings):
    secret_key: str = 'c92e1402-3dfb-4dd9-b22d-3bfe14e07ee7'
    algorithm: str = 'HS256'
    expire_time_min: int = 120
    database_user: str = 'postgres'
    database_port: str = 'localhost'
    database_password: str = ''

    # class Config:
    #     env_file = ".env"


env_settings = EnvSettings()
