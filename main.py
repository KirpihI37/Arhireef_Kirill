import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

# Предопределённый список цитат
quotes = [
    {"text": "Будь собой; все остальные уже заняты.", "author": "Оскар Уайльд", "topic": "саморазвитие"},
    {"text": "Жизнь — это то, что происходит, пока ты строишь планы.", "author": "Джон Леннон", "topic": "жизнь"},
    {"text": "Лучше зажечь свечу, чем проклинать тьму.", "author": "Конфуций", "topic": "мудрость"},
    {"text": "Успех — это сумма маленьких усилий, повторяемых день за днём.", "author": "Роберт Колльер", "topic": "успех"},
    {"text": "Образование — это самое мощное оружие, которое вы можете использовать, чтобы изменить мир.", "author": "Нельсон Мандела", "topic": "образование"},
]

history = []

def load_history():
    global history
    if os.path.exists('history.json'):
        with open('history.json', 'r', encoding='utf-8') as f:
            history = json.load(f)

def save_history():
    with open('history.json', 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

def generate_quote():
    quote = random.choice(quotes)
    display_quote(quote)
    history.append(quote)
    refresh_history()

def display_quote(quote):
    label_quote.config(text=f'"{quote["text"]}"\n\n- {quote["author"]} ({quote["topic"]})')

def refresh_history(filtered=None):
    listbox_history.delete(0, tk.END)
    data = filtered if filtered is not None else history
    for q in data:
        listbox_history.insert(tk.END, f'"{q["text"]}" - {q["author"]} ({q["topic"]})')

def filter_history():
    author_filter = entry_author_filter.get().strip()
    topic_filter = entry_topic_filter.get().strip()

    filtered = history
    if author_filter:
        filtered = [q for q in filtered if q['author'].lower() == author_filter.lower()]
    if topic_filter:
        filtered = [q for q in filtered if q['topic'].lower() == topic_filter.lower()]

    refresh_history(filtered)

# GUI
root = tk.Tk()
root.title("Random Quote Generator")

# Текущая цитата
frame_current = tk.Frame(root)
frame_current.pack(padx=10, pady=10)

label_quote = tk.Label(frame_current, text="", wraplength=400, justify='center', font=('Arial', 14))
label_quote.pack()

btn_generate = tk.Button(root, text="Сгенерировать цитату", command=generate_quote)
btn_generate.pack(pady=5)

# История
frame_history = tk.Frame(root)
frame_history.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

tk.Label(frame_history, text="История").grid(row=0, column=0, columnspan=2)

listbox_history = tk.Listbox(frame_history, height=10, width=80)
listbox_history.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

# Фильтр
tk.Label(frame_history, text="Фильтр по автору").grid(row=2, column=0, sticky='e')
entry_author_filter = tk.Entry(frame_history)
entry_author_filter.grid(row=2, column=1, sticky='w')

tk.Label(frame_history, text="Фильтр по теме").grid(row=3, column=0, sticky='e')
entry_topic_filter = tk.Entry(frame_history)
entry_topic_filter.grid(row=3, column=1, sticky='w')

btn_filter = tk.Button(frame_history, text="Применить фильтр", command=filter_history)
btn_filter.grid(row=4, column=0, columnspan=2, pady=5)

# Загрузка истории при запуске
load_history()
refresh_history()

# Сохраняем историю при закрытии
def on_closing():
    save_history()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
