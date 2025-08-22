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
    def __init__(self, root):
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
        try:
            float(price)
            return True
        except ValueError:
            return False

    def create_order_widgets(self):
        self.client_var = tk.StringVar()
        self.product_var = tk.StringVar()

        tk.Label(self.orders_tab, text="Выберите клиента:", font=('Arial', 10, 'bold')).pack(pady=5)
        self.client_dropdown = ttk.Combobox(self.orders_tab, textvariable=self.client_var)
        self.client_dropdown.pack(pady=5)

        tk.Label(self.orders_tab, text="Выберите товар:", font=('Arial', 10, 'bold')).pack(pady=5)
        self.product_dropdown = ttk.Combobox(self.orders_tab, textvariable=self.product_var)
        self.product_dropdown.pack(pady=5)

        tk.Button(self.orders_tab, text="Добавить заказ", command=self.add_order).pack(pady=10)

        self.orders_display = tk.Text(self.orders_tab, height=15, width=50)
        self.orders_display.pack(pady=10)

    def load_clients(self):
        clients = self.db.get_all_clients()
        self.client_dropdown['values'] = [client[1] for client in clients]  # Имена клиентов
        self.task_listbox.delete(0, tk.END)  # Очищаем перед загрузкой
        for client in clients:  # Изменено на итерацию по clients
            client_id, name, email, phone = client  # Ожидаем, что возвращается id, name, email, phone
            self.task_listbox.insert(tk.END, f"{name} | {email} | {phone}")

    def load_products(self):
        products = self.db.get_all_products()
        self.product_dropdown['values'] = [product[1] for product in products]  # Имена продуктов

    def add_order(self):
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
        client = next((client for client in self.db.get_all_clients() if client[1] == client_name), None)
        return client[0] if client else None

    def get_product_id(self, product_name):
        product = next((product for product in self.db.get_all_products() if product[1] == product_name), None)
        return product[0] if product else None

    def create_client_widgets(self):
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

    def delete_entry(self):
        selected_index = self.task_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Удаление", "Пожалуйста, выберите клиента для удаления.")
            return

        selected_entry = self.task_listbox.get(selected_index)
        name = selected_entry.split(" | ")[0]
        self.db.delete_client(name)  # Предполагается, что метод удаления клиента реализован в db

        self.task_listbox.delete(selected_index)
        messagebox.showinfo("Удаление", f"Клиент '{name}' успешно удален.")

    def is_valid_name(self, name):
        return bool(name) and all(c.isalpha() or c.isspace() for c in name)

    def is_valid_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def is_valid_phone(self, phone):
        return phone.isdigit() and len(phone) == 10  # Предполагаем, что номер состоит из 10 цифр

    def create_export_widgets(self):
        tk.Label(self.export_tab, text="Экспортировать данные:", font=('Arial', 10, 'bold')).pack(pady=10)

        export_csv_button = tk.Button(self.export_tab, text="Экспорт в CSV", command=self.export_to_csv)
        export_csv_button.pack(pady=5)

        export_json_button = tk.Button(self.export_tab, text="Экспорт в JSON", command=self.export_to_json)
        export_json_button.pack(pady=5)

    def export_to_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension='.csv',
                                                 filetypes=[("CSV files", '*.csv'), ("All files", '*.*')])
        if not file_path:
            return

        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Имя", "E-mail", "Номер телефона"])  # Заголовки колонок

            for i in range(self.task_listbox.size()):
                entry = self.task_listbox.get(i).split(" | ")
                writer.writerow(entry)

        messagebox.showinfo("Экспорт завершен", "Данные успешно экспортированы в CSV.")

    def export_to_json(self):
        file_path = filedialog.asksaveasfilename(defaultextension='.json',
                                                 filetypes=[("JSON files", '*.json'), ("All files", '*.*')])
        if not file_path:
            return

        data = [{"name": entry.split(" | ")[0], "email": entry.split(" | ")[1], "phone": entry.split(" | ")[2]} for
                entry in self.task_listbox.get(0, tk.END)]

        with open(file_path, mode='w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        messagebox.showinfo("Экспорт завершен", "Данные успешно экспортированы в JSON.")

    def create_chart_widgets(self):
        tk.Button(self.charts_tab, text="ТОП-5 клиентов", command=self.show_top_clients).pack(pady=10)
        tk.Button(self.charts_tab, text="Динамика заказов", command=self.show_order_trends).pack(pady=10)
        tk.Button(self.charts_tab, text="Сеть клиентов", command=self.show_client_network).pack(pady=10)

    def show_top_clients(self):
        df_top_clients = analysis.top_clients(self.db.connection)
        plt.figure(figsize=(10, 5))
        sns.barplot(x='order_count', hue='name', data=df_top_clients, palette='viridis')
        plt.title("ТОП-5 клиентов по количеству заказов")
        plt.xlabel("Количество заказов")
        plt.ylabel("Клиенты")
        plt.show()

    def show_order_trends(self):
        df_order_trends = analysis.order_trends(self.db.connection)
        plt.figure(figsize=(10, 5))
        sns.lineplot(x='order_date', y='order_count', data=df_order_trends, marker='o')
        plt.title("Динамика количества заказов по датам")
        plt.xticks(rotation=45)
        plt.xlabel("Дата")
        plt.ylabel("Количество заказов")
        plt.show()

    def show_client_network(self):
        G = analysis.client_network(self.db.connection)
        plt.figure(figsize=(12, 12))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, labels=nx.get_node_attributes(G, 'label'))
        plt.title("Сеть клиентов")
        plt.show()

    def on_closing(self):
        self.db.close()  # Закрываем соединение с базой данных перед выходом
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = OrderManagementApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)  # Обрезка события закрытия
    root.mainloop()