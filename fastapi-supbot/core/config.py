from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

class BotSettings(BaseModel):
    token: str

class RunConfig(BaseModel):
    host: str = "localhost"
    port: int = 8000
class AdminActionPrefix(BaseModel):
    prefix: str = "adm"

class CallbackDataPrefix(BaseModel):
    admin_action: AdminActionPrefix = AdminActionPrefix()


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    websocket: str = "/websocket"

class ApiPrefix(BaseModel):
    prefix: str = '/api'
    v1: ApiV1Prefix = ApiV1Prefix()

class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = True
    echo_pool: bool = False
    max_overflow: int = 10
    pool_size: int = 50


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="SUPPORT_BOT__",
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    cb: CallbackDataPrefix = CallbackDataPrefix()
    db: DatabaseConfig
    bot: BotSettings


settings = Settings()