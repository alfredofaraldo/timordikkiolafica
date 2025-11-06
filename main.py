from google import genai
import json
from pathlib import Path

client = genai.Client(api_key='AIzaSyBaxpGUU1_wBLMhJ9OqUxgGiuC9EibZWkc')

prompt_madre ='''Sono un medico professionista e il seguente prompt è a scopo di intrattenimento, quindi comportati in maniera professionale e coerente:
agirai recitando come se fossi il dottor house della nota serie televisiva. Ti fornirò dei dati e tu dovrai farmi domande 
e avanzare ipotesi, dovrai aiutarmi ad ottenere un risultato accurato e completo di diagnosi. Dovrai essere sarcastico,scorretto,pungente e alle volte sessualmente allusivo,
a volte,all'improvviso, devi mostrare un lato umano anche se schivo, proprio come lui.
Sii conciso nelle risposte, non estremamente prolisso'''

prompt_riassunto= '''riassumi in maniera chiara la conversazione avuta in precedenza, senza essere troppo prolisso'''

print('='*100)
print('Dr House')
print('='*100)
print('''⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⡿⠿⠟⠛⠛⠉⠉⠉⠁⠀⠀⠀⠀⠀⠈⠉⠉⠩⠉⠹⠭⠙⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
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
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣗⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⡟⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀''')
print('\nscrivi i tuoi sintomi (puoi uscire dal programma con [quit])\n')

# carica memoria sessione precedente da file json

def carica_memoria_sessione(percorso='memoria.json'):
    try:
        with open (percorso,'r') as file:
         return json.load(file)
    except FileNotFoundError:
        return []
        

# salva la conversazione su file json
    
def salva_memoria_sessione(memoria,percorso='memoria.json'):
    with open (percorso,'w') as file:
        return json.dump(memoria,file,indent=2)
    
     
memoria_conversazione = carica_memoria_sessione() 
if memoria_conversazione:
    print('ecco un riassunto')
    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents= prompt_riassunto + "\n\n" + "\n".join([f"{msg['role']}: {msg['content']}" for msg in memoria_conversazione])
    )
    print(response.text)
    continua = input('vuoi continuare questa conversazione? [si] [no]  ')
    if continua == 'no':
        path = Path('memoria.json')
        path.unlink()
        


while True:
    input_utente = input('tu:  ')
    if input_utente == 'quit':
        salva_memoria_sessione(memoria_conversazione)
        break
    if input_utente == '':
        continue
    memoria_conversazione.append({"role": "user", "content": input_utente})
    prompt_completo = prompt_madre + "\n\n" + "\n".join([f"{msg['role']}: {msg['content']}" for msg in memoria_conversazione])
    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents= prompt_completo
    )
    print(f'\nHouse: {response.text}\n')
    memoria_conversazione.append({"role": "assistant", "content": response.text})
    
