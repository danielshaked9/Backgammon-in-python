import numpy as np
import pygame
from time import sleep
import test_boards as tb
BLACK,WHITE,BROWNISH,GREENISH=(255,255,255),(0,0,0),(155,120,10),(200, 160, 10)
def divide_up_down(idx):
    return 1 if idx %2 ==0 else 0
def is_point_inside_shape(abc, d):
    a,b,c=abc[0],abc[1],abc[2]
    area = abs(0.5 * (a[0]*(b[1]-c[1]) + b[0]*(c[1]-a[1]) + c[0]*(a[1]-b[1])))
    area1 = abs(0.5 * (d[0]*(b[1]-c[1]) + b[0]*(c[1]-d[1]) + c[0]*(d[1]-b[1])))
    area2 = abs(0.5 * (a[0]*(d[1]-c[1]) + d[0]*(c[1]-a[1]) + c[0]*(a[1]-d[1])))
    area3 = abs(0.5 * (a[0]*(b[1]-d[1]) + b[0]*(d[1]-a[1]) + d[0]*(a[1]-b[1])))
    return area == area1 + area2 + area3
def generate_polygons():
    global size,points
    height=size[1]//3
    width=size[0]//13
    for i in range(0,size[0],width):
        if i!=480:
            triangle_down=[[i,size[1]],[(i+width/2),size[1]-height],[i+width,size[1]]]
            points.append(triangle_down)
            triangle_up=[[i,50],[(i+width/2),height],[i+width,50]]
            points.append(triangle_up)
        else:
            square=[[i,size[1]],[i+width,size[1]],[i+width,50],[i,50]]
            points.append(square)
            points.append(square)
def draw_polygons():
    global size,points,screen
    for i in range(len(points)):
        color = BROWNISH if i<12 or i>13 else GREENISH
        pygame.draw.polygon(screen,color,points[i])
