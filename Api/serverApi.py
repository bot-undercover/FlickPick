from flask import Flask, request, render_template
from llama_cpp import Llama
import string
from random import choice
from multiprocessing import Process, Queue

GlobalThreads = {}
app = Flask(__name__)


def genAnswer(llm, text, q):
    q.put(llm.create_chat_completion(messages=[{"role": "user", "content": text}],
                                     max_tokens=400, temperature=0.1)["choices"][0]["message"]["content"])


def genKey():
    return "".join([choice(string.ascii_letters + string.digits) for _ in range(128)])


@app.route('/')
def main():
    return render_template("base.html", ip="127.0.0.1")


@app.route('/api', methods=['GET', 'POST'])
def index():
    out = {}
    if request.method == 'POST':
        data = eval(request.get_data())
        action = data["action"]
        if action == "generate":
            q = Queue()
            p = Process(target=genAnswer, args=(llm, data["text"], q))
            p.start()
            key = genKey()
            out["key"] = key
            GlobalThreads[key] = [p, q]
        elif action == "get":
            if data["key"] in GlobalThreads.keys() and not GlobalThreads[data["key"]][0].is_alive():
                out["answer"] = GlobalThreads[data["key"]][1].get()
                del GlobalThreads[data["key"]]
            else:
                out["answer"] = str(None)
    return str(out)


def start(debug=False, modelPath="./IlyaGusev-saiga_llama3_8b-Q8_0.gguf"):
    global llm
    llm = Llama(
        model_path=modelPath,
        n_ctx=8192,
        verbose=False
    )
    app.run(port=433, debug=debug)


if __name__ == '__main__':
    start(True, "./IlyaGusev-saiga_llama3_8b-Q8_0.gguf")
