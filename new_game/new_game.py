import sys

import pygame




class Animation():
    def __init__(self, duration):
        self.index = 0
        self.duration = duration
        self.counter = 0


    def update(self, frames):
        self.frames = frames
        self.counter += 1
        if self.counter >= self.duration:
            self.counter = 0
            self.index = (self.index + 1) % len(self.frames)

        current_frame = self.frames[self.index]

        return current_frame




class Player:
    """Player object and movement"""
    def __init__(self, maingame):
        self.maingame = maingame
        self.screen = maingame.screen
        self.screen_rect = maingame.screen_rect
        self.events = maingame._check_events()
        self.ship_image = pygame.image.load('C:/Users/Aaron/source/repos/Space-Game/new_game/images/ship1.bmp')
        self.ship_image = pygame.transform.scale(self.ship_image, (64,64))
        self.ship_rect = self.ship_image.get_rect()
        self.ship_rect.midbottom = self.screen_rect.midbottom
        self.ship_rect.y -= 10
        self.ship_speed = 10
        self.ship_health = 3

        self.moving_right = False
        self.move_left = False

    def movement(self):         
        if self.moving_right and self.ship_rect.right < self.screen_rect.right:
            self.ship_rect.x += self.ship_speed
        if self.move_left and self.ship_rect.left > 0:
            self.ship_rect.x -= self.ship_speed

    def show_health(self):
        health_one = pygame.image.load('new_game/images/health1.bmp')
        health_two = pygame.image.load('new_game/images/health2.bmp')
        health_three = pygame.image.load('new_game/images/health3.bmp')
        position = (10,760)
        health = self.ship_health
        if health == 3:
            self.screen.blit(health_three, position)
        elif health == 2:
            self.screen.blit(health_two, position)
        elif health == 1:
            self.screen.blit(health_one, position)


