import requests
import json
import child_process.Instruction as ins

class LocalParent:
    def __init__(self,location):
        self.location = location

    def register_new_child(self,child):
        r = requests.post(self.location + "/register")
        rd = r.json()
        return rd["id"],rd["rate"],rd["algo"]

    def request_instructions(self,child_id):
        instr = ins.instr_from_dct(requests.post(self.location + "/instr",data={'id': child_id}).json())
        return instr

    def report_result(self,child_id,result):
        requests.post(self.location + "/report", data={"res":json.dumps(result),"id":child_id})

    def unregister_child(self,child_id):
        requests.post(self.location + "/kill", data={"id":child_id})
