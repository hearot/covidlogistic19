# See LICENSE

import json
from matplotlib import pyplot
from requests import get
from typing import Any, List, Dict

colours = ('b', 'g', 'r', 'c', 'm')
data_url = ("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/"
            "dati-json/dpc-covid19-ita-andamento-nazionale.json")
parameters = ('deceduti', 'dimessi_guariti', 'nuovi_attualmente_positivi',
              'totale_attualmente_positivi', 'totale_casi')

def draw_general_plot(data):
    global parameters
    
    pyplot.figure(1)
    
    for k, parameter in enumerate(parameters):
        pyplot.plot(*zip(*((i['data'].split()[0][-2:],
                        i[parameter]) for i in data)), color=colours[k],
                    label=parameter.replace('_', ' ').title())
    pyplot.legend(loc="upper left")
    pyplot.xticks(rotation=90)
    pyplot.xlabel('giorno')
    pyplot.ylabel('numero di persone')
    pyplot.grid(True)
    pyplot.savefig("general_plot.png")


def draw_particular_plot(data, parameter: str, code: int):
    pyplot.figure(code+2)

    pyplot.plot(*zip(*((i['data'].split()[0][-2:],
                        i[parameter]) for i in data)),
                color=colours[code],
                label=parameter.replace('_', ' ').title())
    pyplot.legend(loc="upper left")
    pyplot.xticks(rotation=90)
    pyplot.xlabel('giorno')
    pyplot.ylabel('numero di persone')
    pyplot.grid(True)
    pyplot.savefig(f"{parameter}.png")
    

def main() -> List[Dict[str, Any]]:
    data = retrieve_data(data_url)
    draw_general_plot(data)
    for i, parameter in enumerate(parameters):
        draw_particular_plot(data, parameter, i)
    return data


def retrieve_data(url: str) -> List[Dict[str, Any]]:
    return json.loads(get(data_url).text)

   
if __name__ == "__main__":
    main()