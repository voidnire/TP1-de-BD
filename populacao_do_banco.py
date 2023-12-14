with open("teste.txt","r") as file:
    arquivo = file.readlines()
for line in arquivo:
    insert = 0
    if line.startswith("Id"):
        id = line[4:].strip()
        print("id: ",id)
    if line.startswith("ASIN"):
        asin = line[6:].strip()
        print("asin: ",asin)
    if line.startswith("  title"):
        title = line[8:].strip()
        print("title: ",title)
    if line.startswith("  group"):
        group = line[8:].strip()
        print("group: ",group)
    if line.startswith("  salesrank"):
        salesrank = line[11:].strip()
        print("salesrank: ",salesrank)
    if line.startswith("  similar"):
        similar = line[12:].strip()
        similars = similar.split()
        print("similars: ",similars)
    if line.startswith("   |"):#categories
        categories = line[3:].strip()

        category_parts = categories.split("|")
        category_parts = category_parts[1:]
        category_ids = []
        category_names = []
        
        for part in category_parts:
            category_id = part.split("[")[1][:-1]
            category_name = part.split("[")[0]
            category_ids.append(category_id)
            category_names.append(category_name)
        
        print("category_ids: ", category_ids)
        print("category_names: ", category_names)
    if line.startswith("  reviews"):
        if line[18] == "0":
            insert = 1
            review_flag = 0
    if "cutomer" in line:
        review = line.split()
        review_flag = 1
        date = review[0]
        customer_id = review[2]
        rating = review[4]
        votes = review[6]
        helpful = review[8]
        print(date,customer_id,rating,votes,helpful)
        review_flag = 1
        print("")
    if line == " ":
        insert = 1
        
    if insert == 1:
        #inserir dados na tabela
        
        
    #limpar dados e zerar o insert
        insert = 0
