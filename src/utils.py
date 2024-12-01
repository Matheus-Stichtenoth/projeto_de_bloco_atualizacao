import requests
import pandas as pd

# URL base da API
API_URL_TEMPLATE = (
    "https://olinda.bcb.gov.br/olinda/servico/scr_sub_regiao/versao/v1/odata/"
    "scr_sub_regiao(DataBase=@DataBase)?@DataBase={}&$format=json&"
    "$select=DATA_BASE,CLIENTE,ESTADO,SUB_REGIAO,MODALIDADE,CARTEIRA,VENCIDO_ACIMA_DE_15_DIAS"
)

def fetch_bcb_data(start_date=202309, end_date=202409):
    """
    Busca os dados da API do Banco Central para múltiplas datas de referência.

    :param start_date: Data inicial no formato AAAAMM.
    :param end_date: Data final no formato AAAAMM.
    :return: DataFrame contendo os dados de todas as datas especificadas.
    """
    all_data = []
    
    # Gera as datas no formato AAAAMM para iteração
    dates = pd.date_range(
        start=f"{str(start_date)[:4]}-{str(start_date)[4:]}",
        end=f"{str(end_date)[:4]}-{str(end_date)[4:]}",
        freq='MS'
    ).strftime('%Y%m').tolist()

    for date in dates:
        url = API_URL_TEMPLATE.format(date)
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'value' in data:
                all_data.extend(data['value'])  # Adiciona os registros para a lista
        else:
            print(f"Erro ao acessar a API para a data {date}: {response.status_code}")

    # Converte a lista de registros para DataFrame
    if all_data:
        df = pd.DataFrame(all_data)
        df.to_json('.data/api_data.json', orient='records', indent=4)  # Salva os dados como backup local
        return df
    else:
        raise Exception("Não foi possível obter dados da API para o intervalo especificado.")

# Carregar backup local
def load_local_backup(filepath='data/api_data.json'):
    return pd.read_json(filepath)

def calculate_indebtedness(df):
    """
    Calcula a taxa de inadimplência e ordena o DataFrame por ordem decrescente de inadimplência.

    :param df: DataFrame original.
    :return: DataFrame com a coluna "INADIMPLENCIA".
    """
    df['INADIMPLENCIA'] = df['VENCIDO_ACIMA_DE_15_DIAS'] / df['CARTEIRA']
    return df.sort_values('INADIMPLENCIA', ascending=False)