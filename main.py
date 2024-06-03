import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import mysql.connector

try:
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Rgt30012004',
        database='dispetcherskayadb',
        auth_plugin='mysql_native_password'
    )
except mysql.connector.Error as error:
    print(f"Ошибка при подключении к базе данных: {error}")

def clicked():
    username = username_entry.get()
    password = password_entry.get()
    if username == '1' and password == '1':
        window.withdraw()  # Скрываем окно авторизации
        main_window = create_main_window() # Создаем основное окно
    else:
        messagebox.showerror('Ошибка авторизации', "Неверный логин или пароль")

def add_window(main_window, tree):
    add_window = tk.Toplevel()
    add_window.title("Добавить рейс")
    add_window.geometry("300x300")

    # Создание полей ввода
    id_reis_label = tk.Label(add_window, text="Номер рейса:")
    id_reis_label.pack()
    id_reis_entry = tk.Entry(add_window)
    id_reis_entry.pack()

    id_bus_label = tk.Label(add_window, text="Номер автобуса:")
    id_bus_label.pack()
    id_bus_entry = tk.Entry(add_window)
    id_bus_entry.pack()

    id_city1_label = tk.Label(add_window, text="Пункт отправления:")
    id_city1_label.pack()
    id_city1_entry = tk.Entry(add_window)
    id_city1_entry.pack()

    id_city2_label = tk.Label(add_window, text="Пункт назначения:")
    id_city2_label.pack()
    id_city2_entry = tk.Entry(add_window)
    id_city2_entry.pack()

    datatime_label = tk.Label(add_window, text="Дата и время отправления:")
    datatime_label.pack()
    datatime_entry = tk.Entry(add_window)
    datatime_entry.pack()

    def save_data():
        id_reis = id_reis_entry.get()
        id_bus = id_bus_entry.get()
        id_city1 = id_city1_entry.get()
        id_city2 = id_city2_entry.get()
        datatime = datatime_entry.get()
        free_seats = 30  # Предположим, что количество свободных мест по умолчанию равно 30

        # Сохранение данных в базу данных
        mycursor = mydb.cursor()
        sql = "INSERT INTO reis (id_reis, id_bus, id_city1, id_city2, datatime, free_seats) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (id_reis, id_bus, id_city1, id_city2, datatime, free_seats)
        mycursor.execute(sql, values)
        mydb.commit()

        # Обновление таблицы в главном окне
        update_table(main_window, tree)

        add_window.destroy()

    def cancel_data():
        add_window.destroy()

    # Создание кнопок
    save_button = tk.Button(add_window, text="Сохранить", command=save_data)
    save_button.pack(pady=10)
    cancel_button = tk.Button(add_window, text="Отмена", command=cancel_data)
    cancel_button.pack(pady=10)

