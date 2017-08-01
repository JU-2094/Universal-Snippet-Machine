from learntools.Filter import FeatureFilter
from learntools.BasicTool import Utils

query = "select name,title,description from unoporuno_busqueda as ub," \
        "unoporuno_snippet as us, unoporuno_persona as up " \
        "where ub.id=119 and ub.id=up.busqueda_id and up.id=us.persona_id;"

res = Utils.exec_query(Utils(), query)

positive = 0
negative = 0
true_positive = 0
true_negative = 0
false_positive = 0
false_negative = 0

total = res.__len__()

for row in res:
    name = row[0].split('(')
    filter = FeatureFilter(name[0])
    if "pos" in name[1]:
        positive = positive + 1
    else:
        negative = negative + 1

    snippet = row[1] + " " + row[2]

    has_variation = filter.has_nominal(snippet)

    if ("pos" in name[1]) and has_variation:
        true_positive = true_positive + 1
    elif ("pos" in name[1]) and not has_variation:
        false_negative = false_negative + 1
    elif ("neg" in name[1]) and has_variation:
        false_positive = false_positive + 1
        print("name, ", name[0])
        print(snippet)
        print("\n")
    elif ("neg" in name[1]) and not has_variation:
        true_negative = true_negative + 1


precision = true_positive / (true_positive + false_positive)
recall = true_positive / (true_positive + false_negative)
f_measure = (2 * precision * recall) / (precision + recall)


print("positives ", positive)
print("negatives ", negative)
print("true_positive ", true_positive)
print("true_negative ", true_negative)
print("false_positive ", false_positive)
print("false_negative ", false_negative)
print("--------")
print("sum of all ", true_positive+true_negative+false_positive+false_negative)
print("--------")
print("Precision ", precision)
print("Recall ", recall)
print("F-measure ", f_measure)
