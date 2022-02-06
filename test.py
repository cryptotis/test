from typing import NamedTuple
from os import getenv
import requests
from time import sleep
from db import add_user

url = "https://dev.wapp.im/v3/"

headers = {
  'X-Tasktest-Token': getenv("TOKEN")
}


class Chat(NamedTuple):
  chat_id: int
  chat_token: str

class UserInfo(NamedTuple):
  name: str
  phone: str


def get_chat() -> Chat:
  """Получаем чат"""
  r = requests.get(url + "chat/spare?crm=TEST&domain=test", headers=headers)
  r_json = r.json()
  print(r_json)
  return Chat(chat_id=r_json["id"],
              chat_token=r_json["token"])


def get_qr(chat: Chat) -> None:
  """получаем QR code"""
  r = requests.get(url + f"instance{chat.chat_id}/qr_code?token={chat.chat_token}", headers=headers)
  with open("qr_code.html", "w") as file:
      file.write(r.text)
  print(r.text)


def get_status(chat: Chat) -> str:
  """Получаем статус аккаунта"""
  r = requests.get(url + f"instance{chat.chat_id}/status?full=1&token={chat.chat_token}", headers=headers)
  print(r.text)
  r_json = r.json()
  return r_json["accountStatus"]
  

def send_message(chat: Chat, phone: str) -> None:
  """Отправляем сообщения"""
  payload={
    'phone': phone,
    'body': 'Hello, World!',
    'quotedMsgId': '',
    'sendSeen': '1',
    'typeMsg': 'text',
    'latitude': '35.227221',
    'longitude': '25.249377',
    'title': 'Название ',
    'footer': 'Подвал'
  }
  r = requests.post(url + f"instance{chat.chat_id}/sendMessage?token={chat.chat_token}", headers=headers, data=payload)
  print(r.text)


def get_user_info(chat: NamedTuple) -> UserInfo:
  """Получаем информацию о контакте"""
  r = requests.get(url + f"instance{chat.chat_id}/contacts?token={chat.chat_token}", headers=headers)
  user_info = r.json()[-1]
  name, phone = map(user_info.get, ('name', 'number'))
  return UserInfo(name=name, phone=phone)


def delete_chat(chat: Chat, phone: str) -> None:
  """Удаляем чат"""
  r = requests.get(url + f"instance{chat.chat_id}/removeChat?token={chat.chat_token}&phone={phone}", headers=headers)
  print(r.text)


def main():
  try:
    chat = get_chat()
  except Exception:   
    print("Нет свободных чатов")
    return

  get_qr(chat)

  while get_status(chat) != "authenticated":
    sleep(10)
  
  user_info = get_user_info(chat)
  add_user(user_info)
  send_message(chat, user_info.phone)
  delete_chat(chat, user_info.phone)

if __name__ == '__main__':
  main()