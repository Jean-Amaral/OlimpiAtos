from fasthtml.common import *
import requests
from collections import defaultdict

# Função para consumir a API dos resultados das Olimpíadas
def get_olympic_results(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        try:
            data = response.json()
            if 'data' in data and isinstance(data['data'], list):
                return data['data']
            else:
                raise Exception("Os dados retornados não estão no formato esperado (lista)")
        except ValueError:
            raise Exception("Erro ao converter a resposta para JSON")
    else:
        raise Exception("Erro ao acessar a API")

# Função para ordenar o quadro de medalhas
def sort_medal_table(results):
    if isinstance(results, list):
        return sorted(results, key=lambda x: (x.get('gold_medals', 0), x.get('silver_medals', 0), x.get('bronze_medals', 0)), reverse=True)
    else:
        raise Exception("Os resultados não estão no formato esperado (lista)")

# Função para agrupar os resultados por continente
def group_by_continent(results, country_to_continent):
    continent_results = defaultdict(lambda: {'gold': 0, 'silver': 0, 'bronze': 0})
    for country in results:
        if isinstance(country, dict):
            continent = country.get('continent', 'Unknown')
            continent_results[continent]['gold'] += country.get('gold_medals', 0)
            continent_results[continent]['silver'] += country.get('silver_medals', 0)
            continent_results[continent]['bronze'] += country.get('bronze_medals', 0)
        else:
            raise Exception("Formato de país inesperado nos resultados")
    return continent_results

# Função para ranquear os continentes de acordo com o desempenho
def rank_continents(continent_results):
    return sorted(continent_results.items(), key=lambda x: (x[1]['gold'], x[1]['silver'], x[1]['bronze']), reverse=True)

# URL da API
api_url = "https://apis.codante.io/olympic-games/countries"

# Dicionário de mapeamento de países para continentes (completo)
country_to_continent = {
    'KOR': 'Ásia',
    'JPN': 'Ásia',
    'USA': 'América do Norte',
    'CHN': 'Ásia',
    'BRA': 'América do Sul',
    'ARG': 'América do Sul',
    'FRA': 'Europa',
    'GER': 'Europa',
    'AUS': 'Oceania',
    'CAN': 'América do Norte',
    'RUS': 'Europa',
    'GBR': 'Europa',
    'ITA': 'Europa',
    'ESP': 'Europa',
    'MEX': 'América do Norte',
    'IND': 'Ásia',
    'RSA': 'África',
    'EGY': 'África',
    'NGR': 'África',
    'KEN': 'África',
    'SWE': 'Europa',
    'NOR': 'Europa',
    'DEN': 'Europa',
    'FIN': 'Europa',
    'NED': 'Europa',
    'BEL': 'Europa',
    'SUI': 'Europa',
    'AUT': 'Europa',
    'POL': 'Europa',
    'CZE': 'Europa',
    'HUN': 'Europa',
    'POR': 'Europa',
    'GRE': 'Europa',
    'TUR': 'Ásia',
    'IRN': 'Ásia',
    'IRQ': 'Ásia',
    'SAU': 'Ásia',
    'ISR': 'Ásia',
    'EGY': 'África',
    'MAR': 'África',
    'ALG': 'África',
    'TUN': 'África',
    'NGA': 'África',
    'GHA': 'África',
    'CIV': 'África',
    'CMR': 'África',
    'SEN': 'África',
    'ZAF': 'África',
    'NZL': 'Oceania',
    'FIJ': 'Oceania',
    'PNG': 'Oceania',
    'SAM': 'Oceania',
    'TGA': 'Oceania',
    # ... adicione outros países conforme necessário
}

# Configuração do aplicativo FastHTML
app, rt = fast_app()

@rt("/")
def get():
    try:
        results = get_olympic_results(api_url)
        sorted_results = sort_medal_table(results)
        continent_results = group_by_continent(sorted_results, country_to_continent)
        ranked_continents = rank_continents(continent_results)

        # Criar uma lista de elementos HTML para exibir o ranking dos continentes
        continent_list = [
            Li(f"{rank}. {continent} - Ouro: {medals['gold']}, Prata: {medals['silver']}, Bronze: {medals['bronze']}")
            for rank, (continent, medals) in enumerate(ranked_continents, start=1)
        ]
        return Titled("Ranking dos Continentes", Ul(*continent_list))
    except Exception as e:
        return Titled("Erro", P(str(e)))

# Iniciar o servidor
serve()