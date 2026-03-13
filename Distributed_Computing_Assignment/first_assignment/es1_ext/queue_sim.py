#!/usr/bin/env python3

import argparse
import csv
import collections
import logging
import math

from random import expovariate, sample, seed
from discrete_event_sim import Simulation, Event

# columns saved in the CSV file
CSV_COLUMNS = ['algo', 'lambd', 'mu', 'max_t', 'n', 'w']

class Queues(Simulation):

    def __init__(self, lambd, mu, n, max_t, select_algo, num_samp):
        super().__init__()

        self.running = [None] * n  # if not None, the id of the running job (per queue)

        self.queues = [collections.deque() for _ in range(n)]  # FIFO queues of the system

        # NOTE: we don't keep the running jobs in self.queues

        self.arrivals = {}  # dictionary mapping job id to arrival time
        self.completions = {}  # dictionary mapping job id to completion time
        self.time = {}  # list of map used for mapping the number of jobs there are in a server
        self.lambd = lambd  # lambda value
        self.n = n  # number of server
        self.mu = mu  # the value of the serving time in the system
        self.max_t = max_t
        self.arrival_rate = lambd * n  # frequency of new jobs is proportional to the number of queues
        self.schedule(expovariate(lambd), Arrival(0))  # schedule the first arrival
        self.schedule(0, Monitor(1))

        #Fields that we add for our modification
        self.avg = 0.01 #average number of jobs in the queues
        self.variance = 0.01
        self.interval = 5  # we calculate the avg and variance every time that arrive this number of jobs
        self.select_algo = select_algo #Selected algorithm to calculate dynamic-d value
        if select_algo == 4:
            self.mid_d = int(self.n * 0.5)
        self.max_d = int(self.n * 0.8)  #the maximum value that dynamic-d can reach
        self.min_d = int(self.n * 0.2)  #the minimum value that dynamic-d can reach


    def schedule_arrival(self, job_id):
        """Schedule the arrival of a new job."""
        self.schedule(expovariate(self.arrival_rate), Arrival(job_id))

    def schedule_completion(self, job_id, queue_index):
        """Schedule the completion of a job."""
        self.schedule(expovariate(self.mu), Completion(job_id, queue_index))

    def queue_len(self, i):
        """Return the length of the i-th queue."""

        return (self.running[i] is not None) + len(self.queues[i])


class Arrival(Event):
    """Event representing the arrival of a new job."""

    def __init__(self, job_id):
        self.id = job_id

    def process(self, sim: Queues):
        sim.arrivals[self.id] = sim.t  # set the arrival time of the job

        #We don't want that heavy computational operations are made every arrival
        if self.id % sim.interval == 0:
            sim.avg = sum(sim.queue_len(i) for i in range(sim.n)) / sim.n
            sim.variance = sum((sim.queue_len(i) - sim.avg) ** 2 for i in range(sim.n))

        std = sim.variance ** 0.5
    
        if sim.avg > 0:
            cv = std / sim.avg
        else:
            cv = 0.1

        match sim.select_algo:
            case 1:
                sim.dynamic_d = int((math.atan(cv) * sim.max_d * 2) / math.pi)

            case 2:
                sim.dynamic_d = int((math.atan(cv * sim.max_d) * sim.max_d * 2) / math.pi)

            case 3:
                if cv <= 1 or sim.avg <=  3:
                    sim.dynamic_d = int((math.atan(cv) * sim.max_d * 2) / math.pi)
                elif cv > 1:
                    sim.dynamic_d = int((math.atan(cv * sim.max_d) * sim.max_d * 2) / math.pi)

            case 4:
                if cv > 1 and sim.avg > 3:
                    sim.dynamic_d = sim.max_d
                elif cv < 0.5 or (cv > 1 > sim.avg):
                    sim.dynamic_d = sim.min_d
                else:
                    sim.dynamic_d = sim.mid_d

        if sim.dynamic_d == 0:
            sim.dynamic_d = sim.min_d

    
        sample_queues = sample(range(sim.n), sim.dynamic_d)
        queue_index = min(sample_queues, key=sim.queue_len)  # shortest queue among the sampled ones

        if sim.running[queue_index] is not None:  # if there are running job in the queue:
            sim.queues[queue_index].append(self.id)  # put the job into the queue
        else:
            sim.running[queue_index] = self.id  # otherwise, set the incoming one
            sim.schedule_completion(self.id, queue_index)  # schedule its completion
        sim.schedule_arrival(self.id + 1)  # schedule the arrival of the next job


