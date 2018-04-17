import curses #绘制棋盘
from random import randrange, choice
from collections import defaultdict

actions = ['Up', 'Left', 'Down', 'Right', 'Restart', 'Exit']
letter_codes = [ord(c) for c in 'WASDREwasdrex']
actions_dict = dict(zip(letter_codes, actions*2))


def get_user_action(keyboard):
    #getch();接受一个任意键的输入，不用按回车就返回。该函数的返回值是所输入字符的ASCII码，
    #且该函数的输入不会自动显示在屏幕上，需要putchar();函数输出显示。getch()
    char = 'N'
    while char not in actions_dict:
        char = keyboard.getch()
    return actions_dict[char]


def transpose(field):
    return [list(row) for row in zip(*field)]   #zip(*) 二维数组逆操作变换

def invert(field):
    return [row[::-1] for row in field] #顺序相反操作

class Gamefield(object):
    
    def __init__(self, height = 4, width = 4, win = 2048):
        self.height = height
        self.width = width
        self.win_value = win   #过关分数
        self.score = 0          #当前分数
        self.highscore = 0      #最高分
        self.reset()            #重置棋盘
                  
    
    def reset(self):
        #重置棋盘
        if self.score > self.highscore:
            self.highscore = self.score
        self.score = 0
        self.field = [[0 for i in range(self.height)] for j in range(self.width)]
        self.spawn()
        self.spawn()
        
              
    def spawn(self):
        #随机生成一个2或者4
        new_element = 4 if randrange(100)>89 else 2
        (i,j) = choice([(i,j) for i in range(self.height) for j in range(self.width) if self.field[i][j]==0])
        self.field[i][j] = new_element

    
    def move(self,direction):
        #移动
        def move_row_left(row):
            def tighten(row): #把零散的非零单元挤到一起
                new_row = [i for i in row if i != 0]  #去除0
                new_row += [0 for i in range(len(row)-len(new_row))]
                return new_row
            
            def merge(row): #对临近元素进行合并
                new_row = []
                pair = False
                for i in range(len(row)):
                    if pair:
                        new_row.append(row[i]*2)
                        self.score += row[i]*2
                        pair = False
                    else:
                        if i+1<len(row) and row[i]==row[i+1]:
                            new_row.append(0)
                            pair = True
                        else:
                            new_row.append(row[i])
                
                assert len(new_row)==len(row)     
                return new_row
            #先挤到一块再合并再挤到一块
            return tighten(merge(tighten(row)))
            
        
        moves = {}
        moves['Left'] = lambda field : [move_row_left(row) for row in field]
        moves['Right'] = lambda field : invert(moves['Left'](invert(field)))
        moves['Up'] = lambda field : transpose(moves['Left'](transpose(field)))
        moves['Down'] = lambda field : transpose(moves['Right'](transpose(field)))
        
        if direction in moves:
            if self.move_is_possible(direction):
                self.field = moves[direction](self.field)
                self.spawn()
                return True
            else:
                return False
        
    
    def is_win(self):
        return any(any(i >self.win_value for i in row) for row in self.field)
    
    def is_gameover(self):
        return not any(self.move_is_possible(move) for move in actions)
    
    def move_is_possible(self,direction):
        def left_is_moveable(row):
            def change(i):
                if row[i] == 0 and row[i+1] !=0:    #可以移动
                    return True
                if row[i] != 0 and row[i] == row[i+1]:  #可以合并
                    return True
                return False
            return any(change(i) for i in range(len(row)-1))

        check = {}
        check['Left'] = lambda field : any(left_is_moveable(row) for row in field)
        check['Right'] = lambda field : check['Left'](invert(field))
        check['Up'] = lambda field : check['Left'](transpose(field))
        check['Down'] = lambda field : check['Right'](transpose(field))

        if direction in check:
            return check[direction](self.field)
        else:
            return False
    
    def draw(self,screen):
        help_string1 = '(W)Up (S)Down (A)Left (D)Right'
        help_string2 = '     (R)Restart (E)Exit'
        gameover_string = '           GAME OVER'
        win_string = '          YOU WIN!'
        def cast(string):
            screen.addstr(string+'\n')

        #绘制水平分割线
        def draw_hor_separator():
            line = '+-------'*self.width + '+'
            cast(line)

        def draw_row():
            cast(''.join('|'+str(num).center(7) if num>0 else '|       ' for num in row) + '|')

        screen.clear()
        cast('SCORE: '+str(self.score))
        if self.highscore != 0:
            cast('HIGHSCORE: '+ str(self.highscore))

        for row in self.field:
            draw_hor_separator()
            draw_row()
        draw_hor_separator()

        if self.is_win():
            cast(win_string)
        else:
            if self.is_gameover():
                cast(gameover_string)
            else:
                cast(help_string1)
        cast(help_string2)


def main(stdscr):
    
    #four states
    
    def init():
        #重置棋盘
        game_field.reset()
        return 'Game'
    
    def not_game(state): #win or over
        #画出 GameOver 或者 Win 的界面
        game_field.draw(stdscr)
        #读取用户输入得到action，判断是重启游戏还是结束游戏
        action = get_user_action(stdscr)
        responses = defaultdict(lambda:state) #默认是当前状态
        responses['Exit'] = 'Exit'
        responses['Restart'] = 'Init'
        return responses[action]
            
    
    def game():
        #画出棋盘状态
        game_field.draw(stdscr)
        #读取用户输入得到action
        action = get_user_action(stdscr)
        if action == 'Restart':
            return 'Init'
        if action =='Exit':
            return 'Exit'
        
        if game_field.move(action):     #成功移步
            if game_field.is_win():
                return 'Win'
            if game_field.is_gameover():
                return 'Gameover'
        return 'Game' 
    
    
    state_actions = {
            'Init':init,
            'Win': lambda : not_game('Win'),
            'Gameover': lambda : not_game('Gameover'),
            'Game': game}
    
    curses.use_default_colors()
    game_field = Gamefield(win = 2048)
    
    state = 'Init'
    #状态机开始循环
    while state != 'Exit':
        state = state_actions[state]()  #调用函数

curses.wrapper(main)