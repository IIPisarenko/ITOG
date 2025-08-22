import pandas as pd
import sqlite3
import networkx as nx
import matplotlib.pyplot as plt  # Импорт для построения графиков

def top_clients(connection):
    query = """
    SELECT c.name, COUNT(o.id) as order_count
    FROM clients c
    LEFT JOIN orders o ON c.id = o.client_id
    GROUP BY c.name
    ORDER BY order_count DESC
    LIMIT 5;
    """
    return pd.read_sql_query(query, connection)

def order_trends(connection):
    query = """
    SELECT DATE(o.order_date) as order_date, COUNT(o.id) as order_count
    FROM orders o
    GROUP BY order_date
    ORDER BY order_date;
    """
    return pd.read_sql_query(query, connection)

def client_network(connection):
    query = """
    SELECT c1.name as source, c2.name as target
    FROM orders o
    JOIN clients c1 ON o.client_id = c1.id
    JOIN orders o2 ON o.product_id = o2.product_id
    JOIN clients c2 ON o2.client_id = c2.id
    WHERE c1.id != c2.id;
    """
    df = pd.read_sql_query(query, connection)
    G = nx.from_pandas_edgelist(df, 'source', 'target')
    return G

# Пример использования и визуализации данных
if __name__ == "__main__":
    connection = sqlite3.connect('your_database.db')  #

    # Получаем данные о трендах заказов
    trends_df = order_trends(connection)

    # Печатаем DataFrame для проверки
    print(trends_df)

    # Визуализируем количество заказов по продуктам
    if 'product_id' in trends_df.columns and 'order_count' in trends_df.columns:
        plt.figure(figsize=(10, 6))
        plt.bar(trends_df['product_id'], trends_df['order_count'], color='blue')
        plt.xlabel('Product ID')
        plt.ylabel('Order Count')
        plt.title('Order Trends by Product')
        plt.xticks(rotation=45)
        plt.tight_layout()  # Для улучшения расположения
        plt.show()
    else:
        print("Error: Columns 'product_id' or 'order_count' not found in trends_df.")

    connection.close()