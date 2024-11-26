import mysql.connector
import csv
import os

# Configuração do banco de dados
config = {
    "user": "root",
    "password": "admin",
    "host": "localhost",
    "database": "boletins_de_urna",
    "use_pure": True,
    "ssl_disabled": True,
}


def chunk_data(data, chunk_size=15000):
    """Divide os dados em blocos menores"""
    for i in range(0, len(data), chunk_size):
        yield data[i : i + chunk_size]


def connect_to_db():
    try:
        connection = mysql.connector.connect(**config)
        print("Connection established.")
        return connection
    except mysql.connector.Error as error:
        print(f"Connection error: {error}")
        return None


def initialize_db():
    try:
        connection = mysql.connector.connect(
            user=config["user"],
            password=config["password"],
            host=config["host"],
        )
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config['database']};")
        print(f"Database '{config['database']}', OK!")
    except mysql.connector.Error as error:
        print(f"Error while initializing DB: {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def extract_state_from_filename(filename):
    """Extrai o estado do nome do arquivo CSV"""
    try:
        parts = filename.split("_")
        state = parts[2]  # Posição do estado no nome do arquivo
        return state
    except IndexError:
        print(f"Erro ao extrair estado do arquivo: {filename}")
        return None


def sanitize_column_names(columns):
    """Limpa e ajusta os nomes das colunas para o padrão do MySQL"""
    sanitized_columns = []
    for col in columns:
        col = (
            col.strip().replace('"', "").replace(";", "")
        )  # Remove aspas e ponto-e-vírgula
        col = col[:50]  # Trunca o nome da coluna para no máximo 50 caracteres
        sanitized_columns.append(col)
    return sanitized_columns


def create_control_table(connection):
    """Cria uma tabela para rastrear arquivos processados"""
    cursor = connection.cursor()
    sql_create = """
    CREATE TABLE IF NOT EXISTS import_control (
        filename VARCHAR(255) PRIMARY KEY,
        import_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    try:
        cursor.execute(sql_create)
        connection.commit()
        print("Tabela de controle criada/verificada.")
    except mysql.connector.Error as error:
        print(f"Erro ao criar tabela de controle: {error}")
    finally:
        cursor.close()


def create_table(connection, table_name, columns):
    cursor = connection.cursor()

    # Sanitiza os nomes das colunas
    columns = sanitize_column_names(columns)
    columns_def = ", ".join([f"{col} VARCHAR(255)" for col in columns])

    # Definir a chave primária
    primary_key = "NR_ZONA, NR_SECAO, CD_MUNICIPIO"  # Ajuste conforme necessário, usando colunas que existem
    sql_create = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        {columns_def},
        PRIMARY KEY ({primary_key})  -- Define chave primária com colunas existentes
    );
    """
    try:
        cursor.execute(sql_create)
        connection.commit()
        print(f"Tabela '{table_name}' criada ou já existe.")
    except mysql.connector.Error as error:
        print(f"Erro ao criar a tabela: {error}")
    finally:
        cursor.close()


def insert_data(connection, table_name, data_path):
    # Defina as colunas desejadas
    desired_columns = [
        "CD_PLEITO",
        "NR_TURNO",
        "DS_ELEICAO",
        "SG_UF",
        "CD_MUNICIPIO",
        "NM_MUNICIPIO",
        "NR_ZONA",
        "NR_SECAO",
        "CD_CARGO_PERGUNTA",
        "DS_CARGO_PERGUNTA",
        "NR_PARTIDO",
        "SG_PARTIDO",
        "NM_PARTIDO",
        "DT_BU_RECEBIDO",
        "QT_APTOS",
        "QT_COMPARECIMENTO",
        "QT_ABSTENCOES",
        "NR_VOTAVEL",
        "NM_VOTAVEL",
        "QT_VOTOS",
        "QT_ELEI_BIOM_SEM_HABILITACAO",
    ]

    with open(data_path, "r", encoding="latin-1") as data_file:
        reader = csv.reader(data_file, delimiter=";")
        columns = next(reader)

        # Filtra as colunas, mantendo apenas as desejadas
        filtered_columns = [col for col in columns if col in desired_columns]

        # Criação da tabela com as colunas filtradas
        create_table(connection, table_name, filtered_columns)

        data = []  # Lista para armazenar os dados a serem inseridos
        total_lines = 0  # Contador de linhas lidas

        cursor = connection.cursor()
        placeholders = ", ".join(["%s"] * len(filtered_columns))
        sql_insert = f"INSERT IGNORE INTO {table_name} ({', '.join(filtered_columns)}) VALUES ({placeholders})"

        try:
            for row in reader:
                # Filtra os dados da linha, mantendo apenas as colunas desejadas
                filtered_row = [row[columns.index(col)] for col in filtered_columns]
                data.append(filtered_row)
                total_lines += 1

                # A cada 1000 linhas, imprime o progresso
                if total_lines % 1000 == 0:
                    print(f"{total_lines} linhas processadas...")

                # Quando atingir o tamanho do chunk, insira os dados
                if len(data) >= 15000:
                    cursor.executemany(sql_insert, data)
                    connection.commit()
                    print(f"Chunk de {len(data)} registros enviado.")
                    data.clear()  # Limpa a lista de dados para o próximo bloco

            # Caso ainda haja dados restantes que não completaram um chunk
            if data:
                cursor.executemany(sql_insert, data)
                connection.commit()
                print(f"Último chunk de {len(data)} registros enviado.")
        except mysql.connector.Error as error:
            print(f"Error while inserting data: {error}")
        finally:
            cursor.close()


def import_csvs_to_db(dir_foldercsv, connection):

    # Chama a criação da tabela de controle antes de processar qualquer arquivo
    create_control_table(connection)

    for csv in os.listdir(dir_foldercsv):
        if csv.endswith(".csv"):
            state = extract_state_from_filename(csv)
            if state:
                data_path = os.path.join(dir_foldercsv, csv)

                # Verifica se o arquivo já foi processado
                cursor = connection.cursor(dictionary=True)
                cursor.execute(
                    "SELECT filename FROM import_control WHERE filename = %s", (csv,)
                )
                result = cursor.fetchone()
                if result:
                    print(f"Arquivo '{csv}' já foi processado. Pulando...")
                    continue

                # Registra o arquivo como processado
                cursor.execute(
                    "INSERT INTO import_control (filename) VALUES (%s)", (csv,)
                )
                connection.commit()

                table_name = state
                print(f"\nImporting csv: {data_path}")
                insert_data(connection, table_name, data_path)


# Executando o script
if __name__ == "__main__":
    dir_folderscsv = "boletins_de_urna"
    initialize_db()
    connection = connect_to_db()
    if connection:
        import_csvs_to_db(dir_folderscsv, connection)
        connection.close()
