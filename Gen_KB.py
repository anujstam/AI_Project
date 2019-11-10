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

def query_to_feats(sentence):
    sentence = sentence.lower()
    question_words = ["does", "what", "can"]
    query_features = {1:-1,2:-1,3:-1,4:-1}
    target = -1
    values = []
    for c in range(len(class_names)):
        if class_names[c] in sentence:
            target = c
    for t in sentence.split():
        if len(t) > 1:
            if t[0] == ',':
                t = t[1:]
            if t[len(t)-1] == ',':
                t = t[:len(t)-1]
        try:
            values.append(float(t))
        except ValueError:
            pass
    fpositions = []
    for f in feature_names:
        loc = sentence.find(f)
        if loc == -1:
            pass
        else:
            fpositions.append([feature_names.index(f)+1,loc])
    fpositions.sort(key = lambda x: x[1]) 
    for k in range(len(values)):
        query_features[fpositions[k][0]] = values[k]
    return (query_features, target)


s1 = "Petal length is 0.4, Sepal Width is -0.5. Does the flower belong to the class Virginica?"
print(query_to_feats(s1))
s2 = "When Sepal Length is less 0.5, what should be Petal Length so that, the flower belongs to the class Setosa?"
print(query_to_feats(s2))
    
    


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
  

print()
print("Rules generated:")
for i in range(len(rules)):
    print(i, rules[i], inferences[rules[i]])

KB = []
print("Choosing majority inference to remove noise")
print()
print("Final KB:")
for k in range(len(final_rules)):
    print("Rule",k,":",final_rules[k],"->", final_inf[k])
    KB.append([ast.literal_eval(final_rules[k]),final_inf[k]])

print()
print("#######")
print()
print("""
Select:
1. To ask a query
2. To add a rule
3. To delete a rule
Anything else to exit
""")
while(True):
    option = int(input("Your choice : "))
    if option == 1:
        question = input("Enter query :")

    elif option == 2:
        #TODO
        print("kek")
    elif option == 3:
        #TODO
        print("kek")
    else:
        break
    

"""
testfeat = input("Enter a feature set:")
testfeat = ast.literal_eval(testfeat)
# testfeat = {1:-0.4,2:0.4,3:0.9,4:0.1}

for rule in KB:
    #print("Checking rule:", rule)
    result = checkstatement(rule[0], testfeat)
    if  result == True:
        print(rule[0], "is true")
        print("Class inferred ->",rule[1])
    elif result  == False:
        print(rule[0], "is false")
    elif result == "Undecidable":
        print(rule[0], "is undecidable")
"""
