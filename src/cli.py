import requests

API_URL = "http://127.0.0.1:8000/assistant"

def main():
    print("🤖 Calendar Assistant (type 'exit' to quit)")
    while True:
        print(f"\n{'-'*65}", flush=True)
        user_message = input("User: ")
        if user_message.lower() == 'exit':
            break
        resp = requests.post(API_URL, json={"content" : user_message})
        if resp.status_code == 200:
            print(f"\n{'-'*65}\n", flush=True)
            print("Assistant: ", resp.json()["response"])
        else: 
            print("Error", resp.text)

if __name__ == "__main__":
    main()