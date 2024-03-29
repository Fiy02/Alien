import sys
import pygame
from settings import Settings
from ship import Ship
from alien import Alien
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
    # 初始化游戏背景设置；
    pygame.init()
    # 创建 screen 窗口，参数为元组；
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("外星人入侵")
    # 创建play按钮；
    play_button = Button(ai_settings,screen,"play")
    # 创建存储游戏统计信息的实例，并创建记分牌；
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings,screen,stats)
    # 创建一艘飞船；
    ship = Ship(ai_settings,screen)
    # 创建一个用于存储子弹的编组；
    bullets = Group()
    aliens = Group()
    gf.creat_fleet(ai_settings,screen,ship,aliens)

    # 开始游戏的主循环；
    while True:
        # screen.fill(ai_settings.bg_color)
        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)
            gf.update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets)
        gf.update_screen(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)
run_game()