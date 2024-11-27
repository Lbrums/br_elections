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

# Valores padrão para colunas ausentes
DEFAULT_VALUE = "NULL"  # Valor padrão para colunas ausentes


def connect_to_db():
    """Conecta ao banco de dados."""
    try:
        connection = mysql.connector.connect(**config)
        print("Conexão com o banco de dados estabelecida.")
        return connection
    except mysql.connector.Error as error:
        print(f"Erro ao conectar ao banco de dados: {error}")
        return None


def initialize_db():
    """Inicializa o banco de dados."""
    try:
        connection = mysql.connector.connect(
            user=config["user"],
            password=config["password"],
            host=config["host"],
        )
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config['database']};")
        print(f"Banco de dados '{config['database']}' criado/verificado com sucesso.")
    except mysql.connector.Error as error:
        print(f"Erro ao inicializar o banco de dados: {error}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def create_table(connection, table_name, columns):
    cursor = connection.cursor()
    columns_def = ", ".join([f"`{col}` VARCHAR(255)" for col in columns])

    sql_create = f"""
    CREATE TABLE IF NOT EXISTS `{table_name}` (
        id INT AUTO_INCREMENT PRIMARY KEY,
        {columns_def}
    );
    """
    try:
        cursor.execute(sql_create)
        connection.commit()
        print(f"Tabela '{table_name}' criada ou já existe.")
    except mysql.connector.Error as error:
        print(f"Erro ao criar a tabela '{table_name}': {error}")
    finally:
        cursor.close()


def extract_state_from_filename(filename):
    """Extrai o estado do nome do arquivo."""
    try:
        parts = filename.split("_")
        state = parts[
            2
        ]  # Supondo que a posição do estado seja a terceira parte do nome
        return state.upper()  # Retorna o estado em maiúsculas
    except IndexError:
        print(f"Erro ao extrair estado do arquivo: {filename}")
        return None


def process_and_insert_data(connection, table_name, data_path):
    """Processa o arquivo CSV e insere os dados no banco."""
    # Colunas desejadas
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

    total_lines = 0
    inserted_lines = 0

    try:
        with open(data_path, "r", encoding="latin-1") as data_file:
            reader = csv.reader(data_file, delimiter=";")
            file_columns = next(reader)  # Cabeçalho do arquivo CSV

            # Certifica-se de que a tabela contém todas as colunas desejadas
            create_table(connection, table_name, desired_columns)

            cursor = connection.cursor()
            placeholders = ", ".join(["%s"] * len(desired_columns))
            sql_insert = f"""
INSERT IGNORE INTO `{table_name}` ({', '.join(desired_columns)}) 
VALUES ({placeholders})
"""

            batch = []  # Lote de dados a serem enviados

            for row in reader:
                total_lines += 1

                # Cria uma linha completa com valores ausentes substituídos por DEFAULT_VALUE
                completed_row = [
                    (
                        row[file_columns.index(col)].strip()
                        if col in file_columns
                        else DEFAULT_VALUE
                    )
                    for col in desired_columns
                ]

                batch.append(completed_row)

                # Insere em lotes de 15.000 registros
                if len(batch) >= 15000:
                    cursor.executemany(sql_insert, batch)
                    connection.commit()
                    inserted_lines += len(batch)
                    print(f"{inserted_lines} linhas inseridas até agora.")
                    batch.clear()

            # Insere os dados restantes
            if batch:
                cursor.executemany(sql_insert, batch)
                connection.commit()
                inserted_lines += len(batch)

    except Exception as error:
        print(f"Erro ao processar o arquivo {data_path}: {error}")
    finally:
        print(f"Total de linhas processadas no arquivo {data_path}: {total_lines}")
        print(f"Total de linhas inseridas no banco: {inserted_lines}")


def import_csvs_to_db(directory, connection):
    """Importa todos os arquivos CSV no diretório especificado."""
    for csv_file in os.listdir(directory):
        if csv_file.endswith(".csv"):
            state = extract_state_from_filename(csv_file)
            if state:
                table_name = state
                data_path = os.path.join(directory, csv_file)
                print(f"Processando arquivo: {csv_file} na tabela: {table_name}")
                process_and_insert_data(connection, table_name, data_path)


if __name__ == "__main__":
    dir_foldercsv = "boletins_de_urna"
    initialize_db()
    connection = connect_to_db()
    if connection:
        import_csvs_to_db(dir_foldercsv, connection)
        connection.close()
