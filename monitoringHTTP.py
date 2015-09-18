#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# TODO :
# * Envoyer un mail pour dire "Tout va bien", 1x par jour
# * Télécharger depuis une BDD la liste des clients

import urllib.request
import smtplib
from datetime import datetime


class MonitoringHTTP(object):
    def get_status_code(self, url):
        http_code = ""
        try:
            http_code = urllib.request.urlopen(url).getcode()
        except urllib.request.URLError:
            http_code = 404
        return http_code

    def load_urls(self, source_file):
        file = open(source_file, "r")
        urls = file.readlines()
        file.close()
        return urls

    def send_mail(self, url, mail_to, mail_from, password):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(mail_from, password)

        message = "Le site " + str(url) + " semble inaccessible."

        server.sendmail(mail_from, mail_to, message)
        server.quit()

    def save_log_html(self, url):
        now = datetime.now()
        file_date = now.month
        file_log_name = "" + str(file_date) + ".html"
        file = open(file_log_name, "a")
        file.write("Site inaccessible : {0} - Le {1}/{2} à {3}:{4}\n".format(str(url), str(now.day), str(now.month),
                                                                               str(now.hour), str(now.minute)))
        file.close()

    def check_urls(self, urls, mail_to, mail_from, password):
        http_code = 200
        i = 0
        errors = 0
        max = 0
        # Count the number of URLs
        for url in urls:
            max += 1
        current_url = ""
        for url in urls:
            i += 1
            current_url = url
            current_url = current_url.strip("\n")
            print("Analyse de : " + str(current_url) + " [" + str(i) + "/" + str(max) + "]")
            http_code = self.get_status_code(url)
            # If there is a status code 4xx
            if http_code == 404:
                self.save_log_html(url)
                self.send_mail(url, mail_to, mail_from, password)
                errors += 1
        print("*** Analyse terminée : " + str(errors) + " interruptions détectée(s).")
