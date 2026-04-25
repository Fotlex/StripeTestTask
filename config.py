from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DEBUG: bool
    TIMEZONE: str

    DJANGO_SECRET_KEY: str

    DJANGO_ALLOWED_HOSTS: list[str]
    CSRF_TRUSTED_ORIGINS: list[str]

    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    
    STRIPE_PUBLIC_KEY_USD: str
    STRIPE_SECRET_KEY_USD: str
    
    STRIPE_PUBLIC_KEY_EUR: str
    STRIPE_SECRET_KEY_EUR: str
    
    APP_URL: str

    class Config:
        env_file = ".env"


config = Config()
