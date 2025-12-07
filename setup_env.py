#!/usr/bin/env python3
"""
Интерактивный скрипт для создания файла .env
Помогает быстро настроить конфигурацию бота
"""

import os

def create_env_file():
    """Создание файла .env с помощью пользовательского ввода"""
    
    print("🤖 Настройка VK-бота с ИИ")
    print("=" * 40)
    print("Этот скрипт поможет создать файл .env с вашими токенами")
    print()
    
    # Проверяем, существует ли уже файл .env
    if os.path.exists('.env'):
        overwrite = input("⚠️  Файл .env уже существует. Перезаписать? (y/n): ").lower()
        if overwrite != 'y':
            print("Отменено.")
            return
    
    print("📝 Введите ваши токены:")
    print()
    
    # Получаем VK токен
    print("1️⃣ VK токен:")
    print("   Получить можно по инструкции в VK_SETUP_GUIDE.md")
    vk_token = input("   VK_TOKEN: ").strip()
    
    # Получаем ID группы
    print("\n2️⃣ ID группы VK:")
    print("   Это положительное число (например: 12345678)")
    vk_group_id = input("   VK_GROUP_ID: ").strip()
    
    # Получаем OpenAI ключ
    print("\n3️⃣ OpenAI API ключ:")
    print("   Получить можно на platform.openai.com")
    openai_key = input("   OPENAI_API_KEY: ").strip()
    
    # Получаем имя бота
    print("\n4️⃣ Имя бота (необязательно):")
    bot_name = input("   BOT_NAME [AI Assistant]: ").strip() or "AI Assistant"
    
    # Создаем содержимое файла .env
    env_content = f"""# VK Bot Configuration
VK_TOKEN={vk_token}
VK_GROUP_ID={vk_group_id}

# OpenAI Configuration
OPENAI_API_KEY={openai_key}

# Bot Settings
BOT_NAME={bot_name}
MAX_MESSAGE_LENGTH=4096
"""
    
    # Записываем файл
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print("\n✅ Файл .env успешно создан!")
        print("\n🔍 Теперь можно проверить токены:")
        print("   python test_tokens.py")
        print("\n🚀 И запустить бота:")
        print("   python bot.py")
        
    except Exception as e:
        print(f"\n❌ Ошибка при создании файла .env: {e}")

if __name__ == "__main__":
    create_env_file()
