from load import load_from_csv
import interval
import mu
import data as d

if __name__ == "__main__":
    data = []
    data.append(load_from_csv("file.csv"))
    # d.plot(data)
    eps = 1 * 1e-4
    size_range = range(len(data))
    interval.interval(data, eps, 1)
    interval.interval(data, eps, 2)
    interval.interval(data, eps * 7.5490, 3)
    # eps = 2 * 1e-4
    # mu.plot(data, eps)

