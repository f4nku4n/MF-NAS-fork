from . import Algorithm
from models import Network
from copy import deepcopy
import numpy as np
import math

class SuccessiveHalving(Algorithm):
    def __init__(self):
        super().__init__()
        self.list_iepoch = None
        self.n_candidate = -1

    def _run(self):
        assert len(self.list_iepoch) is not None

        list_network = self.sample()
        best_network, search_time, total_epoch = self.search(list_network)
        return best_network, search_time, total_epoch

    def sample(self):
        list_network = []
        for _ in range(self.n_candidate):
            network = Network()
            while True:
                genotype = self.problem.search_space.sample(genotype=True)
                if self.problem.search_space.is_valid(genotype):
                    network.genotype = genotype
                    break
            list_network.append(network)
        return list_network

    def search(self, list_network):
        assert len(list_network) != 0
        checkpoint = 0
        iepoch = self.list_iepoch[checkpoint]

        total_time, total_epoch = 0.0, 0
        list_network = np.array(list_network)

        last_iepoch = 0
        best_network = None
        score_best_network = -np.inf

        n_eval = 0
        last = False
        while (n_eval <= self.problem.max_eval) and (total_time <= self.problem.max_time):
            evaluated_network = []
            network_scores = []

            for network in list_network:
                time = self.problem.evaluate(network, using_zc_metric=self.using_zc_metric, metric=self.metric+f'_{iepoch}')
                diff_epoch = network.info['cur_iepoch'][-1] - last_iepoch
                total_time += time
                total_epoch += diff_epoch

                evaluated_network.append(network)
                network_scores.append(network.score)

                if total_time >= self.problem.max_time:
                    total_time -= time
                    total_epoch -= diff_epoch

                    return best_network, total_time, total_epoch

                if network.score > score_best_network:
                    best_network = deepcopy(network)
                    score_best_network = network.score
            ids = np.flip(np.argsort(network_scores))
            list_network = np.array(evaluated_network)[ids]
            list_network = list_network[:math.ceil(len(list_network) / 2)]
            if len(list_network) == 1 or last:
                return best_network, total_time, total_epoch

            checkpoint += 1
            last_iepoch = iepoch
            iepoch = self.list_iepoch[checkpoint]
            if iepoch == self.list_iepoch[-1]:
                last = True
