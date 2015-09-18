#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from monitoringHTTP import MonitoringHTTP

monitoring = MonitoringHTTP()
urls = monitoring.load_urls("urls.txt")
monitoring.check_urls(urls, "to@mail.com", "from@mail.com", "password")
