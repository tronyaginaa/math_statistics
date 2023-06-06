import pandas as pd
import diagram
import plots
import subint_plots
import load

if __name__ == "__main__":
    data = pd.read_csv('/Users/tronyagina/Downloads/Статистика-измерений/Канал 1_800nm_0.2.csv', sep=';', encoding='cp1251')
    eps = 0.5*10e-4
    print(data)
    data = data['мВ']
    interval_data = []
    for i in range(0, len(data)):
        interval_data.append([data[i] - eps, data[i] + eps])
    diagram.diagram(data, eps, None)
    load.parser(1)
    A1, B1, w1 = load.load_processed('Chi1.txt')
    load.parser(0)
    A0, B0, w0 = load.load_processed('Chi0.txt')
    plots.show_plots(data, eps, A1, B1, w1, A0, B0, w0)
    subint_plots.show_plots(data, eps, A1, B1, A0, B0)
































