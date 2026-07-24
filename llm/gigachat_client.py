import os
import requests
import json
import base64
from typing import Optional
from config import Config

class GigaChatClient:
    def __init__(self, model: Optional[str] = None, temperature: Optional[float] = None):
        self.model = model or Config.GIGACHAT_MODEL
        self.temperature = temperature or Config.TEMPERATURE
        self.token = None
        self._get_token()
    
    def _get_token(self):
        """Получает токен через OAuth (по официальной документации)"""
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        
        # Формируем Basic Authorization
        credentials = f"{Config.GIGACHAT_USERNAME}:{Config.GIGACHAT_PASSWORD}"
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': '123e4567-e89b-12d3-a456-426614174000',
            'Authorization': f'Basic {encoded_credentials}'
        }
        
        # Используем payload как строку (по документации)
        payload = 'scope=GIGACHAT_API_PERS'
        
        try:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            
            print("Получение токена...")
            print(f"Client ID: {Config.GIGACHAT_USERNAME}")
            
            response = requests.post(url, headers=headers, data=payload, verify=False)
            
            print(f"Статус авторизации: {response.status_code}")
            
            if response.status_code == 200:
                token_data = response.json()
                self.token = token_data.get("access_token")
                print("Токен получен успешно!")
                return self.token
            else:
                print(f"Ошибка авторизации: {response.status_code}")
                print(f"Ответ сервера: {response.text}")
                return None
        except Exception as e:
            print(f"Ошибка при получении токена: {e}")
            return None
    
    def generate(self, prompt: str, temperature: Optional[float] = None) -> str:
        try:
            if not self.token:
                self._get_token()
                if not self.token:
                    return "Ошибка: не удалось получить токен"
            
            temp = temperature or self.temperature
            
            # Правильный URL для генерации (по документации)
            url = "https://api.giga.chat/v1/chat/completions"
            
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': f'Bearer {self.token}'
            }
            
            # Формируем payload по документации
            payload = json.dumps({
                "model": self.model,  # GigaChat-2-Pro
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": temp,
                "max_tokens": Config.MAX_TOKENS,
                "profanity_check": False
            })
            
            print("Отправка запроса к GigaChat...")
            response = requests.post(url, headers=headers, data=payload, verify=False)
            
            print(f"Статус запроса: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("choices"):
                    content = result["choices"][0]["message"]["content"]
                    print(f"Получен ответ: {len(content)} символов")
                    return content
                else:
                    return f"Ошибка: нет ответа от модели.\nОтвет: {result}"
            else:
                return f"Ошибка HTTP: {response.status_code}\n{response.text}"
                
        except Exception as e:
            print(f"Ошибка при запросе к GigaChat: {e}")
            return f"Ошибка: {str(e)}"
