import os
import time

import pandas as pd


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from typing import List


class LeagueScrapper:
    def __init__(self, url_template: str, save_folder: str):
        """
        A class for scraping and processing football league standings tables from Transfermarkt

        The class uses Selenium to navigate the website, extract HTML tables, and save the processed data as CSV files.

        Attributes:
            url (str): A URL template containing placeholders for `year` and `matchweek`.
            save_folder (str): The folder path where output CSV files will be saved.
        """
        self.url = url_template
        self.save_folder = save_folder

    def scrape_tables(
        self,
        init_year: int,
        end_year: int,
        init_matchweek: int,
        end_matchweek: int,
        verbose: bool = False,
    ):
        """
        Executes the scraping and saving process for league standings tables.

        Args:
            init_year (int): Starting year for scraping.
            end_year (int): Ending year for scraping.
            init_matchweek (int): Initial matchweek number.
            end_matchweek (int): Final matchweek number.
            verbose (bool): Whether to print debug messages (optional).
        """
        driver = self.__set_driver()

        self.__create_necessary_folders(init_year, end_year)

        rank_table_save_folder = os.path.join(self.save_folder, "rank_tables")

        for year in range(init_year, end_year + 1):
            rank_table_df = pd.DataFrame(
                columns=[i for i in range(init_matchweek, end_matchweek + 1)]
            )
            for matchweek in range(init_matchweek, end_matchweek + 1):
                matchweek_standings_save_folder = os.path.join(
                    self.save_folder, "matchweek_standings", f"{year}"
                )

                while True:
                    try:
                        url = self.url.format(year=year, matchweek=matchweek)

                        if verbose:
                            print("Chegou no loop", url)

                        table = self.__get_classification_table(driver, url)

                        if not table:
                            print(f"Tabela não encontrada em {url}")
                            continue

                        WebDriverWait(driver, 30).until(
                            EC.presence_of_all_elements_located((By.TAG_NAME, "td"))
                        )

                        table_df = self.__get_table_df(table)

                        table_df.to_csv(
                            os.path.join(
                                matchweek_standings_save_folder, f"{matchweek}.csv"
                            )
                        )

                        rank_table_df = self.__update_rank_table(
                            matchweek, rank_table_df, table_df
                        )
                    except Exception:
                        continue

                    break

            rank_table_df.to_csv(os.path.join(rank_table_save_folder, f"{year}.csv"))

        driver.quit()

    def __set_driver(self):
        """
        Sets up and returns an instance of the Chrome WebDriver.

        Returns:
            WebDriver: An instance of Selenium's WebDriver configured for Chrome.
        """
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )

        return driver

    def __create_necessary_folders(self, init_year: int, end_year: int):
        """
        Creates the necessary folders for saving the results.

        Args:
            init_year (int): Starting year of the range.
            end_year (int): Ending year of the range.
        """
        self.__create_folder(self.save_folder)

        self.__create_folder(os.path.join(self.save_folder, "rank_tables"))

        self.__create_folder(os.path.join(self.save_folder, "matchweek_standings"))

        for year in range(init_year, end_year + 1):
            self.__create_folder(
                os.path.join(self.save_folder, "matchweek_standings", f"{year}")
            )

    def __create_folder(self, folder_path: str):
        """
        Creates a folder at the specified path if it does not already exist.

        Args:
            folder_path (str): Path of the folder to create.
        """
        try:
            os.mkdir(folder_path)
        except Exception:
            pass

    def __get_classification_table(
        self, driver: WebDriver, url: str, verbose: bool = False
    ):
        """
        Accesses a specific webpage and extracts the standings table.

        Args:
            driver (WebDriver): Instance of Selenium's WebDriver.
            url (str): The webpage URL to extract the table from.
            verbose (bool): Whether to print debug messages (optional).

        Returns:
            WebElement: The HTML table element extracted from the webpage.
        """
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

    def __get_table_df(self, table: WebElement, verbose: bool = False) -> pd.DataFrame:
        """
        Processes an HTML table element and converts it into a pandas DataFrame.

        Args:
            table (WebElement): The HTML table element to process.
            verbose (bool): Whether to print debug messages (optional).

        Returns:
            pd.DataFrame: A DataFrame containing the table's data.
        """
        # Listas para armazenar os dados
        headers = []
        rows = []
        indexes = []

        thead = table.find_element(By.TAG_NAME, "thead")
        headers = [th.text.strip() for th in thead.find_elements(By.TAG_NAME, "th")]
        headers.append("url")

        tbody = table.find_element(By.TAG_NAME, "tbody")

        rows, indexes = self.__find_table_data(tbody, indexes, rows, verbose)

        table_df = self.__format_standings_data(rows, headers, indexes)

        return table_df

    def __find_table_data(
        self,
        tbody: WebElement,
        indexes: List[str],
        rows: List[str],
        verbose: bool = False,
    ):
        """
        Extracts data from a table body (`<tbody>`) element and populates the provided lists with row indexes and data.

        Args:
            tbody (WebElement): The `<tbody>` element of an HTML table to extract data from.
            indexes (List[str]): A list to store row indexes (e.g., ranking positions).
            rows (List[str]): A list to store row data as lists of cell values.
            verbose (bool): Whether to print debug messages (default is False).

        Returns:
            Tuple[List[str], List[str]]: Updated `rows` and `indexes` lists populated with extracted data.
        """
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

        return rows, indexes

    def __format_standings_data(
        self, rows: List[str], headers: List[str], indexes: List[str]
    ):
        """
        Formats extracted table data into a pandas DataFrame with appropriate column names and transformations.

        Args:
            rows (List[str]): List of row data extracted from the table.
            headers (List[str]): List of table headers to be used as column names.
            indexes (List[str]): List of row indexes to be used as DataFrame indexes.

        Returns:
            pd.DataFrame: A formatted pandas DataFrame representing the standings table.
        """
        df = pd.DataFrame(rows, columns=headers, index=indexes)
        df.index.name = headers[0]

        df = df.loc[:, ~df.columns.duplicated(keep="first")]

        df["Club"] = df[""]

        if "Form" in df.columns:
            df["Pts"] = df["Form"]
            df.drop(columns=["Form"], inplace=True)
            df["GP"] = df["W"]
            df["W"] = df["D"]
            df["D"] = df["L"]
        else:
            df["SG"] = df["Pts"]
            df["Pts"] = df["url"]

        df.drop(columns=["", "url"], inplace=True)

        return df

    def __update_rank_table(
        self,
        current_matchweek: int,
        rank_table_df: pd.DataFrame,
        table_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Updates the cumulative standings table with data from a specific matchweek.

        Args:
            current_matchweek (int): The current matchweek number.
            rank_table_df (pd.DataFrame): The cumulative standings DataFrame.
            table_df (pd.DataFrame): The DataFrame containing the current matchweek's data.

        Returns:
            pd.DataFrame: An updated cumulative standings DataFrame.
        """

        if current_matchweek == 1:
            clubs = table_df["Club"]
            for index, club in enumerate(clubs):
                rank_table_df.at[index, "Club"] = club
                rank_table_df.at[index, current_matchweek] = index + 1
        else:
            for index, row in table_df.iterrows():
                club = row["Club"]

                club_index = rank_table_df[rank_table_df["Club"] == club].index
                club_index = club_index.item()
                rank_table_df.at[club_index, current_matchweek] = row["#"]

        return rank_table_df


if __name__ == "__main__":
    brasileirao_scrapper = LeagueScrapper(
        "https://www.transfermarkt.com/campeonato-brasileiro-serie-a/formtabelle/wettbewerb/BRA1?saison_id={year}&min=1&max={matchweek}",
        os.path.join("data", "Brasileirao"),
    )
    brasileirao_scrapper.scrape_tables(2005, 2023, 1, 38, verbose=True)

    premier_league_scrapper = LeagueScrapper(
        "https://www.transfermarkt.com/premier-league/formtabelle/wettbewerb/GB1?saison_id={year}&min=1&max={matchweek}",
        os.path.join("data", "PremierLeague"),
    )
    premier_league_scrapper.scrape_tables(1995, 2017, 1, 38, verbose=True)