def edit_window(main_window, tree):
    selected_item = tree.focus()
    values = tree.item(selected_item, 'values')

    if not values:
        messagebox.showerror("Ошибка", "Пожалуйста, выберите запись для редактирования")
        return

    edit_window = tk.Toplevel()
    edit_window.title("Редактировать рейс")
    edit_window.geometry("300x300")

    # Создание полей ввода
    id_reis_label = tk.Label(edit_window, text="Номер рейса:")
    id_reis_label.pack()
    id_reis_entry = tk.Entry(edit_window)
    id_reis_entry.insert(0, values[0])
    id_reis_entry.pack()

    id_bus_label = tk.Label(edit_window, text="Номер автобуса:")
    id_bus_label.pack()
    id_bus_entry = tk.Entry(edit_window)
    id_bus_entry.insert(0, values[1])
    id_bus_entry.pack()

    id_city1_label = tk.Label(edit_window, text="Пункт отправления:")
    id_city1_label.pack()
    id_city1_entry = tk.Entry(edit_window)
    id_city1_entry.insert(0, values[2])
    id_city1_entry.pack()

    id_city2_label = tk.Label(edit_window, text="Пункт назначения:")
    id_city2_label.pack()
    id_city2_entry = tk.Entry(edit_window)
    id_city2_entry.insert(0, values[3])
    id_city2_entry.pack()

    datatime_label = tk.Label(edit_window, text="Дата и время отправления:")
    datatime_label.pack()
    datatime_entry = tk.Entry(edit_window)
    datatime_entry.insert(0, values[4])
    datatime_entry.pack()

    def save_data():
        id_reis = id_reis_entry.get()
        id_bus = id_bus_entry.get()
        id_city1 = id_city1_entry.get()
        id_city2 = id_city2_entry.get()
        datatime = datatime_entry.get()
        free_seats = values[5]  # Сохранение текущего значения свободных мест

        # Обновление данных в базе данных
        mycursor = mydb.cursor()
        sql = "UPDATE reis SET id_bus = %s, id_city1 = %s, id_city2 = %s, datatime = %s, free_seats = %s WHERE id_reis = %s"
        values = (id_bus, id_city1, id_city2, datatime, free_seats, id_reis)
        mycursor.execute(sql, values)
        mydb.commit()

        # Обновление таблицы в главном окне
        update_table(main_window, tree)

        edit_window.destroy()

    def cancel_data():
        edit_window.destroy()

    # Создание кнопок
    save_button = tk.Button(edit_window, text="Сохранить", command=save_data)
    save_button.pack(pady=10)
    cancel_button = tk.Button(edit_window, text="Отмена", command=cancel_data)
    cancel_button.pack(pady=10)


def delete_window(main_window, tree):
    selected_item = tree.focus()
    values = tree.item(selected_item, 'values')

    if not values:
        messagebox.showerror("Ошибка", "Пожалуйста, выберите запись для удаления")
        return

    delete_window = tk.Toplevel()
    delete_window.title("Удалить рейс")
    delete_window.geometry("300x150")

    confirm_label = tk.Label(delete_window, text=f"Вы действительно хотите удалить рейс № {values[0]}?")
    confirm_label.pack(pady=10)

    def delete_data():
        id_reis = values[0]

        # Удаление записи из базы данных
        mycursor = mydb.cursor()
        sql = "DELETE FROM reis WHERE id_reis = %s"
        mycursor.execute(sql, (id_reis,))
        mydb.commit()

        # Обновление таблицы в главном окне
        update_table(main_window, tree)

        delete_window.destroy()
        messagebox.showinfo("Успешно", f"Рейс № {id_reis} успешно удален")

    def cancel_data():
        delete_window.destroy()

    # Создание кнопок
    delete_button = tk.Button(delete_window, text="Удалить", command=delete_data)
    delete_button.pack(pady=10)
    cancel_button = tk.Button(delete_window, text="Отмена", command=cancel_data)
    cancel_button.pack(pady=10)


