"""Python file to serve as the frontend"""
import sys
import os
import io
import yaml

import boto3

import pandas as pd

import pandasai
from pandasai import SmartDataframe
from pandasai import SmartDatalake
from pandasai.connectors import PostgreSQLConnector
from pandasai.llm.local_llm import LocalLLM
from pandasai.llm import BedrockClaude



import chainlit as cl


import pandasai 


#llm_local = LocalLLM(api_base="http://localhost:1234/v1")

bedrock_runtime_client = boto3.client('bedrock-runtime',region_name='us-east-1')

llm_bedrock = BedrockClaude(bedrock_runtime_client)


# ec2_data = {
#     'ec2_id': [1, 2, 3, 4, 5],
#     'Name': ['vm01', 'vm02', 'vm03', 'vm04', 'vm05']
# }

# storage_data = {
#     'ec2_id': [1, 2, 3, 4, 5],
#     'storage': [5000, 6000, 4500, 7000, 5500]
# }

# ec2_df = pd.DataFrame(ec2_data)
# storage_df = pd.DataFrame(storage_data)


postgres_connector = PostgreSQLConnector(
    config={
        "host": "SERVER",
        "port": 5432,
        "database": "cq",
        "username": "USERNAME",
        "password": "PASSWORD",
        "table": "aws_ec2_instances",
    }
)



#lake = SmartDatalake([ec2_df,storage_df], config={"llm": model})
df = SmartDataframe(postgres_connector, config={"llm": llm_bedrock})

#    chain = LLMChain(llm=model)



@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": "You are a helpful data analyst."}],
    )




@cl.on_message
async def on_message(message: str):
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})

    question = message.content
    response = df.chat(question)
    msg = cl.Message(content=response)

    await msg.send()


    message_history.append({"role": "assistant", "content": msg.content})
    await msg.update()




    # # Your custom logic goes here...


    # answer = lake.chat(message)

    # # Send a response back to the user
    # await cl.Message(
    #     content=answer,
    # ).send()