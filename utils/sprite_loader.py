import pygame

def load_frames(sheet, frame_width, frame_height, num_frames, scale=2.0):
    frames = []
    sheet_width = sheet.get_width()
    actual_frame_width = sheet_width // num_frames  # Gerçek frame genişliğini hesapla
    
    for i in range(num_frames):
        # Gerçek frame genişliğini kullan
        frame = sheet.subsurface((i * actual_frame_width, 0, actual_frame_width, frame_height))
        # İstenen boyuta ölçekle
        scaled_frame = pygame.transform.scale(frame, 
                                           (int(frame_width * scale), 
                                            int(frame_height * scale)))
        frames.append(scaled_frame)
    return frames 