import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self,ai_settings,screen):
        """初始化飞船及位置"""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load('images/ship.bmp')      # 加载飞船图片;
        self.rect = self.image.get_rect()                   # 获取图片矩形；
        self.screen_rect = screen.get_rect()                # 获取窗口矩形；
        # 使图片的矩形位置等同于窗口的矩形位置，底部居中；
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        # 在飞船的属性center中存储小数值；
        self.center = float(self.rect.centerx)
        # 移动标志，默认不移动；
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """更新飞船的center值,调用时移动飞船位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # 根据self.center更新rect对象；
        self.rect.centerx = self.center

    # 在指定位置绘制飞船；
    def blitme(self):
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        self.center = self.screen_rect.centerx