import time
import math

class Child:
    def __init__(self, parent, verbose=True):
        global GLOBAL_ALGO
        self.alive = True
        self.parent = parent
        self.verbose = verbose
        self.id, self.refresh_rate, algo_string = self.register_with_parent()
        GLOBAL_ALGO = None
        exec(algo_string)

        self.algo = GLOBAL_ALGO
        self.instr = None
        self.loop_exec()

    def loop_exec(self):
        while self.alive:
            time.sleep(1)
            if self.instr != None:
                self.instr.execute(self,self.parent,self.id)
            self.instr = self.request_instructions()


    def report(self, message):
        if self.verbose:
            print(message)

    def register_with_parent(self):
        print("registering")
        return self.parent.register_new_child(self)

    def request_instructions(self):
        if self.alive:
            print("requresting instruction")
            instr = self.parent.request_instructions(self.id)
            return instr

    def run_algo(self, parent_generation):
        res = []
        print(len(parent_generation))
        for elt in parent_generation:
            res.append(self.algo.run_child(elt))
        self.report_gen_results(res)
        time.sleep(.5)
        self.request_instructions()

    def report_gen_results(self, results):
        self.parent.report_result(self.id, results)
        self.request_instructions()

    def repoll_later(self, tme=-1):
        if tme == -1:
            tme = self.refresh_rate
        time.sleep(tme)
        self.instr = None

    def unregister(self):
        print("unregstering")
        self.alive = False
        self.parent.unregister_child(self.id)