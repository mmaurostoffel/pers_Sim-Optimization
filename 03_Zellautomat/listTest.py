list = []
item1 = {}
item1['name'] = "isi"
item1['age'] = 25

item2 = {}
item2['name'] = "lucy"
item2['age'] = 22

item3 = {}
item3['name'] = "laura"
item3['age'] = 20

list.append(item1)
list.append(item2)
list.append(item3)

print(list)

removeList = []
for item in list:
    if item['name'] == "isi":
        removeList.append(item)

print(removeList)
for item in removeList:
    list.remove(item)

print(list)