import psycopg2

# Substitua estas informações pelas suas configurações
db_config = {
    'dbname': 'main',
    'user': 'postgres',
    'password': '123',
    'host': 'localhost',
    'port': '5432'
}
#sudo -u postgres psql


# Comandos SQL para criar as tabelas
create_tables_sql = [
    """
    CREATE TABLE product_group (
      group_id INTEGER PRIMARY KEY,
      group_name VARCHAR
    )
    """,
    """
    CREATE TABLE customer (
      customer_id INTEGER PRIMARY KEY
    )
    """,
    """
    CREATE TABLE product (
      product_id INTEGER PRIMARY KEY,
      ASIN INTEGER UNIQUE,
      group_id INTEGER,
      salesrank INTEGER,
      title VARCHAR,
      similar_value INTEGER,
      FOREIGN KEY (group_id) REFERENCES product_group (group_id)
    )
    """,
    """
    CREATE TABLE product_categories (
      category_id INTEGER PRIMARY KEY,
      category_name VARCHAR,
      parent_category_id INTEGER,
      product_id INTEGER,
      FOREIGN KEY (parent_category_id) REFERENCES product_categories (category_id),
      FOREIGN KEY (product_id) REFERENCES product (product_id)
    )
    """,
    """
    CREATE TABLE product_reviews (
      review_id INTEGER PRIMARY KEY,
      created_at TIMESTAMP,
      votes INTEGER,
      rating INTEGER,
      helpful INTEGER,
      product_id INTEGER,
      customer_id INTEGER,
      FOREIGN KEY (product_id) REFERENCES product (product_id),
      FOREIGN KEY (customer_id) REFERENCES customer (customer_id)
    )
    """,
    """
    CREATE TABLE product_similar (
      similar_id INTEGER PRIMARY KEY,
      product_id INTEGER,
      similar_product_id INTEGER,
      FOREIGN KEY (product_id) REFERENCES product (product_id),
      FOREIGN KEY (similar_product_id) REFERENCES product (product_id)
    )
    """
]

def create_tables():
    # Conecta ao banco de dados PostgreSQL
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    try:
        # Executa os comandos SQL para criar as tabelas
        for command in create_tables_sql:
            cursor.execute(command)
        # Commit as alterações
        conn.commit()
        print("Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"Erro: {e}")
        # Desfaz as alterações em caso de erro
        conn.rollback()
    finally:
        # Fecha a conexão
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_tables()
