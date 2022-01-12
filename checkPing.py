from enum import unique
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import pymysql.cursors  

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    param = '-n' if platform.system().lower()=='windows' else '-c'

    command = ['ping', param, '1', host]

    return subprocess.call(command, stdout=subprocess.DEVNULL) == 0
# a = ping('mail.ru')
# print(a)

# Функция для накатки статистики по пингу
def initialPing():
    connection = pymysql.connect(host='localhost',
                             user='',
                             password='',                             
                             db='',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        sql = f"""select * from domain_fin"""
        cursor.execute(sql)
        mould = [row for row in cursor]
    
    allResource = [[resource['domen'], resource['orgName']] for resource in mould]
    ResourcesAfterClean = []
    for hostname in allResource:
        try: 
            hostname[0].index('/')
            hostname[0] = hostname[0][:hostname[0].index('/')]
            ResourcesAfterClean.append(hostname)
        except ValueError:
            ResourcesAfterClean.append(hostname)
    
    new = [tuple(all) for all in ResourcesAfterClean]
    uniqueResources = list(set(new))
    print(uniqueResources)
    print(len(uniqueResources))

    pingStatistic = []
    for resource in uniqueResources:
        if ping(resource[0]):
            pingStatistic.append((resource[1], resource[0], 1))
        else:
            pingStatistic.append((resource[1], resource[0], 0))

    sql = "INSERT INTO ping_status (orgName, domen, ping) VALUES (%s, %s, %s)"
    with connection.cursor() as cursor:
        cursor.executemany(sql, pingStatistic)
        connection.commit()
    
# Функция для последующего контроля пинг статистики
def continuePing():
    connection = pymysql.connect(host='',
                             user='',
                             password='',                             
                             db='',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        sql = f"""select * from ping_status"""
        cursor.execute(sql)
        mould = [row for row in cursor]
    
    allResource = [[resource['domen'], resource['orgName'], resource['ping']] for resource in mould]
    for resource in allResource:
        statusPing = ping(resource[0])
        if statusPing != bool(resource[2]):
            print(f"Организация: {resource[1]}, ресурс: {resource[0]}, поменялось поведение пинга (старое - {bool(int(resource[2]))}, новое - {statusPing})")

# Накатываем статистику
# initialPing()

# Следим за статистикой
# continuePing()