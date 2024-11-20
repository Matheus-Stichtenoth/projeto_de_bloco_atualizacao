import requests
import pandas as pd

API_URL = "https://olinda.bcb.gov.br/olinda/servico/scr_sub_regiao/versao/v1/odata/scr_sub_regiao(DataBase=@DataBase)?@DataBase=202409&$format=json&$select=DATA_BASE,CLIENTE,ESTADO,SUB_REGIAO,MODALIDADE,CARTEIRA,VENCIDO_ACIMA_DE_15_DIAS"

def fetch_bcb_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data['value'])
        df.to_json('data/api_data.json', orient='records', indent=4)
        return df
    else:
        raise Exception(f"Erro ao acessar a API: {response.status_code}")

# Carregar backup local
def load_local_backup(filepath='data/api_data.json'):
    return pd.read_json(filepath)

def calculate_indebtedness(df):
    df['INADIMPLENCIA'] = df['VENCIDO_ACIMA_DE_15_DIAS'] / df['CARTEIRA']
    return df.sort_values('INADIMPLENCIA', ascending=False)