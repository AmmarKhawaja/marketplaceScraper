import openai
from secret import CHATGPT_API_KEY

VERSION = 'gpt-3.5-turbo-0125'

def setup():
    openai.api_key = CHATGPT_API_KEY

def request(message='Respond with 0.'):
    completion = openai.ChatCompletion.create(
        model=VERSION,
        messages=[
            {'role': 'system', 'content': "I AM GOING TO GIVE YOU AN ITEM, RESPOND 'YES' IF IT IS A VEHICLE (NOT INCLUDING BOATS OR TRAILERS), AND 'NO' IF IT IS NOT. FROM NOW ON, ONLY RESPOND YES OR NO. DO YOU UNDERSTAND?"},
            {'role': 'user', 'content': message},
        ]
    )
    return completion.choices[0].message["content"]