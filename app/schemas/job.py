from typing import Optional

from pydantic import BaseModel


class JobSchema(BaseModel):
    id: int
    title: str
    company: Optional[str] = None
    url: Optional[str] = None
    location: Optional[str] = None
    source: Optional[str] = None

    class Config:
        from_attributes = True
