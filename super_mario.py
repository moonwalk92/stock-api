#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎮 超级玛丽风格游戏 - Super Mario Style Game
使用 Python + Pygame 开发

控制方式:
    ← → 或 A/D : 左右移动
    空格 或 W   : 跳跃
    R          : 重新开始
    ESC        : 退出游戏

运行:
    python3 super_mario.py
"""

import pygame
import sys
import random

# 初始化 Pygame
pygame.init()

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
GROUND_BROWN = (139, 69, 19)
BRICK_RED = (178, 34, 34)
GOLD = (255, 215, 0)
GREEN = (34, 139, 34)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
MARIO_RED = (255, 0, 0)
MARIO_SKIN = (255, 200, 150)

# 物理常量
GRAVITY = 0.8
JUMP_STRENGTH = -15
MOVE_SPEED = 5


class Player(pygame.sprite.Sprite):
    """玩家角色类"""
    
    def __init__(self, x, y):
        super().__init__()
        # 创建玩家形象（简单的玛丽奥造型）
        self.width = 32
        self.height = 48
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # 绘制玛丽奥
        # 帽子
        pygame.draw.rect(self.image, MARIO_RED, (4, 0, 24, 8))
        pygame.draw.rect(self.image, MARIO_RED, (0, 4, 32, 4))
        # 脸
        pygame.draw.rect(self.image, MARIO_SKIN, (6, 8, 20, 14))
        # 眼睛
        pygame.draw.circle(self.image, BLACK, (12, 12), 2)
        pygame.draw.circle(self.image, BLACK, (20, 12), 2)
        # 胡子
        pygame.draw.rect(self.image, BLACK, (8, 18, 16, 3))
        # 身体
        pygame.draw.rect(self.image, MARIO_RED, (6, 22, 20, 14))
        # 背带裤
        pygame.draw.rect(self.image, BLUE, (6, 32, 20, 12))
        # 腿
        pygame.draw.rect(self.image, BLUE, (6, 44, 8, 4))
        pygame.draw.rect(self.image, BLUE, (18, 44, 8, 4))
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.facing_right = True
        
        # 游戏状态
        self.score = 0
        self.lives = 3
        self.coins = 0
    
    def update(self, platforms, enemies):
        # 水平移动
        keys = pygame.key.get_pressed()
        self.vel_x = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -MOVE_SPEED
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = MOVE_SPEED
            self.facing_right = True
        
        self.rect.x += self.vel_x
        
        # 边界检查
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        
        # 垂直移动（重力）
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        
        # 平台碰撞检测
        self.on_ground = False
        for platform in platforms:
            if self.check_collision(platform):
                # 从上方落在平台上
                if self.vel_y > 0 and self.rect.bottom <= platform.rect.top + self.vel_y + 5:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                # 从下方撞到平台
                elif self.vel_y < 0 and self.rect.top >= platform.rect.bottom + self.vel_y - 5:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0
        
        # 掉出屏幕底部
        if self.rect.top > SCREEN_HEIGHT:
            return False  # 死亡
        
        return True
    
    def check_collision(self, platform):
        """检测与平台的碰撞"""
        return (self.rect.colliderect(platform.rect) and
                abs(self.rect.bottom - platform.rect.top) < 20)
    
    def jump(self):
        """跳跃"""
        if self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False
    
    def draw(self, screen):
        """绘制玩家"""
        screen.blit(self.image, self.rect)
        
        # 显示方向指示
        if not self.facing_right:
            # 简单的镜像效果提示
            pass


class Platform(pygame.sprite.Sprite):
    """平台类"""
    
    def __init__(self, x, y, width, height, platform_type='brick'):
        super().__init__()
        self.image = pygame.Surface((width, height))
        
        if platform_type == 'brick':
            self.image.fill(BRICK_RED)
            # 绘制砖块纹理
            for i in range(0, width, 32):
                for j in range(0, height, 16):
                    pygame.draw.rect(self.image, (150, 30, 30), (i, j, 30, 14), 2)
        elif platform_type == 'ground':
            self.image.fill(GROUND_BROWN)
            # 绘制草地
            pygame.draw.rect(self.image, GREEN, (0, 0, width, 8))
        elif platform_type == 'pipe':
            self.image.fill(GREEN)
            pygame.draw.rect(self.image, (0, 100, 0), (0, 0, width, height), 3)
        elif platform_type == 'question':
            self.image.fill(GOLD)
            pygame.draw.rect(self.image, (200, 170, 0), (0, 0, width, height), 3)
            # 绘制问号
            font = pygame.font.Font(None, 36)
            text = font.render('?', True, BLACK)
            text_rect = text.get_rect(center=(width//2, height//2))
            self.image.blit(text, text_rect)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = platform_type


class Coin(pygame.sprite.Sprite):
    """金币类"""
    
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, GOLD, (10, 10), 10)
        pygame.draw.circle(self.image, (200, 170, 0), (10, 10), 10, 2)
        # 闪光效果
        pygame.draw.circle(self.image, WHITE, (7, 7), 3)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.animation_frame = 0
    
    def update(self):
        """金币动画"""
        self.animation_frame += 1
        # 简单的上下浮动
        offset = abs((self.animation_frame % 60) - 30) / 5
        self.rect.y = self.rect.y + (offset if self.animation_frame % 60 < 30 else -offset)


class Enemy(pygame.sprite.Sprite):
    """敌人类（栗子怪）"""
    
    def __init__(self, x, y, patrol_distance=100):
        super().__init__()
        self.width = 32
        self.height = 32
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # 绘制栗子怪
        # 身体
        pygame.draw.ellipse(self.image, (139, 69, 19), (2, 10, 28, 22))
        # 头
        pygame.draw.ellipse(self.image, (139, 69, 19), (4, 0, 24, 16))
        # 眼睛
        pygame.draw.circle(self.image, WHITE, (10, 8), 5)
        pygame.draw.circle(self.image, WHITE, (22, 8), 5)
        pygame.draw.circle(self.image, BLACK, (10, 8), 2)
        pygame.draw.circle(self.image, BLACK, (22, 8), 2)
        # 眉毛
        pygame.draw.line(self.image, BLACK, (6, 4), (14, 8), 2)
        pygame.draw.line(self.image, BLACK, (26, 4), (18, 8), 2)
        # 脚
        pygame.draw.ellipse(self.image, BLACK, (4, 28, 10, 4))
        pygame.draw.ellipse(self.image, BLACK, (18, 28, 10, 4))
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.vel_x = -2
        self.start_x = x
        self.patrol_distance = patrol_distance
        self.animation_frame = 0
    
    def update(self):
        """敌人移动"""
        self.rect.x += self.vel_x
        
        # 巡逻逻辑
        if abs(self.rect.x - self.start_x) > self.patrol_distance:
            self.vel_x = -self.vel_x
        
        self.animation_frame += 1


class Game:
    """游戏主类"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('🎮 超级玛丽风格游戏 - Super Mario Style')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        self.reset_game()
    
    def reset_game(self):
        """重置游戏"""
        # 玩家
        self.player = Player(50, SCREEN_HEIGHT - 150)
        
        # 平台组
        self.platforms = pygame.sprite.Group()
        self.create_level()
        
        # 金币组
        self.coins = pygame.sprite.Group()
        self.create_coins()
        
        # 敌人组
        self.enemies = pygame.sprite.Group()
        self.create_enemies()
        
        # 游戏状态
        self.game_over = False
        self.win = False
        self.level = 1
    
    def create_level(self):
        """创建关卡"""
        # 地面
        self.platforms.add(Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40, 'ground'))
        
        # 平台
        platforms_data = [
            # 左侧平台
            (100, 450, 150, 32, 'brick'),
            (300, 380, 100, 32, 'brick'),
            (500, 320, 150, 32, 'brick'),
            (200, 250, 100, 32, 'question'),
            (400, 200, 120, 32, 'brick'),
            (650, 250, 100, 32, 'question'),
            # 管道
            (700, SCREEN_HEIGHT - 120, 50, 80, 'pipe'),
            # 高台
            (50, 150, 200, 32, 'brick'),
            (300, 120, 150, 32, 'question'),
        ]
        
        for x, y, w, h, ptype in platforms_data:
            self.platforms.add(Platform(x, y, w, h, ptype))
    
    def create_coins(self):
        """创建金币"""
        coin_positions = [
            (150, 420), (350, 350), (550, 290),
            (250, 220), (450, 170), (700, 220),
            (100, 120), (350, 90),
        ]
        
        for x, y in coin_positions:
            self.coins.add(Coin(x, y))
    
    def create_enemies(self):
        """创建敌人"""
        enemy_positions = [
            (400, SCREEN_HEIGHT - 72, 150),
            (600, SCREEN_HEIGHT - 72, 100),
            (550, 288, 80),
        ]
        
        for x, y, dist in enemy_positions:
            self.enemies.add(Enemy(x, y, dist))
    
    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_w:
                    if not self.game_over:
                        self.player.jump()
                
                if event.key == pygame.K_r:
                    self.reset_game()
                
                if event.key == pygame.K_ESCAPE:
                    return False
        
        return True
    
    def update(self):
        """更新游戏状态"""
        if self.game_over:
            return
        
        # 更新玩家
        alive = self.player.update(self.platforms, self.enemies)
        
        if not alive:
            self.player.lives -= 1
            if self.player.lives <= 0:
                self.game_over = True
            else:
                # 重生
                self.player.rect.x = 50
                self.player.rect.y = SCREEN_HEIGHT - 150
                self.player.vel_y = 0
        
        # 更新敌人
        self.enemies.update()
        
        # 更新金币
        self.coins.update()
        
        # 金币碰撞
        coin_hits = pygame.sprite.spritecollide(self.player, self.coins, True)
        self.player.coins += len(coin_hits)
        self.player.score += len(coin_hits) * 100
        
        # 敌人碰撞
        enemy_hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        for enemy in enemy_hits:
            # 从上方踩死敌人
            if self.player.vel_y > 0 and self.player.rect.bottom < enemy.rect.centery:
                enemy.kill()
                self.player.score += 200
                self.player.vel_y = JUMP_STRENGTH / 2
            else:
                self.player.lives -= 1
                if self.player.lives <= 0:
                    self.game_over = True
                else:
                    self.player.rect.x = 50
                    self.player.rect.y = SCREEN_HEIGHT - 150
                    self.player.vel_y = 0
    
    def draw(self):
        """绘制游戏画面"""
        # 背景
        self.screen.fill(SKY_BLUE)
        
        # 绘制平台
        self.platforms.draw(self.screen)
        
        # 绘制金币
        self.coins.draw(self.screen)
        
        # 绘制敌人
        self.enemies.draw(self.screen)
        
        # 绘制玩家
        self.player.draw(self.screen)
        
        # UI 显示
        self.draw_ui()
        
        # 游戏结束画面
        if self.game_over:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def draw_ui(self):
        """绘制 UI"""
        # 分数
        score_text = self.font.render(f'Score: {self.player.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # 金币
        coin_text = self.font.render(f'Coins: {self.player.coins}', True, GOLD)
        self.screen.blit(coin_text, (10, 45))
        
        # 生命
        lives_text = self.font.render(f'Lives: {self.player.lives}', True, RED)
        self.screen.blit(lives_text, (10, 80))
        
        # 控制提示
        hint_text = self.font.render('← → 移动 | 空格 跳跃 | R 重来 | ESC 退出', True, WHITE)
        self.screen.blit(hint_text, (SCREEN_WIDTH - 450, SCREEN_HEIGHT - 30))
    
    def draw_game_over(self):
        """绘制游戏结束画面"""
        # 半透明遮罩
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        # 游戏结束文字
        game_over_text = self.big_font.render('GAME OVER', True, RED)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
        self.screen.blit(game_over_text, text_rect)
        
        # 最终分数
        final_score = self.font.render(f'Final Score: {self.player.score}', True, WHITE)
        score_rect = final_score.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        self.screen.blit(final_score, score_rect)
        
        # 重来提示
        restart_text = self.font.render('Press R to Restart', True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        self.screen.blit(restart_text, restart_rect)
    
    def run(self):
        """运行游戏主循环"""
        running = True
        
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


def main():
    """主函数"""
    print("=" * 50)
    print("🎮 超级玛丽风格游戏")
    print("=" * 50)
    print("\n控制方式:")
    print("  ← → 或 A/D : 左右移动")
    print("  空格 或 W   : 跳跃")
    print("  R          : 重新开始")
    print("  ESC        : 退出游戏")
    print("\n游戏目标:")
    print("  🟡 收集金币 (+100 分)")
    print("  🍄 踩死敌人 (+200 分)")
    print("  ❤️  避免掉入深渊和碰到敌人")
    print("\n" + "=" * 50)
    print("正在启动游戏...")
    
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
