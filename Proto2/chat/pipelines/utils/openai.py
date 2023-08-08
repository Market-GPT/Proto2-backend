import os
import openai
from dotenv import load_dotenv
# _ = load_dotenv('.env.dev')   # Not required in production
import tiktoken

openai.api_key  = os.environ['OPENAI_API_KEY']

delimiter = "####"
system_message = f"""
Answer user queries appropriately.
The customer query will be delimited with four hashtags,\
i.e. {delimiter}.
"""

def get_completion_from_messages(messages,
                                 model="gpt-3.5-turbo",
                                 temperature=0, max_tokens=500):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message["content"]

def get_completion(prompt, model="gpt-3.5-turbo",temperature=0):
    messages =  [
      {'role':'system',
      'content': system_message},
      {'role':'user',
      'content': f"{delimiter}{prompt}{delimiter}"},
      ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def count_tokens(text: str) -> int:
    # Get the encoding for gpt-3.5-turbo model
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    num_tokens = len(encoding.encode(text))
    return num_tokens

def curtail_output(output: str) -> str:
    # Check if the number of tokens is less than 14k
    if count_tokens(output) < 14000:
        return output
    else:
        # Curtail the output if it's more than 14k tokens
        # Here, we're truncating the string, but you might want a more sophisticated way
        # like summarizing or compressing the output
        truncated_output = output[:10000] + "... [Output truncated due to token limit]"
        return truncated_output