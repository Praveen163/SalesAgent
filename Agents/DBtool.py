from agents import Agent
from Model.geminiModel import gemini_model
from Tools.MongoData import run_mongo_command

instructions3 = """
- You are a mongoDB expert with years of experience you generate the mongodb query based on user query
- You have database schema context 
- Create the mangodb  query for the user input 
- You just create the mongodb queries dont try to get data for the user 
- You have a tool 'run_mongo_command'  only in condition where you need to know things like unique datas or want to check if something exists in databasa that you are using in query
- Try mostly to avoid use of the tool for creation of simple queries
- You uses the tool if you dont know something , you dont assume data in queries it should be geniune query only

- Context : Database Schema
{
  "_id": {
    "$oid": "685ebb7a7bdbe0f9f59a5c75"
  },
  "program": "BTECH",
  "specialization": "Computer Science",
  "fees": 150000,
  "deadline": "2025-08-31",
  "eligibility": "10+2 with Physics, Chemistry, Mathematics; min 75 aggregate",
  "seat_availability": {
    "total": 120,
    "available": 35
  },
  "admissions": "Entrance exam (JEE Main) + Counseling"
}
"""

Mongo_agent = Agent(
        name="Mongo query generator",
        instructions=instructions3,
        tools=[run_mongo_command],
        model=gemini_model
)





Readable_agent = Agent(
        name="Readable query",
        instructions= " you recives the mongodb resoponse in a list formate...you make that reponse readable for a human",
        tools=[run_mongo_command],
        model=gemini_model
)


description = "generate the mongo query based on what user asked"

mongoQueryTool = Mongo_agent.as_tool(tool_name="sales_agent3", tool_description=description)
readable_agent_tool = Readable_agent.as_tool(tool_name="mongo reponse read", tool_description="converst the mongo list reponse into readable reponse")