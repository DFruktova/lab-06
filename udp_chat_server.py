import socket
import threading

def run_udp_chat_server(host='0.0.0.0', port=12345):
    """Запускает UDP-сервер для чата."""
    print("Запуск UDP-сервера...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (host, port)
    server_socket.bind(server_address)

    clients = set()  # Множество для хранения адресов клиентов
    print(f"Сервер запущен на {host}:{port}, ожидает сообщений...")

    def handle_client(data, client_address):
         message = data.decode().strip()
         if message.lower() == 'exit':
           print(f"Клиент {client_address} отключился.")
           clients.discard(client_address) # Удалить клиента
           return

         print(f"Получено от {client_address}: {message}")

         # Рассылаем сообщение всем подключенным клиентам, кроме отправителя
         for address in clients:
          if address != client_address:
            try:
              server_socket.sendto(f"{client_address}: {message}".encode(), address)
            except Exception as e:
                print(f"Ошибка при отправке клиенту {address}: {e}")


    try:
      while True:
            data, client_address = server_socket.recvfrom(1024)
            if client_address not in clients:
                clients.add(client_address) # Добавить клиента в список
                print(f"Новый клиент {client_address} подключился.")

            client_thread = threading.Thread(target=handle_client, args=(data,client_address,))
            client_thread.start()

    except KeyboardInterrupt:
      print("\nОстановка сервера...")
    except Exception as e:
        print(f"Ошибка сервера: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    run_udp_chat_server()