import pygame
from ui.health_bar import HealthBar
from ui.stamina_bar import StaminaBar

class Knight:
    def __init__(self, x, y, speed, jump_power, sprite_sheets):
        self.pos = [x, y - (40 * (2.0 - 1))]
        self.speed = speed
        self.jump_power = jump_power
        self.is_jumping = False
        self.is_attacking = False
        self.is_crouching = False
        self.is_climbing = False
        self.is_hurt = False
        self.jump_count = 10
        self.current_frame = 0
        self.frame_rate = 0.5
        self.frame_counter = 0
        self.facing_right = True
        self.sprite_sheets = sprite_sheets
        self.current_animation = sprite_sheets['idle']
        self.animation_state = 'idle'
        self.attack_cooldown = 0
        self.attack_duration = 20
        self.max_health = 100
        self.current_health = self.max_health
        self.max_stamina = 100
        self.current_stamina = self.max_stamina
        self.stamina_regen = 0.5
        self.stamina_jump_cost = 50
        self.health_bar = HealthBar(10, 10, 200, 20, 100)
        self.health_bar.set_extra_health(200)
        self.stamina_bar = StaminaBar(20, 55, 200, 25, self.max_stamina)
        self.scale = 2.0
        
        # Puan ve seviye sistemi
        self.score = 0
        self.level = 1
        self.exp = 0
        self.exp_to_next_level = 100  # İlk seviye için gereken deneyim puanı
        
        # Seviye bazlı güçlendirmeler
        self.base_damage = 20
        self.damage_multiplier = 1.0

    def set_animation(self, state):
        if state != self.animation_state:
            self.animation_state = state
            self.current_animation = self.sprite_sheets[state]
            self.current_frame = 0
            self.frame_counter = 0

    def update_stamina(self):
        if self.current_stamina < self.max_stamina:
            self.current_stamina = min(self.max_stamina, self.current_stamina + self.stamina_regen)

    def move(self, keys):
        mouse_buttons = pygame.mouse.get_pressed()
        
        if self.is_attacking:
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1
            else:
                self.is_attacking = False
                self.set_animation('idle')
            return

        # Sol tık normal saldırı
        if mouse_buttons[0] and self.current_stamina >= 20:  # Sol tık
            self.is_attacking = True
            self.attack_cooldown = self.attack_duration
            self.current_stamina -= 20
            if self.is_crouching:
                self.set_animation('crouch_sword_slash')
            elif self.is_jumping:
                self.set_animation('jump_attack')
            else:
                self.set_animation('sword_slash')
        
        # Sağ tık yukarı saldırı
        elif mouse_buttons[2] and self.current_stamina >= 20:  # Sağ tık
            self.is_attacking = True
            self.attack_cooldown = self.attack_duration
            self.current_stamina -= 20
            self.set_animation('attack_up')

        if keys[pygame.K_s]:
            self.is_crouching = True
            if self.is_attacking:
                self.set_animation('crouch_sword_slash')
            else:
                self.set_animation('crouch')
        else:
            self.is_crouching = False

        if self.is_jumping:
            if self.jump_count >= -10:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.pos[1] -= (self.jump_count ** 2) * 0.5 * neg
                self.jump_count -= 1
                if keys[pygame.K_j]:
                    self.set_animation('jump_attack')
                else:
                    self.set_animation('jump')
            else:
                self.is_jumping = False
                self.jump_count = 10
                self.set_animation('idle')
        else:
            if keys[pygame.K_w] and not self.is_crouching and self.current_stamina >= self.stamina_jump_cost:
                self.is_jumping = True
                self.jump_count = 10
                self.current_stamina -= self.stamina_jump_cost
                self.set_animation('jump')

        if not self.is_crouching and not self.is_attacking:
            if keys[pygame.K_a]:
                self.pos[0] -= self.speed
                self.facing_right = False
                if not self.is_jumping:
                    self.set_animation('run')
            elif keys[pygame.K_d]:
                self.pos[0] += self.speed
                self.facing_right = True
                if not self.is_jumping:
                    self.set_animation('run')
            elif not self.is_jumping and not self.is_attacking:
                self.set_animation('idle')

    def update_animation(self):
        if self.current_animation and len(self.current_animation) > 0:
            self.frame_counter += self.frame_rate
            if self.frame_counter >= 1:
                self.current_frame = (self.current_frame + 1) % len(self.current_animation)
                self.frame_counter = 0

    def draw(self, screen):
        if self.current_animation and len(self.current_animation) > 0:
            frame_to_draw = self.current_animation[self.current_frame]
            if not self.facing_right:
                frame_to_draw = pygame.transform.flip(frame_to_draw, True, False)
            screen.blit(frame_to_draw, self.pos)

        self.health_bar.draw(screen, self.current_health)
        self.stamina_bar.draw(screen, self.current_stamina)

        # Puan ve seviye göstergesi
        font = pygame.font.Font(None, 24)
        level_text = font.render(f"Level: {self.level}", True, (255, 255, 255))
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        exp_text = font.render(f"EXP: {self.exp}/{self.exp_to_next_level}", True, (255, 255, 255))
        
        screen.blit(level_text, (20, 90))
        screen.blit(score_text, (20, 110))
        screen.blit(exp_text, (20, 130))

    def take_damage(self, amount):
        self.current_health = max(0, self.current_health - amount)
        if self.current_health > 0:
            self.is_hurt = True
            self.set_animation('hurt') 

    def add_exp(self, amount):
        self.exp += amount
        self.score += amount * 10  # Her exp için 10 puan
        
        # Seviye atlama kontrolü
        while self.exp >= self.exp_to_next_level:
            self.level_up()
    
    def level_up(self):
        self.level += 1
        self.exp -= self.exp_to_next_level
        self.exp_to_next_level = int(self.exp_to_next_level * 1.5)  # Her seviyede %50 daha fazla exp gerekir
        
        # Seviye atladıkça güçlenme
        self.damage_multiplier += 0.1
        self.max_health += 10
        self.current_health = self.max_health
        self.max_stamina += 5
        self.current_stamina = self.max_stamina
        
    def get_current_damage(self):
        return int(self.base_damage * self.damage_multiplier) 