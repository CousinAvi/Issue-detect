import socket
from requests.exceptions import Timeout
import whois
import requests
import time
import datetime
from .sslCheck import CheckSSLExp
from .tls import getTLSVersion
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def getTimestamp(year, month, day):
    d = datetime.date(year, month, day)
    unixtime = time.mktime(d.timetuple())
    return int(unixtime)


# Функция поиска DNS-записи
def dnsResolve(domain):
    try:
        domain.index('/')
        domain = domain[:domain.index('/')]
    except ValueError:
        pass
    try:
        # Запись успешно нашлась
        domainInfo = socket.gethostbyname_ex(domain)
        # domainInfo = ('mail.ru', [], ['94.100.180.201', '94.100.180.200', '217.69.139.202', '217.69.139.200'])
        return domainInfo[2]
    except:
        # DNS-запись не обнаружена
        return []


# Функция дублирующая nc
def netcat(orgName, regNumber, hostname, port):
    initialHostname = hostname
    try:
        hostname.index('/')
        hostname = hostname[:hostname.index('/')]
    except ValueError:
        pass
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    try:
        s.connect((hostname, port))
    except:
        # print("Не поднимается коннект по порту")
        return {'company': orgName, 'service': initialHostname, 'reg_number': regNumber, 'port': '443',
                'issue': 'Не поднимается коннект по 443 порту'}

    s.settimeout(None)
    s.close()


# Запрашивает service и выдает ошибку, если такая была при запросе веб-страницы
def checkHttpError(orgName, regNumber, port, hostname=None, verifySSL=True):  # hostname = https://...
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        response = requests.get(hostname, verify=verifySSL, headers=headers, timeout=5)
        response.raise_for_status()

    except (requests.exceptions.SSLError, requests.HTTPError, requests.exceptions.Timeout, requests.ConnectionError) as exception:
        return {'company': orgName, 'service': hostname, 'reg_number': regNumber, 'port': port,
                'issue': f'{exception}'}


def whoIs(orgName, regNumber, hostname=None):
    w = whois.whois(hostname)
    # print(w)
    expDate = str(w["expiration_date"])
    timeMassiv = expDate.split()[0].split('-')
    year, month, day = range(3)

    currentTime = int(time.time())  # Текущее время
    expTime = getTimestamp(int(timeMassiv[year]), int(timeMassiv[month]), int(timeMassiv[day]))
    if currentTime > expTime:
        return {'company': orgName, 'service': hostname, 'reg_number': regNumber, 'port': '',
                'issue': 'Срок аренды домена истек'}


def main(hostname, orgName, regNumber, port=443):
    # print(regNumber, hostname)
    verifySSL = True
    errors = []
    # 1. Проверяем резолвится ли service и поднимается ли коннект по порту (443)
    if dnsResolve(hostname) == []:
        print("Ресурс не резолвится")
        errors.append({'company': orgName, 'service': hostname, 'reg_number': regNumber, 'port': '',
                       'issue': 'Не найдена А-запись домена'})
        return errors
    # пытаемся достучаться до serviceа по порту, елси нет --> выход
    netcatResult = netcat(orgName, regNumber, hostname, port)
    if netcatResult is not None:
        errors.append(netcatResult)
        return errors

    # Проверка не просрочен ли сертификат
    checkSSLErrors = CheckSSLExp(hostname, 443)
    if checkSSLErrors is not None:
        errors.append(checkSSLErrors)
        verifySSL = False  # необходимо чтобы requests в checkHttpError запросил service

    # Проверка на самоподписанный и крипту в серте
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

        requests.get('https://' + hostname, headers=headers, timeout=5)
    except (
    requests.exceptions.SSLError, requests.exceptions.TooManyRedirects, requests.exceptions.Timeout) as instance:
        errors.append(
            {'company': orgName, 'service': hostname, 'reg_number': regNumber, 'port': '', 'issue': f'{instance}'})
        verifySSL = False

    # 2. Проверяем ошибки при запросе к веб-странице в HTTP (403, 500 etc)
    if verifySSL:
        httpErrorsResult = checkHttpError(orgName, regNumber, 443, 'https://' + hostname, verifySSL)
        if httpErrorsResult is not None:
            if errors.count(httpErrorsResult) != 0:
                errors.append(httpErrorsResult)
    else:
        httpErrorsResult = checkHttpError(orgName, regNumber, 80, 'http://' + hostname, verifySSL)
        if httpErrorsResult is not None:
            if errors.count(httpErrorsResult) != 0:
                errors.append(httpErrorsResult)

    # 3. Проверяем истек ли срок аренды домена
    try:
        whoIsResult = whoIs(orgName, regNumber, hostname)
        if whoIsResult is not None:
            errors.append(whoIsResult)
    except:
        pass

    # Проверка на SSLv3, TLSv1, TLSv1.1
    if verifySSL:
        try:
            currentTLS = getTLSVersion(hostname)
            if currentTLS == "SSLv3" or currentTLS == "TLSv1" or currentTLS == "TLSv1.1":
                errors.append({'company': orgName, 'service': hostname, 'reg_number': regNumber,
                               'issue': f'Используется устаревший метод шифрования канала {currentTLS}'})
        except:
            pass
            # errors.append({'company': orgName, 'service': hostname, 'reg_number': regNumber, 'port': '', 'issue': "Сертификат выпущен УЦ R3 (Let's encrypt)'"}) # TODO Внести как предупреждение о том, что уровень серта не очень для ФО
    return errors

# Берем инфу из бд и проверяем все serviceы
# checkFromSQL()

# пример одного запроса
# main('1000-sans.badssl.com', 'Ресурс', 123)