import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# VK Bot настройки
VK_TOKEN = os.getenv('VK_TOKEN', '')
VK_GROUP_ID = int(os.getenv('VK_GROUP_ID', '0'))

# OpenAI настройки
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

# Настройки бота
BOT_NAME = os.getenv('BOT_NAME', 'AI Assistant')
MAX_MESSAGE_LENGTH = int(os.getenv('MAX_MESSAGE_LENGTH', '4096'))

# Проверяем наличие обязательных переменных
if not VK_TOKEN:
    raise ValueError("VK_TOKEN не найден в переменных окружения")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY не найден в переменных окружения")
