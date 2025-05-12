import matplotlib.pyplot as plt


def plotResults(durations, sizes):
    plt.plot(durations)
    plt.title('Game Duration Over Time')
    plt.xlabel('Training Session')
    plt.ylabel('Duration')
    plt.show()

    plt.plot(sizes)
    plt.title('Snake Size Over Time')
    plt.xlabel('Training Session')
    plt.ylabel('Size')
    plt.show()


def saveResults(data, outfile):
    try:
        with open(outfile, 'w') as f:
            f.write(str(data))
        print("\033[92m\033[1mModel saved to", outfile, "\033[0m")
    except Exception:
        print("\033[91m\033[1mEXCEPTION RAISED: Error trying to save\
 results to ", outfile, ". Cancelling.\033[0m", sep='')


def loadResults(infile):
    try:
        with open(infile, 'r') as f:
            data = eval(f.read())
        print("\033[92m\033[1mModel loaded from", infile, "\033[0m")
        return data
    except Exception:
        print("\033[91m\033[1mEXCEPTION RAISED: Error trying to load results \
 from ", infile, ". Will start with default qTable.\033[0m",
              sep='')
        return {}
