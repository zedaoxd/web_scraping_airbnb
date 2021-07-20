from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from bs4 import BeautifulSoup as bs
import pandas as pd

destino = input('Pra onde você deseja viajar: ')
qtd_adultos = int(input('Digite o numero de adultos: '))
salvar = input('Deseja salvar os dados em um arquivo .cvs: (S/N) ').lower()

options = Options()
options.add_argument('window-size=400,800')
options.add_argument('--headless')

url = 'https://www.airbnb.com.br/'

navegador = webdriver.Chrome(options=options)

navegador.get(url)

sleep(2)

input1 = navegador.find_element_by_xpath('//*[@id="Koan-mobile-p1-koan-search-bar__input"]')
input1.send_keys(destino)
input1.submit()

sleep(1)

button_stay = navegador.find_element_by_css_selector('button > img')
button_stay.click()

sleep(1)

# botao de lugar
navegador.find_elements_by_tag_name('button')[-1].click()

sleep(1)
# add adulto
add_adult = navegador.find_elements_by_css_selector('button > span > svg > path[d="m2 16h28m-14-14v28"]')[0]
for _ in range(qtd_adultos):
    sleep(0.5)
    add_adult.click()

# botao de busca final
navegador.find_elements_by_tag_name('button')[-1].click()

sleep(1)

page_content = navegador.page_source
site = bs(page_content, 'html.parser')

hospedagens = site.findAll('div', attrs={'itemprop': 'itemListElement'})
lista_dados = []

for hospedagem in hospedagens:
    hospedagem_descricao = hospedagem.find('meta', attrs={'itemprop': 'name'})

    hospedagem_url = hospedagem.find('meta', attrs={'itemprop': 'url'})

    hospedagem_detalhes = hospedagem.find('div', attrs={'style': 'margin-bottom: 2px;'}).findAll('li')
    hospedagem_detalhes = ''.join([detalhe.text for detalhe in hospedagem_detalhes])

    preco = hospedagem.findAll('span')[-1].text

    lista_dados.append([hospedagem_descricao['content'], hospedagem_detalhes, hospedagem_url['content'], preco])

navegador.close()
df_dados = pd.DataFrame(lista_dados, columns=['descricao', 'detalhes', 'url', 'preco'])

if salvar[0] == 's':
    df_dados.to_csv('detalhes_busca.csv', index=False)

print(df_dados)