def get_triangle_index(pos):
    global points
    up=[23,22,21,20,19,18,50,17,16,15,14,13,12]
    down=[0,1,2,3,4,5,50,6,7,8,9,10,11]
    for i in range(len(points)):
        if is_point_inside_shape(points[i],pos):
            return down[i//2] if divide_up_down(i) else up[i//2]
    else:
        return 50
def convert_idx_to_pixels(idx):
    screen_offsets=[40,120,200,280,360,440,600,680,760,840,920,1000]
    if idx < 12: pos = screen_offsets[idx]
    elif idx ==50: pos=520
    else: pos = screen_offsets[23-idx]
    return pos
def draw_pile(posx,amount,rad,color,idx,size,screen):
    for i in range(amount):
        if idx<12: pygame.draw.circle(screen,color,(posx,size[1]-rad-i*2*rad),rad)
        else: pygame.draw.circle(screen,color,(posx,50+rad+i*2*rad),rad)
def draw_jail():
    global jail,screen,player
    color=WHITE if player else BLACK 
    rival_color=BLACK if player else WHITE
    rad=30
    for i in range(jail[0]):
        if jail[0]>0: pygame.draw.circle(screen,rival_color,(convert_idx_to_pixels(50),500+i*2*rad),rad)
    for i in range(jail[1]):
        if jail[1]>0: pygame.draw.circle(screen,color,(convert_idx_to_pixels(50),400-rad-i*2*rad),rad)
def draw_board():
    global board,size,screen,jail,player,status,decide_begin,dices
    screen.fill((255, 200, 20))
    pause = pygame.image.load('img/pause.png')
    screen.blit(pause, (10,-10))
    draw_polygons()
    color=BLACK  if player else WHITE
    rival_color=WHITE if player else BLACK 
    for i in range(len(board)):
            draw_pile(convert_idx_to_pixels(i),np.abs(board[i]),30, color if board[i]>0 else rival_color, i,size,screen)
    draw_jail()
    dice_img_list=['dice1.png','dice2.png','dice3.png','dice4.png','dice5.png','dice6.png']
    if decide_begin==0:
        if dices[0]!=-1:
            dice1 = pygame.image.load(dice_img_list[dices[0]-1])
            dice1 = pygame.transform.rotate(dice1, angles[0])
            screen.blit(dice1, (100,300))
        if dices[1]!=-1:
            dice2 = pygame.image.load(dice_img_list[dices[1]-1])
            dice2 = pygame.transform.rotate(dice2, angles[1])
            screen.blit(dice2, (500,300))
        if len(dices)==4:
            if dices[2]!=-1:
                dice1 = pygame.image.load(dice_img_list[dices[2]-1])
                dice1 = pygame.transform.rotate(dice1, angles[0])
                screen.blit(dice1, (100,300))
            if dices[3]!=-1:
                dice2 = pygame.image.load(dice_img_list[dices[3]-1])
                dice2 = pygame.transform.rotate(dice2, angles[1])
                screen.blit(dice2, (500,300))
def roll_dices():
    global status,dices,screen,dice1,dice2,dice_img_list,dices_sound,angles,decide_begin,angles
    pygame.mixer.Sound.play(dices_sound)
    sleep(0.3)
    die1=np.random.randint(1,7)
    die2=np.random.randint(1,7)
    if die1==die2: dices=[die1,die1,die1,die1]
    else: dices=[die1,die2]
    status[3]=len(dices)
    angles=[np.random.randint(1,360),np.random.randint(1,360)]
def draw_dices(dices2draw,angles2draw):
    dice_img_list=['dice1.png','dice2.png','dice3.png','dice4.png','dice5.png','dice6.png']
    val=100
    for i in range(len(dices2draw)):
        dice = pygame.image.load(dice_img_list[dices2draw[i]-1])
        dice = pygame.transform.rotate(dice, angles2draw[i])
        screen.blit(dice, (val,300))
        val+=400
        pygame.display.update()
def check_phase():
    x=sum_board(6,24)
    return 1 if x==0 else 0
def is_in_rival_house():
    global idx
    check=[23,22,21,20,19,18]
    return idx[1] in check
def is_dice_fitj():
    global idx,dices
    check=[23,22,21,20,19,18]
    return check.index(idx[1])+1 in dices
def is_point_blocked():
    global idx,board
    return 1 if board[idx[1]] > -1 else 0 
def is_point_exposed():
    global idx,board
    return 1 if board[idx[1]] == -1 else 0
def negate_board():
    global board
    board=board[::-1]
    for i in range(len(board)):
        board[i]=-board[i]
def is_end_turn():
    global status,board,jail,fetch_idx,out,player,screen,count_sound,no_moves,decide_begin
    draw_board()
    if check_win(): winner()
    if status[0]==status[3] or status[4]:
        if not decide_begin:
            if check_win(): winner()
            display_message('end turn') # turn end
        sleep(1)
        pygame.mixer.Sound.play(count_sound)
        for i in reversed(range(3)):
            display_message(f'flipping board in {i}')
            sleep(1)
        negate_board()
        jail=jail[::-1]
        out=out[::-1]
        player=not player
        fetch_idx=0
        status=[0,0,0,0,0]
        turn='white' if player else 'black'
        roll_dices() #turn begins
    reset_idx()
    if check_win(): winner()
def skip_turn():
    global status
    status[4]=1
    sleep(1)
    pygame.mixer.Sound.play(no_moves)
    display_message('no moves availible')
    sleep(1)
    is_end_turn()
def eat():
    global board,jail,idx,eat_sound
    pygame.mixer.Sound.play(eat_sound)
    jail[1]+=1
    board[idx[1]]=0
    draw_board()
def jail_movement():
    global board,jail,idx,dices,checker_sound
    jail[0]-=1
    board[idx[1]]+=1
    pygame.mixer.Sound.play(checker_sound)
    status[0]+=1
    check=[23,22,21,20,19,18]
    check_idx=check.index(idx[1])
    dice_idx=dices.index(check_idx+1)
    dices[dice_idx]=-1
    draw_board()
    is_end_turn()
def is_all_blocked():
    global idx,board,dices
    check=[23,22,21,20,19,18]
    flag=0
    for i in dices:
        if board[check[i-1]]<-1: flag+=1
        if i==-1: flag+=1
    if len(dices)==2: return 1 if flag==2 else 0
    if len(dices)==4: return 1 if flag==4 else 0
def is_specific_blocked():
    global idx,board,dices
    check=[23,22,21,20,19,18]
    flag=0
    for i in dices:
        if i!=-1:
            board[check[i-1]]<-1
            return 1
        else: return 0
def jail_move():
    if is_all_blocked(): skip_turn()
    #elif is_specific_blocked(): 
        #skip_turn()
    else:
        if idx[0]==50:
            if is_in_rival_house():
                if is_dice_fitj():
                    if is_point_blocked(): jail_movement()
                    else: 
                        if is_point_exposed():
                            pygame.mixer.Sound.play(checker_sound)
                            eat()
                            jail_movement()
                        else: reset_idx()
                else: reset_idx()
            else: reset_idx()
        else: reset_idx()
def sum_board(a,b):
    global board
    x=0
    for i in range(a,b):
        if board[i]>0: x+=board[i]
    return x
def is_can_move_out():
    for i in dices:
        if idx[0]+1==i: return 1
        if idx[0]+1 <=i and sum_board(idx[0]+1,6)==0: return 1
    return 0
def move_out():
    global board,idx,out
    out[0]+=1
    board[idx[0]]-=1
    dice_idx=0
    for i in range(len(dices)):
        if idx[0]+1==dices[i]:
            dice_idx=i
            break
    if not dice_idx:
        for i in range(len(dices)):
            if idx[0]+1<dices[i]:
                dice_idx=i
                break
    dices[dice_idx]=-1
    status[0]+=1
def check_win():
    global out
    return sum_board(0,24)==0
def winner():
    global running,win_sound
    turn='white' if player else 'black'
    display_message(f'{turn} wins the game')
    pygame.mixer.Sound.play(win_sound)
    sleep(3)
    if sum_board(0,17)<0:
        if jail[1]>0:
            score_board[not player]+=3 #star mars
        else:
            score_board[not player]+=2 #turkish mars
    else:
        score_board[not player]+=1 
    running=False
def phase_move():
    if check_win(): 
        winner()
        return
    if idx[0]<6:
        if is_point_valid():
            if is_can_move_out():
                move_out()
                if check_win(): 
                    winner()
                    return
                else: is_end_turn()
            else: move()
        else: reset_idx()
    else: reset_idx()
def is_point_valid():
    global board,idx
    if idx[0]==50 and jail[0]==0:
        return 0
    return board[idx[0]]>0 and idx[0]!=50 and idx[0]-idx[1] >= 0
def is_dice_fit():
    global dices,idx
    return np.abs(idx[0]-idx[1]) in dices
def movement():
    global board,jail,idx,dices,checker_sound
    pygame.mixer.Sound.play(checker_sound)
    board[idx[0]]-=1
    board[idx[1]]+=1
    status[0]+=1
    dice_idx=dices.index(np.abs(idx[0]-idx[1]))
    dices[dice_idx]=-1
    draw_board()
    pygame.display.flip()
    is_end_turn()
def move():
    global status,dices,board,jail,out,fetch_idx,idx
    if is_point_valid():
        if is_dice_fit():
            if is_point_exposed():
                eat()
                movement()
            else:
                if is_point_blocked():
                    movement()
                    draw_board()
                else:
                    reset_idx()
        else: reset_idx()
    else: reset_idx()
def check_status():
    global status,board,jail
    status[1]= 1 if jail[0] > 0 else 0
    status[2] = 1 if check_phase() else 0
def reset_idx():
    global idx
    idx=[]
def decoder():
    global status,dices,board,jail,out,fetch_idx,idx
    if check_win(): 
        winner()
        return
    if status[1]: jail_move()
    elif status[2]: phase_move()
    else: move()
def get_move_from_player():
    #client side input
    global fetch_idx,idx,status
    if status[1] and is_all_blocked(): skip_turn()
    fetch_idx=1 if len(idx)<2 else 0
    if len(idx)==2: decoder()
def decide_first():
    global dices,decide_begin,player,board,jail,angles
    players_dices=[]
    players_angles=[]
    turn='white' if player else 'black'
    display_message(f'{turn} player, press to roll a dice')
    while decide_begin:
        if decide_begin==0:
            break
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if check_pause(pos):
                    menu(1)
                roll_dices()
                players_dices.append(dices[0])
                players_angles.append(angles[0])
                player= not player
                turn='white' if player else 'black'
                display_message(f'{turn} player, press to roll a dice')
                draw_dices(players_dices,players_angles)
                if len(players_dices)==2:
                    if players_dices[0]>players_dices[1]: 
                        player = 1
                        decide_begin = 0
                        dices=players_dices
                        angles=players_angles
                    elif players_dices[0]<players_dices[1]: 
                        player = 0
                        decide_begin = 0
                        dices=players_dices
                        angles=players_angles
                    else:
                        players_dices=[]
                        player=not player
    turn='white' if player else 'black'
    display_message(f'{turn} player is doing the first turn')
    sleep(2)
def text_objects(text, font):
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()
def display_message(text):
    global size,screen
    draw_board()
    largeText = pygame.font.Font("freesansbold.ttf",30)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((size[0]/2),(25))
    screen.blit(TextSurf, TextRect)
    pygame.display.flip()
def check_pause(pos):
    if is_point_inside_shape([[0,0],[0,45],[100,45],[100,0]],pos):
        return 1
def reset_game():
    global status,dices,board,jail,out,decide_begin
    status,dices,board,jail,out,decide_begin=[0,0,0,0,0],[],tb.initial_board,[0,0],[0,0],0
def menu(where_flag):
    global size,running,score_board,decide_begin,status,dices,board,jail,out
    flag=True
    restart_game=0
    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                flag = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()        
                if is_point_inside_shape([[400,100],[400,300],[620,300],[600,100]],pos) and where_flag !=2: #play
                    flag=False
                    return
                if is_point_inside_shape([[400,100],[400,300],[620,300],[600,100]],pos) and where_flag ==2: #restart
                    flag=False
                    running=True
                    return
                if is_point_inside_shape([[430,800],[430,960],[670,960],[630,800]],pos): #quit
                    pygame.quit()
        if restart_game:
            restart_game=0
            break
        screen.fill((255, 200, 20))
        play = pygame.image.load('img/play.png')
        restart = pygame.image.load('img/restart.png')
        quit = pygame.image.load('img/quit.png')
        screen.blit(play, (400,100)) if where_flag ==0 or where_flag ==1 else screen.blit(restart, (400,100))
        screen.blit(quit, (400,800))
        largeText = pygame.font.Font("freesansbold.ttf",30)
        text=f'White: {score_board[0]}   Black: {score_board[1]}'
        TextSurf, TextRect = text_objects(text, largeText)
        TextRect.center = ((size[0]/2),(25))
        screen.blit(TextSurf, TextRect)
        pygame.display.update()
def game_loop():
    global running
    roll_dices()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:        
                pos = pygame.mouse.get_pos()
                if check_pause(pos):
                    menu(1)
                if fetch_idx:
                    idx.append(get_triangle_index(pos))
        turn='white' if player else 'black'
        check_status()
        display_message(f'{turn} player turn')
        if check_win():
            winner()
            return
        get_move_from_player()
        pygame.display.flip()
def main():
    global player,score_board
    global size,UP,DOWN,screen,points,status,dices,board,jail,out,fetch_idx,idx,running,player,dices_sound,checker_sound,count_sound,no_moves,decide_begin,font,win_sound,eat_sound
    size,UP,DOWN,decide_begin,points,status,dices,board,jail,out,fetch_idx,idx,running,score_board,player=(1040,1040),1,0,1,[],[0,0,0,0,0],[],tb.initial_board,[0,0],[0,0],0,[],True,[0,0],1
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Backgammon")
    pygame.font.init()
    font = pygame.font.Font(None, 30)
    pygame.mixer.init()
    dices_sound = pygame.mixer.Sound('sound/dices.wav')
    checker_sound = pygame.mixer.Sound('sound/checker.wav')
    count_sound =  pygame.mixer.Sound('sound/count.wav')
    no_moves = pygame.mixer.Sound('sound/no_moves.wav')
    win_sound = pygame.mixer.Sound('sound/win.wav')
    eat_sound = pygame.mixer.Sound('sound/eat.wav')
    generate_polygons()
    menu(0)
    decide_first()
    while True:
        game_loop()
        menu(2)
        reset_game()
if __name__ == '__main__':
    main()

