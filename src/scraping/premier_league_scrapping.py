import os
import pandas as pd

from utils.utils import get_classification_table, get_table_df

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_experimental_option(
    "excludeSwitches", ["enable-logging"]
)  # Remove logs desnecessários
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

for year in range(2015, 2018):
    rank_table_df = pd.DataFrame(columns=[i for i in range(1, 39)])
    for matchweek in range(1, 39):
        while True:
            try:  # Se há algum erro, só tenta de novo
                url = f"https://www.transfermarkt.com/premier-league/formtabelle/wettbewerb/GB1?saison_id={year}&min=1&max={matchweek}"

                print("Chegou no loop", url)

                table = get_classification_table(driver, url)

                if not table:
                    print(f"Tabela não encontrada em {url}")
                    continue

                WebDriverWait(driver, 30).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, "td"))
                )

                df = get_table_df(table)

                if matchweek == 1:
                    clubs = df['Club']
                    for index, club in enumerate(clubs):
                        rank_table_df.at[index,'Club'] = club
                        rank_table_df.at[index,matchweek] = index + 1
                else:
                    for index, row in df.iterrows():
                        club = row['Club']

                        club_index = rank_table_df[rank_table_df['Club'] == club].index
                        club_index = club_index.item()
                        rank_table_df.at[club_index, matchweek] = row['#']

            except Exception:
                continue

            break

        rank_table_df.to_csv(os.path.join("data", "PremierLeague", f"{year}.csv"))

# Fechar o navegador
driver.quit()
