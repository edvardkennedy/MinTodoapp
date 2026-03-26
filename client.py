import requests
 
BASE_URL = "http://127.0.0.1:5000/todos"
 
def vis_meny():
    print("\n--- TODO KLIENT ---")
    print("1. Vis alle lister")
    print("2. Hent spesifikk liste (ID)")
    print("3. Opprett ny liste")
    print("4. Avslutt")
    return input("Velg handling (1-4): ")
 
def hent_alle():
    res = requests.get(BASE_URL)
    data = res.json()
    print("\nAlle todo-lister:")
    for item in data:
        print(f"{item['id']} - {item['title']}")
 
def hent_en():
    todo_id = input("Skriv inn ID: ")
    res = requests.get(f"{BASE_URL}/{todo_id}")
    if res.status_code == 200:
        todo = res.json()
        print(f"\nTittel: {todo['title']}")
        print("Oppgaver:")
        for t in todo['tasks']:
            status = "[x]" if t['done'] else "[ ]"
            print(f"{status} {t['text']}")
    else:
        print("Fant ikke listen.")
 
def opprett_ny():
    tittel = input("Tittel: ")
    oppgaver = []
    print("Legg til oppgaver (tom linje for å stoppe):")
    while True:
        tekst = input("Oppgave: ")
        if not tekst: break
        oppgaver.append({"text": tekst, "done": False})
    payload = {"title": tittel, "tasks": oppgaver}
    res = requests.post(BASE_URL, json=payload)
    print(f"Notat opprettet! ID: {res.json()['id']}")
 
# Hovedløkke
while True:
    valg = vis_meny()
    if valg == "1":
        hent_alle()
    elif valg == "2":
        hent_en()
    elif valg == "3":
        opprett_ny()
    elif valg == "4":
        break
    else:
        print("Ugyldig valg.")