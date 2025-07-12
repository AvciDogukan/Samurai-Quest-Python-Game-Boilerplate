import pygame
import json
import os

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = pygame.font.Font(None, 36)
        
    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

class Menu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.state = 'main'  # main, settings, pause
        
        # Renkler
        self.button_color = (200, 200, 200)
        self.hover_color = (150, 150, 150)
        
        # Ana menü butonları
        button_width = 200
        button_height = 50
        button_spacing = 20
        start_y = screen_height // 3
        
        self.main_buttons = {
            'new_game': Button(screen_width//2 - button_width//2, start_y, 
                             button_width, button_height, "Yeni Oyun", 
                             self.button_color, self.hover_color),
            'load_game': Button(screen_width//2 - button_width//2, start_y + button_height + button_spacing, 
                              button_width, button_height, "Oyunu Yükle", 
                              self.button_color, self.hover_color),
            'settings': Button(screen_width//2 - button_width//2, start_y + (button_height + button_spacing) * 2, 
                             button_width, button_height, "Ayarlar", 
                             self.button_color, self.hover_color),
            'quit': Button(screen_width//2 - button_width//2, start_y + (button_height + button_spacing) * 3, 
                          button_width, button_height, "Çıkış", 
                          self.button_color, self.hover_color)
        }
        
        # Ayarlar menüsü butonları
        self.settings_buttons = {
            'music': Button(screen_width//2 - button_width//2, start_y,
                          button_width, button_height, "Müzik: Açık",
                          self.button_color, self.hover_color),
            'sound': Button(screen_width//2 - button_width//2, start_y + button_height + button_spacing,
                          button_width, button_height, "Ses: Açık",
                          self.button_color, self.hover_color),
            'back': Button(screen_width//2 - button_width//2, start_y + (button_height + button_spacing) * 3,
                         button_width, button_height, "Geri",
                         self.button_color, self.hover_color)
        }
        
        # Ayarlar
        self.settings = {
            'music': True,
            'sound': True
        }
        self.load_settings()
        
        # Arka plan resmini yükle
        self.background = pygame.image.load("assets/menu_background.png")
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
    
    def save_game(self, player_data):
        """Oyun durumunu kaydet"""
        save_data = {
            'player': {
                'health': player_data.current_health,
                'level': player_data.level,
                'exp': player_data.exp,
                'score': player_data.score
            }
        }
        with open('save_game.json', 'w') as f:
            json.dump(save_data, f)
    
    def load_game(self):
        """Kaydedilmiş oyunu yükle"""
        try:
            with open('save_game.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
    
    def save_settings(self):
        """Ayarları kaydet"""
        with open('settings.json', 'w') as f:
            json.dump(self.settings, f)
    
    def load_settings(self):
        """Ayarları yükle"""
        try:
            with open('settings.json', 'r') as f:
                self.settings = json.load(f)
        except FileNotFoundError:
            self.save_settings()
    
    def handle_events(self, events):
        """Menü olaylarını işle"""
        for event in events:
            if self.state == 'main':
                for button_name, button in self.main_buttons.items():
                    if button.handle_event(event):
                        return button_name
            elif self.state == 'settings':
                for button_name, button in self.settings_buttons.items():
                    if button.handle_event(event):
                        if button_name == 'music':
                            self.settings['music'] = not self.settings['music']
                            button.text = f"Müzik: {'Açık' if self.settings['music'] else 'Kapalı'}"
                            self.save_settings()
                        elif button_name == 'sound':
                            self.settings['sound'] = not self.settings['sound']
                            button.text = f"Ses: {'Açık' if self.settings['sound'] else 'Kapalı'}"
                            self.save_settings()
                        return button_name
        return None
    
    def draw(self, screen):
        """Menüyü çiz"""
        # Arka plan resmini çiz
        screen.blit(self.background, (0, 0))
        
        # Başlık
        font = pygame.font.Font(None, 72)
        title = font.render("Samuray Macerası", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen_width//2, self.screen_height//4))
        
        # Başlık arka planı (okunabilirlik için)
        title_bg = pygame.Surface((title.get_width() + 20, title.get_height() + 10))
        title_bg.fill((0, 0, 0))
        title_bg.set_alpha(128)  # Yarı saydam
        title_bg_rect = title_bg.get_rect(center=(self.screen_width//2, self.screen_height//4))
        screen.blit(title_bg, title_bg_rect)
        screen.blit(title, title_rect)
        
        # Butonları çiz
        if self.state == 'main':
            for button in self.main_buttons.values():
                button.draw(screen)
        elif self.state == 'settings':
            for button in self.settings_buttons.values():
                button.draw(screen) 