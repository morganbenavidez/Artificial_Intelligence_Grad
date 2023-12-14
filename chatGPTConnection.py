import openai
CRED, CRBLUE, CRCYAN, CRGREEN, CEND = '\033[91m', '\033[94m', '\033[96m', '\033[92m', '\033[0m'
openai.api_key = "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"
model_engine = "text-davinci-003"

import pandas as pd

questions = []
answers = []

df = pd.read_csv('questions.csv')
for i in range(len(df)):
    questions.append(df.iloc[i]['Question'])

for i in range(0,5):
    print(questions[i])

def generate_response(input):
    #model_engine = "text-davinci-003"
    #prompt = (f"{input}")
    response = openai.Completion.create(
        engine=model_engine,
        prompt=input,
        temperature=0.6,
        max_tokens=300,
        top_p=1.0,
        frequency_penalty=1,
        presence_penalty=1
    )
    #print(response)
    output = response['choices'][0]['text']
    #parent_id = response['parent_id']
    #print(parent_id)
    conversation_id = response['id'] 
    #print(conversation_id)
    #print(output)
    #return response['choices'][0]['text']
    return output

def handle_input(input_str : str, conversation_history : str, USERNAME : str, AI_NAME : str):
    # Update the conversation history
    conversation_history += f"{USERNAME}: {input_str}\n"
    # Generate a response using GPT-3
    message = generate_response(conversation_history)
    # Update the conversation history
    conversation_history += f"{AI_NAME}: {message}\n"
    # Print the response
    print(CRBLUE +f'{AI_NAME}: {message}'+ CEND)
    #return conversation_history
    return message

INITIAL_PROMPT = ('''''')
conversation_history = INITIAL_PROMPT + "\n"
USERNAME = 'Input'
AI_NAME = "AI Outputs"

# This is for live stream questioning
liveStream_or_CSV = input("Do you want live stream or csv reader? (ls or csv)")

if (liveStream_or_CSV == 'ls'):

    while True:
        # Get the user's input / live ask
        user_input = input(f"{USERNAME}: ")
        # Handle the input
        conversation_history=handle_input(user_input, conversation_history, USERNAME, AI_NAME)

elif (liveStream_or_CSV == 'csv'):
    for i in range(len(questions)):
        # Pass questions
        user_input = questions[i]
        # Handle the input
        conversation_history=handle_input(user_input, conversation_history, USERNAME, AI_NAME)
        answer = conversation_history[9:]
        answers.append(answer)
    data = {'Answer': answers}
    answers_DataFrame = pd.DataFrame(data)
    #print(answers_DataFrame)
    answers_DataFrame.to_csv('Answers.csv')
    for i in range(0,len(answers)):
        print(answers[i])

else:
    while True:
        liveStream_or_CSV = input("Do you want live stream or csv reader? (ls or csv)")


