#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# TODO :
# * Sauvegarder l'heure d'envoi d'un mail en CSV
# * Envoyer un mail pour dire "Tout va bien", 1x par jour
# * Télécharger depuis une BDD la liste des clients

import urllib.request
import smtplib


class MonitoringHTTP(object):
    def get_status_code(self, url):
        http_code = ""
        try:
            http_code = urllib.request.urlopen(url).getcode()
        except:
            http_code = 404
        return http_code

    def load_urls(self, source_file):
        file = open(source_file, "r")
        urls = file.readlines()
        file.close()
        return urls

    def send_mail(self, url, mail_to, mail_from):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("login", "mdp")

        message = "Le site " + str(url) + " semble inaccessible."

        server.sendmail(mail_from, mail_to, message)
        server.quit()

    def check_urls(self, urls, mail_to, mail_from):
        http_code = 200
        for url in urls:
            http_code = self.get_status_code(url)
            if http_code == 404:
                self.send_mail(url, mail_to, mail_from)
