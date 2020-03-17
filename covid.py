# Copyright (C) Hearot - All Rights Reserved
# Written by Gabriel Hearot <gabriel@hearot.it>.
# See LICENSE.

import json
from matplotlib import pyplot
from requests import get
from typing import Any, List, Dict

colours = ('b', 'g', 'r', 'c', 'm', 'y',
           'k', '#4F7942', '#00FFFF', '#FF2400')
data_url = ("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/"
            "dati-json/dpc-covid19-ita-andamento-nazionale.json")
extensions = {'.png': "📈 Scala lineare", '_log.png': "📈 Scala logaritmica",
              '_bars.png': "📊 Grafico a barre"}
general_excluded_plots = ('_bars.png',)
general_plot_parameters = ('deceduti', 'dimessi_guariti',
                           'isolamento_domiciliare', 'ricoverati_con_sintomi',
                           'tamponi', 'terapia_intensiva',
                           'totale_attualmente_positivi', 'totale_casi',
                           'totale_ospedalizzati')
parameters = general_plot_parameters + ('nuovi_attualmente_positivi',)
files = sorted(parameters + ('general_plot',))

def draw_general_plot(data):
    global general_plot_parameters
    
    pyplot.figure(1)
        
    for k, parameter in enumerate(general_plot_parameters):
        pyplot.plot(*zip(*((i['data'].split()[0][-2:],
                        i[parameter]) for i in data)), color=colours[k],
                    label=parameter.replace('_', ' ').title())
    pyplot.legend(loc="upper left")
    pyplot.xticks(rotation=90)
    pyplot.xlabel('giorno')
    pyplot.ylabel('numero di persone')
    pyplot.grid(True)
    pyplot.savefig("general_plot.png")
    pyplot.yscale("log")
    pyplot.savefig("general_plot_log.png")
    pyplot.clf()


def draw_particular_plot(data, parameter: str, code: int):
    pyplot.figure(code+2)

    dates, data = tuple(zip(*((i['data'].split()[0][-2:],
                        i[parameter]) for i in data)))
    pyplot.plot(dates, data,
                color=colours[code],
                label=parameter.replace('_', ' ').title())
    pyplot.legend(loc="upper left")
    pyplot.xlabel('giorno')
    pyplot.ylabel('numero di persone')
    pyplot.grid(True)
    pyplot.savefig(f"{parameter}.png")
    pyplot.yscale("log")
    pyplot.savefig(f"{parameter}_log.png")
    pyplot.cla()
    pyplot.bar(dates, data,
               color=colours[code],
               label=parameter.replace('_', ' ').title())
    pyplot.legend(loc="upper left")
    pyplot.xlabel('giorno')
    pyplot.ylabel('numero di persone')
    pyplot.savefig(f"{parameter}_bars.png")
    pyplot.clf()
    

def draw_plots() -> List[Dict[str, Any]]:
    data = retrieve_data(data_url)
    draw_general_plot(data)
    for i, parameter in enumerate(parameters):
        draw_particular_plot(data, parameter, i)
    return data


def retrieve_data(url: str) -> List[Dict[str, Any]]:
    return json.loads(get(data_url).text)

   
if __name__ == "__main__":
    draw_plots()
