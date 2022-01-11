import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
from multiprocessing import Pool
import pymysql.cursors  

def revokeList(url):

    # ИНТЕРПРОМБАНК, Лицензия отозвана
    # https://cbr.ru/banking_sector/credit/coinfo/?id=450001207

    response = requests.get('https://cbr.ru/banking_sector/credit/cowebsites/'+url)
    soup = BeautifulSoup(response.text, 'html.parser')

    mould = [part.text.strip() for part in soup.findAll('div', {'class': 'coinfo_item_text col-md-13 offset-md-1'})]
    revoked = False
    for pfrase in mould:
        try:
            str(pfrase).index('Лицензия отозвана приказом') != -1
            revoked = True
            break
        except ValueError:
            continue
        

    return revoked

def writeDb(orgName, regNumber, domains):
    
    connection = pymysql.connect(host='',
                             user='',
                             password='',                             
                             db='',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        for domain in domains:
            if domain.find('http://') != -1:
                stripDomain = domain.replace('http://', '')
            else:
                stripDomain = domain.replace('https://', '')
            print(f"Insert into domain_fin values ('{orgName}',{int(regNumber)},'{stripDomain}')")
            cursor.execute(f"Insert into domain_fin values ('{orgName}',{int(regNumber)},'{stripDomain}')")
            connection.commit()

def makeAll(mould):
    url = mould[0]
    orgName = mould[1]
    orgNumber = mould[2]
    revoked = revokeList(url)
    organization = mould[3]
    domainAfterCheck = []
    iskl = ['vk.com','youtube.com','facebook.com','twitter.com','ok.ru/','instagram','google.com','odnoklassniki','t.me/']
    hasSocial = False
    if not revoked:
        for link in organization:
            for social in iskl:
                if link.find(social) != -1:
                    hasSocial = True
                    break
            if not hasSocial:
                domainAfterCheck.append(link)
    if domainAfterCheck != []:
        writeDb(str(orgName), orgNumber, domainAfterCheck)
    
def main():
    response = requests.get('https://cbr.ru/banking_sector/credit/cowebsites/')
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find_all('table')
    df = pd.read_html(str(table))[0]
    
    orgNameMassiv = [orgName for orgName in df["Наименование кредитной организации"].values]
    regNumberMassiv = [regNumber for regNumber in df['Рег. номер'].values]
    linkMassiv = [link.split() for link in df["Адрес Web сайта"].values]

    table = soup.find('table')
    links = []
    for tr in table.findAll("tr"):
        trs = tr.findAll("td")
        for each in trs:
            try:
                link = each.find('a')['href']
                links.append(link)
            except:
                pass
    links = links[::2]
    
    массивОбработка = []
    for i in range(len(orgNameMassiv)):
        массивОбработка.append([links[i],orgNameMassiv[i], regNumberMassiv[i], linkMassiv[i]])

    startTime = time.time()
    with Pool(8) as p:           
       p.map(makeAll, массивОбработка)
    print("--- %s seconds ---" % (time.time() - startTime))

if __name__ == '__main__':
    main()





