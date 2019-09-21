import numpy
import pandas
import multiprocessing as mp
import pickle
import time

def tao(l, m, tx, ty):
    temp = numpy.zeros(4)
    temp[0] = tx[l + 1] - tx[l]
    temp[1] = tx[l] - tx[l - 1]
    temp[2] = ty[m + 1] - ty[m]
    temp[3] = ty[m] - ty[m - 1]

    toReturn = numpy.nanmin(temp) / 2
    return toReturn

def Qxy(w):
    Sx = w[0]
    Sy = w[1]
    timeLag = w[2]
    city = w[3]
    otherCity = w[4]

    sxlen = len(Sx)
    sylen = len(Sy)

    if min([sxlen,sylen]) < 5:
        out = (city, otherCity, 0)
        return out

    Cxy = 0
    for l in range(1, sxlen - 1):
        for m in range(1, sylen - 1):
            t = tao(l, m, Sx, Sy)
            if t + timeLag > Sx[l] - Sy[m] > 0:
                Cxy += 1
            elif Sx[l] == Sy[m]:
                Cxy += .5

    Cyx = 0
    for l in range(1, sylen - 1):
        for m in range(1, sxlen - 1):
            t = tao(l, m, Sy, Sx)
            if t + timeLag > Sy[l] - Sx[m] > 0:
                Cyx += 1
            elif Sy[l] == Sx[m]:
                Cyx += .5

    nominator = Cxy + Cyx
    denominator = (sxlen - 2) * (sylen - 2)
    outPut = nominator / numpy.sqrt(denominator)

    out = (city, otherCity, outPut)

    return out


if __name__ == '__main__':
    newDF = pandas.read_csv('PreprossecedData.csv')

    # df['RealMax'] = numpy.nan

    # print('starting to make the RealMax column')

    # dflen = len(df)

    # for i in range(dflen):
    #     print('making the realMax step {} in {}'.format(i,dflen))
    #     temp = numpy.zeros(4)
    #     temp[0] = df['max'].iloc[i]
    #     temp[1] = df['max.1'].iloc[i]
    #     temp[2] = df['max.2'].iloc[i]
    #     temp[3] = df['max.3'].iloc[i]
    #     df['RealMax'].iloc[i] = numpy.nanmax(temp)

    # df = df[['name','lon','lat','data','shamsi_date','RealMax']]

    cities = newDF['name'].unique()

    # cities = cities[2:]

    lenCities = len(cities)

    # newDF = pandas.DataFrame(columns=['name','lon','lat','data','shamsi_date','RealMax'])

    # print('start to cut the 95%')
    # cityCounter = 0
    # for city in cities:
    #     tempDF = df[df['name'] == city]
    #     threshold = tempDF['RealMax'].mean()*.95
    #     tempDF = tempDF[tempDF['RealMax'] >= threshold]
    #     newDF = newDF.append(tempDF,ignore_index = True)
    #     cityCounter+=1
    #     print('cutting the 95 percent step {} in {}'.format(cityCounter,lenCities))



    # newDF['data'] = pandas.to_datetime(newDF['data'])

    # # convert date types to integers to make them more readable
    # newDF['data'] = (newDF['data'] - pandas.Timestamp("1996-01-01")) // pandas.Timedelta('1day')


    timeLag = 1

    print('start to do the rest')

    li = []
    # man = mp.Manager()
    man = mp.Manager()
    q = man.Queue()
    mp.freeze_support()


    for numberOfCities, city in enumerate(cities):
        print('we are in the last one step {} in {}'.format(numberOfCities, lenCities))
        firstDF = newDF[newDF['name'] == city]
        sx = firstDF['data']
        st = time.time()
        to = []
        for i,otherCity in enumerate(cities[numberOfCities + 1:]): # numberOfCities + 1:

            secondDf = newDF[newDF['name'] == otherCity]
            sy = secondDf['data']
            w = (list(sx), list(sy), timeLag, city, otherCity)
            to.append(w)


        with mp.Pool(processes=20) as pool: # if you have a better processor feel free to increase the number of processesors
            li.append(pool.map(Qxy, to))

        theFile = open("net.pickle","wb")#it says to write in bite
        pickle.dump(li, theFile)
        theFile.close()
        print('it got {} seconds'.format(time.time() - st))

    theFile = open("finalnet.pickle", "wb")  # it says to write in bite
    pickle.dump(li, theFile)
    theFile.close()

    print("the peace of shit finished/nIf you reading this please shot down the system")