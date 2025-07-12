import pygame

class HealthBar:
    def __init__(self, x, y, width, height, max_health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_health = max_health
        self.base_max_health = max_health
        self.extra_health = 0
        
        # Renkler
        self.border_color = (0, 0, 0)  # Siyah
        self.health_color = (255, 0, 0)  # Kırmızı
        self.extra_health_color = (255, 215, 0)  # Altın rengi
        self.background_color = (169, 169, 169)  # Gri

    def draw(self, screen, current_health):
        total_height = self.height * 2 if self.extra_health > 0 else self.height
        
        # Arka plan (gri)
        pygame.draw.rect(screen, self.background_color, 
                        (self.x, self.y, self.width, total_height))
        
        # Normal can barı (kırmızı) - üstte
        health_width = min(current_health, self.base_max_health) / self.base_max_health * self.width
        if health_width > 0:
            pygame.draw.rect(screen, self.health_color, 
                           (self.x, self.y, health_width, self.height))
        
        # Ekstra can barı (altın rengi) - altta
        if self.extra_health > 0:
            if current_health > self.base_max_health:
                extra_health = current_health - self.base_max_health
                extra_width = (min(extra_health, self.extra_health) / self.base_max_health) * self.width
                if extra_width > 0:
                    pygame.draw.rect(screen, self.extra_health_color, 
                                   (self.x, self.y + self.height, extra_width, self.height))
        
        # Çerçeve (siyah)
        pygame.draw.rect(screen, self.border_color, 
                        (self.x, self.y, self.width, total_height), 1)

    def set_extra_health(self, amount):
        """Ekstra can miktarını ayarla"""
        self.extra_health = amount
        self.max_health = self.base_max_health + amount 