from fastapi import FastAPI, Request
import json
from uagents.query import query
from uagents import Model

#  --host 0.0.0.0 --port 8001
app = FastAPI()


InputReaderParseAgentAddress = "agent1qdrw2u2ffm8j2fpfrtfce40hce77vkylndrwq7dzrez2cw3n5pa4savw0ps"


class InputReaderAgentMessage(Model):
    message: str



@app.get("/CreateDatabase")
async def CallInputReaderParseAgent():
    """
    Calls the InputReaderParseAgent to create a database.

    Returns:
        dict: The response from the InputReaderParseAgent.
    """
    print("\n ------Calling InputReaderParseAgent---------. \n")
    response = await query(InputReaderParseAgentAddress, InputReaderAgentMessage(message="CreateDatabase ne api call ki hai "),timeout=15.0)
    print("\n ------Called InputReaderParseAgent successfully---------. \n")
    return response