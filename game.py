import pygame
import sys
from characters.knight import Knight
from characters.enemy import Enemy
from ui.health_bar import HealthBar
from ui.stamina_bar import StaminaBar
from utils.sprite_loader import load_frames
from ui.menu import Menu

# Pygame'i başlat
pygame.init()

# Ekran boyutları
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Platform Macerası")

# Arka plan resmi yükle
background_image = pygame.image.load("assets/Background.png")

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)

class PhaseManager:
    def __init__(self, screen_width, ground_level, wolf_sprites, samurai_sprites):
        self.screen_width = screen_width
        self.ground_level = ground_level
        self.wolf_sprites = wolf_sprites
        self.samurai_sprites = samurai_sprites
        self.current_phase = 1
        self.enemies = []
        self.phase_complete = False
        
    def start_phase(self):
        self.enemies.clear()
        self.phase_complete = False
        
        if self.current_phase == 1:
            # Phase 1: 2 kurt
            self.enemies.append(Enemy(100, self.ground_level, 3, self.wolf_sprites, 'wolf'))
            self.enemies.append(Enemy(self.screen_width - 100, self.ground_level, 3, self.wolf_sprites, 'wolf'))
            
        elif self.current_phase == 2:
            # Phase 2: 4 kurt (2 soldan, 2 sağdan)
            self.enemies.extend([
                Enemy(50, self.ground_level, 3, self.wolf_sprites, 'wolf'),
                Enemy(150, self.ground_level, 3, self.wolf_sprites, 'wolf'),
                Enemy(self.screen_width - 50, self.ground_level, 3, self.wolf_sprites, 'wolf'),
                Enemy(self.screen_width - 150, self.ground_level, 3, self.wolf_sprites, 'wolf')
            ])
            
        elif self.current_phase == 3:
            # Phase 3: Boss Samuray
            samurai = Enemy(self.screen_width - 100, self.ground_level, 2, self.samurai_sprites, 'samurai')
            samurai.max_health = 500  # Boss için extra can
            samurai.current_health = samurai.max_health
            samurai.damage = 60  # Boss için extra hasar
            self.enemies.append(samurai)
    
    def update(self):
        # Tüm düşmanlar öldüyse phase'i tamamla
        if not self.phase_complete and len(self.enemies) > 0:
            alive_enemies = [e for e in self.enemies if not e.is_dead]
            if len(alive_enemies) == 0:
                self.phase_complete = True
                self.current_phase += 1
                if self.current_phase <= 3:  # Maximum 3 phase
                    self.start_phase()

