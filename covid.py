# Copyright (C) Hearot - All Rights Reserved
# Written by Gabriel Hearot <gabriel@hearot.it>.
# See LICENSE.

import iso8601
import json
from matplotlib import pyplot
from requests import get
from typing import Any, List, Dict

colours = ('b', 'g', 'r', 'c', 'm', 'y',
           'k', '#4F7942', '#00FFFF', '#FF2400')
data_url = ("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/"
            "dati-json/dpc-covid19-ita-andamento-nazionale.json")
extensions = {'.png': "📈 Scala lineare", '_log.png': "📈 Scala logaritmica",
              '_bars.png': "📊 Grafico a barre delle differenze"}
general_excluded_plots = ('_bars.png',)
plot_parameters = ('deceduti', 'dimessi_guariti',
                   'isolamento_domiciliare', 'ricoverati_con_sintomi',
                   'tamponi', 'terapia_intensiva',
                   'totale_attualmente_positivi', 'totale_casi',
                   'totale_ospedalizzati')
files = sorted(plot_parameters + ('general_plot',))

def draw_general_plot(dataset):
    global plot_parameters
    
    pyplot.figure(1)
        
    for k, parameter in enumerate(plot_parameters):
        pyplot.plot(*zip(*((iso8601.parse_date(i['data']).strftime('%d/%m'),
                        i[parameter]) for i in dataset)), color=colours[k],
                    label=parameter.replace('_', ' ').title())
    pyplot.legend(loc="upper left")
    pyplot.xticks(rotation='vertical')
    pyplot.ylabel('numero di persone')
    pyplot.grid(True)
    pyplot.savefig("general_plot.png")
    pyplot.yscale("log")
    pyplot.savefig("general_plot_log.png")
    pyplot.clf()


def draw_particular_plot(dataset, parameter: str, code: int):
    pyplot.figure(code+2)

    dates, data = zip(*((iso8601.parse_date(i['data']).strftime('%d/%m'),
                        i[parameter]) for i in dataset))
    pyplot.plot(dates, data,
                color=colours[code],
                label=parameter.replace('_', ' ').title())
    pyplot.legend(loc="upper left")
    pyplot.xticks(rotation='vertical')
    pyplot.ylabel('numero di persone')
    pyplot.grid(True)
    pyplot.savefig(f"{parameter}.png")
    pyplot.yscale("log")
    pyplot.savefig(f"{parameter}_log.png")
    pyplot.cla()
    
    deltas = (0,) + tuple(y-x for x, y in zip(data, data[1:]))
    pyplot.bar(dates, deltas,
               color=colours[code],
               label=parameter.replace('_', ' ').title())
    pyplot.legend(loc="upper left")
    pyplot.xticks(rotation='vertical')
    pyplot.ylabel('differenza nel numero di persone')
    pyplot.savefig(f"{parameter}_bars.png")
    pyplot.clf()
    

def draw_plots() -> List[Dict[str, Any]]:
    data = retrieve_data(data_url)
    draw_general_plot(data)
    for i, parameter in enumerate(plot_parameters):
        draw_particular_plot(data, parameter, i)
    return data


def retrieve_data(url: str) -> List[Dict[str, Any]]:
    return json.loads(get(data_url).text)

   
if __name__ == "__main__":
    draw_plots()