class Enemy:
    def __init__(self, maingame):
        """A class for enemy objects and behavior"""
        self.animation = Animation(30)
        self.screen = maingame.screen
        self.screen_rect = maingame.screen_rect
        self.enemy_image = pygame.image.load('C:/Users/Aaron/source/repos/Space-Game/new_game/images/alien_ship1.bmp')
        self.enemy_frame1 = pygame.image.load('new_game/images/alien_ship1.bmp')
        self.enemy_frame2 = pygame.image.load('new_game/images/alien_ship_frame2.bmp')
        self.enemy_frame3 = pygame.image.load('new_game/images/alien_ship_frame3.bmp')
        self.enemy_frames = [self.enemy_frame1, self.enemy_frame2, self.enemy_frame3]
        self.enemy_rect = self.enemy_image.get_rect()
        self.enemy_list_left = []
        self.enemy_list_right = []
        self.enemy_bullet_list = []
        self.left_enemy_dead = 0
        self.right_enemy_dead = 0
        self.enemy_wave = 1
        self.enemy_wave_max = 1
        

    def is_list_empty(self, list):
        if len(list) <= 0:
            return True

        return False

    def make_enemy(self, direction, moving_right, list):
        enemy_health = 3
        spacing = 100
        new_enemy = self.enemy_image.get_rect()

        #right side enemies
        if moving_right:
            new_enemy.x = direction + (len(list) * spacing)
            start_y = self.screen_rect.y + 75
        else:
        #left side enemies
            new_enemy.x = direction - (len(list) * spacing)
            start_y = self.screen_rect.y

        new_enemy.y = start_y
        enemy_data = {
            'rect': new_enemy,
            'moving_right': moving_right,
            'spawned': False,
            'speed': 3,
            'health': enemy_health,
        } 
        return enemy_data
           
    def spawn_enemy_left(self):
        left = self.screen_rect.left
        list = self.enemy_list_left
        enemy_animate = self.animation.update(self.enemy_frames)
        while len(self.enemy_list_left) <= 5 and self.left_enemy_dead == 0:
            self.enemy_list_left.append(self.make_enemy(left, False, list))

        for enemy_data in self.enemy_list_left:
            self.screen.blit(enemy_animate, enemy_data['rect'])
        
    
    def spawn_enemy_right(self):
        right = self.screen_rect.right - 75
        list = self.enemy_list_right
        enemy_animate = self.animation.update(self.enemy_frames)
        while len(self.enemy_list_right) <= 5 and self.right_enemy_dead == 0:
            self.enemy_list_right.append(self.make_enemy(right, True, list))
            
        for enemy_data in self.enemy_list_right:
            self.screen.blit(enemy_animate, enemy_data['rect'])
    
    def movement(self, list):
        """Enemy movement stuff"""
        for enemy_data in list:
            enemy = enemy_data['rect']
            if enemy.left <= self.screen_rect.left:
                enemy_data['moving_right'] = True
            elif enemy.right >= self.screen_rect.right:
                enemy_data['moving_right'] = False

        for enemy_data in list:
            if enemy_data['moving_right']:
                enemy_data['rect'].x += enemy_data['speed']
            else:
                enemy_data['rect'].x -= enemy_data['speed']

    def check_spawned(self, left_list, right_list):
        for enemy_data in left_list:
            enemy = enemy_data['rect']
            if enemy.right >= self.screen_rect.right:
                enemy_data['spawned'] = True

        for enemy_data in right_list:
            enemy = enemy_data['rect']
            if enemy.left <= self.screen_rect.left:
                enemy_data['spawned'] = True



    def move_down(self, list):
        for enemy_data in list:
            enemy = enemy_data['rect']
            if enemy_data['spawned']:
                if enemy.left <= self.screen_rect.left:
                    enemy_data['rect'].y += 75
                elif enemy.right >= self.screen_rect.right:
                    enemy_data['rect'].y += 75


    def respawn_enemy(self, list, side, enemy_projectiles):
        if len(list) == 0 and self.enemy_wave <= self.enemy_wave_max:
            if side == 'left':
                self.left_enemy_dead = 0
            elif side == 'right':
                self.right_enemy_dead = 0
            self.enemy_wave += 1
            enemy_projectiles.laser_blast['times_shot'] = 0
            print(f'WAVE {self.enemy_wave}')

    def kill_enemy(self, list, side):
        for enemy_data in list:
            if enemy_data['health'] == 0:
                if side == 'left':
                    self.left_enemy_dead += 1
                elif side == 'right':
                    self.right_enemy_dead += 1
                list.remove(enemy_data)

