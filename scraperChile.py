from bs4 import BeautifulSoup
import requests
from unidecode import unidecode
import numpy as np



def scraper_data_chile():
    """
    Function that get data from https://es.wikipedia.org/wiki/Chile with
    BeautifulSoup and return 3 numpy output
    """

    url = 'https://es.wikipedia.org/wiki/Chile'
    page_response = requests.get(url, timeout=10)
    page_content = BeautifulSoup(page_response.content, "html.parser")

    title=[]
    chile_data=[]
    chile_data2=[]
    population = []

    chile_rows = page_content.find(
        'table',{
            'class':'wikitable col1izq col2der col3der col4der col5der col6izq'
        }
    )
    list_td = chile_rows.find_all('td')
    list_th = chile_rows.find_all('th')

    for l_th in list_th[1:-6]:
        l_th = unidecode(l_th.get_text()).split(" ")
        title.append(l_th[0])
    title.append('Porcentaje')

    for l_td in list_td:
        if list_td.index(l_td) == 5:
            continue
        if l_td.find_all('a'):
            a=l_td.find_all('a')
            chile_data2.append(a[0].get_text())
        else:
            l_td = unidecode(l_td.get_text()).replace(" ","").replace(",",".")
            if '(' in l_td:
                l_td = l_td.split("(")[0]
            chile_data2.append(float(l_td))
            if len(chile_data2) == 2:
                population.append(chile_data2[1])
        if len(chile_data2) == 5:
            chile_data.append(chile_data2)
            chile_data2=[]

    return np.array([title]), np.array(chile_data), np.array([population])


def percentage(population):
    """
    Function to calculate the percentage of population
    """
    percentage_population = []

    for i in population:
        percentage_population.append(i/np.sum(population)*100)

    return np.array(percentage_population)


def csv_output(title, table, population_percentage):
    """
    Function that create the output file csv with the information of Chile
    """
    output = np.concatenate((table, population_percentage.T),axis=1)
    output = np.concatenate((title, output), axis=0)
    output = output.astype('str')

    return np.savetxt('Chile.csv', output, delimiter=",",fmt="%s")



if __name__ == '__main__':
    title,table,population = scraper_data_chile()
    population_percentage = percentage(population)
    csv_output(title,table,population_percentage)
