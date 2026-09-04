from pydantic import BaseModel,HttpUrl
from datetime import datetime
class URLRequest(BaseModel):
    url : HttpUrl
    expires_in: int | None = None 

class URLResponse(BaseModel):
    original_url:HttpUrl
    shortcode:str
    expires_at:datetime | None = None

class URLStatsResponse(BaseModel):
    shortcode:str
    original_url:HttpUrl
    clicks:int
    expires_at:datetime | None = None    