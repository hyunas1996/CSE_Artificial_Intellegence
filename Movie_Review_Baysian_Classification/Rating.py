valid_traied = open('ratings_result_valid.txt', 'r', encoding="UTF-8")
valid_origin = open('ratings_valid.txt', 'r', encoding="UTF-8")

count = 0
length = 0
trained = []
origin = []

for line_t in valid_traied:
    tmp = list(line_t.split())[-1]
    trained.append(tmp)
    length += 1

for line_o in valid_origin:
    tmp = list(line_o.split())[-1]
    origin.append(tmp)

for i in range(length):
    if trained[i] == origin[i]:
        count += 1

print('accuracy : ' + str((count/length) *100))
