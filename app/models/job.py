from sqlalchemy import Column, Integer, String

from app.core.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    company = Column(String)
    location = Column(String)
    url = Column(String, unique=True)
    source = Column(String)
