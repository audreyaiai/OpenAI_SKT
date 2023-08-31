from typing import Optional, Type
from pydantic import BaseModel

from langchain.tools import BaseTool

from database.database import DataBase

class DatabaseTool(BaseTool):
    name = "database"
    description = "A tool that allows the agent to query a database"
    args_schema: Optional[Type[BaseModel]] = None
    """Pydantic model class to validate and parse the tool's input arguments."""

    def __init__(self, database) -> None:
        super().__init__()
        self.database = database

    def search(self, input_dict: dict) -> dict:
        query = input_dict['query']
        result = self.database.query(query)
        return result
    
    async def async_search(self, input_dict: dict) -> dict:
        query = input_dict['query']
        result = self.database.query(query)
        return result