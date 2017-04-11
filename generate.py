import begin
import os
import requests
import json

from jinja2 import Environment, FileSystemLoader, select_autoescape

@begin.start(auto_convert=True)
@begin.logging
def start(output_file: 'Select website directory to write index.html'= os.path.join(os.path.split(__file__)[0],'website', 'index.html')):
    # This parts get the data from GitHub
    url = "https://api.github.com/repos/asrob-uc3m/impresoras-asrob/issues?state=open&labels=NO%20FUNCIONA,{}"
    printers = {'BLACKY': {
                    'name':'Blacky',
                    'id':'blacky',
                    'index':0,
                    'description':'La impresora negra.',
                    'issues':[]},

                'HIJA RESURRECTION':{
                    'name':'Hija Resurrection',
                    'id':'hijares',
                    'index':1,
                    'description':'La otra impresora',
                    'issues':[]}}

    for printer_name in printers:
        printer_name_for_url = printer_name.replace(" ", "%20")
        response = requests.get(url.format(printer_name_for_url))
        obj = json.loads(response.text)
        for issue in obj:
            printers[printer_name]['issues'].append({'title':issue['title'], 'url':issue['html_url']})

    # print(printers)

    # This part generates the webpage
    env = Environment(loader=FileSystemLoader('./templates'), autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template('index.html')
    html = template.render(printers=sorted(list(printers.values()), key=lambda x: x['index']))

    # Only thing left is to save the rendered template
    with open(output_file, 'w') as f:
        f.write(html)

