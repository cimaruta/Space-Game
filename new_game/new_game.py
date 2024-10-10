import sys

import pygame

class Player:
    """Player object and movement"""
    def __init__(self, maingame):
        self.screen_rect = maingame.screen_rect
        self.events = maingame._check_events()
        self.ship_image = pygame.image.load('nonsense/new_game/images/ship5.bmp')
        self.ship_image = pygame.transform.scale(self.ship_image, (75,75))
        self.ship_rect = self.ship_image.get_rect()
        self.ship_rect.midbottom = self.screen_rect.midbottom
        self.ship_speed = 10

        self.move_right = False
        self.move_left = False

    def movement(self):         
        if self.move_right and self.ship_rect.right < self.screen_rect.right:
            self.ship_rect.x += self.ship_speed
        if self.move_left and self.ship_rect.left > 0:
            self.ship_rect.x -= self.ship_speed

class Enemy:
    def __init__(self, maingame):
        """A class for enemy objects and behavior"""
        self.screen = maingame.screen
        self.screen_rect = maingame.screen_rect
        self.enemy_list = []
        self.enemy_image = pygame.image.load('nonsense/new_game/images/minion.bmp')
        self.enemy_image = pygame.transform.scale(self.enemy_image, (75,75))
        self.enemy_rect = self.enemy_image.get_rect()
        self.enemy_rect.left = self.screen_rect.left
        self.enemy_move_right = False
        self.enemy_move_left = False

    def movement(self):
        """Enemy movement stuff"""
        if self.enemy_rect.left <= self.screen_rect.left:
            self.enemy_move_right = True
            self.enemy_move_left = False

        if self.enemy_rect.right >= self.screen_rect.right:
            self.enemy_move_right = False
            self.enemy_move_left = True



        if self.enemy_move_right:
            self.enemy_rect.x += 3

        if self.enemy_move_left:
            self.enemy_rect.x -= 3


class NewGame:
    """The main game class"""
    def __init__(self):
        pygame.init()
        self.bullet_list = []
        self.screen = pygame.display.set_mode((800,800))
        self.screen_rect = self.screen.get_rect()
        self.background_image = pygame.image.load('nonsense/new_game/images/sky1.bmp')
        self.enemy = Enemy(self)
        self.player = Player(self)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("I dont know")

        
    def run_game(self):
        while True:
            self._screen()
            self._check_events()
            self.enemy.movement()
            self._bullet_movement()
            self.player.movement()
            pygame.display.flip()
            self.clock.tick(60)


    def _screen(self):
        self.screen.fill((0,100,0))
        self.screen.blit(self.background_image, self.screen_rect)
        self.screen.blit(self.player.ship_image, self.player.ship_rect)
        self.screen.blit(self.enemy.enemy_image, self.enemy.enemy_rect)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.player.move_right = True
                if event.key == pygame.K_LEFT:
                    self.player.move_left = True
                if event.key == pygame.K_SPACE:
                    bullet = pygame.Rect(0,0, 5, 10)
                    bullet.center = self.player.ship_rect.center
                    self.bullet_list.append(bullet)
                    

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.player.move_right = False
                if event.key == pygame.K_LEFT:
                    self.player.move_left = False

    def on_collision(self, bullet):
        # Check horizontal overlap
        horizontal_overlap = (bullet.left < self.enemy.enemy_rect.right and
                            bullet.right > self.enemy.enemy_rect.left)

        # Check vertical overlap
        vertical_overlap = (bullet.top < self.enemy.enemy_rect.bottom and
                            bullet.bottom > self.enemy.enemy_rect.top)

        # A collision occurs if both overlaps are true
        collision = horizontal_overlap and vertical_overlap
        return collision
    
    def _bullet_movement(self):

        for bullet in self.bullet_list[:]:
            pygame.draw.rect(self.screen, (255,0,0), bullet)
            bullet.y -= 10

            #print(collision)
            if bullet.y <= self.screen_rect.y:
                self.bullet_list.remove(bullet)

            elif self.on_collision(bullet):
                self.bullet_list.remove(bullet)
            #print(self.bullet_list)

if __name__ == '__main__':
    ng = NewGame()
    ng.run_game()