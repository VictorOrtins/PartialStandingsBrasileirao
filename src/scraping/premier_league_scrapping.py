import os
import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Remove logs desnecessários
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

for year in range(1995, 2018):
    for matchweek in [10, 20, 30, 38]:
        try: #Se há algum erro, só ignora
            url = f'https://www.transfermarkt.com/premier-league/formtabelle/wettbewerb/GB1?saison_id={year}&min=1&max={matchweek}'

            print('Chegou no loop', url)
            
            driver.get(url)

            time.sleep(10)
            
            print('Esperando a tabela ser carregada')

            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "responsive-table"))
            )
            
            responsive_div = driver.find_element(By.CLASS_NAME, "responsive-table")

            table = responsive_div.find_element(By.TAG_NAME, "table")

            if not table:
                print(f"Tabela não encontrada em {url}")
                continue

            WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "td"))
            )


            # Listas para armazenar os dados
            headers = []
            rows = []
            indexes = []

            print("Encontrando cabeçalhos da tabela")
            thead = table.find_element(By.TAG_NAME, 'thead')
            headers = [th.text.strip() for th in thead.find_elements(By.TAG_NAME, 'th')]    
            headers.append('url')

            tbody = table.find_element(By.TAG_NAME, 'tbody')

            for row in tbody.find_elements(By.TAG_NAME, 'tr'):
                columns = row.find_elements(By.TAG_NAME, 'td')
                if columns:
                    # Posição na tabela
                    index = row.find_elements(By.TAG_NAME, 'td')[0].text.strip() if row.find_elements(By.TAG_NAME, 'td') else '-'
                    print(index)
                    indexes.append(index)

                    # Resto das linhas
                    row_data = [col.text.strip() for col in columns]
                    print(row_data)
                    rows.append(row_data)

            df = pd.DataFrame(rows, columns=headers, index=indexes)
            df.index.name = headers[0]

            # Remover colunas duplicadas
            df = df.loc[:, ~df.columns.duplicated(keep='first')]

            df['Club'] = df['']
            df['SG'] = df['Pts']
            df['Pts'] = df['url']
            df.drop(columns=['', 'url'], inplace=True)
            
            df.to_csv(os.path.join('data', 'PremierLeague', f'{year}_{matchweek}.csv'))
        except Exception:
            continue

# Fechar o navegador
driver.quit()
