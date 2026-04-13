# -*- coding: utf-8 -*-
"""敌人小怪类"""
import pygame
from constants import *

class Enemy(pygame.sprite.Sprite):
    """敌人基类"""
    def __init__(self, x, y, enemy_type="mushroom"):
        super().__init__()
        self.enemy_type = enemy_type
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.image = self._create_sprite()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.velocity_x = ENEMY_SPEED
        self.direction = 1
        self.on_ground = False
        
        self.health = 1
        self.is_alive = True
        self.damage = 1
    
    def _create_sprite(self):
        """创建敌人精灵"""
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        if self.enemy_type == "mushroom":
            # 蘑菇敌人
            pygame.draw.circle(surface, RED, (20, 15), 15)  # 红色帽子
            pygame.draw.circle(surface, WHITE, (20, 15), 10)  # 白点
            pygame.draw.circle(surface, (255, 200, 150), (20, 30), 12)  # 脸
            pygame.draw.circle(surface, BLACK, (15, 28), 3)  # 眼睛
            pygame.draw.circle(surface, BLACK, (25, 28), 3)
            pygame.draw.rect(surface, BROWN, (8, 40, 24, 10))  # 脚
        
        elif self.enemy_type == "turtle":
            # 乌龟敌人
            pygame.draw.ellipse(surface, GREEN, (5, 15, 30, 20))  # 壳
            pygame.draw.circle(surface, (255, 200, 150), (20, 12), 8)  # 头
            pygame.draw.circle(surface, BLACK, (16, 10), 2)  # 眼睛
            pygame.draw.circle(surface, BLACK, (24, 10), 2)
            pygame.draw.rect(surface, GREEN, (10, 35, 8, 5))  # 脚
            pygame.draw.rect(surface, GREEN, (22, 35, 8, 5))
        
        return surface
    
    def update(self, platforms):
        """更新敌人"""
        if not self.is_alive:
            return
        
        # 应用重力
        self.rect.y += 5
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits:
            self.rect.bottom = hits[0].rect.top
            self.on_ground = True
        self.rect.y -= 5
        
        # 水平移动
        self.rect.x += self.velocity_x * self.direction
        
        # 边界检测
        if self.rect.left < 0:
            self.direction = 1
        if self.rect.right > SCREEN_WIDTH:
            self.direction = -1
        
        # 平台边缘检测 - 掉头
        future_rect = self.rect.copy()
        future_rect.x += self.velocity_x * self.direction * 5
        if not pygame.sprite.spritecollide(self, platforms, False):
            self.direction *= -1
    
    def take_damage(self):
        """受到伤害"""
        self.health -= 1
        if self.health <= 0:
            self.die()
        return self.health <= 0
    
    def die(self):
        """死亡"""
        self.is_alive = False
        self.kill()

class Turtle(Enemy):
    """乌龟（可滚动攻击）"""
    def __init__(self, x, y):
        super().__init__(x, y, "turtle")
        self.is_shell = False
        self.shell_timer = 0
    
    def kick(self):
        """被踢后变成龟壳"""
        self.is_shell = True
        self.velocity_x = 0
        self.image.fill(BLACK)
        pygame.draw.ellipse(self.image, GREEN, (5, 15, 30, 20))
    
    def update(self, platforms):
        """更新乌龟"""
        if self.is_shell:
            if self.shell_timer > 0:
                self.shell_timer -= 1
            return
        
        super().update(platforms)