class Completion(Event):
    """Job completion."""

    def __init__(self, job_id, queue_index):
        self.job_id = job_id
        self.queue_index = queue_index

    def process(self, sim: Queues):
        queue_index = self.queue_index
        assert sim.running[queue_index] == self.job_id  # the job must be the one running
        sim.completions[self.job_id] = sim.t
        queue = sim.queues[queue_index]

        if queue:  # queue is not empty
            sim.running[queue_index] = new_job_id = queue.popleft()  # assign the first job in the queue
            sim.schedule_completion(new_job_id, queue_index)  # schedule its completion
        else:
            sim.running[queue_index] = None  # no job is running on the queue
    
            sample_queues = sample(range(sim.n), sim.dynamic_d)
            queue_index_max = max(sample_queues, key=sim.queue_len)
            num_of_round = sim.queue_len(queue_index_max)//2
            for i in range(0, num_of_round):
                pop_jobs = sim.queues[queue_index_max].pop()
                queue.append(pop_jobs)


class Monitor(Event):

    def __init__(self, interval=5):
        self.interval = interval

    def process(self, sim: Queues):
        for x in range(0, sim.n):
            if (sim.queue_len(x) in sim.time):
                sim.time[sim.queue_len(x)] += 1
            else:
                sim.time[sim.queue_len(x)] = 1

        tot = 0
        list_key = list(sim.time.keys())
        list_key.sort(reverse=True)

        for x in sim.time.keys():
            tot += sim.time[x]

        for x in sim.time.keys():
            sim.time[x] = sim.time[x] / tot

        for x in range(1, len(list_key)):
            sim.time[list_key[x]] += sim.time[list_key[x - 1]]

        sim.schedule(self.interval, self)



def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--algo', type=int, default=4, help="select the algo that we will use for the d-dynamic calculation")
    parser.add_argument('--num_samp', type=int, default=2, help="num of try sample")
    parser.add_argument('--lambd', type=float, default=0.99, help="arrival rate")
    parser.add_argument('--mu', type=float, default=1, help="service rate")
    parser.add_argument('--max-t', type=float, default=1_000_000, help="maximum time to run the simulation")
    parser.add_argument('--n', type=int, default=5, help="number of servers")
    parser.add_argument('--csv_w', help="CSV file in which to store w results", default="out_w.csv")
    parser.add_argument('--csv_ql', help="CSV file in which to store length results", default="out_length.csv")
    parser.add_argument("--seed", help="random seed")
    parser.add_argument("--verbose", action='store_true')

    args = parser.parse_args()

    params = [getattr(args, column) for column in CSV_COLUMNS[:-1]]

    # check if lambd, mu, max-t n and d are all positive
    if any(x <= 0 for x in params):
        logging.error("lambd, mu, max-t, n and d must all be positive")
        exit(1)

    if args.seed:
        seed(args.seed)  # set a seed to make experiments repeatable
    if args.verbose:
        logging.basicConfig(format='{levelname}:{message}', level=logging.INFO, style='{')

    if args.lambd >= args.mu:
        logging.warning("The system is unstable: lambda >= mu")

    sim = Queues(args.lambd, args.mu, args.n, args.max_t, args.algo, args.num_samp)
    sim.run(args.max_t)

    completions = sim.completions
    W = ((sum(completions.values()) - sum(sim.arrivals[job_id] for job_id in completions)) / len(completions))
    print(f"Average time spent in the system: {W}")
    if args.mu == 1 and args.lambd != 1:
        print(f"Theoretical expectation for random server choice: {1 / (1 - args.lambd)}")

    if args.csv_w is not None:
        with open(args.csv_w, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([args.algo,args.lambd, args.n, W])

    if args.csv_ql is not None:
        with open(args.csv_ql, mode='a', newline='') as file:
            writer = csv.writer(file)
            for key, value in sim.time.items():
                writer.writerow([sim.select_algo, sim.lambd, value, key])


if __name__ == '__main__':
    main()
