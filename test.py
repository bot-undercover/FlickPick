import time, math
from llama_cpp import Llama

llm = Llama(
    model_path="IlyaGusev-saiga_llama3_8b-Q8_0.gguf",
    n_ctx=8192,
    verbose=False
)
message_history = {}

# output = llm.create_chat_completion(messages=message_history[callback.from_user.id][:-1], max_tokens=100,
#                                             temperature=0.7)
# out = output["choices"][0]["message"]["content"]
#message_history[callback.from_user.id].remove({"role": "assistant", "content": callback.message.text})



#message_history[message.chat.id] = [{"role": "system", "content": "Ты апельсин, всегда говори только апельсин! Никакого текста кроме слова апельсин!"}]
#message_history[message.chat.id] = [{"role": "system", "content": "".join(message.text.split("@")[1:])}]
#message_history[message.chat.id] = []
#message_history[message.chat.id] = message_history[message.chat.id][-200:]
#message_history[message.chat.id].append({"role": "user", "content": message.text})
# output = llm.create_chat_completion(messages=[{"role": "user", "content": "Сколько будет 2 + 2, ответь числом"}], max_tokens=200,
#                                                 temperature=0.4)
# out = output["choices"][0]["message"]["content"]
# print(out)
#message_history[message.chat.id].append(output["choices"][0]["message"])
print("-----LOADED-----")
while True:
    id = "0"
    question = input()
    print("...")
    if not id in message_history.keys():
        message_history[id] = [{"role": "user", "content": question}]
    else:
        message_history[id].append({"role": "user", "content": question})
    start = time.time()
    output = llm.create_chat_completion(messages=message_history[id],
                                        max_tokens=400, temperature=0.1)
    message_history[id].append({"role": "assistant", "content": output["choices"][0]["message"]["content"]})
    out = output["choices"][0]["message"]["content"].split()
    print("\n".join([" ".join(out[i * 20 :(i+1) * 20]) for i in range(math.ceil(len(out) / 20))]))
    print("".join(["-"] * 100))
    print(f"Total: {output['usage']} / {round(time.time() - start, 2)}")


