class Paddle:
    """ プレイヤー(パドル)のクラス
    基本的には形作って移動させるだけ。
    """
    
    def __init__(self, canvas, color):
        """ 初期化処理。
        Canvas と色を受け取って矩形(長方形)を描く
        移動できるのは横方向のみ。
        """
        self.canvas = canvas
        # 矩形を描画して管理番号を保存しておく
        self.id = self.canvas.create_rectangle(0, 0, 100, 10, fill=color)
        # Canvas の幅をとっておく。
        self.canvas_width = self.canvas.winfo_width()
        # 移動速度をとりあえず0で初期化。
        self.x = 0
        # 初期位置へ移動。(絶対座標)
        self.canvas.moveto(self.id, self.canvas_width / 2 - 50, 650)

    def draw(self):
        """ 必要に応じて移動処理とか。
        移動後は画面外に出ていかないよう調整する。
        """
        # 現在のx軸方向の速度分移動する。
        self.canvas.move(self.id, self.x, 0)
        # 移動後の座標(左上xy/右下xy)をとる
        pos = self.canvas.coords(self.id)

        # 左に当たった(pos[0]が越えた)かどうか
        if pos[0] <= 0:
            self.x = 0
            self.canvas.move(self.id, -pos[0], 0)

        # 右に当たった(pos[2]が越えた)かどうか
        if pos[2] >= self.canvas_width:
            self.x = 0
            self.canvas.move(self.id, -(pos[2] - self.canvas_width), 0)

    def turn_left(self, evt):
        """ 左キーのイベントハンドラ
        x軸の移動速度をマイナスで設定する。
        """
        self.x = -3

    def turn_right(self, evt):
        """ 右キーのイベントハンドラ
        x軸の移動速度をプラスで設定する。
        """
        self.x = 3
