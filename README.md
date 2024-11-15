# Análise de Predição de Classificações Parciais em Ligas de Futebol

Este repositório contém uma análise inspirada no artigo *"[Hidden Dynamics of Soccer Leagues: The Predictive ‘Power’ of Partial Standings](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0225696)"*, que examina a capacidade das classificações parciais em ligas de futebol para prever as posições finais dos times ao final da temporada. 

## Objetivo

O objetivo inicial deste projeto é reproduzir os resultados do artigo citado, especificamente para a Premier League. Em seguida, aplicaremos a mesma metodologia para o Campeonato Brasileiro (Brasileirão) no período de 2006 (primeira edição com 20 clubes em sistema de pontos corridos) até 2023, a fim de avaliar a previsibilidade das classificações parciais em uma liga diferente.

## Metodologia

1. **Reprodução dos Resultados do Artigo**: Implementação da metodologia descrita no artigo, incluindo o cálculo das métricas de correlação de Spearman e distância de Kendall Tau para as posições dos times nas rodadas 10, 20 e 30, com a análise voltada para a Premier League.
   
2. **Aplicação ao Brasileirão**: Utilizando a mesma metodologia, as classificações parciais das rodadas 10, 20 e 30 de cada temporada do Brasileirão, entre 2006 e 2023, serão comparadas com as classificações finais de cada ano, a fim de verificar padrões de estabilidade e previsibilidade semelhantes.

3. **Ferramentas Estatísticas**: As métricas de correlação de Spearman e distância de Kendall Tau são aplicadas para avaliar a similaridade entre as classificações parciais e finais ao longo da temporada, indicando em qual ponto as posições dos times tornam-se mais estáveis e previsíveis.

## Estrutura do Projeto

- **`data/`**: CSVs com as tabelas dos campeonatos e txts com os links para o scraping. Os csvs não estarão dentro do repositório, porém devem ser gerados localmente com os scripts de scraping
  - **`PremierLeague/`**: Tabelas de 1995-1996 até 2016-2017.
  - **`Brasileirao/`**: Tabelas de 2006 até 2023.
- **`notebooks/`**: Notebooks Jupyter que documentam a reprodução dos resultados do artigo e a análise aplicada ao Brasileirão.
- **`src/`**: Contém os scripts Python para coleta de dados e cálculos estatísticos:
  - **`scraping/`**: Scripts para web scraping das tabelas de classificação.
  - **`calculations/`**: Scripts para o cálculo de correlações e análise de estabilidade nas classificações parciais.
- **`README.md`**: Documento explicativo do repositório (você está aqui).
- **`requirements.txt`**: Dependências utilizadas no projeto 

## Pré-requisitos

Para executar as análises, certifique-se de ter instalado:
- Python 3.12+
- Bibliotecas Python:
  - `pandas`
  - `numpy`
  - `scipy`
  - `matplotlib`

Instale as dependências com:
```bash
pip install -r requirements.txt
