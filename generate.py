import begin
import requests
import json


@begin.start(auto_convert=True, config_file='config.txt')
@begin.logging
def start():
    url = "https://api.github.com/repos/asrob-uc3m/impresoras-asrob/issues?state=open&labels={}" # NO%20FUNCIONA,
    printers = ["BLACKY", "HIJA RESURRECTION"]
    printers_status = {}

    for printer_name in printers:
        printer_name_for_url = printer_name.replace(" ", "%20")
        response = requests.get(url.format(printer_name_for_url))
        obj = json.loads(response.text)
        for issue in obj:
            printers_status[printer_name]=  issue['title']

    print(printers_status)