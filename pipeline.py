import requests
import pandas as pd
import mysql.connector

DB_CONFIG = {
    "database": "NomeDoBanco",
    "user": "NomeDoUsuario",
    "password": "Senha",
    "host": "localhost",
    "port": "3306"
}

def extract():
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Falha ao extrair os dados")

def transform(data):
    df = pd.DataFrame(data)
    df = df[["id", "name", "username", "email", "phone"]] 
    df.rename(columns={"id": "idUsuario", "name": "nome", "username": "usuario", "phone": "telefone"}, inplace=True)
    return df

def load(df):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                idUsuario INT PRIMARY KEY,
                nome TEXT,
                usuario TEXT,
                email TEXT,
                telefone TEXT
            )
        """)
        
        for _, row in df.iterrows():
            cur.execute(
                """
                INSERT IGNORE INTO usuarios (idUsuario, nome, usuario, email, telefone)
                VALUES (%s, %s, %s, %s, %s)
                """, tuple(row)
            )
        
        conn.commit()
        cur.close()
        conn.close()
        print("Dados carregados com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar os dados: {e}")

def pipeline():
    print("Iniciando Pipeline...")
    data = extract()
    df = transform(data)
    load(df)
    print("Pipeline concluído!")

if __name__ == "__main__":
    pipeline()
