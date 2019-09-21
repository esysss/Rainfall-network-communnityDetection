import networkx
import numpy
import re
import matplotlib.pyplot as plt
import community as cm
from sklearn.metrics.cluster import normalized_mutual_info_score
import otherFuns
import matplotlib.pyplot as plt
from sklearn.decomposition import NMF
import skfuzzy as fuzz



def LPANB(net):
    print('')
    return 'hi'

def NMFf(net,numberOfCommunities):
    M = networkx.adjacency_matrix(net)
    M = M.todense()  # the sparse adjacency matrix of our network
    model = NMF(n_components=numberOfCommunities, init='random', random_state=0, max_iter=200)

    W = model.fit_transform(M)
    H = model.components_
    communities = []
    for i, arr in enumerate(H.T):
        communities.append(numpy.argmax(arr))

    q = []
    [q.append([]) for i in range(max(communities) + 1)]
    for i, arr in enumerate(communities):
        q[arr].append(i)

    return q

def CMeans(net, clusterNumbers):
    M = networkx.adjacency_matrix(net)
    M = M.todense()  # the sparse adjacency matrix of our network

    cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
        M, clusterNumbers, 2, error=0.005, maxiter=1000, init=None)
    cluster_membership = numpy.argmax(u, axis=0)

    communities = []
    for i in range(clusterNumbers):
        communities.append(numpy.where(cluster_membership == i)[0])

    return communities