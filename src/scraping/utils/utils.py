import pandas as pd
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement


def get_classification_table(driver: WebDriver, url: str, verbose: bool = False):
    driver.get(url)

    time.sleep(10)

    if verbose:
        print("Esperando a tabela ser carregada")

    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "responsive-table"))
    )

    responsive_div = driver.find_element(By.CLASS_NAME, "responsive-table")

    table = responsive_div.find_element(By.TAG_NAME, "table")

    if verbose:
        print(f"Tabela: {table}")

    return table

def get_table_df(table: WebElement, verbose: bool = False):
    # Listas para armazenar os dados
    headers = []
    rows = []
    indexes = []

    thead = table.find_element(By.TAG_NAME, "thead")
    headers = [th.text.strip() for th in thead.find_elements(By.TAG_NAME, "th")]
    headers.append("url")

    tbody = table.find_element(By.TAG_NAME, "tbody")

    for row in tbody.find_elements(By.TAG_NAME, "tr"):
        columns = row.find_elements(By.TAG_NAME, "td")
        if columns:
            # Posição na tabela
            index = (
                row.find_elements(By.TAG_NAME, "td")[0].text.strip()
                if row.find_elements(By.TAG_NAME, "td")
                else "-"
            )

            if verbose:
                print(index)
            
            indexes.append(index)

            # Resto das linhas
            row_data = [col.text.strip() for col in columns]

            if verbose:
                print(row_data)
            
            rows.append(row_data)

    df = pd.DataFrame(rows, columns=headers, index=indexes)
    df.index.name = headers[0]

    # Remover colunas duplicadas
    df = df.loc[:, ~df.columns.duplicated(keep="first")]

    df["Club"] = df[""]
    df["SG"] = df["Pts"]
    df["Pts"] = df["url"]
    df.drop(columns=["", "url"], inplace=True)

    return df