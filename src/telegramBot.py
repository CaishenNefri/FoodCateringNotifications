import requests
from dotenv import load_dotenv
import os

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

KVUri = f"https://kvzc.vault.azure.net/"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)

telegram_token = client.get_secret("telegram-token").value
telegram_chat_id = client.get_secret("telegram-chat-id").value

message_text = "Hello World\nline2\nline3"
method = "sendMessage"

url = f"https://api.telegram.org/bot{telegram_token}/{method}?chat_id={telegram_chat_id}&text={message_text}"

x = requests.post(url)
print(x.text)