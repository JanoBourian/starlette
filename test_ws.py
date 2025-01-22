import threading
import asyncio
import websockets
import time
import random
import string

HOST = "127.0.0.1"
PORT = 8000
ENDPOINT = "/ws"
URL = f"ws://{HOST}:{PORT}{ENDPOINT}"

def generate_random_text(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

async def websocket_client(thread_id):
    try:
        async with websockets.connect(URL) as websocket:
            while True:
                message = generate_random_text()
                await websocket.send(f"Client {thread_id}: {message}")
                response = await websocket.recv()
                print(f"Thread {thread_id}: Received response - {response}")
                await asyncio.sleep(0.5)
    except Exception as e:
        print(f"Thread {thread_id}: Error - {e}")

def manage_connection(thread_id):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(websocket_client(thread_id))

def main():
    num_clients = 1000
    threads = []

    print("Starting WebSocket test...")
    start_time = time.time()

    for i in range(num_clients):
        thread = threading.Thread(target=manage_connection, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"Test completed. Time taken: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
