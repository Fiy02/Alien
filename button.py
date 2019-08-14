import pygame

class Button():
    """创建开始按钮"""
    def __init__(self,ai_settings,screen,msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        # 设置按钮的大小与其他设置；
        self.width,self.height = 200,50
        self.button_color = (100,100,100)
        self.text_color = (255,255,255)
        # 使用默认字体和字号为48；
        self.font = pygame.font.SysFont(None,48)
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = self.screen_rect.center
        self.prep_msg(msg)

    def prep_msg(self,msg):
        """将字体（msg）渲染为图像，并在按钮上居中"""
        self.msg_image = self.font.render(msg,True,self.text_color,self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """使用 fill 绘制按钮的矩形，使用 blit 关联图像"""
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)