import random
import math
import itertools
from tkinter import font
class Ball:
    """ ボールクラス
    円を描く関数を使って表現する。
    """
    A = True
    def __init__(self, canvas, color, paddle, block, tk):
        """ 初期化処理
        メイン側から Canvas を受け取る。
        ボールの色も str 型で受け取る。
        衝突判定に使うパドルを受け取る。
        """
        self.tk = tk
        self.canvas = canvas
        self.paddle = paddle
        self.block = block 
        # 楕円を描く関数できれいな円を描画する。識別番号を保持しておく。
        self.id = self.canvas.create_oval(10, 10, 25, 25, fill=color, tag="ball")
        # 画面サイズ(縦/横)を取得しておく。
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        # ボールの初期位置を計算で決める。リセット時のことを考えて保存しておく。
        self.init_x = self.canvas_width / 2 - 7.5
        self.init_y = self.canvas_height / 2 - 7.5
        # ボールの移動スピードをとりあえず0で作っておく
        self.speed = 3
        # ボールのx/yのスピードを0でとりあえず初期化
        self.x = 0
        self.y = 0
        self.end = 0
        self.block_list = [[1 for i in range(7)]for i in range(8)]

        
        # ボール始動
        self.start()

    def start(self):
        # 初期位置へ移動(絶対座標)
        self.canvas.moveto(self.id, self.init_x, self.init_y)
        self.speed = 4     # 移動スピードe
        """ 発射角度のリストを生成(angle の処理内容)
            1 - range() で 20 - 60 のデータを作成
            2 - list() でリスト型に変換
            3 - random.choice() でリストから1個をランダムで選択
            4 - math.radians() で度数法から弧度法(ラジアン)に変換
        """
        angle = math.radians(random.choice(list(range(20, 65, 5))))
        direction = random.choice([1, -1])  # xの向きをランダムに。
        # 三角関数をつかって、x軸y軸それぞれの移動速度を求める。
        self.x = math.cos(angle) * self.speed * direction
        self.y = math.sin(angle) * self.speed
    
    def draw(self):
        # ボールを移動させる
        self.canvas.move(self.id, self.x, self.y)

        # 移動したあとの座標(左上xy,右下xy)を取得する
        pos = self.canvas.coords(self.id)

        # 左に当たった(pos[0]が越えた)かどうか
        if pos[0] <= 0:
            self.fix(pos[0] - 0, 0)

        # 上に当たった(pos[1]が越えた)かどうか
        if pos[1] <= 0:
            self.fix(0, pos[1])

        # 右に当たった(pos[2]が越えた)かどうか
        if pos[2] >= self.canvas_width:
            self.fix(pos[2] - self.canvas_width, 0)
            

        # 下に当たった(pos[3]が越えた)かどうか
        if pos[3] >= self.canvas_height:
            self.fix(0, pos[3] - self.canvas_height)
            self.failed()  #プレイヤーのミスを処理する関数を呼ぶ

        # パドルとの衝突判定
        paddle_pos = self.canvas.coords(self.paddle.id)
        # b.x2 >= p.x1
        # b.x1 <= p.x2
        # p.y1 <= b.y2 <= p.y2
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2] \
           and paddle_pos[1] <= pos[3] <= paddle_pos[3]:
            self.fix(0, pos[3] - paddle_pos[1])

        for x in range(8):
            for y in range(7):
                if pos[0] <= (x+1)*62.5 and pos[2] >= x*62.5 and \
                    pos[1] <= (y+1)*31 and pos[3] >= y*31 and \
                    self.block_list[x][y] == 1:
                    if (y+1)*29 <= pos[1] <= (y+1)*31: #下
                        #self.x = -self.x
                        self.canvas.delete("ぶろっく"+str(x)+str(y))
                        self.block_list[x][y] = 0
                        self.y = -self.y
                    #    self.fix(0, pos[1] - (y+1)*31)

                    elif (x+1)*60 <= pos[0] <= (x+1)*63.5: #左
                        self.canvas.delete("ぶろっく"+str(x)+str(y))
                        self.block_list[x][y] = 0
                        self.fix(pos[0] - (x+1)*63.5, 0)

                    elif x*65 >= pos[2] >= x*63.5: #右
                        self.canvas.delete("ぶろっく"+str(x)+str(y))
                        self.block_list[x][y] = 0
                        self.fix(pos[2] - x*63.5, 0)
                    elif  y*31 >= pos[3] >= y*30: #上
                        self.canvas.delete("ぶろっく"+str(x)+str(y))
                        self.block_list[x][y] = 0
                        self.fix(0 , pos[3] - y*30)
        block_list = sum(self.block_list, [])
        if 1 not in block_list:
            self.canvas.move(self.id, -3000, -3000)
            self.canvas.move(self.paddle.id, -3000, -3000)
            for x in range(8):
                for y in range(7):
                    self.canvas.delete("ぶろっく"+str(x)+str(y))
            self.canvas.create_text(250,320, text="GAME CLEAR!", font=("HG丸ｺﾞｼｯｸM-PRO", 50), fill="red")
            self.canvas.create_text(250,365, text="enter to quit", font=("HG丸ｺﾞｼｯｸM-PRO", 20))
            def ss(evt):
                quit(self.tk)
            self.canvas.bind_all("<KeyPress-Return>", ss)
            self.x = 0
            self.y = 0
            self.speed = 0
        
    def fix(self, diff_x, diff_y):
        # x/y の差分を受け取って、2倍した数を逆に移動する。
        self.canvas.move(self.id, -(diff_x * 2), -(diff_y * 2))
        # 差分があったら(0でなければ)跳ね返ったとして向きを反転させる。
        if diff_x != 0:
            self.x = -self.x
            
        if diff_y != 0:
            self.y = -self.y

    def failed(self):
        # 動きを止める
        self.canvas.move(self.id, -3000, -3000)
        self.canvas.move(self.paddle.id, -3000, -3000)
        for x in range(8):
            for y in range(7):
                self.canvas.delete("ぶろっく"+str(x)+str(y))
        self.canvas.create_text(250,320, text="GAME OVER", font=("HG丸ｺﾞｼｯｸM-PRO", 50))
        self.canvas.create_text(250,365, text="enter to quit", font=("HG丸ｺﾞｼｯｸM-PRO", 20))
        def ss(evt):
            quit(self.tk)
        self.canvas.bind_all("<KeyPress-Return>", ss)
        self.x = 0
        self.y = 0
        self.speed = 0
