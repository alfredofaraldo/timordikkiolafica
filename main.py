from google import genai
import json
from pathlib import Path
from dotenv import load_dotenv
from pick import pick
import os

load_dotenv()

api_key = os.getenv('API_KEY')

client = genai.Client(api_key=api_key)

root_prompt = '''I'm a medical professional, and the following prompt is for entertainment purposes only, so please behave professionally and consistently:
You will act as if you were Dr. House from the popular TV series. I will provide you with data, and you will be expected to ask me questions
and make hypotheses. You will help me obtain an accurate and complete diagnosis. You will be expected to be sarcastic, incorrect, biting, and sometimes sexually suggestive.
Sometimes, suddenly, you will need to show a human side, even if shy, just like him.
Be concise in your answers, not extremely wordy.'''

summarize_prompt = '''clearly summarize the previous conversation, without being too long-winded'''

def choose_file():
    folder = './allegati'
    try:
        files = os.listdir(folder)
    except FileNotFoundError:
        print(f"Folder '{folder}' not found.")
        return None
    if not files:
        print("Folder empty.")
        return None
    title = "File to upload:"
    option, index = pick(files, title)
    return os.path.join(folder, option)

# load previous session in json

def load_session_memory(path='memory.json'):
    try:
        with open (path,'r') as file:
         return json.load(file)
    except FileNotFoundError:
        return []
        
# save conversation in json
    
def save_session_memory(memory,path='memory.json'):
    with open (path,'w') as file:
        return json.dump(memory,file,indent=2)

print('='*66)
print(' '*28 + 'Dr House')
print('='*66)
print('''\n⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⡿⠿⠟⠛⠛⠉⠉⠉⠁⠀⠀⠀⠀⠀⠈⠉⠉⠩⠉⠹⠭⠙⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⡿⠿⠫⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠀⠀⠀⠀⠈⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⣀⠀⠈⠁⠀⠒⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠒⣩⠥⡽⣛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣶⣖⡄⠀⠈⠀⠀⠀⠀⠀⣀⠠⠤⠶⠄⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠖⠂⠀⠀⠀⠀⠀⠀⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⢙⡻⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡿⣛⡯⠖⠀⠀⠀⠀⠀⠀⠰⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⡀⠤⡈⢷⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⠿⠏⠰⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⠶⠈⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠰⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⢶⣹⣿⣿⣿⣿⣿
⣿⣿⣿⣿⡛⠅⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠁⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡄⠀⢀⠀⠀⠀⠄⠀⠠⠀⠀⡠⠤⠀⠀⠀⠙⢻⣿⣿⣿⣿
⣿⣿⣿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣠⣤⣤⣤⡀⠤⢤⠌⢡⠤⣀⣤⣤⣴⠰⣀⣴⣼⣾⣿⣾⣿⣿⣮⣤⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⢾⣿⣿⣿
⣿⣿⣁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠦⢐⣥⣦⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣾⣿⣿⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣇⣀⣼⡂⠀⢀⠀⠀⠀⠀⠁⠀⠀⠀⠠⢤⣿⣿⣿
⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠰⢏⢦⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⢢⠙⣆⠀⠀⠀⠀⡘⠀⠀⠀⠘⣻⣿⣿
⣿⣿⡗⠀⠀⠀⠀⠀⠀⠀⠀⡆⢺⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⡨⢐⠡⠀⠀⠁⢀⠀⠀⠀⠈⠈⢿⣿⣿
⣿⣿⢃⡄⠀⠀⠀⠀⠀⠀⠀⢾⢯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣖⠇⠃⠌⠀⠀⠀⠀⠀⠀⠀⠀⢀⢸⣿⣿
⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⢂⣯⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⡂⠁⠞⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿
⣿⣿⣿⣇⠏⠀⠀⠀⠀⠀⠠⡘⣮⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣅⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣾⣿⣿
⣿⣿⣿⣟⡀⠀⠀⠀⠀⠀⠰⠱⠞⢿⣿⣿⠿⠿⠿⠿⣿⣿⣿⢿⣿⣿⣟⢿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⡿⠿⡿⢿⠻⠿⠿⠿⠿⠟⠀⢘⠀⡄⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿
⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠣⢃⠀⠈⠀⠀⠈⠈⠀⠉⠈⠉⠉⠁⠉⠁⠉⠁⠀⣙⣿⣿⣮⡉⠉⠈⠉⠈⠈⠉⠁⠀⠀⠀⠈⠘⠚⠡⠄⠀⠀⠀⠘⠐⠠⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿
⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⢸⡀⠀⠀⠀⠀⣀⣾⡀⠆⠰⢀⣶⣆⠀⠀⠀⠀⠀⣀⣀⣉⣹⣏⠀⠀⠀⠀⠀⣀⣶⣆⡰⠶⠆⣰⣆⠀⠀⠀⠀⠀⠁⡀⠉⠀⠀⠀⠀⢀⠀⢾⣿⣿⣿
⣿⣿⣿⣿⣿⣧⠀⠀⠀⠈⠲⣜⣶⣤⣦⣄⠘⠉⡻⠟⢛⠿⠭⣩⣱⣽⣯⣧⣞⣿⣻⣿⣿⣿⣰⣬⣿⣿⣯⣼⠟⣯⠭⠯⢋⠭⠑⢁⣤⣄⣠⣒⡤⠁⠀⠂⠀⠠⣌⠀⢠⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣧⠠⡀⠀⢹⢺⣿⣿⣿⣾⣷⣶⣶⣶⣾⣶⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣶⣖⣶⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⢐⠚⢀⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠀⢔⡀⠈⠎⢹⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣯⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⡛⠀⠀⠀⠀⡴⢁⢀⣼⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣆⠸⠳⠄⠘⡀⠘⢻⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢘⣠⣿⣿⣿⣿⣿⣿⣷⣈⣣⠙⣾⣿⣿⣿⣿⣿⣿⣿⣿⡿⠙⠅⠁⠀⠀⠀⠀⢿⡱⠈⣼⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣾⠀⠀⠀⠁⡙⠬⡹⣿⣿⣿⣿⣿⣿⣿⡃⡟⠿⣿⣿⣿⣿⣿⣿⠟⢸⢩⠆⣿⣿⣿⣿⣿⣿⣿⣏⠣⠌⠁⠂⠀⠀⠀⠀⣶⣤⣴⣾⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠑⡳⣄⣾⢿⣿⣿⣿⣿⣿⣇⠀⠀⠈⠙⠛⠛⠉⠁⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣳⢂⡑⡆⠀⠀⠄⠁⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⡄⠀⠈⠾⣶⢿⣿⡿⡿⢿⡿⠟⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠜⠟⡿⣛⢿⣿⣿⠅⢮⢠⠁⠀⠈⠆⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⢉⣏⡛⠉⠱⠁⠁⡀⠁⠀⠀⠀⠀⡀⠀⠀⠘⢔⠀⠄⠀⡌⡀⠘⢂⠀⠃⠛⡇⠃⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠈⠀⠀⠄⠀⠀⠂⠀⠀⠐⠂⠡⠐⠲⢇⣠⣤⠾⠂⠘⠀⠙⠐⠈⠀⠀⠀⠀⠐⡌⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⢠⠀⠀⠀⠀⠀⠖⠀⠄⣤⣶⣶⣶⣶⣶⣶⣶⣦⣤⣤⣶⣶⣶⣶⣶⡶⣶⠦⢢⡀⠂⠜⠀⠀⠀⠀⠀⠀⠀⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⣷⠆⠀⠀⠀⠀⠀⠀⠏⠱⠉⡸⠎⠏⠈⠉⠁⠀⠈⠁⠉⠿⠹⠉⠉⠉⠇⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠉⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⠿⠟⠛⠛⠉⠀⠀⠀⠀⠀⡿⣖⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣮⠀⠀⠀⠀⠙⠻⢿⣿⣿⣿⣿⣿⣿
⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣦⠀⠀⠀⠀⠀⠀⢀⣠⠤⢀⢤⡵⢢⣽⡾⡴⢷⡽⣶⡿⣾⣷⢂⠠⡀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⡖⠁⠀⠀⠀⠀⠀⠀⠈⠉⠛⠛⠿⢿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢽⣿⡆⠀⠀⠀⠀⠀⠀⠀⠂⡀⠎⠀⠌⡀⠁⠍⡀⠘⡋⠐⠁⠠⠀⠒⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⠷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣾⣷⡤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣏⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣗⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⡟⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n''')




