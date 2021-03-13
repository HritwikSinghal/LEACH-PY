from src import LEACH

# import matplotlib
# matplotlib.use('TkAgg')
# import matplotlib.pyplot as plt

def main():
    myLeach = LEACH.LEACHSimulation(n=200)
    myLeach.start()


if __name__ == '__main__':
    main()
    # print(matplotlib.is_interactive())