# 通过环境变量管理敏感配置，并使用配置层统一加载，避免将 API Key 等敏感信息硬编码到业务代码中。
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  llm_api_key:str
  llm_base_url:str
  llm_model:str

  class Config:
    env_file = ".env"

settings = Settings()