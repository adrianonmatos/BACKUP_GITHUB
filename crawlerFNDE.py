import time
import sys
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

import pandas as pd

options = webdriver.ChromeOptions()
options.headless = False


### LOAD THE PAGE #########################################
driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = options)
driver.get("https://www.fnde.gov.br/pls/simad/internet_fnde.LIBERACOES_01_PC")

time.sleep(1)

### FIND AND SET VALUES ON WEB ELEMENTS ###################
ANO = "2021"
select_ano = driver.find_element(By.XPATH,"/html/body/center/table[3]/tbody/tr[1]/td/form/table[2]/tbody/tr[1]/td[2]/font/select")
select_ano_obj = Select(select_ano)
select_ano_obj.select_by_visible_text(ANO)

select_estado = driver.find_element(By.XPATH,"/html/body/center/table[3]/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/font/select")    
select_estado_obj = Select(select_estado)
select_estado_obj.select_by_visible_text("Amazonas")

### ITERATE OVER MUNICIPIOS LIST ##########################
select_municipio = driver.find_element(By.XPATH,"/html/body/center/table[3]/tbody/tr[2]/td/table/tbody/tr[4]/td[2]/font/select")
select_municipio_obj = Select(select_municipio)
options = select_municipio_obj.options
for index in range(len(options)-1):
### VISIT THE MUNICIPIO ###################################
    time.sleep(1)
    TEMPO_MAX = 200
    select_municipio_obj.select_by_index(index)
    MUNICIPIO = select_municipio_obj.first_selected_option().text
    WebDriverWait(driver,TEMPO_MAX).until(
            EC.presence_of_element_located((By.XPATH,"/html/body/center/table[3]/tbody/tr[3]/td/input[1]"))
            ).click()

### DATAFRAME EXTRACT DATA FUNCTION DEFINITION ############
    def dataframe_extract_info(dfs):
        print("ANO: ", ANO)
        print("MUNICIPIO: ", MUNICIPIO)
        print("CNPJ: ", cnpj)
        dataframe_list_size = len(dfs)
        ### ITERATE OVER DATAFRAMES. SKIP FIRST PAGE HEADER ONE
        for df_idx in range(1, dataframe_list_size):
            df = dfs[df_idx]
            print(df.columns)
            print(df.head(2))
    
### CHECK IF LOADED PAGE IS A DATA TYPE ###################
    
    dfs = pd.read_html(driver.page_source, header=1)
    if(driver.find_element(By.TAG_NAME, "body").text.find("LISTA DE ENTIDADES ENCONTRADAS") == -1):
        dataframe_extract_info(dfs)
        driver.back()
    else:    
        df = dfs[1]
        df.columns = df.iloc[0]
        link_list = df["CNPJ"]
        link_list_size = len(link_list)
        for link_idx in range(1, link_list_size):
            cnpj = link_list[link_idx]
            link = driver.find_element(by=By.LINK_TEXT, value=cnpj).click()
            dfs2lvl = pd.read_html(driver.page_source, header=1)
            dataframe_extract_info(dfs2lvl)
            driver.back()
        time.sleep(1)
        driver.back()
        ### DONT KNOW WHY IT NEEDS TWO BACK ACTIONS #######
        driver.back()

driver.quit()
