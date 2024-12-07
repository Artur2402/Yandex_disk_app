import os
import requests


def get_public_file(public_key: str) -> dict:
  yandex_disk_token = os.getenv('YANDEX_DISK_TOKEN')
  # Проверка наличия токена
  if not yandex_disk_token:
    return {'error': 'Токен доступа отсутсвует. Проверьте переменные окружения'}

  url = f"https://cloud-api.yandex.net/v1/disk/public/resources?public_key={public_key}"
  headers = {'Authorization': f'OAuth {yandex_disk_token}'}

  try:
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
      return response.json()
    elif response.status_code == 404:
      return {'error': 'Рессурс не найден. Проверьте публичный ключ'}
    elif response.status_code == 401:
      return {'error': 'Неавторизованный запрос. Проверьте токен авторизации.'}
    else:
      return {'error': f'Ошибка {response.status_code}: {response.text}'}
  except requests.exceptions.RequestException as e:
    return {'error': f'Ошибка соединения: {str(e)}'}