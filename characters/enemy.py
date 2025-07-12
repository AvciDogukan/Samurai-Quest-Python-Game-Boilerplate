import pygame
import math
from ui.health_bar import HealthBar
import random

class Enemy:
    def __init__(self, x, y, speed, sprite_sheets, enemy_type='wolf'):
        self.pos = [x, y]
        self.speed = speed
        self.enemy_type = enemy_type
        self.current_frame = 0
        self.frame_rate = 0.5
        self.frame_counter = 0
        self.facing_right = True
        self.sprite_sheets = sprite_sheets
        self.current_animation = sprite_sheets['idle']
        self.animation_state = 'idle'
        self.scale = 2.0
        self.screen_width = 800  # Ekran genişliğini başlangıçta tanımla
        
        # Düşman tipine göre özellikler
        if enemy_type == 'wolf':
            base_health = 100
            self.max_health = base_health
            self.health_bar = HealthBar(0, 0, 60, 10, base_health)  # Kurt için health bar
            self.attack_range = 100
            self.chase_range = 300
            self.damage = 15
            self.retreat_health = 50
            self.sprite_width = 96
            self.sprite_height = 76
            self.attack_cooldown_max = 30
            self.retreat_speed_multiplier = 1.5
        elif enemy_type == 'samurai':
            base_health = 300
            extra_health = 200  # Boss için ekstra can
            self.max_health = base_health + extra_health
            self.health_bar = HealthBar(0, 0, 60, 10, base_health)
            self.health_bar.set_extra_health(extra_health)  # Ekstra canı ayarla
            self.attack_range = 100
            self.chase_range = 500
            self.damage = 45
            self.retreat_health = 150
            self.sprite_width = 96
            self.sprite_height = 96
            self.attack_cooldown_max = 30
            self.dodge_chance = 0.4
            self.counter_attack_chance = 0.5
            self.scale = 2.0
            self.retreat_speed_multiplier = 2.0
        
        self.current_health = self.max_health
        self.is_dead = False
        self.death_time = 0
        self.death_message_duration = 60  # 2 saniye (30 FPS'de)
        
        # Yapay zeka parametreleri
        self.attack_cooldown = 0
        self.attack_cooldown_max = 30
        self.is_attacking = False
        self.state = 'idle'

    def set_animation(self, state):
        if state != self.animation_state:
            self.animation_state = state
            self.current_animation = self.sprite_sheets[state]
            self.current_frame = 0
            self.frame_counter = 0

    def move(self, screen_width):
        self.screen_width = screen_width
        old_pos = self.pos[0]
        self.pos[0] += self.speed
        
        # Ekran sınırlarını kontrol et
        if self.pos[0] < 0:
            self.pos[0] = 0
            if self.enemy_type == 'samurai':
                self.speed = abs(self.speed)
        elif self.pos[0] > self.screen_width - self.sprite_width * self.scale:
            self.pos[0] = self.screen_width - self.sprite_width * self.scale
            if self.enemy_type == 'samurai':
                self.speed = -abs(self.speed)

        # Hareket animasyonunu ayarla - Saldırı durumunda animasyonu değiştirme
        if self.animation_state != 'attack':  # Önemli değişiklik burada
            if abs(self.speed) > 0 and old_pos != self.pos[0]:
                self.set_animation('run')
            else:
                self.set_animation('idle')

        # Yön kontrolü
        if self.speed != 0:
            self.facing_right = self.speed > 0

    def update_animation(self):
        if self.current_animation and len(self.current_animation) > 0:
            self.frame_counter += self.frame_rate
            if self.frame_counter >= 1:
                self.current_frame = (self.current_frame + 1) % len(self.current_animation)
                self.frame_counter = 0
                
                # Saldırı animasyonu bitince idle'a dön
                if self.animation_state == 'attack' and self.current_frame == 0:
                    self.set_animation('idle')
                    self.is_attacking = False

    def draw(self, screen):
        if not self.is_dead:  # Sadece düşman ölü değilse çiz
            if self.current_animation and len(self.current_animation) > 0:
                frame_to_draw = self.current_animation[self.current_frame]
                if not self.facing_right:
                    frame_to_draw = pygame.transform.flip(frame_to_draw, True, False)
                screen.blit(frame_to_draw, self.pos)
                
                # Can barını düşmanın üstünde çiz
                bar_x = self.pos[0] + (frame_to_draw.get_width() - self.health_bar.width) // 2
                bar_y = self.pos[1] - self.health_bar.height - 5
                self.health_bar.x = bar_x
                self.health_bar.y = bar_y
                self.health_bar.draw(screen, self.current_health)

    def take_damage(self, amount):
        if not self.is_dead:
            if self.enemy_type == 'samurai':
                # Kaçınma şansı
                if random.random() < self.dodge_chance:
                    return False  # Hasardan kaçındı
                
                # Hasar alınca hurt animasyonu
                self.set_animation('hurt')
                self.current_health = max(0, self.current_health - amount)
                
                # Karşı saldırı şansı
                if random.random() < self.counter_attack_chance:
                    self.state = 'attack'
                    self.attack_cooldown = 0  # Hemen karşı saldırı yapabilir
                
            else:
                self.current_health = max(0, self.current_health - amount)
            
            if self.current_health <= 0:
                self.is_dead = True
                self.death_time = pygame.time.get_ticks()
                return True
        return False

    def update_ai(self, player):
        if self.is_dead:
            return

        dx = player.pos[0] - self.pos[0]
        dy = player.pos[1] - self.pos[1]
        distance = math.sqrt(dx*dx + dy*dy)
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if self.enemy_type == 'samurai':
            base_speed = 4
            
            if distance <= self.attack_range:
                # Saldırı mesafesindeyse
                self.state = 'attack'
                # Oyuncuya doğru bak
                self.facing_right = dx > 0
                # Saldırı
                self.attack(player)
                print(f"Mesafe: {distance}, Saldırı menzili: {self.attack_range}")  # Debug için
            else:
                # Normal durumda saldırgan davran
                if distance <= self.chase_range:
                    # Oyuncuya doğru koş
                    self.state = 'chase'
                    self.speed = base_speed * (1 if dx > 0 else -1)
                    self.set_animation('run')
                else:
                    # Uzaktaysa hızlı yaklaş
                    self.state = 'chase'
                    self.speed = base_speed * 1.5 * (1 if dx > 0 else -1)
                    self.set_animation('run')

            # Her durumda hareket et
            self.move(self.screen_width)
        else:  # Kurt için AI
            base_speed = 3  # Kurt için temel hız
            
            # Kurt'un davranışları
            if self.current_health < self.retreat_health:
                # Düşük canda kaçış davranışı
                self.state = 'retreat'
                retreat_direction = -1 if dx > 0 else 1
                self.speed = base_speed * retreat_direction * 1.5
            else:
                if distance <= self.attack_range:
                    # Saldırı mesafesindeyse
                    self.state = 'attack'
                    self.facing_right = dx > 0
                    self.attack(player)
                    # Saldırı sırasında yavaş hareket
                    self.speed = base_speed * 0.5 * (1 if dx > 0 else -1)
                elif distance <= self.chase_range:
                    # Takip mesafesindeyse
                    self.state = 'chase'
                    self.speed = base_speed * (1 if dx > 0 else -1)
                    self.set_animation('run')
                else:
                    # Devriye gezme
                    self.state = 'patrol'
                    if abs(self.speed) == 0:
                        self.speed = base_speed
                    self.patrol()

            # Her durumda hareket et
            self.move(self.screen_width)

    def patrol(self):
        # Normal devriye davranışı
        if self.pos[0] > self.screen_width - self.sprite_width * self.scale:
            self.speed = -abs(self.speed)
        elif self.pos[0] < 0:
            self.speed = abs(self.speed)
        
        self.move(self.screen_width)

    def attack(self, player):
        if self.attack_cooldown <= 0:
            self.attack_cooldown = self.attack_cooldown_max
            
            if self.enemy_type == 'samurai':
                # Saldırı animasyonunu başlat
                self.set_animation('attack')
                self.is_attacking = True
                
                # Saldırı hitbox'u ve hasar verme
                attack_width = self.sprite_width * 1.2
                # Saldırı mesafesini ayarla
                if self.facing_right:
                    attack_rect = pygame.Rect(self.pos[0] + (self.sprite_width * self.scale * 0.5), 
                                           self.pos[1], 
                                           attack_width * self.scale, 
                                           self.sprite_height * self.scale)
                else:
                    attack_rect = pygame.Rect(self.pos[0] - (attack_width * self.scale * 0.5), 
                                           self.pos[1], 
                                           attack_width * self.scale, 
                                           self.sprite_height * self.scale)
                
                player_rect = pygame.Rect(player.pos[0], 
                                        player.pos[1], 
                                        96 * player.scale, 
                                        76 * player.scale)
                
                # Çarpışma kontrolü ve hasar verme
                if attack_rect.colliderect(player_rect):
                    player.take_damage(self.damage)
                    print("Samuray hasar verdi!")  # Debug için
            else:
                # Kurt için normal saldırı kodu
                enemy_rect = pygame.Rect(self.pos[0], self.pos[1], 
                                    self.sprite_width * self.scale, self.sprite_height * self.scale)
                
                player_rect = pygame.Rect(player.pos[0], player.pos[1], 
                                    96 * player.scale, 76 * player.scale)
                
                if enemy_rect.colliderect(player_rect):
                    player.take_damage(self.damage) 