# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
ball_pos = [WIDTH/2,HEIGHT/2]
ball_v= [0,0]
BALL_RADIUS = 20

PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
left_pad = [HALF_PAD_WIDTH, HEIGHT/2]
right_pad = [WIDTH - HALF_PAD_WIDTH , HEIGHT/2]
left_pad_v = [0,0]
right_pad_v = [0,0]

scores = [0,0]
direction = random.choice([1,-1])

def spawn_ball():
    global ball_pos, ball_v, direction 
    def faqiu():
        global ball_v
        ball_v= [random.randrange(2,4)*direction, random.randrange(1, 3)*random.choice([1,-1])]  
        timer.stop()
    ball_pos = [WIDTH/2,HEIGHT/2]    
    ball_v= [0,0]
    timer = simplegui.create_timer(1000, faqiu)    
    timer.start()
    
def new_game(): 
    global scores,direction
    direction = random.choice([1,-1])
    scores = [0,0]
    spawn_ball()

def draw(canvas):
    global score1, score2, direction,ball_v     
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_v[0]
    ball_pos[1] += ball_v[1]
    if ball_pos[0] < PAD_WIDTH + BALL_RADIUS :
        if left_pad[1] - HALF_PAD_HEIGHT < ball_pos[1] < left_pad[1] + HALF_PAD_HEIGHT:
            ball_v = [(0.01*v**2 + abs(v)+0.5)*v/abs(v) for v in ball_v]
            ball_v[0] *= -1            
        else :
            scores [1] += 1
            direction = 1
            spawn_ball()  
    if ball_pos[0] > WIDTH - PAD_WIDTH -1 -BALL_RADIUS:
        if right_pad[1] - HALF_PAD_HEIGHT < ball_pos[1] < right_pad[1] + HALF_PAD_HEIGHT:
            ball_v = [(0.01*v**2 + abs(v)+0.5)*v/abs(v) for v in ball_v]
            ball_v[0] *= -1            
        else :
            scores [0] += 1
            direction = -1
            spawn_ball()
    
    if not BALL_RADIUS < ball_pos[1] < HEIGHT-BALL_RADIUS :
        ball_v[1] *= -1
    
    # update paddle's vertical position, keep paddle on the screen
    left_pad[1] += left_pad_v[0] + left_pad_v[1]
    right_pad[1] += right_pad_v[0] + right_pad_v[1]
    if left_pad[1] > HEIGHT - HALF_PAD_HEIGHT :
        left_pad[1] = HEIGHT - HALF_PAD_HEIGHT 
    if left_pad[1] < HALF_PAD_HEIGHT :
        left_pad[1] = HALF_PAD_HEIGHT 
    if right_pad[1] > HEIGHT - HALF_PAD_HEIGHT :
        right_pad[1] = HEIGHT - HALF_PAD_HEIGHT 
    if right_pad[1] < HALF_PAD_HEIGHT :
        right_pad[1] = HALF_PAD_HEIGHT 
        
    # draw paddles
    canvas.draw_line([left_pad[0], left_pad[1]-HALF_PAD_HEIGHT], [left_pad[0], left_pad[1]+HALF_PAD_HEIGHT], PAD_WIDTH, 'white')
    canvas.draw_line([right_pad[0], right_pad[1]-HALF_PAD_HEIGHT], [right_pad[0], right_pad[1]+HALF_PAD_HEIGHT], PAD_WIDTH, 'white')
    
    # draw scores
    canvas.draw_text(str(scores[0]), [135,180], 100,'white')
    canvas.draw_text(str(scores[1]), [425,180], 100,'white')
    
    # draw ball
    ball_color = 'rgb' + str((255,int(max(255-(ball_v[0]**2 + ball_v[1]**2)**0.5*10, 0)),0))
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, 'White', ball_color)
        
def keydown(key):
    # I make pad_v have two element so you can push up
    # and down at same time
    if key == simplegui.KEY_MAP['w'] :
        left_pad_v[0] = -6
    if key == simplegui.KEY_MAP['s'] :
        left_pad_v[1] = 6
    if key == simplegui.KEY_MAP['up'] :
        right_pad_v[0] = -6
    if key == simplegui.KEY_MAP['down'] :
        right_pad_v[1] = 6
   
def keyup(key):
    global left_pad_v, right_pad_v
    if key == simplegui.KEY_MAP['w'] :
        left_pad_v[0] = 0
    if key == simplegui.KEY_MAP['s'] :
        left_pad_v[1] = 0
    if key == simplegui.KEY_MAP['up'] :
        right_pad_v[0] = 0
    if key == simplegui.KEY_MAP['down'] :
        right_pad_v[1] = 0



frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
Restart = frame.add_button('Restart', new_game,100)


print 'left right hand war began'
spawn_ball()
frame.start()
