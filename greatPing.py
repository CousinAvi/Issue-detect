import socket
import whois
import requests
import time
import datetime
from sslCheck import CheckSSLExp
from tls import getTLSVersion

def getTimestamp(year, month, day):
    d = datetime.date(year,month,day)
    unixtime = time.mktime(d.timetuple())
    return int(unixtime)

# Функция поиска DNS-записи
def dnsResolve(domain):
    try: 
        # Запись успешно нашлась
        domainInfo = socket.gethostbyname_ex(domain)
        # domainInfo = ('mail.ru', [], ['94.100.180.201', '94.100.180.200', '217.69.139.202', '217.69.139.200'])
        return domainInfo[2]
    except:
        # DNS-запись не обнаружена
        return []

# Функция дублирующая nc
def netcat(hostname, port):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    try: 
        s.connect((hostname, port))
    except:
        print("Не поднимается коннект по порту")
        return {'ресурс': hostname, 'port': port, 'issue': 'Не поднимается коннект по порту'} 
    s.settimeout(None)
    # s.sendall(bytes(content, encoding = 'utf-8'))
    # s.send("Hello Client!".encode())
    # s.shutdown(socket.SHUT_WR)

    # data = s.recv(1024)
    # if data == "":
    #     return {'ресурс': hostname, 'port': port, 'issue': 'Пустой ответ от ресурса'} 
    # # print ("Received:", repr(data))
    # # print ("Connection closed")
    s.close()

def getWebPage(hostname):
    # requestStrinf = f'GET / HTTP/1.1\nHost: {hostname}\n\n'
    # request = f'GET / HTTP/1.1\nHost: {hostname}\n\n'.encode()
    request = b"GET / HTTP/1.1\nHost: stackoverflow.com\n\n"
    print(request)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("stackoverflow.com", 80))
    s.send(request)
    result = s.recv(10000)
    while (len(result) > 0):
        print(result)
        result = s.recv(10000)  

# Запрашивает ресурс и выдает ошибку, если такая была при запросе веб-страницы
def checkHttpError(hostname=None, verifySSL=True): # hostname = https://...
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        response = requests.get(hostname, verify=verifySSL, headers=headers)
        response.raise_for_status()

    except requests.HTTPError as exception:
        return {'ресурс': hostname, 'port': 443, 'issue': f'{exception}'} 

# Важно: ЦБ (cbr.ru) не перекидывает с HTTP на HTTPS
# checkHttpError('https://www.cbr.ru/1141241')
# dnsResolve('mail.ru')
# netcat('mail.ru', 80)

def whoIs(hostname=None ):
    w = whois.whois(hostname)
    expDate = str(w["expiration_date"])
    timeMassiv = expDate.split()[0].split('-')
    year, month, day = range(3)

    currentTime = int(time.time()) # Текущее время
    expTime = getTimestamp(int(timeMassiv[year]),int(timeMassiv[month]),int(timeMassiv[day]))
    if currentTime > expTime:
        return {'ресурс': hostname, 'port': '', 'issue': 'Срок аренды домена истек'} 


def main():
    hostname = 'sberbank.ru'
    port = 443
    verifySSL = True
    errors = []
    # 1. Проверяем резолвится ли ресурс и поднимается ли коннект по порту (443)
    if dnsResolve(hostname) == []:
        print("Ресурс не резолвится")
        errors.append({'ресурс': hostname, 'port': '', 'issue': 'Не резолвится DNS-запись'})
        return errors

    # пытаемся достучаться до ресурса по порту, елси нет --> выход
    netcatResult = netcat(hostname, port)
    if netcatResult is not None:
        errors.append(netcatResult)
        return errors

    # Проверка не просрочен ли сертификат
    checkSSLErrors = CheckSSLExp(hostname, 443)
    if checkSSLErrors is not None:
        errors.append(checkSSLErrors)
        verifySSL = False # необходимо чтобы requests в checkHttpError запросил ресурс
    
    # Проверка на самоподписанный и крипту в серте
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        requests.get('https://'+hostname, headers=headers)
    except requests.exceptions.SSLError as instance:
        # print(instance.args[0].reason.args[0].reason)
        # print(instance.args[0].reason.args[0].strerror)
        
        errors.append({'ресурс': hostname, 'port': '', 'issue': f'{instance.args[0].reason.args[0].strerror}'})
        verifySSL = False

    # 2. Проверяем ошибки при запросе к веб-странице в HTTP (403, 500 etc)
    if verifySSL:
        httpErrorsResult = checkHttpError('https://'+hostname, verifySSL)
        if httpErrorsResult is not None:
            errors.append(httpErrorsResult)
    
    # 3. Проверяем истек ли срок аренды домена
    whoIsResult = whoIs(hostname)
    if whoIsResult is not None:
        errors.append(whoIsResult)

    # Проверка на SSLv3, TLSv1, TLSv1.1
    if verifySSL:
        try:
            currentTLS = getTLSVersion(hostname)
            if currentTLS == "SSLv3" or currentTLS == "TLSv1" or currentTLS == "TLSv1.1":
                errors.append({'ресурс': hostname, 'port': '', 'issue': f'Используется устаревший метод шифрования канала {currentTLS}'})
        except:
            print("балуемся Lets encrypt") # TODO Внести как предупреждение о том, что уровень серта не очень для ФО
    print(errors)

main()