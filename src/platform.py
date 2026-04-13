# -*- coding: utf-8 -*-
"""平台类和碰撞检测"""
import pygame
from constants import *

class Platform(pygame.sprite.Sprite):
    """平台类"""
    def __init__(self, x, y, width, height, platform_type="grass"):
        super().__init__()
        self.width = width
        self.height = height
        self.platform_type = platform_type
        self.image = self._create_surface()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def _create_surface(self):
        """创建平台表面"""
        surface = pygame.Surface((self.width, self.height))
        
        if self.platform_type == "grass":
            surface.fill(GRASS_GREEN)
            # 添加草地纹理
            pygame.draw.rect(surface, GREEN, (0, 0, self.width, 5))
        elif self.platform_type == "brick":
            surface.fill(BRICK_RED)
            # 添加砖块纹理
            for i in range(0, self.width, BRICK_SIZE):
                pygame.draw.rect(surface, DARK_GRAY, (i, 0, 1, self.height))
                pygame.draw.rect(surface, DARK_GRAY, (0, self.height//2, self.width, 1))
        elif self.platform_type == "ground":
            surface.fill(BROWN)
            pygame.draw.rect(surface, GRASS_GREEN, (0, 0, self.width, 8))
        elif self.platform_type == "castle":
            surface.fill(GRAY)
            # 城堡石块纹理
            for i in range(0, self.width, 20):
                for j in range(0, self.height, 10):
                    pygame.draw.rect(surface, DARK_GRAY, (i, j, 1, 1))
        
        return surface

class MovingPlatform(Platform):
    """移动平台"""
    def __init__(self, x, y, width, height, move_range=100, move_speed=2):
        super().__init__(x, y, width, height)
        self.start_x = x
        self.move_range = move_range
        self.move_speed = move_speed
        self.direction = 1
    
    def update(self):
        """更新移动平台位置"""
        self.rect.x += self.move_speed * self.direction
        
        if self.rect.x > self.start_x + self.move_range:
            self.direction = -1
        elif self.rect.x < self.start_x - self.move_range:
            self.direction = 1

class Portal(pygame.sprite.Sprite):
    """传送门/出口"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 80))
        self.image.fill(PURPLE)
        # 添加装饰
        pygame.draw.rect(self.image, WHITE, (5, 5, 30, 70), 2)
        pygame.draw.circle(self.image, YELLOW, (20, 20), 8)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - 40

class QuestionBlock(pygame.sprite.Sprite):
    """问号箱"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(BRICK_RED)
        # 绘制问号
        font = pygame.font.Font(None, 36)
        text = font.render("?", True, YELLOW)
        self.image.blit(text, (14, 6))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_empty = False
    
    def hit(self):
        """被撞击时触发"""
        if not self.is_empty:
            self.is_empty = True
            self.image.fill(DARK_GRAY)
            return True
        return False