# summary of previous conversation

conversation_memory = load_session_memory() 
if conversation_memory:
    print("\nHere's a summary of the previous conversation:\n")
    response = client.models.generate_content(
    model ="gemini-2.5-flash",
    contents = summarize_prompt + "\n\n" + "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_memory])
    )
    print(response.text)
    message = input('\nDo you want resume previous conversation [yes] [no]  ')
    if message == 'no':
        path = Path('memory.json')
        path.unlink()
        conversation_memory.clear()
        
# chat core

print('\nDescribe your symptoms, type [quit] to exit or [upload] to upload file\n')
        
while True:
    user_input = input('You:  ')
    if user_input == 'quit':
        save_session_memory(conversation_memory)
        break
    elif user_input == '':
        continue
    elif user_input == "upload":
            file = choose_file()
            if file:
                print(f"Loading {file}...")
                myfile = client.files.upload(file=file)
                text_image = input('\nPlease insert request:  ')
                text_image += '''Divide your answer in two. The second part of your answer must be preceded by this text: "DESCRIPTION"
                where you will describe the contents of the file.'''
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[
                        text_image + root_prompt + "\n\n" + "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_memory]),
                        myfile
                    ]
                )
                before, _, after = response.text.partition("DESCRIPTION")
                print(f'\nHouse: {before}\n')
                conversation_memory.append({"role": "user", "content": before}) 
                conversation_memory.append({"role": "assistant", "content": after})
    else:
      conversation_memory.append({"role": "user", "content": user_input})
      full_prompt = root_prompt + "\n\n" + "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_memory])
      response = client.models.generate_content(
      model ="gemini-2.5-flash",
      contents = full_prompt
      )
      print(f'\nHouse: {response.text}\n')
      conversation_memory.append({"role": "assistant", "content": response.text})
    

 
 

 

 
    
