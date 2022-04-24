from typing import Optional

from sqlalchemy.orm import Session

import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
from multiprocessing import Pool, Value
from ..db import models
from ..db import get_db


class Renewer:
    def __init__(self):
        self.currently_run = Value("i", 0)
        self.db: Optional[Session] = None

    @classmethod
    def revokeList(self, url):

        response = requests.get(
            "https://cbr.ru/banking_sector/credit/cowebsites/" + url
        )
        soup = BeautifulSoup(response.text, "html.parser")

        mould = [
            part.text.strip()
            for part in soup.findAll(
                "div", {"class": "coinfo_item_text col-md-13 offset-md-1"}
            )
        ]
        revoked = False
        for pfrase in mould:
            if str(pfrase).find("Лицензия отозвана приказом") != -1:
                revoked = True
                break

        return revoked

    @classmethod
    def writeDb(self, orgName, regNumber, domains):

        for domain in domains:
            if domain.find("http://") != -1:
                stripDomain = domain.replace("http://", "")
            else:
                stripDomain = domain.replace("https://", "")
            db = next(get_db())
            organization = (
                db.query(models.Organization)
                .filter(models.Organization.reg_number == int(regNumber))
                .one_or_none()
            )
            if organization is None:
                db.add(models.Organization(reg_number=int(regNumber), name=orgName))
            same_portal = (
                db.query(models.OrganizationPortal)
                .filter(models.OrganizationPortal.address == stripDomain)
                .one_or_none()
            )
            if same_portal is None:
                db.add(
                    models.OrganizationPortal(
                        organization_number=int(regNumber), address=stripDomain
                    )
                )
            db.commit()

    @classmethod
    def makeAll(self, mould):
        url = mould[0]
        orgName = mould[1]
        orgNumber = mould[2]
        revoked = self.revokeList(url)
        organization = mould[3]
        domainAfterCheck = []
        exceptions = [
            "vk.com",
            "youtube.com",
            "facebook.com",
            "twitter.com",
            "ok.ru/",
            "instagram",
            "google.com",
            "odnoklassniki",
            "t.me/",
        ]
        is_social = False
        if not revoked:
            for link in organization:
                for social in exceptions:
                    if social in link:
                        is_social = True
                        break
                if not is_social:
                    domainAfterCheck.append(link)
        if domainAfterCheck != []:
            self.writeDb(str(orgName), orgNumber, domainAfterCheck)

    def run(self):

        db = next(get_db())
        db.query(models.OrganizationPortal).delete()
        db.query(models.Organization).delete()
        db.commit()

        if self.currently_run.value == 1:
            return
        self.currently_run.value = 1
        response = requests.get("https://cbr.ru/banking_sector/credit/cowebsites/")
        html = response.text
        soup = BeautifulSoup(html, "lxml")
        table = soup.find_all("table")
        df = pd.read_html(str(table))[0]

        orgNameMassiv = [
            orgName for orgName in df["Наименование кредитной организации"].values
        ]
        regNumberMassiv = [regNumber for regNumber in df["Рег. номер"].values]
        linkMassiv = [link.split() for link in df["Адрес Web сайта"].values]

        table = soup.find("table")
        links = []
        for tr in table.findAll("tr"):
            trs = tr.findAll("td")
            for each in trs:
                try:
                    link = each.find("a")["href"]
                    links.append(link)
                except:
                    pass
        links = links[::2]

        arrayProcessing = []
        for i in range(len(orgNameMassiv)):
            arrayProcessing.append(
                [links[i], orgNameMassiv[i], regNumberMassiv[i], linkMassiv[i]]
            )

        startTime = time.time()
        with Pool(8) as p:
            p.map(Renewer.makeAll, arrayProcessing)
        print("--- %s seconds ---" % (time.time() - startTime))

        self.currently_run.value = 0

        return
