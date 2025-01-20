import socket

def run_udp_chat_client(host='127.0.0.1', port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (host, port)

    try:
        while True:
            message = input()
            client_socket.sendto(message.encode(), server_address)
            if message.lower() == 'exit':
                break

            # Простой прием без select
            try:
                data, addr = client_socket.recvfrom(1024)
                print(data.decode().strip())
            except OSError as e:
                print(f"Ошибка при приеме: {e}")
                break  # Выходим из цикла при ошибке

    except KeyboardInterrupt:
        print("Client interrupted by user.")
    except Exception as e:
        print(f"Ошибка в клиенте: {e}")
    finally:
        client_socket.close()
        print("Сокет клиента закрыт.")

if __name__ == "__main__":
    run_udp_chat_client()