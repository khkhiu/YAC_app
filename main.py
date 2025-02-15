from src.bot.handlers import setup_handlers
from src.utils.logger import setup_logging

def main():
    setup_logging()
    app = setup_handlers()
    app.run_polling()

if __name__ == '__main__':
    main()