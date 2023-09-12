from typing import List

from models.llm import QnAAgent
from tools import DatabaseTool, SearchTool, TimeTool, SearchByURLTool

# search_by_url_tool = SearchByURLTool()
# search_tool = SearchTool(search_by_url_tool=search_by_url_tool)
# time_tool = TimeTool()
# database_tool = DatabaseTool()

# tools=[database_tool, search_tool, time_tool]

class QnAInstance:
    def __init__(self, 
                verbose=False, 
                search_tool=None,
                database_tool=None,
                qna_prompt_path="../openai_skt/models/templates/qna_prompt_template.txt",
                summary_chunk_template=None,
                input_variables=None,) -> None:
        self.summary_chunk_template = summary_chunk_template
        self.input_variables = input_variables
        self.search_by_url_tool = SearchByURLTool()
        self.search_tool = search_tool
        if search_tool == None:
            self.search_tool = SearchTool(search_by_url_tool=self.search_by_url_tool)
        self.time_tool = TimeTool()
        self.database_tool = database_tool
        if database_tool == None:
            self.database_tool = DatabaseTool()

        tools = [self.database_tool, self.search_tool, self.time_tool]
        self.qna_agent = QnAAgent(
            tools=tools, verbose=verbose, model="gpt-3.5-turbo-16k", qna_prompt_path=qna_prompt_path
        )

    def run(self, database, question: str, qna_history: List[List[str]], queue=None):
        tools = self.set_tools(database)
        answer = self.qna_agent.run(tools=tools, question=question, qna_history=qna_history, queue=queue)
        return answer
    
    async def arun(self, database, question:str, qna_history:List[List[str]], queue=None):
        tools = self.set_tools(database)
        answer = await self.qna_agent.run(tools=tools, question=question, qna_history=qna_history, queue=queue)
        return answer
    
    def set_tools(self, database):
        database_tool = DatabaseTool()
        database_tool.set_database(database)
        tools = [database_tool, self.search_tool, self.time_tool]
        return tools