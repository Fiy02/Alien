import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
from ship import Ship
from time import sleep
from button import Button

def check_keydown_events(event,ai_settings,screen,ship,bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event,ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    """监视键盘和鼠标事件"""
    for event in pygame.event.get():
        # 点击关闭按钮时关闭窗口；
        if event.type == pygame.QUIT:
            sys.exit()

        # 按下键盘与松开事件，让飞船持续移动；
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)

def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
    """点击PLAY事件"""
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True
        # 重置记分牌图像；
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        creat_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

# 发射子弹；
def fire_bullet(ai_settings,screen,ship,bullets):
    """如果没达到限制时，创建一颗子弹，并加入到编组bullets中"""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)

def update_screen(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    """绘制事件"""
    # 每次循环时重绘屏幕；
    screen.fill(ai_settings.bg_color)
    # 自定义背景图
    # background = pygame.image.load("images/bjin.bmp").convert()
    # screen.blit(background, (0, 0))
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # 将飞船绘制在背景前；
    ship.blitme()
    aliens.draw(screen)
    # 显示得分；
    sb.show_score()
    # 游戏在非活动状态时绘制按钮play；
    if not stats.game_active:
        play_button.draw_button()
    # 更新屏幕，让最近绘制的屏幕可见；
    pygame.display.flip()

def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """删除超过窗口的子弹"""
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)

def get_number_aliens_x(ai_settings,alien_width):
    """计算每行可容纳多少个外星人"""
    avaiable_space_x = ai_settings.screen_width - alien_width * 2
    number_alien_x = int(avaiable_space_x / (2 * alien_width))
    return number_alien_x

def get_number_rows(ai_settings,ship_height,alien_height):
    """计算屏幕可容纳多少行"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def creat_fleet(ai_settings,screen,ship,aliens):
    """创建外星人群"""
    alien = Alien(ai_settings,screen)
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    # 创建第一行外星人；
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # 根据每个外星人的位置将其添加到aliens组；
            create_alien(ai_settings,screen,aliens,alien_number,row_number)

def update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """检查是否有外星人位于屏幕边缘，并更新外星人群所有外星人的位置"""
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    # 检查外星人和飞船相撞；
    if pygame.sprite.spritecollideany(ship,aliens):
        # 相撞时重新绘制飞船爆炸图片；
        ship.image = pygame.image.load("images/die.bmp")
        ship.blitme()
        pygame.display.flip()
        ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
        # ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
    # 检查外星人是否抵达屏幕底部；
    check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets)

def check_fleet_edges(ai_settings,aliens):
    """外星人到达边缘时采取的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    """将整群外星人下移，并改变他们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):
    """响应子弹和外星人发碰撞"""
    # 检查并删除碰到子弹的外星人；
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)
    # 删除现有所有子弹，加快速度并创建新的外星人群；
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        # 提高等级；
        stats.level += 1
        sb.prep_level()
        creat_fleet(ai_settings,screen,ship,aliens)

def ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        # 更新记分牌；
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        ship.image = pygame.image.load('images/ship.bmp')
        creat_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_setings,screen,stats,sb,ship,aliens,bullets):
    """警察是否有外星人抵达屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被外星人撞到一样处理；
            ship_hit(ai_setings,screen,stats,sb,ship,aliens,bullets)
            break

def check_high_score(stats,sb):
    """检查是否诞生新的最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()