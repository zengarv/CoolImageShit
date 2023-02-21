import pygame
from ColorPicker import ColorPicker
from numba import njit, prange
import numpy as np
from PIL import Image

"""
Controls:

Drag and drop image from file explorer to work on it
Hold middle mouse button to scroll around
':)' button selects the color
'>_<' button centers the image
':0' generates the images with selected colors
Left click to mess around with color picker and press buttons
Middle click on selected colors to delete them
Right click anywhere on the screen to select that pixel color

"""
@njit(fastmath=True, parallel=True)
def compute_image(image, cols):
    final = np.zeros_like(image)
    shape = final.shape
    
    for i in prange(shape[0]):
        for j in prange(shape[1]):
            min_dist = 4*256*256
            min_col = 0    
            for colindex in prange(len(cols)):
                col = cols[colindex]
                dist = np.sum((col - image[i,j])**2)
                if dist < min_dist:
                    min_col = colindex
                    min_dist = dist
            
            final[i, j] = cols[min_col]
            
    return final
                
compute_image(np.ones([4, 4, 4]), np.array([[255, 255, 255, 255], [30, 30, 30, 30]]))

img_surf = pygame.Surface((800, 800))
img_rect = img_surf.get_rect()
img_surf.fill((50, 50, 50))

screen = pygame.display.set_mode((1200, 800))

run = True
file = None
color_picker = ColorPicker((img_rect.right+80, 20))

class Button:
	def __init__(self,text,width,height,pos,elevation):
		#Core attributes 
		self.pressed = False
		self.elevation = elevation
		self.dynamic_elecation = elevation
		self.original_y_pos = pos[1]

		# top rectangle 
		self.top_rect = pygame.Rect(pos,(width,height))
		self.top_color = '#475F77'

		# bottom rectangle 
		self.bottom_rect = pygame.Rect(pos,(width,height))
		self.bottom_color = '#354B5E'
		#text
		self.text_surf = gui_font.render(text,True,'#FFFFFF')
		self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

	def draw(self):
		# elevation logic 
		self.top_rect.y = self.original_y_pos - self.dynamic_elecation
		self.text_rect.center = self.top_rect.center 

		self.bottom_rect.midtop = self.top_rect.midtop
		self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

		pygame.draw.rect(screen,self.bottom_color, self.bottom_rect,border_radius = 12)
		pygame.draw.rect(screen,self.top_color, self.top_rect,border_radius = 12)
		screen.blit(self.text_surf, self.text_rect)
		self.check_click()

	def check_click(self):
		mouse_pos = pygame.mouse.get_pos()
		if self.top_rect.collidepoint(mouse_pos):
			self.top_color = '#D74B4B'
			if pygame.mouse.get_pressed()[0]:
				self.dynamic_elecation = 0
				self.pressed = True
			else:
				self.dynamic_elecation = self.elevation
				if self.pressed == True:
					self.klik()
					self.pressed = False
		else:
			self.dynamic_elecation = self.elevation
			self.top_color = '#475F77'
   
	def klik(self):
		pass
    
gui_font = pygame.font.Font(None,30)

button1 = Button(':)', 120, 40, (color_picker.rect.left, color_picker.rect.bottom + 10), 5)
button1.klik = lambda: cols.append(color_picker.col) if color_picker.col not in cols else None
center = Button('>_<', 120, 40, (color_picker.rect.left, color_picker.rect.bottom + 10+60), 5)
button2 = Button(':o', 120, 40, (color_picker.rect.left+128+8, color_picker.rect.bottom + 10), 5)

def beech_mein_lao():
    global img_rect
    img_rect.center = 400, 400
center.klik = beech_mein_lao
    
cols = []
midmousebuttondown = False

def generate():
    global img_surf, img_rect, cols, file
    im = Image.open(file, 'r').convert("RGBA")
    img_surf = pygame.transform.rotate(pygame.transform.flip(pygame.surfarray.make_surface(compute_image(np.array(im.getdata()).reshape(im.height, im.width, 4), np.array(cols))[:, :, :3]), 0, 1), -90)
    img_rect = img_surf.get_rect()
    img_rect.center = (400, 400)
button2.klik = generate

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        elif event.type == pygame.DROPFILE:
            file = event.file
            img_surf = pygame.image.load(event.file)
            img_rect = img_surf.get_rect()
            img_rect.center = (400, 400)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 2:
                if color_picker.rect.left <= event.pos[0] <= color_picker.rect.right and event.pos[1] >= color_picker.rect.bottom+120:
                    pos = event.pos[0] - color_picker.rect.left, event.pos[1] - color_picker.rect.bottom-120
                    index = pos[1]//64*4 + pos[0]//64
                    if index < len(cols): cols.pop(index) 
                
                else:
                    midmousebuttondown = True
            
            elif event.button == 3:
                cols.append(screen.get_at(event.pos)) if screen.get_at(event.pos) not in cols else None
                    
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 2:
                midmousebuttondown = False
        
        elif event.type == pygame.MOUSEMOTION and midmousebuttondown:
            img_rect.centerx += event.rel[0]
            img_rect.centery += event.rel[1]
            
    mouse_pos = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0]:
        if color_picker.rect.collidepoint(mouse_pos): color_picker.hold(mouse_pos)
    
    screen.fill((50, 50, 50))
    screen.blit(img_surf, img_rect)
    screen.fill((30, 30, 30), (800, 0, 400, 800))
    
    button1.draw()
    button2.draw()
    center.draw()
    color_picker.draw(screen)
    
    for i, col in enumerate(cols):
        pygame.draw.rect(screen, col, pygame.Rect(color_picker.rect.left+i%4*64, color_picker.rect.bottom+120+i//4*64, 64, 64))
    
    pygame.display.update()
            
            
pygame.quit()