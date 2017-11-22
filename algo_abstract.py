# template:

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