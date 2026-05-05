import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os

# Глобальные переменные
books = []

# Функции для работы с JSON
def load_books():
    global books
    if os.path.exists('books.json'):
        with open('books.json', 'r', encoding='utf-8') as f:
            books = json.load(f)
    else:
        books = []

def save_books():
    with open('books.json', 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=4)

# Функция добавления книги
def add_book():
    title = entry_title.get().strip()
    author = entry_author.get().strip()
    genre = entry_genre.get().strip()
    pages = entry_pages.get().strip()

    # Проверка корректности
    if not title or not author or not genre or not pages:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
        return
    if not pages.isdigit():
        messagebox.showerror("Ошибка", "Количество страниц должно быть числом")
        return

    book = {
        "title": title,
        "author": author,
        "genre": genre,
        "pages": int(pages)
    }
    books.append(book)
    refresh_treeview()
    clear_entries()

def clear_entries():
    entry_title.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    entry_genre.delete(0, tk.END)
    entry_pages.delete(0, tk.END)

# Функция обновления таблицы
def refresh_treeview(filtered_books=None):
    for item in tree.get_children():
        tree.delete(item)
    data = filtered_books if filtered_books is not None else books
    for book in data:
        tree.insert('', tk.END, values=(book['title'], book['author'], book['genre'], book['pages']))

# Фильтрация
def filter_books():
    genre_filter = filter_genre_var.get()
    pages_filter = filter_pages_var.get()

    filtered = books
    if genre_filter != "Все":
        filtered = [b for b in filtered if b['genre'] == genre_filter]
    if pages_filter:
        try:
            pages_threshold = int(pages_filter)
            filtered = [b for b in filtered if b['pages'] > pages_threshold]
        except ValueError:
            messagebox.showerror("Ошибка", "Порог страниц должен быть числом")
            return
    refresh_treeview(filtered)

# Сохранить и загрузить
def save_data():
    save_books()

def load_data():
    load_books()
    refresh_treeview()

# Создание GUI
root = tk.Tk()
root.title("Book Tracker")

# Ввод данных
frame_input = tk.Frame(root)
frame_input.pack(padx=10, pady=10)

tk.Label(frame_input, text="Название книги").grid(row=0, column=0)
entry_title = tk.Entry(frame_input)
entry_title.grid(row=0, column=1)

tk.Label(frame_input, text="Автор").grid(row=1, column=0)
entry_author = tk.Entry(frame_input)
entry_author.grid(row=1, column=1)

tk.Label(frame_input, text="Жанр").grid(row=2, column=0)
entry_genre = tk.Entry(frame_input)
entry_genre.grid(row=2, column=1)

tk.Label(frame_input, text="Количество страниц").grid(row=3, column=0)
entry_pages = tk.Entry(frame_input)
entry_pages.grid(row=3, column=1)

btn_add = tk.Button(frame_input, text="Добавить книгу", command=add_book)
btn_add.grid(row=4, column=0, columnspan=2, pady=5)

# Таблица
columns = ('title', 'author', 'genre', 'pages')
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col.capitalize())

tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Фильтр
frame_filter = tk.Frame(root)
frame_filter.pack(padx=10, pady=5)

tk.Label(frame_filter, text="Фильтр по жанру").grid(row=0, column=0)
genres = ["Все"]
# Можно расширить список жанров автоматически
genres += list({b['genre'] for b in books})
filter_genre_var = tk.StringVar(value="Все")
genre_menu = ttk.Combobox(frame_filter, textvariable=filter_genre_var, values=genres)
genre_menu.grid(row=0, column=1)
genre_menu.bind("<<ComboboxSelected>>", lambda e: filter_books())

tk.Label(frame_filter, text="Показать книги с количеством страниц больше").grid(row=0, column=2)
filter_pages_var = tk.StringVar()
entry_filter_pages = tk.Entry(frame_filter, textvariable=filter_pages_var)
entry_filter_pages.grid(row=0, column=3)

btn_filter = tk.Button(frame_filter, text="Применить фильтр", command=filter_books)
btn_filter.grid(row=0, column=4, padx=5)

# Загрузка данных при запуске
load_books()
refresh_treeview()

# Сохранение данных при закрытии
def on_closing():
    save_books()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
