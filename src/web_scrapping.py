import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL do site
url = "https://www.serasa.com.br/limpa-nome-online/blog/mapa-da-inadimplencia-e-renogociacao-de-dividas-no-brasil/"

meses = [
    'Maio/2021',
    'Junho/2021',
    'Julho/2021',
    'Agosto/2021',
    'Setembro/2021',
    'Outubro/2021',
    'Novembro/2021',
    'Dezembro/2021',
    'Janeiro/2022',
    'Fevereiro/2022',
    'Março/2022',
    'Abril/2022',
    'Maio/2022',
    'Junho/2022',
    'Julho/2022',
    'Agosto/2022',
    'Setembro/2022',
    'Outubro/2022',
    'Novembro/2022',
    'Dezembro/2022',
    'Janeiro/2023',
    'Fevereiro/2023',
    'Março/2023',
    'Abril/2023',
    'Maio/2023',
    'Junho/2023',
    'Julho/2023',
    'Agosto/2023',
    'Setembro/2023',
    'Outubro/2023',
    'Novembro/2023',
    'Dezembro/2023',
    'Janeiro/2024',
    'Fevereiro/2024',
    'Março/2024',
    'Abril/2024',
    'Maio/2024',
    'Junho/2024',
    'Julho/2024',
    'Agosto/2024',
    'Setembro/2024'
]

# Requisição ao site
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

df_final = pd.DataFrame(columns=["Mês", "conteudo"])

for mes in meses:
    section = soup.find("h2", string=mes)
    if section:
        ul = section.find_next("ul")
        if ul:
            items = [li.text for li in ul.find_all("li")]

            data = {"Mês": [mes] * len(items), "conteudo": items}
            df = pd.DataFrame(data)

            df_final = pd.concat([df_final, df], ignore_index=True)

df_final.to_csv('data/informacoes_inadimplencia.csv', index = False)