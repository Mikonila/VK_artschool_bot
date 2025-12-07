# Деплой VK бота на VPS

## Подготовка VPS сервера

1. **Установите Docker и Docker Compose:**
```bash
# Обновляем систему
sudo apt update && sudo apt upgrade -y

# Устанавливаем Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Устанавливаем Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Перезагружаемся для применения изменений
sudo reboot
```

2. **Создайте директорию для проекта:**
```bash
mkdir -p ~/vk-bot
cd ~/vk-bot
```

## Загрузка файлов на сервер

1. **Скопируйте все файлы проекта на сервер:**
```bash
# Создайте архив на локальной машине
tar -czf vk-bot.tar.gz http_bot.py config.py .env Dockerfile docker-compose.yml requirements.txt deploy.sh

# Загрузите на сервер (замените YOUR_SERVER_IP)
scp vk-bot.tar.gz user@YOUR_SERVER_IP:~/vk-bot/

# На сервере распакуйте
cd ~/vk-bot
tar -xzf vk-bot.tar.gz
```

2. **Проверьте файл .env:**
```bash
cat .env
```

Убедитесь, что все переменные заполнены:
```
VK_TOKEN=your_vk_token
VK_GROUP_ID=your_group_id
BOT_NAME=AI Assistant
MAX_MESSAGE_LENGTH=4096
```

## Запуск бота

1. **Запустите деплой:**
```bash
./deploy.sh
```

2. **Проверьте статус:**
```bash
docker-compose ps
```

3. **Просмотрите логи:**
```bash
docker-compose logs -f
```

## Управление ботом

- **Остановить:** `docker-compose down`
- **Перезапустить:** `docker-compose restart`
- **Обновить:** `./deploy.sh`
- **Логи:** `docker-compose logs -f`

## Автозапуск при перезагрузке сервера

Добавьте в crontab:
```bash
crontab -e
```

Добавьте строку:
```
@reboot cd /home/user/vk-bot && docker-compose up -d
```

## Мониторинг

- **Статус контейнера:** `docker-compose ps`
- **Использование ресурсов:** `docker stats vk-bot`
- **Логи в реальном времени:** `docker-compose logs -f`

