import dotenv
import os

dotenv.load_dotenv(verbose=True)

telegram_bot = {
    'token': os.getenv('TELEGRAM_BOT_TOKEN'),
    'chat_id': os.getenv('TELEGRAM_BOT_CHAT_ID')
}

everytime = {
    'id': os.getenv('EVERYTIME_ID'),
    'password': os.getenv('EVERYTIME_PASSWORD'),
    'board': os.getenv('EVERYTIME_BOARD_ID')
}

saved = {
    "file_name": os.getenv("BOARD_NAME")
}
