import psycopg2
import sys

# Configurações do banco de dados
db_config = {
    'dbname': 'main',
    'user': 'postgres',
    'password': '123',
    'host': 'localhost',
    'port': '5432'
}

# Função para executar uma consulta SQL e escrever os resultados em um arquivo
def execute_query(query, filename):
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    with open(filename, 'a') as file:
        for row in results:
            file.write(str(row) + '\n')
    cursor.close()
    conn.close()

# Função para mostrar o menu e capturar a escolha do usuário
def show_menu():
    print("\nDashboard de Consultas SQL")
    print("1. Comentários mais úteis e com maior avaliação")
    print("2. Comentários mais úteis e com menor avaliação")
    print("3. Produtos similares com maiores vendas")
    print("4. Evolução diária das médias de avaliação")
    print("5. 10 produtos líderes de venda em cada grupo")
    print("6. 10 produtos com a maior média de avaliações úteis positivas")
    print("7. 5 categorias com a maior média de avaliações úteis positivas")
    print("8. 10 clientes que mais fizeram comentários por grupo")
    print("9. Sair")
    return input("Escolha uma opção: ")

def main():
    filename = "query_results.txt"  # Arquivo onde os resultados serão salvos

    while True:
        choice = show_menu()

        if choice == '1':
            product_id = input("Digite o ID do produto: ")
            query = f"""
                SELECT * FROM product_reviews pr
                INNER JOIN product p ON pr.product_id = p.product_id
                WHERE p.product_id = {product_id}  
                ORDER BY rating DESC, helpful DESC 
                LIMIT 5;
            """
            execute_query(query, filename)

        elif choice == '2':
            product_id = input("Digite o ID do produto: ")
            query = f"""
                SELECT * FROM product_reviews pr
                INNER JOIN product p ON pr.product_id = p.product_id
                WHERE p.product_id = {product_id} 
                ORDER BY rating ASC, helpful DESC 
                LIMIT 5;
            """
            execute_query(query, filename)

        elif choice == '3':
            product_asin = input("Digite o ASIN do produto: ")
            query = f"""
                SELECT ps.similar_id, ps.product_asin, ps.similar_product_asin, p1.salesrank, p2.salesrank
                FROM product_similar ps
                JOIN product p1 ON ps.product_asin = p1.asin
                JOIN product p2 ON ps.similar_product_asin = p2.asin
                WHERE p2.salesrank > p1.salesrank
                ORDER BY p2.salesrank DESC;
            """
            execute_query(query, filename)

        elif choice == '4':
            product_id = input("Digite o ID do produto: ")
            query = f"""
                SELECT rating, created_at FROM product_reviews
                WHERE product_id = {product_id}
                AND created_at >= '2003-11-29'
                AND created_at <= '2005-02-21';
            """
            execute_query(query, filename)

        elif choice == '5':
            query = """
                WITH ranked_products AS (
                    SELECT *, ROW_NUMBER() OVER (PARTITION BY group_id ORDER BY salesrank DESC) AS rank_in_group
                    FROM product)
                SELECT * FROM ranked_products WHERE rank_in_group <= 10 AND salesrank IS NOT NULL;
            """
            execute_query(query, filename)

        elif choice == '6':
            query = """
                WITH helpful_products AS (
                    SELECT product_id, AVG(helpful) AS avg_helpful, ROW_NUMBER() OVER (ORDER BY AVG(helpful) DESC) AS rank_helpful
                    FROM product_reviews WHERE helpful > 0 GROUP BY product_id)
                SELECT * FROM helpful_products WHERE rank_helpful <= 10;
            """
            execute_query(query, filename)

        elif choice == '7':
            query = """
                WITH helpful_categories AS (
                    SELECT p.group_id, AVG(pr.helpful) AS avg_helpful, ROW_NUMBER() OVER (ORDER BY AVG(pr.helpful) DESC) AS rank_helpful
                    FROM product_reviews pr JOIN product p ON pr.product_id = p.product_id WHERE pr.helpful > 0 GROUP BY p.group_id)
                SELECT * FROM helpful_categories WHERE rank_helpful <= 5;
            """
            execute_query(query, filename)

        elif choice == '8':
            query = """
                WITH top_reviewers_per_group AS (
                    SELECT p.group_id, pr.customer_id, COUNT(*) AS review_count, ROW_NUMBER() OVER (PARTITION BY p.group_id ORDER BY COUNT(*) DESC) AS rank_reviewer
                    FROM product_reviews pr JOIN product p ON pr.product_id = p.product_id GROUP BY p.group_id, pr.customer_id)
                SELECT group_id, customer_id, review_count FROM top_reviewers_per_group WHERE rank_reviewer <= 10;
            """
            execute_query(query, filename)

        elif choice == '9':
            print("Saindo...")
            sys.exit()
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
