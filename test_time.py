import threading
import http.client
import time

HOST = "127.0.0.1"
PORT = 8000
ENDPOINT = "/"

def make_request(thread_id):
    try:
        conn = http.client.HTTPConnection(HOST, PORT, timeout=5)
        conn.request("GET", ENDPOINT)
        response = conn.getresponse()
        print(f"Thread {thread_id}: {response.status} {response.reason}")
        conn.close()
    except Exception as e:
        print(f"Thread {thread_id}: Error - {e}")

def main():
    num_requests = 1000
    threads = []

    print("Starting test...")

    start_time = time.time()

    for i in range(num_requests):
        thread = threading.Thread(target=make_request, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()

    print(f"Test completed. Time taken: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
