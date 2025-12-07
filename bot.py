import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import openai
import logging
from config import VK_TOKEN, VK_GROUP_ID, OPENAI_API_KEY, BOT_NAME, MAX_MESSAGE_LENGTH

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class VKAIBot:
    def __init__(self):
        """Инициализация VK бота с ИИ"""
        self.vk_session = vk_api.VkApi(token=VK_TOKEN)
        self.vk = self.vk_session.get_api()
        self.longpoll = VkBotLongPoll(self.vk_session, VK_GROUP_ID)
        
        # Настройка OpenAI
        openai.api_key = OPENAI_API_KEY
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        logger.info(f"Бот {BOT_NAME} успешно инициализирован")

    def get_ai_response(self, user_message, user_id):
        """Получение ответа от ИИ"""
        try:
            # Формируем промпт для ИИ
            system_prompt = f"""Ты - полезный AI ассистент по имени {BOT_NAME}. 
            Отвечай на русском языке, будь дружелюбным и полезным. 
            Если вопрос неясен, попроси уточнить."""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Обрезаем сообщение если оно слишком длинное
            if len(ai_response) > MAX_MESSAGE_LENGTH:
                ai_response = ai_response[:MAX_MESSAGE_LENGTH-3] + "..."
            
            return ai_response
            
        except Exception as e:
            logger.error(f"Ошибка при получении ответа от ИИ: {e}")
            return "Извините, произошла ошибка при обработке вашего запроса. Попробуйте позже."

    def send_message(self, user_id, message):
        """Отправка сообщения пользователю"""
        try:
            self.vk.messages.send(
                user_id=user_id,
                message=message,
                random_id=0
            )
            logger.info(f"Сообщение отправлено пользователю {user_id}")
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения: {e}")

    def handle_message(self, event):
        """Обработка входящих сообщений"""
        user_id = event.message['from_id']
        message_text = event.message['text']
        
        logger.info(f"Получено сообщение от пользователя {user_id}: {message_text}")
        
        # Игнорируем сообщения от ботов
        if event.message.get('out') == 1:
            return
        
        # Обрабатываем команды
        if message_text.lower() in ['/start', '/help', 'помощь', 'команды']:
            help_message = f"""Привет! Я {BOT_NAME} - ваш AI ассистент.
            
Доступные команды:
/start, /help - показать это сообщение
/status - проверить статус бота

Просто напишите мне любой вопрос, и я постараюсь помочь!"""
            self.send_message(user_id, help_message)
            return
        
        if message_text.lower() in ['/status', 'статус']:
            self.send_message(user_id, "✅ Бот работает нормально! Готов отвечать на ваши вопросы.")
            return
        
        # Получаем ответ от ИИ
        ai_response = self.get_ai_response(message_text, user_id)
        self.send_message(user_id, ai_response)

    def run(self):
        """Запуск бота"""
        logger.info("Запуск бота...")
        
        try:
            for event in self.longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    self.handle_message(event)
        except KeyboardInterrupt:
            logger.info("Бот остановлен пользователем")
        except Exception as e:
            logger.error(f"Критическая ошибка: {e}")
            raise

def main():
    """Главная функция"""
    try:
        bot = VKAIBot()
        bot.run()
    except Exception as e:
        logger.error(f"Не удалось запустить бота: {e}")
        print(f"Ошибка: {e}")
        print("Проверьте настройки в файле .env")

if __name__ == "__main__":
    main()
