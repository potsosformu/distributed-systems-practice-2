import socket
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_client(host: str = '127.0.0.1', port: int = 8888):
    """
    Запуск TCP клиента.
    
    Args:
        host: Адрес сервера
        port: Порт сервера
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Подключение к серверу
        logger.info(f"Подключение к серверу {host}:{port}...")
        client_socket.connect((host, port))
        logger.info("Подключение установлено успешно!")
        
        # Цикл обмена сообщениями
        while True:
            # Ввод сообщения от пользователя
            message = input("\nВведите сообщение (или 'exit' для выхода): ").strip()
            
            if not message:
                continue
            
            # Отправка сообщения (кодирование в байты)
            client_socket.send(message.encode('utf-8'))
            logger.info(f"Отправлено серверу: {message}")
            
            # Проверка на команду выхода
            if message.lower() == 'exit':
                # Получение прощального сообщения от сервера
                farewell = client_socket.recv(1024).decode('utf-8')
                logger.info(f"Сервер ответил: {farewell}")
                break
            
            # Получение ответа от сервера
            response = client_socket.recv(1024).decode('utf-8')
            logger.info(f"Получен ответ от сервера: {response}")
            
    except ConnectionRefusedError:
        logger.error("Не удалось подключиться к серверу. Убедитесь, что сервер запущен.")
    except ConnectionResetError:
        logger.error("Соединение с сервером разорвано")
    except Exception as e:
        logger.error(f"Ошибка клиента: {e}")
    finally:
        # Корректное закрытие сокета
        client_socket.close()
        logger.info("Клиент завершил работу")

if __name__ == "__main__":
    run_client()