class Boss:
    def __init__(self, maingame):
        self.animation = Animation(5)
        self.screen = maingame.screen
        self.screen_rect = maingame.screen_rect
        self.boss_image = pygame.image.load('new_game/images/boss1.bmp')
        self.boss_bullet_image = pygame.image.load('new_game/images/boss_bullet1.bmp')
        self.tractor_beam_one = pygame.image.load('new_game/images/boss_laser_charge1.bmp')
        self.tractor_beam_two = pygame.image.load('new_game/images/boss_laser_charge2.bmp')
        self.tractor_beam_three = pygame.image.load('new_game/images/boss_laser_charge3.bmp')
        self.tractor_beam_frames = [self.tractor_beam_one, self.tractor_beam_two, self.tractor_beam_three]
        self.boss_laser_ring = pygame.image.load('new_game/images/boss_laser_ring.bmp')
        self.boss = {
            'rect': self.boss_image.get_rect(),
            'health': 30,
            'spawned': False,
            'phase_one': False,
            'phase_two': False,
            'phase_three': False,
            'port_one': [],
            'port_four': [],
            'basic_fired': 0
        }
        self.boss_timer = 0

    def three_second_timer(self):
        three_seconds = 160
        self.boss_timer += 1
        if self.boss_timer >= three_seconds:
            self.boss_timer = 0

    def spawn_boss(self, enemy):
        enemy_wave = enemy.enemy_wave
        enemy_wave_max = enemy.enemy_wave_max
        enemies_dead = len(enemy.enemy_list_left) == 0 and len(enemy.enemy_list_right) == 0 and enemy_wave >= enemy_wave_max
        if enemies_dead:
            self.boss['spawned'] = True

        wait_phase = self.boss['spawned'] and not self.boss['phase_one'] and not self.boss['phase_two'] and not self.boss['phase_three']

        if wait_phase:
            self.three_second_timer()
            self.boss['rect'].midtop = self.screen_rect.midtop
            self.screen.blit(self.boss_image, self.boss['rect'])

    def phase_one(self, ship):
        wait = 120
        if self.boss['spawned'] and self.boss_timer >= wait:
            self.boss['phase_one'] = True
        if self.boss['phase_one']:
            self.boss['rect'].centerx = ship.ship_rect.centerx
            self.screen.blit(self.boss_image, self.boss['rect'])

    def make_bullet(self, port, direction):
        if len(port) <= 2 and self.boss['phase_one']:
            bullet_rect = self.boss_bullet_image.get_rect()
            bullet_rect.center = self.boss['rect'].midbottom
            if direction == 'left':
                bullet_rect.x -= 95
            elif direction == 'right':
                bullet_rect.x += 95
            port.append(bullet_rect)


    def basic_attack(self, ship, port):
        ship_rect = ship.ship_rect
        for ammo in port[:]:
            self.screen.blit(self.boss_bullet_image, ammo)
            ammo.y += 15
            if ship_rect.x > ammo.x:
                ammo.x += 3
            elif ship_rect.x < ammo.x:
                ammo.x -= 3

            horizontal_overlap = (ammo.left < ship_rect.right and
                            ammo.right > ship_rect.left)

            vertical_overlap = (ammo.bottom > ship_rect.top and
                                ammo.top < ship_rect.bottom)

            collision = horizontal_overlap and vertical_overlap
            if collision:
                ship.ship_health = 0
                port.remove(ammo)

            elif ammo.bottom >= self.screen_rect.bottom:
                port.remove(ammo)
                self.boss['basic_fired'] += 1

    def tractor_beam(self):
        if self.boss['phase_one']:
            animation = self.animation.update(self.tractor_beam_frames)
            laser_rect = self.tractor_beam_one.get_rect()
            laser_rect.midtop = self.boss['rect'].midbottom
            laser_rect.y -= 15
            self.screen.blit(animation, laser_rect)
            ring_rect = self.boss_laser_ring.get_rect()
            ring_rect.midtop = laser_rect.midbottom
            self.screen.blit(self.boss_laser_ring, ring_rect)
            ring_rect.y += 15




