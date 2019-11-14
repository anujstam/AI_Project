import ast

# Features : Sepal length, Sepal Width, Petal Length, Petal Width
# Classes  : 0 - Setosa, 1 - Versicolour, 2 - Virginica

feature_names = ["sepal length", "sepal width", "petal length", "petal width"]
class_names = ["setosa", "versicolour", "virginica"]

filename = "data.txt"
features = []
explanations = []
classes = []

def checkclause(clause, data):
    direction, fno, cutpoint = clause
    if direction == 'L':
        if data[fno] < cutpoint :
            return True
        else:
            return False
    if direction == 'R':
        if data[fno] > cutpoint : 
            return True
        else:
            return False

def checkstatement(rule, data):
    # data is feature vector of 4 features
    status = True
    for clause in rule:
        if clause[1] in data.keys():
            if status == True:
                status = checkclause(clause, data)
        else:
            status = "Undecidable"
    return status

def query_eval(query, KB):
    # Query set has known info and requested unknowns
    # EG : sl is 0.3, pl is 0.5, class is setosa, what is pw
    d = {}
    requests = []
    feats = ["sl", "sw", "pl", "pw"]
    class_list = ["setosa","versicolour","virginica"]
    target_class = -1
    query = query.split(",")
    feat_request = 0
    for sub in query:
        sub.rstrip(" ")
        sub.rstrip(".")
        sub.rstrip("?")
        sub.lstrip(" ")
        info = sub.split(" ")
        if info[0] == '':
            info = info[1:]
        if info[0] == "class":
            target_class = class_list.index(info[2])
        elif info[0] == "what":
            index = feats.index(info[2])
            requests.append(index+1)
            feat_request+= 1
        else:
            index = feats.index(info[0])
            d[index+1] = float(info[2])
    print(d)
    print(requests)
    if feat_request > 0 and target_class == -1 :
        print("Too many requests but not enough info!")
    else:
        if target_class != -1:
            nonefound = True
            answers = []
            for rule in KB:
                rule_ans = []
                status = True
                if rule[1] == target_class:
                    for clause in rule[0]:
                        if clause[1] in d.keys():
                            if status == True:
                                status = checkclause(clause, d)
                        else:
                            if clause[1] in requests:
                                rule_ans.append(clause)
                    if status == True:
                        answers.append(rule_ans)
            print("Entailments are:")
            for ans in answers:
                print(ans)
                        
                            
                #finish this
                # check how many requirements the rule meets and see the ones with -1
                # results will be the clause of the -1 feat in the rule and anything if it's absent
                
        else:   # Just evaluating features and finding class
             eval_featset(d,KB)
        
        
            
            
def eval_featset(feat_set, KB):
    classes_reached = []
    err = False
    for rule in KB:
        result = checkstatement(rule[0],feat_set)
        if result == True:
            for c in classes_reached:
                if c!=rule[1]:
                    err = True
                    break
                classes_reached.append(rule[1])
    if len(classes_reached) == 0:
        classes_reached = ["Undecidable"]
    if not err:
        print("The datapoint belongs to class ",classes_reached[0])
    else:
        print("Conflicting rules! Check the KB!")

def addrule(rule, kb):
    rule = rule.split("=>")
    rule[0] = "["+rule[0]+"]"
    clause = ast.literal_eval(rule[0])
    implication = int(rule[1])
    add = True
    for index in range(len(kb)):
        if kb[index][0] == clause:
            if kb[index][1] != implication:
                print("Attempting to insert a conflicting rule!")
            add = False
    if add:
        kb.append([clause, implication])
    


file = open(filename, 'r')
contents = file.readlines()
file.close()
contents = contents[1:]
for line in contents:
    info = line.split("\t")
    if len(info) > 1:
        sample_features = info[0]
        sample_reason = info[2]
        sample_class = info[3]
        sample_features = ast.literal_eval(sample_features)
        sample_class = int(sample_class)
        features.append(sample_features)
        explanations.append(sample_reason)
        classes.append(sample_class)
        
rules = []
inferences = {}

for e in range(len(explanations)):
    exp = explanations[e]
    if exp not in rules:
        rules.append(exp)
        inferences[exp] = [[classes[e],1]]
    else:
        newclass = True
        for inf in range(len(inferences[exp])):
            if inferences[exp][inf][0] == classes[e]:
                newclass = False
                inferences[exp][inf][1] += 1
                break
        if newclass:
            inferences[exp].append([classes[e],1])

final_rules = []
final_inf = []
for r in range(len(rules)):
    final_rules.append(ast.literal_eval(rules[r]))
    best_pred = inferences[rules[r]][0][0]
    pred_count = inferences[rules[r]][0][1]
    for inf in range(len(inferences[rules[r]])):
        if pred_count < inferences[rules[r]][inf][1]:
            pred_count = inferences[rules[r]][inf][1]
            best_pred = inferences[rules[r]][inf][0]
    final_inf.append(best_pred)


verbose = input(("Rules read from database. View them? (Y/N)"))
if verbose == "Y" or verbose == "y":
    for i in range(len(rules)):
        print(i, rules[i], inferences[rules[i]])
    print("********")
    
print()
KB = []
print("Choosing majority inference to remove noise")
print()
print("Final KB:")
for k in range(len(final_rules)):
    print("Rule",k,":",final_rules[k],"->", final_inf[k])
    KB.append([ast.literal_eval(final_rules[k]),final_inf[k]])

print()
print("#######")
print("""
To query use the following phrases:
Feature 1 is Sepal Length. Use sl in query
Feature 2 is Sepal Width. Use sw in query
Feature 3 is Petal Length. Use pl in query
Feature 4 is Petal Width. Use pw in query

Class 0 : setosa
Class 1 : virginica
Class 2 : versicolour

Example query : what is pw, class is virginica, pl is 1.5

""")
print("#######")
print()
print("""
Select:
1. To ask a query
2. To add a rule
3. To delete a rule
4. To predict the class of a feature set
Anything else to exit
""")
while(True):
    option = int(input("Your choice : "))
    if option == 1:
        question = input("Enter query :")
        query_eval(question, KB)
    elif option == 2:
        user_rule = input("Enter a rule :")
        addrule(user_rule, KB)
        print("Final KB:")
        for k in KB:
            print("Rule:",k[0],"->",k[1])
    elif option == 3:
        print("Current KB")
        ct = 0
        for k in KB:
            ct += 1
            print("Rule No.",ct," :",k[0],"->",k[1])
        choice = int(input("Enter index of the rule you wish to delete:"))
        index = choice-1
        if index in range(0,len(KB)):
            KB.remove(KB[index])
            print("Rule deleted!")
            print("KB is now:")
            ct = 0
            for k in KB:
                ct += 1
                print("Rule No.",ct," :",k[0],"->",k[1])
        else:
            print("Sorry that rule doesn't exist!")
    elif option == 4:
        feat_set =  input("Enter a dictionary of feature values:")
        feat_set = ast.literal_eval(feat_set)
        eval_featset(feat_set, KB)

    else:
        break
    
