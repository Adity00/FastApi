from pydantic import BaseModel,HttpUrl
from datetime import datetime

class URLRequest(BaseModel):
    url : HttpUrl
    expires_in: int | None = None 

class URLRecord(BaseModel)    :
    url:HttpUrl
    clicks:int
    expires_at:datetime|None=None