class EnemyProjectiles(Enemy):
    def __init__(self, maingame):
        super().__init__(maingame)
        self.enemy_bullet = pygame.image.load('C:/Users/Aaron/source/repos/Space-Game/new_game/images/enemy_bullet1.bmp')
        self.enemy_bullet = pygame.transform.scale(self.enemy_bullet, (20,20))
        self.laser_one_image = pygame.image.load('new_game/images/laser_beam2.bmp')
        self.laser_two_image = pygame.image.load('new_game/images/laser_beam1.bmp')
        self.laser_blast = {
            'phase_one': False,
            'phase_two': False,
            'times_shot': 0,
            'phase_one_rect': self.laser_one_image.get_rect(),
            'phase_two_rect': self.laser_two_image.get_rect()
        }
        self.phase_timer = 0

    def make_projectile(self, list, ship_rect):
        for enemy_data in list:
            enemy = enemy_data['rect']
            if enemy.x == ship_rect.x:
                bullet = self.enemy_bullet
                bullet_rect = bullet.get_rect()
                bullet_rect.center = enemy.center
                self.enemy_bullet_list.append(bullet_rect)

    def shoot(self):
        for bullet in self.enemy_bullet_list[:]:
            self.screen.blit(self.enemy_bullet, bullet)
            bullet.y += 12
            if bullet.bottom >= self.screen_rect.bottom:
                self.enemy_bullet_list.remove(bullet)

    def on_collision(self, bullet, ship):
        ship_rect = ship.ship_rect
        horizontal_overlap = (bullet.left < ship_rect.right and
                            bullet.right > ship_rect.left)

        vertical_overlap = (bullet.bottom > ship_rect.top and
                            bullet.top < ship_rect.bottom)

        collision = horizontal_overlap and vertical_overlap
        if collision:
            return True
        else:
            return False

    def hit_ship(self, ship):
        for bullet in self.enemy_bullet_list:
            collision = False
            collision = self.on_collision(bullet, ship)
            if collision:
                self.enemy_bullet_list.remove(bullet)
                ship.ship_health -= 1

    def check_laser_phase(self, list):
        times_shot = self.laser_blast['times_shot']
        #phase one
        if len(list) <= 3 and self.phase_timer <= 120 and times_shot == 0:
            self.laser_blast['phase_one'] = True
            self.laser_blast['phase_two'] = False
        #phase two
        elif self.laser_blast['phase_one'] and self.phase_timer >= 120:
            self.laser_blast['phase_one'] = False
            self.laser_blast['phase_two'] = True
        #end phase
        if self.phase_timer >= 180:
            self.laser_blast['phase_one'] = False
            self.laser_blast['phase_two'] = False
            self.laser_blast['times_shot'] += 1
            self.phase_timer = 0
        

    def shoot_laser(self, list, ship):
        phase_one = self.laser_blast['phase_one']
        phase_two = self.laser_blast['phase_two']
        self.check_laser_phase(list)
        if phase_one and not phase_two:
            phase_one_rect = self.laser_blast['phase_one_rect']
            if self.phase_timer < 100:
                phase_one_rect.midbottom = ship.ship_rect.midbottom
            else:
                phase_one_rect.midbottom = phase_one_rect.midbottom
            self.screen.blit(self.laser_one_image, phase_one_rect)
            self.phase_timer += 1
        elif phase_two and not phase_one:
            phase_two_rect = self.laser_blast['phase_two_rect']
            phase_two_rect.midbottom = self.laser_blast['phase_one_rect'].midbottom
            self.screen.blit(self.laser_two_image, phase_two_rect)
            self.phase_timer += 1
            ship_rect = ship.ship_rect
            laser_rect = phase_two_rect
            left_overlap = (ship_rect.left < laser_rect.right and ship_rect.right > laser_rect.left)

            right_overlap = (ship_rect.right > ship_rect.left and ship_rect.left < laser_rect.right)

            vertical_overlap = (ship_rect.top < laser_rect.bottom and
                            ship_rect.bottom > laser_rect.top)

            phase_three = self.phase_timer >= 120 and self.phase_timer <= 180
            collision = (right_overlap and left_overlap) and vertical_overlap and phase_three
            if collision:
                ship.ship_health = 0

class Projectiles:
    def __init__(self, maingame, enemy):
        self.bullet_list = []
        self.bullet_frames = [
            pygame.image.load('new_game/images/player_bullet1.bmp'),
            pygame.image.load('new_game/images/player_bullet2.bmp')
        ]
        self.animation_fps = 35
        self.animation = Animation(self.animation_fps)
        self.bullet_image = maingame.player_bullet
        self.screen = maingame.screen
        self.screen_rect = maingame.screen_rect
        self.enemy = enemy

    def make_projectile(self):

        for bullet in self.bullet_list[:]:
            animation = self.animation.update(self.bullet_frames)
            self.screen.blit(animation, bullet)
            bullet.y -= 10

    def on_collision(self, bullet, list):
        for enemy_data in list:
            enemy = enemy_data['rect']
            horizontal_overlap = (bullet.left < enemy.right and
                                bullet.right > enemy.left)

            vertical_overlap = (bullet.top < enemy.bottom and
                                bullet.bottom > enemy.top)

            collision = horizontal_overlap and vertical_overlap
            if collision:
                enemy_data['health'] -= 1
                
                return True

        return False

    def remove_bullet(self):
        for bullet in self.bullet_list[:]:
            if bullet.y <= self.screen_rect.y:
                self.bullet_list.remove(bullet)

            elif self.on_collision(bullet, self.enemy.enemy_list_left) or self.on_collision(bullet, self.enemy.enemy_list_right):
                self.bullet_list.remove(bullet)