def main():
    # Sprite sheet dosyalarını yükle
    fall_sheet = pygame.image.load("assets/Werewolf/werewolf-fall.png")
    jump_sheet = pygame.image.load("assets/Werewolf/werewolf-jump.png")
    idle_sheet = pygame.image.load("assets/Werewolf/werewolf-idle.png")
    run_sheet = pygame.image.load("assets/Werewolf/werewolf-run.png")

    # Kurt düşman animasyonları
    wolf_sprite_sheets = {
        'fall': load_frames(fall_sheet, 96, 76, 2, scale=2.0),
        'jump': load_frames(jump_sheet, 96, 76, 2, scale=2.0),
        'idle': load_frames(idle_sheet, 96, 76, 5, scale=2.0),
        'run': load_frames(run_sheet, 96, 76, 6, scale=2.0)
    }

    # Knight sprite'larını yükle
    knight_sprites = {
        'air_sword_slash': pygame.image.load("assets/Knight/player-AirSwordSlash.png"),
        'attack_crouch': pygame.image.load("assets/Knight/player-Attack Crouch.png"),
        'attack_up': pygame.image.load("assets/Knight/player-Attack Up.png"),
        'attack_side': pygame.image.load("assets/Knight/player-AttackSide.png"),
        'climb_ledge': pygame.image.load("assets/Knight/player-ClimbLedge.png"),
        'crouch': pygame.image.load("assets/Knight/player-Crouch.png"),
        'crouch_sword_slash': pygame.image.load("assets/Knight/player-CrouchSwordSlash.png"),
        'hurt': pygame.image.load("assets/Knight/player-Hurt.png"),
        'idle': pygame.image.load("assets/Knight/player-Idle.png"),
        'jump': pygame.image.load("assets/Knight/player-Jump.png"),
        'jump_attack': pygame.image.load("assets/Knight/player-JumpAttack.png"),
        'run': pygame.image.load("assets/Knight/player-Run.png"),
        'sword_slash': pygame.image.load("assets/Knight/player-Sword Slash.png")
    }

    # Samuray sprite'ları
    samurai_sprite_sheets = {
        'idle': load_frames(pygame.image.load("assets/Samurai/IDLE.png"), 96, 96, 10, scale=2.0),
        'run': load_frames(pygame.image.load("assets/Samurai/RUN.png"), 96, 96, 16, scale=2.0),
        'attack': load_frames(pygame.image.load("assets/Samurai/ATTACK 1.png"), 96, 96, 7, scale=2.0),
        'hurt': load_frames(pygame.image.load("assets/Samurai/HURT.png"), 96, 96, 4, scale=2.0)
    }

    def get_sprite_info(sprite_sheet):
        width = sprite_sheet.get_width()
        height = sprite_sheet.get_height()
        num_frames = width // 128
        frame_width = 128
        return frame_width, height, num_frames

    # Knight animasyonları
    knight_animations = {}
    for key, sprite_sheet in knight_sprites.items():
        frame_width, frame_height, num_frames = get_sprite_info(sprite_sheet)
        knight_animations[key] = load_frames(sprite_sheet, frame_width, frame_height, num_frames, scale=2.0)

    # Zemin seviyesini belirle
    ground_level = screen_height - 150

    # Değişkenler
    kill_message = ""
    kill_message_timer = 0
    kill_message_duration = 60
    phase_message = ""
    phase_message_timer = 0
    font = pygame.font.Font(None, 36)

    # Menu'yü oluştur
    menu = Menu(screen_width, screen_height)
    game_state = 'menu'  # menu, game, pause
    
    # Oyun nesneleri
    player = None
    phase_manager = None

    # Oyun döngüsü
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if game_state == 'game':
                        game_state = 'pause'
                        menu.state = 'main'
                    elif game_state == 'pause':
                        game_state = 'game'

        if game_state in ['menu', 'pause']:
            action = menu.handle_events(events)
            if action == 'new_game':
                game_state = 'game'
                # Yeni oyun başlat
                player = Knight(screen_width // 2, ground_level, 5, 10, knight_animations)
                player.max_health = 300
                player.current_health = player.max_health
                phase_manager = PhaseManager(screen_width, ground_level, wolf_sprite_sheets, samurai_sprite_sheets)
                phase_manager.start_phase()
            elif action == 'load_game':
                save_data = menu.load_game()
                if save_data:
                    game_state = 'game'
                    # Kayıtlı oyunu yükle
                    player = Knight(screen_width // 2, ground_level, 5, 10, knight_animations)
                    player.load_data(save_data['player'])
                    phase_manager = PhaseManager(screen_width, ground_level, wolf_sprite_sheets, samurai_sprite_sheets)
                    phase_manager.start_phase()
            elif action == 'settings':
                menu.state = 'settings'
            elif action == 'back':
                menu.state = 'main'
            elif action == 'quit':
                running = False
            
            menu.draw(screen)
        
        elif game_state == 'game':
            # Normal oyun güncellemeleri
            keys = pygame.key.get_pressed()
            
            # F5'e basılınca kaydet
            if keys[pygame.K_F5]:
                menu.save_game(player)

            # Karakter güncellemeleri
            player.move(keys)
            player.update_animation()
            player.update_stamina()

            # Düşmanları güncelle
            for enemy in phase_manager.enemies:
                if not enemy.is_dead:
                    enemy.update_ai(player)
                    enemy.update_animation()

                    # Saldırı çarpışma kontrolü
                    if player.is_attacking:
                        enemy_rect = pygame.Rect(enemy.pos[0], enemy.pos[1], 96 * enemy.scale, 76 * enemy.scale)
                        player_rect = pygame.Rect(player.pos[0], player.pos[1], 96 * player.scale, 76 * player.scale)
                        
                        if player_rect.colliderect(enemy_rect):
                            if enemy.take_damage(player.get_current_damage()):
                                kill_message = f"{enemy.enemy_type.capitalize()} Öldürüldü! +50 EXP"
                                kill_message_timer = kill_message_duration
                                player.add_exp(50)

            # Phase manager'ı güncelle
            phase_manager.update()
            
            # Phase değiştiğinde mesaj göster
            if phase_manager.phase_complete:
                if phase_manager.current_phase <= 3:
                    phase_message = f"Phase {phase_manager.current_phase} Başladı!"
                    phase_message_timer = 60

            # Çizimler
            screen.blit(background_image, (0, 0))
            
            # Düşmanları çiz
            for enemy in phase_manager.enemies:
                if not enemy.is_dead:
                    enemy.draw(screen)
            
            player.draw(screen)

            # Mesajları çiz
            if kill_message_timer > 0:
                kill_message_timer -= 1
                text_surface = font.render(kill_message, True, (255, 0, 0))
                text_rect = text_surface.get_rect(center=(screen_width/2, 50))
                screen.blit(text_surface, text_rect)

            if phase_message_timer > 0:
                phase_message_timer -= 1
                text_surface = font.render(phase_message, True, (255, 215, 0))
                text_rect = text_surface.get_rect(center=(screen_width/2, 100))
                screen.blit(text_surface, text_rect)

            # Phase bilgisini göster
            phase_text = font.render(f"Phase: {phase_manager.current_phase}/3", True, (255, 255, 255))
            screen.blit(phase_text, (screen_width - 150, 20))

        pygame.display.flip()
        pygame.time.Clock().tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()