# Функция для создания основного окна диспетчерской автовокзала
def create_main_window():
    main_window = tk.Toplevel(window)
    main_window.title('Диспетчерская автовокзала')
    main_window["bg"] = "#E0FFFF"
    main_window.geometry('800x600')
    main_window.resizable(False, False)

    # Создание холста для рисования
    canvas = tk.Canvas(main_window, width=800, height=50, bg="#008B8B")
    canvas.pack()

    def search():
        search_text = entry.get()
        # Здесь можно добавить код для обработки введенного текста поиска

    # Создание левого фрейма для кнопок
    left_frame = tk.Frame(main_window, bg="#E0FFFF")
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

    # Создайте строку поиска (Entry)
    entry = tk.Entry(left_frame, width=40)
    entry.pack(pady=10)

    # Создайте кнопку для выполнения поиска
    search_button = tk.Button(left_frame, text='Поиск', command=search, bg="#20B2AA", width=15, height=1)
    search_button.pack(pady=10)

    # Создание кнопок
    add_btn = tk.Button(left_frame, text='Добавить', command=lambda: add_window(main_window, tree), bg="#20B2AA",
                        width=15, height=1)
    add_btn.pack(pady=10)
    edit_btn = tk.Button(left_frame, text='Редактировать', command=lambda: edit_window(main_window, tree), bg="#20B2AA",
                         width=15, height=1)
    edit_btn.pack(pady=10)
    delete_btn = tk.Button(left_frame, text='Удалить', command=lambda: delete_window(main_window, tree), bg="#20B2AA",
                           width=15, height=1)
    delete_btn.pack(pady=10)

    # Создание правого фрейма для таблицы
    right_frame = tk.Frame(main_window, bg="#E0FFFF")
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    columns = ("id_reis", "id_bus", "id_city1", "id_city2", "datatime", "free_seats")
    tree = ttk.Treeview(right_frame, columns=columns, show="headings")

    # Настройка заголовков столбцов
    tree.heading("id_reis", text="Номер рейса")
    tree.heading("id_bus", text="Номер автобуса")
    tree.heading("id_city1", text="Пункт отправления")
    tree.heading("id_city2", text="Пункт назначения")
    tree.heading("datatime", text="Дата и время отправления")
    tree.heading("free_seats", text="Свободные места")

    # Настройка ширины столбцов
    tree.column("id_reis", width=100)
    tree.column("id_bus", width=100)
    tree.column("id_city1", width=150)
    tree.column("id_city2", width=150)
    tree.column("datatime", width=150)
    tree.column("free_seats", width=100)

    tree.pack(fill=tk.BOTH, expand=True)

    update_table(main_window, tree)

    return main_window


def update_table(main_window, tree):
    # Очистка таблицы
    for item in tree.get_children():
        tree.delete(item)

    # Получение данных из базы данных
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM reis")
    results = mycursor.fetchall()

    # Заполнение таблицы данными
    for row in results:
        tree.insert("", tk.END, values=row)


class Reis:
    def __init__(self, id_reis, id_bus, id_city1, id_city2, datatime, free_seats):
        self.id_reis = id_reis
        self.id_bus = id_bus
        self.id_city1 = id_city1
        self.id_city2 = id_city2
        self.datatime = datatime
        self.free_seats = free_seats


class City1:
    def __init__(self, id_city1, name_city1):
        self.id_city1 = id_city1
        self.name_city1 = name_city1


class City2:
    def __init__(self, id_city2, name_city2):
        self.id_city2 = id_city2
        self.name_city2 = name_city2


class Tickets:
    def __init__(self, id_ticket, id_reis, id_bus, id_seats, datatime, id_passager):
        self.id_ticket = id_ticket
        self.id_reis = id_reis
        self.id_bus = id_bus
        self.id_seats = id_seats
        self.datatime = datatime
        self.id_passager = id_passager


class Bus:
    def __init__(self, id_bus, namber_bus, ranges, model):
        self.id_bus = id_bus
        self.namber_bus = namber_bus
        self.ranges = ranges
        self.model = model


class Seats:
    def __init__(self, id_bus, id_seat):
        self.id_bus = id_bus
        self.id_seat = id_seat


font_header = ('Arial', 15)
font_entry = ('Arial', 12)
label_font = ('Arial', 11)
base_padding = {'padx': 10, 'pady': 8}
header_padding = {'padx': 10, 'pady': 12}

window = tk.Tk()
window.configure(bg="#E0FFFF")
window.title('Авторизация')
window.geometry('450x330')
window.resizable(False, False)

main_label = tk.Label(window, text='Авторизация', font=font_header, justify=tk.CENTER, **header_padding, bg="#E0FFFF")
main_label.pack()
username_label = tk.Label(window, text='Имя пользователя', font=label_font, **base_padding, bg="#E0FFFF")
username_label.pack()

username_entry = tk.Entry(window, bg='#fff', fg='#444', font=font_entry)
username_entry.pack()

password_label = tk.Label(window, text='Пароль', font=label_font, **base_padding, bg="#E0FFFF")
password_label.pack()

password_entry = tk.Entry(window, show="*", bg='#fff', fg='#444', font=font_entry)
password_entry.pack()

send_btn = tk.Button(window, text='Войти', command=clicked, bg="#20B2AA")
send_btn.pack(**base_padding)

window.mainloop()