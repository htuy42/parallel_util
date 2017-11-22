import json
import sys

import time

from child_process import Instruction
import random


def sprint(txt):
    print(txt, file=sys.stderr)


class Worker:
    def __init__(self, id, refresh_rate):
        self.id = id
        self.report = []
        self.refresh_rate = refresh_rate
        self.current_response = Instruction.WaitInstruction(self.refresh_rate,
                                                            "Waiting for initial request. Will retry in " + str(
                                                                refresh_rate) + " seconds.")

    def delegate_task(self, task_array):
        self.current_response = Instruction.GenInstruction(task_array, "Running new task for parent")

    def current_instruction(self):
        return self.current_response.make_dict()

    def kill(self):
        self.current_response = Instruction.KillInstruction()

    def wait_for_next_gen(self, report):
        self.report = json.loads(report)
        self.current_response = Instruction.WaitInstruction(self.refresh_rate,
                                                            "Waiting for next generation to begin. Will poll again every " + str(
                                                                self.refresh_rate) + " seconds.")

    def get_result(self):
        return self.report

    def expect_response(self):
        pass


def load_algo_files(files):
    res = ""
    for f in files:
        fopen = open(f)
        res += fopen.read()
        res += "\n\n"
    return res


class ControlParent:
    def __init__(self, algo_files, num_algos):
        global GLOBAL_ALGO
        self.will_run_next = True
        self.waiting_for_first_worker = True
        self.algo_file_lines = load_algo_files(algo_files)
        GLOBAL_ALGO = None
        exec(self.algo_file_lines)
        self.workers = {}
        self.num_workers = 0
        self.gen_number = 0
        self.refresh_rate = 1
        self.current_gens = GLOBAL_ALGO.generate_seed()
        self.best_score = float('inf')
        self.expected_reports_left = 0

    def request_instruction(self, id):
        return self.workers[id].current_instruction()

    def add_child(self, id):
        global GLOBAL_ALGO
        if GLOBAL_ALGO.max_workers >= self.num_workers:
            new_child = Worker(id, self.refresh_rate)
            self.workers[id] = new_child
            self.num_workers += 1
            if self.waiting_for_first_worker:
                if GLOBAL_ALGO.min_workers <= self.num_workers:
                    self.waiting_for_first_worker = False
                    self.run_generation()
            return {"algo": self.algo_file_lines, "rate": self.refresh_rate, "id": id}
        else:
            return {"status":400, "message":"too many workers already, request to join rejected."}

    def run_generation(self):
        splt = GLOBAL_ALGO.split(self.current_gens,self.num_workers)
        x = -1
        for y in self.workers:
            x += 1
            self.workers[y].delegate_task(splt[x])
        self.wait_for_responses()

    def wait_for_responses(self):
        self.expected_reports_left = len(self.workers)

    def report_result(self, id, json):
        self.workers[id].wait_for_next_gen(json)
        self.expected_reports_left -= 1
        if self.expected_reports_left == 0:
            self.score_generation()
        return {"status": "success"}

    def score_generation(self):
        gen_res = []
        for worker in self.workers:
            gen_res += self.workers[worker].get_result()

        combo = GLOBAL_ALGO.combine(gen_res)
        self.current_gens = GLOBAL_ALGO.generate_subsequent_gen(combo)
        if GLOBAL_ALGO.should_continue(combo):
            self.run_generation()
        else:
            self.kill_children()

    def kill_children(self):
        for worker in self.workers:
            self.workers[worker].kill()

    def unregister(self, id):
        self.num_workers -= 1
        del self.workers[id]
