import sys
import time
import math
import random
import os
import os.path


# A file must contain at least the definition of a class named algo. Algo must contain a method
# run_child, which must take a <child_object> and output a <run_child> object
# algo must also contain a method generate_seed, which must create a <set> of <child_object>
# algo must also contain a method generate_subsequent_gen, which must create a <set> of <child_object>
# given a <set> of <child_object>
# algo must also contain a method split, which must take a <set> <child_object> and a number, and must return a list of list
# of <child_object>, with number sublists.
# algo must also contain a method combine, which must take a list of list of <run_child> objects and produce a <set> of <child_object>
# algo can define set, child, and run child however it likes, other than that child and run child must serialize nicely.
# if they don't serialize nicely, algo can define a serialize and deserialize method to perform this


#note also that an actual instance of the class will be created in each child, so if desired
# the thing may hold state about how to use the child.
class Algo:
    def __init__(self):
        self.genome_size = 10#choose genome size
        self.gen_1_size = 1000#choose
        self.other_gen_size = 1000#choose
        #may have a minimum and maximum number of workers, if desired. Current values will start as soon as a worker appears
        self.min_workers = 1
        self.max_workers = float('inf')
        self.num_gens = 0

    def score_child(self,child):
        #replace as desired
        return 2

    def log(self,gen):
        global os
        if not os.path.exists("gen_data"):
            os.makedirs("gen_data")
        #modify to do logging as desired
        global json
        self.num_gens += 1
        with open("gen_data/" + "gens_"+str(self.num_gens) + ".txt", "w") as fo:
            score = sum([x[0] for x in gen])
            fo.write("SCORE: " + str(score))
            for elt in gen[:10]:
                fo.write("\n")
                fo.write(json.dumps(elt[1]))


    def should_continue(self,prev_gen):
        # modify terminus as needed, or just close it from cmd line: either returning
        # false here or cmd line killing will kill all children
        return True

    def run_child(self, child):
        score = self.score_child(child)
        return (score,child)

    def generate_seed(self):
        return self.seed_first_generation()

    def seed_next_generation(self, parent_generation):
        # modify as desired, but this is generally fairly reasonable
        global random
        res = parent_generation[:len(parent_generation) // 3]
        def make_child(p1,p2):
            tres = []
            for y in range(self.genome_size):
                take_type = random.randint(0,100)
                if take_type < 20:
                    tres.append(p1[y])
                elif take_type < 40:
                    tres.append(p2[y])
                elif take_type < 70:
                    tres.append((p1[y] + p2[y]) / 2)
                elif take_type < 90:
                    mult = random.random() + .5
                    if take_type < 80:
                        tres.append(p1[y] * mult)
                    else:
                        tres.append(p2[y] * mult)
                else:
                    tres.append(random.randint(-10,10))
            return tres
        for x in range(len(res),self.other_gen_size):
            action = random.randint(0,100)
            if action < 10:
                r = random.randint(0,len(parent_generation)) - 1
                res.append(parent_generation[r])
            elif action < 95:
                p1 = parent_generation[random.randint(0,len(parent_generation) - 1)]
                p2 = parent_generation[random.randint(0,len(parent_generation) - 1)]
                res.append(make_child(p1,p2))
            else:
                sub = []
                for y in range(self.genome_size):
                    nxt = random.randint(-10, 10)
                    sub.append(nxt)
                res.append(sub)
        return res

    def split(self,to_split,split_into):
        global sys
        #note that this isn't striclty guaranteed to actually run every single child if there
        # are divisibility issues. If this is a problem you can tweak params.
        # this will also do nothing if there are processes > num_children
        res = []
        children_per_worker = len(to_split) // split_into
        for x in range(split_into):
            res.append(to_split[x*children_per_worker:(x+1)*children_per_worker])
        return res

    def combine(self,to_combine):
        return to_combine


    def generate_subsequent_gen(self,run_prev_gen):
        srted = sorted(run_prev_gen)
        self.log(run_prev_gen)
        tp = [x[1] for x in srted[:len(srted) // 10]]
        return self.seed_next_generation(tp)

    def seed_first_generation(self):
        global random
        res = []
        for x in range(self.gen_1_size):
            sub = []
            for y in range(self.genome_size):
                nxt = random.randint(-10,10)
                sub.append(nxt)
            res.append(sub)
        return res




global GLOBAL_ALGO
GLOBAL_ALGO = Algo()
