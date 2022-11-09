from ticker_rules import rules



usdt = []

for i in rules:
    if i.endswith("USDT"):
        usdt.append(i)


list1 = []
list2 = []
list3 = []
list4 = []
other = []
for i in usdt: 
    if len(list1) <= 100:
        list1.append(i)
    elif len(list2) <= 100:
        list2.append(i)
    elif len(list3) <= 100:
        list3.append(i)
    elif len(list4) <= 100:
        list4.append(i)
    else:
        other.append(i)



# print(len(list1))
# print('------------------------------')
# print(len(list2))
# print('------------------------------')
# print(len(list3))
# print('------------------------------')
# print(len(list4))
# print('------------------------------')
# print(len(other))
