import random

def openFile(filename):
    frozen_lake = []

    tmp_lake = list(open(filename, 'r', encoding="UTF-8"))

    lakeInfo = tmp_lake[0].rstrip('\n')
    tmp_lake.pop(0)

    for line in tmp_lake:
        frozen_lake.append(line.rstrip('\n'))

    return frozen_lake, lakeInfo

#FrozenLake 1,2,3 에 대한 정보 : version
#state 개수가 몇 개인지 : 가로 * 세로 = state_num
#FrozenLake의 가로, 세로를 유지하며 0으로 초기화된 2차원 배열
def initQtable(lakeInfo):
    Info = lakeInfo.split();
    version = int(Info[0])
    height = int(Info[1])
    width = int(Info[2])
    state_num = int(Info[1]) * int(Info[2])

    Qtable = [[0 for col in range(4)] for row in range(state_num)]

    return version, state_num, Qtable, height, width

def Qlearning(Qtable, frozen_lake, height, width):
    num_trial = 30000
    max_step = 99
    discount = 0.5

    for trial in range(num_trial):
        step = 0
        done = False
        total_reward = 0

        state = findStart(frozen_lake, height, width)

        for step in range(max_step):
            #print(state)
            reward = 0

            #tradeOff = random.uniform(0,1)
            #if tradeOff > epsilon:

            lrud = Qtable[state]

            tmp_direction_index = [0,1,2,3]
            #벽으로 가는 경우 제거
            if state % width == 0:
                tmp_direction_index.remove(0)
            if state % width == width-1:
                tmp_direction_index.remove(1)
            if state // width == 0:
                tmp_direction_index.remove(2)
            if state // width == height-1:
                tmp_direction_index.remove(3)

            tmp_max = max(lrud)
            possible_direction_index = tmp_direction_index
            #max 방향만 남기기
            for possible_direction in tmp_direction_index:
                if lrud[possible_direction] != tmp_max:
                    possible_direction_index.remove(possible_direction)

            action = random.choice(possible_direction_index)

            if action == 0:
                new_state = state - 1
            elif action == 1:
                new_state = state + 1
            elif action == 2:
                new_state = state - width
            elif action == 3:
                new_state = state + width

            #new state의 frozen lake에서의 좌표 구하기
            new_state_width = new_state % width
            new_state_height = new_state // width

            #구덩이에 빠진 경우, reward -1, 해당 step 종료
            if frozen_lake[new_state_height][new_state_width] == 'H':
                reward = -1
                done = True

            #목적지에 도착한 경우, reward +1, 해당 step 종료
            if frozen_lake[new_state_height][new_state_width] == 'G':
                reward = 1
                done = True

            if frozen_lake[new_state_height][new_state_width] == 'F' or frozen_lake[new_state_height][new_state_width] == 'S':
                reward = 0
                done = False


            Qtable[state][action] = reward + discount * max(Qtable[new_state])

            total_reward = total_reward + reward

            state = new_state

            if done == True:
                break;


    return Qtable

def findStart(frozen_lake, height, width):
    for i in range(height):
        for j in range(width):
            if frozen_lake[i][j] == 'S':
                return i*width + j

def findGoal(frozen_lake, height, width):
    for i in range(height):
        for j in range(width):
            if frozen_lake[i][j] == 'G':
                return i*width + j

def findPath(result_Qtable, frozen_lake, height, width):
    path = []

    position = findStart(frozen_lake, height, width)
    goal = findGoal(frozen_lake, height, width)

    path.append(position)

    while True:
        new_position_direction = result_Qtable[position].index(max(result_Qtable[position]))

        if new_position_direction == 0:
            position = position - 1
        elif new_position_direction == 1:
            position = position + 1
        elif new_position_direction == 2:
            position = position - width
        elif new_position_direction == 3:
            position = position + width

        if position == goal:
            path.append(position)
            break

        path.append(position)

    return path

def makeResultFrozenLake(frozen_lake, path, height, width):
    lake_list = []
    path.pop(0)
    path.pop(len(path)-1)

    for i in range(height):
        for j in range(width):
            if i*width + j not in path:
                lake_list.append(frozen_lake[i][j])
            elif i*width+j in path:
                lake_list.append('R')

    result_frozen_lake = []

    while len(lake_list) != 0:
        tmp = lake_list[:width]
        result_frozen_lake.append(tmp)
        lake_list = lake_list[width:]

    return result_frozen_lake

def makeResultFile(result_frozen_lake, lakeInfo, height, width):
    Info = list(lakeInfo.split())
    version = Info[0]

    res_file_name = "FrozenLake_" + version + "_output.txt"
    result_file = open(res_file_name, 'w', encoding="UTF-8")

    result_file.write(lakeInfo)
    result_file.write('\n')

    for i in range(height):
        for j in range(width):
            result_file.write(result_frozen_lake[i][j])
        result_file.write('\n')


if __name__ == '__main__':
    frozen_lake, lakeInfo = openFile('FrozenLake_3.txt')
    version, state_num, Qtable, height, width = initQtable(lakeInfo)
    result_Qtable = Qlearning(Qtable, frozen_lake, height, width)

    path = findPath(result_Qtable, frozen_lake, height, width)
    result_frozen_lake = makeResultFrozenLake(frozen_lake, path, height, width)

    makeResultFile(result_frozen_lake, lakeInfo, height, width)

