import pygame
import random
import time
import math
pygame.init()

W,H = 800,600

WIN = pygame.display.set_mode((W,H))
pygame.display.set_caption("Aim Trainer")

TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT
TARGET_PADDING = 30
BG_COLOR = "black"
LIVES = 3
FONT_LABEL = pygame.font.SysFont("comicsans", 24)
TOP_BAR_H = 50



class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = "red"
    SEC_COLOR = "white"

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True

    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False

        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR,(self.x,self.y),self.size)
        pygame.draw.circle(win, self.SEC_COLOR,(self.x,self.y),self.size *0.8)
        pygame.draw.circle(win, self.COLOR,(self.x,self.y),self.size *0.6)
        pygame.draw.circle(win, self.SEC_COLOR,(self.x,self.y),self.size *0.4)

    def collide(self, x, y):
        dis = math.sqrt((x - self.x)**2 + (y - self.y)**2)
        return dis <= self.size

def draw(win,targets):
    win.fill(BG_COLOR)

    for target in targets:
        target.draw(win)

def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000) / 100)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)

    return f"{minutes:02d}:{seconds:02d}.{milli}"

def draw_top_bar(win, elapsed_time, target_pressed, misses):
    pygame.draw.rect(win, "grey", (0,0, W, TOP_BAR_H))
    time_label = FONT_LABEL.render(f"Time: {format_time(elapsed_time)}", 1,"black")
    win.blit(time_label, (5,5))

    hit_label = FONT_LABEL.render(f"Hits: {target_pressed}", 1,"black")
    win.blit(hit_label, (450,5)) 

    lives_label = FONT_LABEL.render(f"Lives: {LIVES-misses}", 1,"black")
    win.blit(lives_label, (650,5)) 

    speed = round(target_pressed / elapsed_time, 1)
    speed_label = FONT_LABEL.render(f"Speed: {speed} t/s", 1, "black")
    win.blit(speed_label, (200,5)) 

def end_screen(win, elapsed_time, targets_pressed, clicks):
    win.fill(BG_COLOR)
    time_label = FONT_LABEL.render(
        f"Time: {format_time(elapsed_time)}", 1, "white")

    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = FONT_LABEL.render(f"Speed: {speed} t/s", 1, "white")

    hits_label = FONT_LABEL.render(f"Hits: {targets_pressed}", 1, "white")

    accuracy = round(targets_pressed / clicks * 100, 1)
    accuracy_label = FONT_LABEL.render(f"Accuracy: {accuracy}%", 1, "white")

    restart_label = FONT_LABEL.render(f"Press ENTER to restart the game", 1, "white")

    win.blit(time_label, (get_middle(time_label), 100))
    win.blit(speed_label, (get_middle(speed_label), 200))
    win.blit(hits_label, (get_middle(hits_label), 300))
    win.blit(accuracy_label, (get_middle(accuracy_label), 400))
    win.blit(restart_label, (get_middle(restart_label),500))

    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                quit()
            
            if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                     main()


def get_middle(surface):
    return W / 2 - surface.get_width()/2

def main():
    run = True

    targets = [] 
    clock = pygame.time.Clock()

    target_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    pygame.time.set_timer(TARGET_EVENT,TARGET_INCREMENT)


    while run:
        clock.tick(60)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time()-start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
                break

            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING , W-TARGET_PADDING)
                y = random.randint(TARGET_PADDING + TOP_BAR_H , H-TARGET_PADDING)
                new_target=Target(x,y)

                collision = False
                for target in targets:
                    if target.collide(x, y):
                        collision = True
                        break

                if not collision:
                    targets.append(new_target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        for target in targets:
            target.update()

            if target.size <=0:
                targets.remove(target)
                misses += 1

            if click and target.collide(*mouse_pos):
                targets.remove(target)
                target_pressed += 1

            if misses >= LIVES:
                end_screen(WIN, elapsed_time, target_pressed, clicks)

        draw(WIN,targets)
        draw_top_bar(WIN, elapsed_time, target_pressed, misses)
        pygame.display.update()
        
    pygame.quit()
      

if __name__ == "__main__":
    main()