
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import re
import csv
import json
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from models import Client, Product, Order  # Импортируем классы
from db import Database  # Импортируем нашу базу данных
import analysis  # Импортируем модуль анализа


class OrderManagementApp:
    """
    Основной класс приложения для управления заказами, клиентами и товарами.

    Атрибуты
    --------
    root : tkinter.Tk
        Главное окно приложения.
    db : Database
        Объект подключения и взаимодействия с базой данных.
    notebook : ttk.Notebook
        Виджет вкладок интерфейса.
    clients_tab : ttk.Frame
        Вкладка для работы с клиентами.
    products_tab : ttk.Frame
        Вкладка для работы с товарами.
    orders_tab : ttk.Frame
        Вкладка для работы с заказами.
    charts_tab : ttk.Frame
        Вкладка для отображения графиков.
    export_tab : ttk.Frame
        Вкладка для экспорта данных.

    Методы
    -------
    create_product_widgets():
        Создает интерфейс для добавления и отображения товаров.
    save_product():
        Сохраняет новый товар в базу данных.
    is_valid_price(price):
        Проверяет корректность введенной цены.
    create_order_widgets():
        Создает интерфейс для добавления нового заказа.
    load_clients():
        Загружает список клиентов из базы данных и отображает.
    load_products():
        Загружает список товаров из базы данных.
    add_order():
        Добавляет новый заказ в базу данных.
    get_client_id(client_name):
        Возвращает id клиента по его имени.
    get_product_id(product_name):
        Возвращает id товара по его названию.
    create_client_widgets():
        Создает интерфейс для добавления и удаления клиентов.
    add_entry():
        Добавляет нового клиента.
    delete_entry():
        Удаляет выбранного клиента.
    is_valid_name(name):
        Проверяет корректность имени.
    is_valid_email(email):
        Проверяет правильность email.
    is_valid_phone(phone):
        Проверяет корректность номера телефона.
    create_export_widgets():
        Создает интерфейс для экспорта данных.
    export_to_csv():
        Экспортирует данные в CSV файл.
    export_to_json():
        Экспортирует данные в JSON файл.
    create_chart_widgets():
        Создает кнопки для отображения аналитических графиков.
    show_top_clients():
        Отображает топ-5 клиентов по заказам.
    show_order_trends():
        Показывает динамику заказов по датам.
    show_client_network():
        Визуализирует сеть клиентов.
    on_closing():
        Обрабатывает событие закрытия окна, закрывает соединение с БД.
    """

    def __init__(self, root):
        """
        Инициализация главного окна и компонентов интерфейса.

        Parameters
        ----------
        root : tkinter.Tk
            Главное окно приложения.
        """
        self.root = root
        self.db = Database()  # Инициализируем базу данных

        self.root.title("Система учета заказов")
        self.root.geometry("800x600+300+300")
        self.root.config(bg="grey")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        # Создание вкладок
        self.clients_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.clients_tab, text='Клиенты')

        self.products_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.products_tab, text='Товары')

        self.orders_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.orders_tab, text='Заказы')

        self.charts_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.charts_tab, text='Графики')

        self.export_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.export_tab, text='Экспорт')

        # Создание интерфейсов
        self.create_client_widgets()
        self.create_product_widgets()
        self.create_order_widgets()
        self.create_export_widgets()
        self.create_chart_widgets()

        # Загружаем данные из базы
        self.load_clients()
        self.load_products()

    def create_product_widgets(self):
        """
        Создает интерфейс для добавления товаров и отображения существующих.
        """
        self.product_name_var = tk.StringVar()
        self.product_price_var = tk.StringVar()

        tk.Label(self.products_tab, text="Введите название товара:", font=('Arial', 10, 'bold')).pack(pady=5)
        tk.Entry(self.products_tab, textvariable=self.product_name_var, width=30).pack(pady=5)

        tk.Label(self.products_tab, text="Введите цену товара:", font=('Arial', 10, 'bold')).pack(pady=5)
        tk.Entry(self.products_tab, textvariable=self.product_price_var, width=30).pack(pady=5)

        tk.Button(self.products_tab, text="Сохранить товар", command=self.save_product).pack(pady=10)

        self.product_display = tk.Text(self.products_tab, height=15, width=50)
        self.product_display.pack(pady=10)

    def save_product(self):
        """
        Сохраняет товар в базу данных, при проверке валидности данных.
        """
        product_name = self.product_name_var.get()
        product_price = self.product_price_var.get()

        if product_name and self.is_valid_price(product_price):
            price = float(product_price)
            self.db.add_product(product_name, price)
            self.product_display.insert(tk.END, f'Товар: {product_name}, Цена: {price:.2f}\n')
            self.product_name_var.set("")
            self.product_price_var.set("")
        else:
            messagebox.showwarning("Ошибка", "Пожалуйста, введите корректное название и цену товара.")

    def is_valid_price(self, price):
        """
        Проверяет, что введенная цена является числом.

        Parameters
        ----------
        price : str
            Введенная строка с ценой.

        Returns
        -------
        bool
            True, если цена является числом, иначе False.
        """
        try:
            float(price)
            return True
        except ValueError:
            return False

    def create_order_widgets(self):
        """
        Создает интерфейс выбора клиента и товара для добавления заказа.
        """
        self.client_var = tk.StringVar()
        self.product_var = tk.StringVar()

        tk.Label(self.orders_tab, text="Выберите клиента:", font=('Arial', 10, 'bold')).pack(pady=5)
        self.client_dropdown = ttk.Combobox(self.orders_tab, textvariable=self.client_var)
        self.client_dropdown.pack(pady=5)

        tk.Label(self.orders_tab, text="Выберите товар:", font=('Arial', 10, 'bold')).pack(pady=5)
        self.product_dropdown = ttk.Combobox(self.orders_tab, textvariable=self.product_var)
        self.product_dropdown.pack(pady=5)
        self.load_products()

        tk.Button(self.orders_tab, text="Добавить заказ", command=self.add_order).pack(pady=10)

        self.orders_display = tk.Text(self.orders_tab, height=15, width=50)
        self.orders_display.pack(pady=10)

    def load_clients(self):
        """
        Загружает список клиентов из базы и отображает их в интерфейсе.
        """
        clients = self.db.get_all_clients()
        self.client_dropdown['values'] = [client[1] for client in clients]  # Имена клиентов
        # Предполагается, что каждый клиент - кортеж (id, name, email, phone)

        # дополнительно можно обновить список отображения
        # (здесь вызывается, например, только для обновления dropdown)

    def load_products(self):
        """
        Загружает список товаров из базы.
        """
        products = self.db.get_all_products()
        self.product_dropdown['values'] = [product[1] for product in products]  # Имена продуктов

    def add_order(self):
        """
        Добавляет заказ в базу, исходя из выбранных клиента и товара.
        """
        selected_client_name = self.client_var.get()
        selected_product_name = self.product_var.get()

        client_id = self.get_client_id(selected_client_name)
        product_id = self.get_product_id(selected_product_name)

        if client_id is not None and product_id is not None:
            self.orders_display.insert(tk.END, f'Клиент: {selected_client_name}, Товар: {selected_product_name}\n')
            self.db.add_order(Order(client_id, product_id))
        else:
            messagebox.showwarning("Ошибка", "Пожалуйста, выберите клиента и товар.")

    def get_client_id(self, client_name):
        """
        Ищет id клиента по имени.

        Parameters
        ----------
        client_name : str
            Имя клиента.

        Returns
        -------
        int or None
            Идентификатор клиента или None, если не найден.
        """
        client = next((client for client in self.db.get_all_clients() if client[1] == client_name), None)
        return client[0] if client else None

    def get_product_id(self, product_name):
        """
        Ищет id товара по названию.

        Parameters
        ----------
        product_name : str
            Название товара.

        Returns
        -------
        int or None
            Идентификатор товара или None, если не найден.
        """
        product = next((product for product in self.db.get_all_products() if product[1] == product_name), None)
        return product[0] if product else None
        self.load_products()

    def create_client_widgets(self):
        """
        Создает интерфейс для ввода данных клиентов и управления списком.
        """
        tk.Label(self.clients_tab, text="Введите имя клиента:", font=('Arial', 10, 'bold')).grid(row=1, column=0,
                                                                                                 sticky=tk.W, pady=5,
                                                                                                 padx=5)
        self.entry_1 = tk.Entry(self.clients_tab)
        self.entry_1.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(self.clients_tab, text="Введите e-mail:", font=('Arial', 10, 'bold')).grid(row=2, column=0,
                                                                                            sticky=tk.W, pady=5, padx=5)
        self.entry_2 = tk.Entry(self.clients_tab)
        self.entry_2.grid(row=2, column=1, pady=5, padx=5)

        tk.Label(self.clients_tab, text="Введите номер телефона:", font=('Arial', 10, 'bold')).grid(row=3, column=0,
                                                                                                    sticky=tk.W, pady=5,
                                                                                                    padx=5)
        self.entry_3 = tk.Entry(self.clients_tab)
        self.entry_3.grid(row=3, column=1, pady=5, padx=5)

        tk.Label(self.clients_tab, text="Имя    |    E-mail    |    Номер телефона", font=('Arial', 12, 'bold')).grid(
            row=4, column=0, columnspan=2, sticky=tk.W + tk.E, pady=3, padx=3)

        self.task_listbox = tk.Listbox(self.clients_tab, width=50, height=10)
        self.task_listbox.grid(row=5, column=0, columnspan=2, pady=10)

        tk.Button(self.clients_tab, text="Добавить", command=self.add_entry).grid(row=6, column=1, sticky=tk.E, pady=5,
                                                                                  padx=5)
        tk.Button(self.clients_tab, text="Удалить", command=self.delete_entry).grid(row=6, column=0, sticky=tk.W,
                                                                                    pady=5, padx=5)

    def add_entry(self):
        """
        Добавляет нового клиента после валидации данных.
        """
        name = self.entry_1.get().strip()
        email = self.entry_2.get().strip()
        phone = self.entry_3.get().strip()

        if not self.is_valid_name(name):
            messagebox.showwarning("Ввод неверен", "Имя клиента должно содержать только буквы и пробелы.")
            return

        if not self.is_valid_email(email):
            messagebox.showwarning("Ввод неверен", "Пожалуйста, введите корректный e-mail.")
            return

        if not self.is_valid_phone(phone):
            messagebox.showwarning("Ввод неверен", "Номер телефона должен содержать ровно 10 цифр.")
            return

        self.db.add_client(name, email, phone)
        self.task_listbox.insert(tk.END, f"{name} | {email} | {phone}")

        self.entry_1.delete(0, tk.END)
        self.entry_2.delete(0, tk.END)
        self.entry_3.delete(0, tk.END)
        self.load_clients()

    def delete_entry(self):
        """
        Удаляет выбранного клиента из базы данных и интерфейса.
        """
        selected_index = self.task_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Удаление", "Пожалуйста, выберите клиента для удаления.")
            return

        selected_entry = self.task_listbox.get(selected_index)
        name = selected_entry.split(" | ")[0]
        self.db.delete_client(name)  # Предполагается, что этот метод реализован
        self.task_listbox.delete(selected_index)
        messagebox.showinfo("Удаление", f"Клиент '{name}' успешно удален.")
        self.load_clients()

    def is_valid_name(self, name):
        """
        Проверяет, что имя содержит только буквы и пробелы.

        Parameters
        ----------
        name : str
            Имя клиента.

        Returns
        -------
        bool
            True, если имя корректно, иначе False.
        """
        return bool(name) and all(c.isalpha() or c.isspace() for c in name)

    def is_valid_email(self, email):
        """
        Проверяет валидность email.

        Parameters
        ----------
        email : str
            Электронная почта.

        Returns
        -------
        bool
            True, если email валиден, иначе False.
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def is_valid_phone(self, phone):
        """
        Проверяет, что номер телефона состоит из 10 цифр.

        Parameters
        ----------
        phone : str
            Номер телефона.

        Returns
        -------
        bool
            True, если номер валиден, иначе False.
        """
        return phone.isdigit() and len(phone) == 10

    def create_export_widgets(self):
        """
        Создает интерфейс для экспорта данных в CSV и JSON.
        """
        tk.Label(self.export_tab, text="Экспортировать данные:", font=('Arial', 10, 'bold')).pack(pady=10)

        export_csv_button = tk.Button(self.export_tab, text="Экспорт в CSV", command=self.export_to_csv)
        export_csv_button.pack(pady=5)

        export_json_button = tk.Button(self.export_tab, text="Экспорт в JSON", command=self.export_to_json)
        export_json_button.pack(pady=5)

    def export_to_csv(self):
        """
        Экспортирует список клиентов и заказов в CSV-файл.
        """
        file_path = filedialog.asksaveasfilename(defaultextension='.csv',
                                                 filetypes=[("CSV files", '*.csv'), ("All files", '*.*')])
        if not file_path:
            return

        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Имя", "E-mail", "Номер телефона"])

            for i in range(self.task_listbox.size()):
                entry = self.task_listbox.get(i).split(" | ")
                writer.writerow(entry)

        messagebox.showinfo("Экспорт завершен", "Данные успешно экспортированы в CSV.")

    def export_to_json(self):
        """
        Экспортирует список клиентов и заказов в JSON-файл.
        """
        file_path = filedialog.asksaveasfilename(defaultextension='.json',
                                                 filetypes=[("JSON files", '*.json'), ("All files", '*.*')])
        if not file_path:
            return

        data = [{"name": entry.split(" | ")[0],
                 "email": entry.split(" | ")[1],
                 "phone": entry.split(" | ")[2]} for entry in self.task_listbox.get(0, tk.END)]

        with open(file_path, mode='w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        messagebox.showinfo("Экспорт завершен", "Данные успешно экспортированы в JSON.")

    def create_chart_widgets(self):
        """
        Создает кнопки для отображения графиков аналитики.
        """
        tk.Button(self.charts_tab, text="ТОП-5 клиентов", command=self.show_top_clients).pack(pady=10)
        tk.Button(self.charts_tab, text="Динамика заказов", command=self.show_order_trends).pack(pady=10)
        tk.Button(self.charts_tab, text="География клиентов", command=self.show_client_network).pack(pady=10)

    def show_top_clients(self):
        """
        Отображает график топ-5 клиентов по заказам.
        """
        df_top_clients = analysis.top_clients(self.db.connection)
        plt.figure(figsize=(10, 5))
        sns.barplot(x='order_count', hue='name', data=df_top_clients, palette='viridis')
        plt.title("ТОП-5 клиентов по количеству заказов")
        plt.xlabel("Количество заказов")
        plt.ylabel("Клиенты")
        plt.show()

    def show_order_trends(self):
        """
        Отображает график динамики заказов по датам.
        """
        df_order_trends = analysis.order_trends(self.db.connection)
        plt.figure(figsize=(10, 5))
        sns.lineplot(x='order_date', y='order_count', data=df_order_trends, marker='o')
        plt.title("Динамика количества заказов по датам")
        plt.xticks(rotation=45)
        plt.xlabel("Дата")
        plt.ylabel("Количество заказов")
        plt.show()

    def show_client_network(self):
        """
        Визуализирует сеть клиентов с помощью графа.
        """
        G = analysis.client_network(self.db.connection)
        plt.figure(figsize=(12, 12))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, labels=nx.get_node_attributes(G, 'label'))
        plt.title("Сеть клиентов")
        plt.show()

    def on_closing(self):
        """
        Обрабатывает событие закрытия окна: закрывает соединение с БД.
        """
        self.db.close()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = OrderManagementApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
