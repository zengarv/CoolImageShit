import pygame
pygame.init()
import colorsys
import numpy as np

def hsv2rgb(col: np.array):
    return tuple(i * 255 for i in colorsys.hsv_to_rgb(*col/255))

class ColorPicker:
    def __init__(self, pos:np.array, size=(256, 256+90)):
        self.surf = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.surf.get_rect()
        self.rect.topleft = pos
        
        self.hue_bar = pygame.Rect(0, 256+70, 256, 10)
        self.pointer = pos
        self.grad = pygame.Rect(0, 0, 256, 256)
        
        self.preview_rect = pygame.Rect(pos[0], pos[1]+self.grad.height, 256, 70)
        
        # Draw hues
        for i in range(256):
            pygame.draw.rect(self.surf, hsv2rgb(np.array([i, 255, 255])), pygame.Rect(i, self.hue_bar.top, 1, self.hue_bar.height))
        
        hue_selector_rect_width = 4
        self.hue_selector_rect = pygame.Rect(pos[0]-hue_selector_rect_width//2, self.hue_bar.top+pos[1], hue_selector_rect_width, self.hue_bar.height)
        self.h = 0
        
        self.white_overlay = pygame.Surface((256, 256), pygame.SRCALPHA)
        for i in range(256):
            pygame.draw.rect(self.white_overlay, (i, i, i, i), pygame.Rect(255-i, 0, 1, 256))
        self.black_overlay = pygame.Surface((256, 256), pygame.SRCALPHA)
        for i in range(256):
            pygame.draw.rect(self.black_overlay, (255-i, 255-i, 255-i, i), pygame.Rect(0, i, 256, 1))
        self.draw_grad()
        
    def draw(self, screen):
        screen.blit(self.surf, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.hue_selector_rect, width=1)
        self.col = self.surf.get_at((self.pointer[0]-self.rect.left, self.pointer[1]-self.rect.top))
        pygame.draw.rect(screen, self.col, self.preview_rect)
        pygame.draw.circle(screen, (255, 255, 255), self.pointer, 4, 2)
    
    def hold(self, pos):
        pos = np.array([pos[0]-self.rect.left, pos[1]-self.rect.top])
        if self.hue_bar.collidepoint(pos):
            self.hue_selector_rect.centerx = self.rect.left+pos[0]
            self.h = pos[0]
            self.draw_grad()
        elif self.grad.collidepoint(pos):
            self.pointer = self.rect.left + pos[0], self.rect.top + pos[1]
            

    def draw_grad(self):
        self.surf.fill(hsv2rgb(np.array([self.h, 255, 255])), self.grad)
        self.surf.blit(self.white_overlay, (0, 0))
        self.surf.blit(self.black_overlay, (0, 0))


if __name__  == '__main__':
    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()
    col_pick = ColorPicker(np.array([300, 300]))
    
    FPS = 60
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if col_pick.rect.collidepoint(mouse_pos): col_pick.hold(mouse_pos)
            
        screen.fill((30, 30, 30))
        col_pick.draw(screen)
        
        pygame.display.update()

    pygame.quit()
    