class GameOver:
    def __init__(self, maingame, ship):
        pygame.init()
        self.maingame = maingame
        self.screen = maingame.screen
        self.screen_rect = maingame.screen_rect
        self.bg_color = (0,0,0)
        self.font = pygame.font.SysFont("Corbel", 48)
        self.ship = ship

    def game_over(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            game_over_message = pygame.image.load('new_game/images/space_bg_gameover.bmp')
            self.screen.fill(self.bg_color)
            self.screen.blit(game_over_message, self.screen_rect)
            pygame.display.flip()

    def check_game_over(self, list):
        if self.ship.ship_health <= 0:
            self.game_over()
        for enemy_data in list:
            enemy = enemy_data['rect']
            if enemy.bottom > self.ship.ship_rect.top:
                self.game_over()



class NewGame:
    """The main game class"""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800,800))
        self.player_bullet = pygame.image.load('new_game/images/player_bullet1.bmp')
        self.player_bullet_rect = self.player_bullet.get_rect()
        self.background_image = pygame.image.load('new_game/images/space_bg.bmp')
        self.screen_rect = self.screen.get_rect()
        self.player = Player(self)
        self.enemy = Enemy(self)
        self.boss = Boss(self)
        self.enemy_projectile = EnemyProjectiles(self)
        self.projectiles = Projectiles(self, self.enemy)
        self.game_over = GameOver(self, self.player)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("I dont know")

    

    def run_game(self):
        while True:
            self._screen()
            self._check_events()
            self.player.movement()
            self.player.show_health()
            self.projectiles.make_projectile()
            self.projectiles.remove_bullet()
            self.enemy.spawn_enemy_left()
            self.enemy.spawn_enemy_right()
            self.enemy.movement(self.enemy.enemy_list_left)
            self.enemy.movement(self.enemy.enemy_list_right)
            self.enemy.check_spawned(self.enemy.enemy_list_left, self.enemy.enemy_list_right)
            self.enemy.move_down(self.enemy.enemy_list_left)
            self.enemy.move_down(self.enemy.enemy_list_right)
            self.enemy.kill_enemy(self.enemy.enemy_list_left, 'left')
            self.enemy.kill_enemy(self.enemy.enemy_list_right, 'right')
            self.enemy.respawn_enemy(self.enemy.enemy_list_left, 'left', self.enemy_projectile)
            self.enemy.respawn_enemy(self.enemy.enemy_list_right, 'right', self.enemy_projectile)
            self.enemy_projectile.make_projectile(self.enemy.enemy_list_left, self.player.ship_rect)
            self.enemy_projectile.make_projectile(self.enemy.enemy_list_right, self.player.ship_rect )
            self.enemy_projectile.shoot()
            self.enemy_projectile.hit_ship(self.player)
            self.enemy_projectile.shoot_laser(self.enemy.enemy_list_right, self.player)
            self.boss.spawn_boss(self.enemy)
            self.boss.phase_one(self.player)
            self.boss.make_bullet(self.boss.boss['port_one'], 'left')
            self.boss.make_bullet(self.boss.boss['port_four'], 'right')
            self.boss.basic_attack(self.player, self.boss.boss['port_one'])
            self.boss.basic_attack(self.player, self.boss.boss['port_four'])
            self.boss.tractor_beam()
            self.game_over.check_game_over(self.enemy.enemy_list_left)
            self.game_over.check_game_over(self.enemy.enemy_list_right)
            print(self.boss.boss['basic_fired'])
            pygame.display.flip()
            self.clock.tick(60)

    def _screen(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.background_image, self.screen_rect)
        self.screen.blit(self.player.ship_image, self.player.ship_rect)
        
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.player.moving_right = True
                if event.key == pygame.K_LEFT:
                    self.player.move_left = True
                if event.key == pygame.K_SPACE:
                    bullet = self.player_bullet
                    bullet_rect = bullet.get_rect()
                    bullet_rect.center = self.player.ship_rect.center
                    self.projectiles.bullet_list.append(bullet_rect)
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.player.moving_right = False
                if event.key == pygame.K_LEFT:
                    self.player.move_left = False


if __name__ == '__main__':
    ng = NewGame()
    ng.run_game()