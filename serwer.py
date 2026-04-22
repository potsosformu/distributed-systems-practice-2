import socket
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def modify_message(message: str) -> str:
    """
    Модификация полученного сообщения.
    В данном случае: преобразование в верхний регистр и реверс.
    """
    return message.upper()[::-1]

def run_server(host: str = '127.0.0.1', port: int = 8888):
    """
    Запуск TCP эхо-сервера.
    
    Args:
        host: Адрес сервера (по умолчанию localhost)
        port: Порт сервера (по умолчанию 8888)
    """
    # Создание TCP сокета
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Опция для переиспользования адреса (избегаем ошибки Address already in use)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # Привязка сокета к адресу и порту
        server_socket.bind((host, port))
        
        # Начало прослушивания (максимум 5 клиентов в очереди)
        server_socket.listen(5)
        logger.info(f"Сервер запущен на {host}:{port}")
        logger.info("Ожидание подключения...")
        
        while True:
            # Принятие входящего подключения
            # После accept() создается НОВЫЙ сокет для общения с клиентом,
            # а server_socket продолжает слушать новые подключения
            client_socket, client_address = server_socket.accept()
            
            client_ip, client_port = client_address
            logger.info(f"Клиент подключен: {client_ip}:{client_port}")
            
            try:
                # Цикл обмена сообщениями с текущим клиентом
                while True:
                    # Получение данных (максимум 1024 байта)
                    data = client_socket.recv(1024)
                    
                    if not data:
                        # Клиент закрыл соединение
                        logger.info(f"Клиент {client_ip}:{client_port} отключился")
                        break
                    
                    # Декодирование байтов в строку
                    received_message = data.decode('utf-8')
                    logger.info(f"Получено от {client_ip}:{client_port}: {received_message}")
                    
                    # Проверка на команду выхода
                    if received_message.lower() == 'exit':
                        logger.info(f"Клиент {client_ip}:{client_port} инициировал завершение")
                        client_socket.send(b"Goodbye!")
                        break
                    
                    # Модификация сообщения
                    modified_message = modify_message(received_message)
                    
                    # Отправка ответа (кодирование строки в байты)
                    response = f"Эхо: {modified_message}".encode('utf-8')
                    client_socket.send(response)
                    logger.info(f"Отправлено клиенту {client_ip}:{client_port}: {modified_message}")
                    
            except ConnectionResetError:
                logger.warning(f"Соединение с {client_ip}:{client_port} разорвано")
            except Exception as e:
                logger.error(f"Ошибка при общении с {client_ip}:{client_port}: {e}")
            finally:
                # Корректное закрытие сокета клиента
                client_socket.close()
                
    except KeyboardInterrupt:
        logger.info("Получен сигнал завершения работы сервера")
    except Exception as e:
        logger.error(f"Ошибка сервера: {e}")
    finally:
        # Корректное закрытие серверного сокета
        server_socket.close()
        logger.info("Сервер остановлен")

if __name__ == "__main__":
    run_server()