import pygame

class StaminaBar:
    def __init__(self, x, y, width, height, max_stamina):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_stamina = max_stamina
        self.current_stamina = max_stamina
        self.regen_rate = 0.5
        self.border_color = (40, 40, 40)
        self.background_color = (70, 70, 70)
        self.stamina_color = (40, 100, 220)
        self.border_width = 2

    def draw(self, screen, current_stamina):
        pygame.draw.rect(screen, self.background_color, 
                        (self.x, self.y, self.width, self.height))
        
        ratio = current_stamina / self.max_stamina
        stamina_width = self.width * ratio
        if ratio > 0:
            pygame.draw.rect(screen, self.stamina_color, 
                           (self.x, self.y, stamina_width, self.height))
        
        pygame.draw.rect(screen, self.border_color, 
                        (self.x, self.y, self.width, self.height), 
                        self.border_width)
        
        font = pygame.font.Font(None, 24)
        text = font.render(f"{int(current_stamina)}/{self.max_stamina}", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (self.x + self.width // 2, self.y + self.height // 2)
        screen.blit(text, text_rect) 