from uagents import Agent, Bureau, Context, Model
import json
from agents.DocumentParsingAgent import process_pdfs
from agents.DocumentParsingAgent2 import extract_transactions, process_all_files
from agents.GetReleventTransaction import get_relevance, get_relevant_transactions
from agents.GetUserQueryOutput import answerQuery


#kis tarah ke message se trigger hoga 
class InputReaderAgentMessage(Model):
    message: str

class ReleventDocumentAgentMessage(Model):
    message: str
    query : str
    ftd : list

class QueryAnswerAgentMessage(Model):
    message: str
    query : str
    fld : list


InputReaderParseAgent = Agent(name="InputReaderAgent", seed="InputReaderAgent recovery phrase", port=8000)

# ReleventDocumentAgent = Agent(name="ReleventDocumentAgent", seed="ReleventDocumentAgent recovery phrase", port=8000)

# QueryAnswerAgent = Agent(name="QueryAnswerAgent", seed="QueryAnswerAgent recovery phrase", port=8000)


# @InputReaderParseAgent.on_message(model=InputReaderAgentMessage)
@InputReaderParseAgent.on_query(model=InputReaderAgentMessage)
async def input_reader_agent(ctx: Context,sender: str , message: InputReaderAgentMessage):
    """
    Handles the input reader agent's message.

    Args:
        context (Context): The context of the agent.
        sender (str): The sender of the message.
        message (InputReaderAgentMessage): The message from the input reader agent.
    """
    
    print("\n ------Parsing the input---------. \n")
    ptd = process_pdfs("INFO/data")
    ftd = process_all_files(ptd)
    with open("INFO/processed_output.json", "w", encoding="utf-8") as outfile:
        json.dump(ftd, outfile, indent=4)
    print("\n ------Parsed the input successfully---------. \n")
    print(InputReaderParseAgent.address)
    
    await ctx.send(sender, ftd)



# @ReleventDocumentAgent.on_message(model=ReleventDocumentAgentMessage)
# async def relevent_document_agent(ctx: Context, sender: str , message: ReleventDocumentAgentMessage):
#     """
#     Handles the relevant document agent's message.

#     Args:
#         context (Context): The context of the agent.
#         sender (str): The sender of the message.
#         message (InputReaderAgentMessage): The message from the relevant document agent.
#     """
    
#     print("\n ------Getting relevant transactions---------. \n")
#     flq = get_relevance(message.query)
#     fld = get_relevant_transactions(flq, message.ftd)
#     print("\n ------Got relevant transactions successfully---------. \n")
    
#     await ctx.send(sender, fld)



# @QueryAnswerAgent.on_message(model=QueryAnswerAgentMessage)
# async def query_answer_agent(ctx: Context, sender: str , message: QueryAnswerAgentMessage):
#     """
#     Handles the query answer agent's message.

#     Args:
#         context (Context): The context of the agent.
#         sender (str): The sender of the message.
#         message (InputReaderAgentMessage): The message from the query answer agent.
#     """
    
#     print("\n ------Getting answer to the query---------. \n")
#     ans = answerQuery(message.query,message.fld)
#     print("\n ------Got answer to the query successfully---------. \n")
    
#     await ctx.send(sender, ans)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# demo agent who calls input_reader_agent 
# class DemoAgentMessage(Model):
#     message: str

# DemoAgent = Agent(name="DemoAgent", seed="DemoAgent recovery phrase", port=8000)

# @DemoAgent.on_event("startup")
# async def startup(ctx: Context):
#     """
#     Handles the startup event of the demo agent.

#     Args:
#         context (Context): The context of the agent.
#     """
#     print("Demo agent started.")
#     await ctx.send(InputReaderParseAgent.address, InputReaderAgentMessage(message="Demo agent called me , i am starting the input reader agent"))

# bureau = Bureau()
# bureau.add(InputReaderParseAgent)
# bureau.add(DemoAgent)

if __name__ == "__main__":
    # bureau.run()
    InputReaderParseAgent.run()