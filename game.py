import pygame ,random


pygame.init()

DIS_WIDTH = 1200
DIS_HEIGHT = 700

screen = pygame.display.set_mode((DIS_WIDTH,DIS_HEIGHT))
pygame.display.set_caption("Space Invaders")

FPS = 60
clock =pygame.time.Clock()

#classes
class Game():
    """A Class to help control and update gameplay"""
    def __init__(self,player,alien_grp,player_bullet_grp,alien_bullet_group):
        self.round_number = 1
        self.score = 0
        self.player = player
        self.alien_group = alien_grp
        self.player_bullet_group = player_bullet_grp
        self.alien_bullet_group = alien_bullet_group

        self.new_round_snd = pygame.mixer.Sound("assets/new_round.wav")
        self.breach_snd = pygame.mixer.Sound("assets/breach.wav")
        self.alien_hit_snd = pygame.mixer.Sound("assets/alien_hit.wav")
        self.player_hit_snd = pygame.mixer.Sound("assets/player_hit.wav")

        self.font = pygame.font.Font("assets/Facon.ttf",32)
    def update(self):
        self.Shift_Aliens()
        self.check_collisions()
        self.check_round_completion()
    def draw(self):
        WHITE = (255,255,255)
        score_txt = self.font.render("Score: " + str(self.score),True,WHITE)
        score_rect = score_txt.get_rect()
        score_rect.centerx = DIS_WIDTH//2
        score_rect.top = 10
        round_txt = self.font.render("Round: " + str(self.round_number),True,WHITE)
        round_rect = round_txt.get_rect(topleft = (20,10))
        lives_txt = self.font.render("Lives: " + str(self.player.lives),True,WHITE)
        lives_rect = lives_txt.get_rect(topright = (DIS_WIDTH-20,10))

        screen.blit(score_txt,score_rect)
        screen.blit(round_txt,round_rect)
        screen.blit(lives_txt,lives_rect)

        pygame.draw.line(screen,WHITE,(0,50),(DIS_WIDTH,50),4)
        pygame.draw.line(screen,WHITE,(0,DIS_HEIGHT-100),(DIS_WIDTH,DIS_HEIGHT-100))

    def Shift_Aliens(self):
        shift = False
        for alien in (self.alien_group.sprites()):
            if alien.rect.left <=0 or alien.rect.right>=DIS_WIDTH:
                shift = True
        
        if shift:
            breach = False
            for alien in (self.alien_group.sprites()):
                alien.rect.y += 10*self.round_number
                alien.direction *= -1
                alien.rect.x += alien.direction*alien.velocity

                if alien.rect.bottom>= DIS_HEIGHT-100:
                    breach = True
            if breach: 
                self.breach_snd.play()
                self.player.lives -= 1
                self.check_game_status("Aliens breached the line!" , "Press 'Enter' to continue")
    def check_collisions(self):
        if pygame.sprite.groupcollide(self.player_bullet_group,self.alien_group,True,True):
            self.alien_hit_snd.play()
            self.score += 100
        if pygame.sprite.spritecollide(self.player,self.alien_bullet_group,True):
            self.player_hit_snd.play()
            self.player.lives -= 1
            self.check_game_status("Yo've been hit!","Press 'Enter' to continue") 
    def statrt_new_round(self):
        
        #creating grid of aliens
        for i in range(11):
            for j in range(5):
                alien = Alien(64*i + 64 , 64 + 64*j,self.round_number*1,self.alien_bullet_group)
                self.alien_group.add(alien)

        #pause and ask to start
        self.new_round_snd.play()
        self.pause_game("Space Invadors Round " + str(self.round_number) , "Press 'Enter' to begin")
    def check_round_completion(self):
        if not (self.alien_group):
            self.round_number += 1
            self.score += 1000*self.round_number
            self.statrt_new_round()
    def check_game_status(self,main_txt,sub_txt):
        self.alien_bullet_group.empty()
        self.player_bullet_group.empty()
        self.player.reset()
        for alien in self.alien_group:
            alien.reset()
        if self.player.lives == 0:
            self.reset_game()
        else:
           self.pause_game(main_txt,sub_txt) 
    def pause_game(self,main_txt,sub_txt):
        global running
        WHITE = (255,255,255)
        BLACK = (0,0,0)

        main_txt = self.font.render(main_txt,True,WHITE)
        main_rect = main_txt.get_rect(center = (DIS_WIDTH//2,DIS_HEIGHT//2))

        sub_txt = self.font.render(sub_txt,True,WHITE)
        sub_rect = sub_txt.get_rect(center = (DIS_WIDTH//2,DIS_HEIGHT//2+64))

        screen.fill(BLACK)
        screen.blit(main_txt,main_rect)
        screen.blit(sub_txt,sub_rect)

        pygame.display.update()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_paused = False
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False
        
    def reset_game(self):
        self.pause_game("Final Score: " + str(self.score) , "Press 'Enter' to play again")

        self.score = 0
        self.round_number = 1
        self.player.lives = 5
        self.alien_bullet_group.empty()
        self.player_bullet_group.empty()
        self.alien_group.empty()
        self.statrt_new_round()
class Player(pygame.sprite.Sprite):
    """A class to model a spaceship"""
    def __init__(self, player_bullet_group):
        pygame.sprite.Sprite.__init__(self )
        self.image = pygame.image.load("assets/player_ship.png")
        self.rect = self.image.get_rect(centerx = DIS_WIDTH//2)
        self.rect.bottom = DIS_HEIGHT

        self.lives = 5
        self.velocity = 8

        self.bullet_group = player_bullet_group

        self.shoot_snd = pygame.mixer.Sound("assets/player_fire.wav") 
    def update(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] and self.rect.left>0) or (keys[pygame.K_a] and self.rect.left>0):
            self.rect.x -= self.velocity
        if (keys[pygame.K_RIGHT] and self.rect.right<DIS_WIDTH) or (keys[pygame.K_d] and self.rect.right<DIS_WIDTH):
            self.rect.x += self.velocity
    def fire(self):
        if len(self.bullet_group)<2:
            self.shoot_snd.play()
            PlayerBullet(self.rect.centerx,self.rect.top,self.bullet_group)
    def reset(self):
        self.rect.centerx = DIS_WIDTH//2

class Alien(pygame.sprite.Sprite):
    """A class to model an enemy Alien"""
    def __init__(self , x , y,veloctiy,bullet_group):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/alien.png")
        self.rect = self.image.get_rect(topleft = (x,y))

        self.startingx = x
        self.startingy = y

        self.direction = 1
        self.velocity = veloctiy
        self.bullet_group = bullet_group

        self.shoot_snd = pygame.mixer.Sound("assets/alien_fire.wav")         
    def update(self):
        self.rect.x +=  self.direction*self.velocity

        if random.randint(0,1000)>999 and len(self.bullet_group)<3:
            self.shoot_snd.play()
            self.fire()

    def fire(self):
        AlienBullet(self.rect.centerx,self.rect.bottom,self.bullet_group)

    def reset(self):
        self.rect.topleft = (self.startingx,self.startingy)
        self.direction = 1

class PlayerBullet(pygame.sprite.Sprite):
    """A class to model bullet fired by player"""
    def __init__(self,x,y,bullet_group):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/green_laser.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.velocity = 10
        bullet_group.add(self)
    def update(self):
        self.rect.y -= self.velocity
        
        #killing bullet
        if self.rect.bottom<0:
            self.kill()

class AlienBullet(pygame.sprite.Sprite):
    """A class to model bullet fired by enemy"""
    def __init__(self,x,y,bullet_group):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/red_laser.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.velocity = 10
        bullet_group.add(self)
    def update(self):
        self.rect.y += self.velocity

        if self.rect.top >DIS_HEIGHT:
            self.kill()


my_player_bullet_group = pygame.sprite.Group()
my_alien_bullet_group = pygame.sprite.Group()
my_player_group = pygame.sprite.Group()
my_player = Player(my_player_bullet_group)
my_player_group.add(my_player)
my_alien_group = pygame.sprite.Group()

my_game = Game(my_player,my_alien_group,my_player_bullet_group,my_alien_bullet_group)
my_game.statrt_new_round() 


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_player.fire()
    
    screen.fill((0,0,0))

    my_player_group.update()
    my_player_group.draw(screen)
    my_alien_group.update()
    my_alien_group.draw(screen)
    my_alien_bullet_group.update()
    my_alien_bullet_group.draw(screen)
    my_player_bullet_group.update()
    my_player_bullet_group.draw(screen)
    my_game.update()
    my_game.draw()


    pygame.display.update()
    clock.tick(FPS)

pygame.quit()