# coding UTF-8
import numpy as np
import random
from flask import Flask, render_template

app = Flask(__name__)


class Maze(object):
    # 穴掘り法で迷路を作成する
    def __init__(self, size, start_pos, goal_pos):
        # maze[y][x]で表現
        self.maze = np.ones(size)
        self.H = self.maze.shape[0]
        self.W = self.maze.shape[1]
        self.start_pos = start_pos
        self.goal_pos = goal_pos

    def disp(self):
        w, h = self.maze.shape
        for y in range(h):
            print(self.maze[y])

    def sel_start_point(self):
        s_x = random.randint(0, (self.W-3)/2)*2 + 1
        s_y = random.randint(0, (self.H-3)/2)*2 + 1

        return s_x, s_y

    def sel_direction(self):
        # 0 北 1 東 2 南 3  西
        return random.randint(0, 3)

    def check_2cell(self, s_x, s_y, direction):
        ret = True
        if direction == 0:
            #北方向2マス先
            x = s_x
            y = s_y - 2
        elif direction == 1:
            # 東の2マス先
            x = s_x + 2
            y = s_y
        elif direction == 2:
            # 南
            x = s_x
            y = s_y + 2
        else:
            #西
            x = s_x - 2
            y = s_y
        if x <= 0 or x >= self.W:
            ret = False
        elif y <= 0 or y >= self.H:
            ret = False
        elif self.maze[y][x] == 0:
            ret = False

        return ret

    def fin_check(self):
        # もう掘るところがないかチェック
        for y in range(1, self.H, 2):
            for x in range(1, self.W, 2):
                for d in range(0, 4, 1):
                    if self.check_2cell(x, y, d):
                        return True, (x, y, d)

        return False, (-1, -1, -1)

    def digging(self, s_x, s_y, direction):
        last_x = s_x
        last_y = s_y
        if direction == 0:
            #北方向2マス先
            d_x = s_x
            d_y = s_y
            s_y = s_y - 2
            last_x = s_x
            last_y = s_y

        elif direction == 1:
            # 東の2マス先
            d_x = s_x + 2
            d_y = s_y
            last_x = d_x
            last_y = s_y

        elif direction == 2:
            # 南
            d_x = s_x
            d_y = s_y + 2
            last_x = s_x
            last_y = d_y

        else:
            #西
            d_x = s_x
            s_x = s_x - 2
            d_y = s_y
            last_x = s_x
            last_y = s_y

        for y in range(s_y, d_y+1, 1):
            for x in range(s_x, d_x+1, 1):
                self.maze[y][x] = 0

        return last_x, last_y

    def can_direct_list(self, x, y):
        can_direct = []
        for i in range(4):
            if self.check_2cell(x, y, i):
                can_direct.append(i)
        return can_direct

    def create_goal(self):
        s_x = self.start_pos[0]
        s_y = self.start_pos[1]
        g_x = self.goal_pos[0]
        g_y = self.goal_pos[1]
        point_list = []
        while True:
            can_direct = self.can_direct_list(s_x, s_y)
            if len(can_direct) > 0:
                r = random.randint(0, len(can_direct)-1)
                direction = can_direct[r]
                point_list.append([s_x, s_y])
                s_x, s_y = self.digging(s_x, s_y, direction)
                if s_x == g_x and s_y == g_y:
                    break
            else:
                pos = point_list.pop()
                s_x = pos[0]
                s_y = pos[1]

        for i in range(len(point_list)):
            r = random.randint(0, len(point_list) - 1)
            pos = point_list.pop(r)
            s_x = pos[0]
            s_y = pos[1]

            while True:
                can_direct = self.can_direct_list(s_x, s_y)
                if len(can_direct) > 0:
                    r = random.randint(0, len(can_direct) - 1)
                    direction = can_direct[r]
                    point_list.append([s_x, s_y])
                    s_x, s_y = self.digging(s_x, s_y, direction)
                else:
                    break

    def get_list(self):
        return self.maze.tolist()

@app.route("/")
def maze():
    maze = Maze((33, 33), (1, 31), (7, 7))
#    maze.create_maze((1, 15), (7, 7))
    maze.create_goal()
    maze_data = maze.get_list()
    maze_data[7][7] = 2
    maze_data[31][1] = 3
    print(maze_data)

    payload = {"data":maze_data}
    return render_template("index.html", maze_data=maze_data)


if __name__ == "__main__":
    # webサーバー立ち上げ
    app.run(debug=True)


