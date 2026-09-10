import pandas as pd
from data_txt import *
import os

pasta_xml = '.\data_xml'

for data in pasta_xml.iterdir():
    df = pd.read_xml()
    chave = df[chaveAcesso]
    valor = df[valorTotal]
    df.to_csv('arquivo_final.csv', index=False)  

