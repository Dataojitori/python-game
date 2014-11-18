
import simplegui
import random

def new_game():
    global guess, turn, state, backup
    guess = [ [str(i),1] for i in range(8)+range(8) ]
    random.shuffle(guess)
    turn, state = 0,0
    backup = []
    label.set_text("Turns = "+str(turn))

def mouseclick(pos):
    global state, turn, backup
    n = pos[0]/50
    if guess[n][1] :
        guess[n][1] = 0
        if state == 0 :
            for num in backup :
                num[1] = 1
            backup = [guess[n]]    
            state = 1
            
        elif state == 1 :                    
            backup.append(guess[n])
            if backup[0][0] == backup[1][0] :
                backup = []
            turn += 1
            label.set_text("Turns = "+str(turn))
            state = 0    

def draw(canvas):    
    for i in range(len(guess)) :
        x = i * 50 
        canvas.draw_text(guess[i][0], (x+5, 75), 70, 'white')        
        canvas.draw_polygon([(x,0), (x+50,0), (x+50, 100),
                             (x, 100)], 1 , 'Blue', 
                            'rgba(200,200,0,%d)'%guess[i][1])

frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)


new_game()
frame.start()

