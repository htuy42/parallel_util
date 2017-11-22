from abc import ABC


class BaseInstruction(ABC):
    def execute(self, child, parent, child_id):
        pass


class WaitInstruction(BaseInstruction):
    def __init__(self, tme, message):
        self.tme = tme
        self.message = message

    def execute(self, child, parent, child_id):
        child.report(self.message)
        child.repoll_later(self.tme)

    def make_dict(self):
        return {'type':'wait','time':self.tme,'message':self.message}


class GenInstruction(BaseInstruction):
    def __init__(self, parent_generation, message):
        self.parent_gen = parent_generation
        self.message = message

    def execute(self, child, parent, child_id):
        child.report(self.message)
        child.run_algo(self.parent_gen)

    def make_dict(self):
        return {'type':'gen','parent':self.parent_gen,'message':self.message}


class KillInstruction(BaseInstruction):
    def execute(self, child, parent, child_id):
        child.unregister()

    def make_dict(self):
        return {'type':'kill'}

def instr_from_dct(dct):
    type = dct['type']
    if type == 'gen':
        return GenInstruction(dct['parent'],dct['message'])
    elif type == 'kill':
        return KillInstruction()
    elif type == 'wait':
        return WaitInstruction(int(dct['time']),dct['message'])
