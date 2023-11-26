import requests
from dotenv import load_dotenv
import os

load_dotenv()


token = os.getenv("telegram_token")
chat_id = os.getenv("telegram_chat_id")
message_text = "Hello World\nline2\nline3"
method = "sendMessage"

url = f"https://api.telegram.org/bot{token}/{method}?chat_id={chat_id}&text={message_text}"

x = requests.post(url)
print(x.text)