from tkinter import Tk, Frame, Canvas

from objects import Paddle, Ball, Brick


class Game(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.lives = 3
        self.width = 600
        self.height = 400
        self.canvas = Canvas(self, width=self.width, height=self.height, bg='#aaaaff')
        self.canvas.pack()
        self.pack()

        self.add_objects()

        self.hud = None
        self.setup_game()
        self.canvas.focus_set()
        self.canvas.bind('<Left>', lambda _: self.paddle.move(-10))
        self.canvas.bind('<Right>', lambda _: self.paddle.move(10))

    def add_objects(self):
        self.ball = None
        self.items = {}
        self.add_paddle()
        self.add_ball()
        for x in range(5, self.width - 5, 75):
            self.add_brick(x + 37.5, 50, 2)
            self.add_brick(x + 37.5, 70, 2)
            self.add_brick(x + 37.5, 90, 2)

    def add_paddle(self):
        self.paddle = Paddle(self.canvas, self.width / 2, 326)
        self.items[self.paddle.item] = self.paddle

    def add_ball(self):
        if self.ball is not None:
            self.ball.delete()
        paddle_coords = self.paddle.get_position()
        x = (paddle_coords[0] + paddle_coords[2]) * 0.5
        self.ball = Ball(self.canvas, x, 310)

    def add_brick(self, x, y, hits):
        brick = Brick(self.canvas, x, y, hits)
        self.items[brick.item] = brick

    def setup_game(self):
        self.update_lives_text()
        self.text = self.draw_text(300, 200, 'Press Space to start')
        self.canvas.bind('<space>', lambda _: self.start_game())

    def draw_text(self, x, y, text, size='40'):
        font = ('Helvetica', size)
        return self.canvas.create_text(x, y, text=text, font=font)

    def update_lives_text(self):
        text = f'Lives: {self.lives}'
        if self.hud is None:
            self.hud = self.draw_text(50, 20, text, '15')
        else:
            self.canvas.itemconfig(self.hud, text=text)

    def start_game(self):
        self.canvas.unbind('<space>')
        self.canvas.delete(self.text)
        self.paddle.ball = None
        self.game_loop()

    def game_loop(self):
        self.check_collisions()
        num_bricks = len(self.canvas.find_withtag('brick'))
        if num_bricks == 0:
            self.ball.speed = 0
            self.draw_text(300, 200, 'You win')
        elif self.ball.get_position()[3] >= self.height:
            self.ball.speed = None
            self.lives -= 1
            if self.lives < 0:
                self.draw_text(300, 200, 'You lose')
            else:
                self.after(1999, self.setup_game)
        else:
            self.ball.update()
            self.after(50, self.game_loop)

    def check_collisions(self):
        ball_coords = self.ball.get_position()
        items = self.canvas.find_overlapping(*ball_coords)
        objects = [self.items[x] for x in items if x in self.items]
        self. ball.collide(objects)


if __name__ == '__main__':
    root = Tk()
    root.title('Breakout Game!')
    game = Game(root)
    game.mainloop()
