import threading, socket, os, time
from Main.serverMain import start as serverMainStart
from Api.serverApi import start as serverApiStart

def updating():
    startTime = time.time()
    os.system("cls")
    while True:
        seconds = int(time.time() - startTime)
        days, hours, minutes = seconds // 86400, seconds // 3600, seconds // 60
        print(f"""############################################\nЗапущены два сервера:\n\t* Основной сайт: http://{socket.gethostbyname(socket.gethostname())}\n\t* Сайт с api ИИ: http://127.0.0.1:433\n############################################\nСервер запущен: {days}d {hours % 24}h {minutes % 60}m {seconds % 60}s""")
        time.sleep(1)
        os.system("cls")

if __name__ == "__main__":
    [task.start() for task in [threading.Thread(target=serverMainStart), threading.Thread(target=serverApiStart), threading.Thread(target=updating)]]
