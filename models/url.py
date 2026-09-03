from pydantic import BaseModel,HttpUrl
class URLRequest(BaseModel):
    url : HttpUrl
    expires_in: int | None = None 
