from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # DB
    postgres_user: str
    postgres_password: str
    postgres_db: str
    database_url: str

    # AUTH
    environment: str
    host: str
    secret_key: str
    algorithm: str = "HS256"

    # ADMIN SUPERUSER
    admin_user: str
    admin_pass: str

    telegram_token: str
    webhook_url: str

    class Config:
        env_file = ".env"


settings = Settings()
