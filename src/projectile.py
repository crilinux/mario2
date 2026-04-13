# -*- coding: utf-8 -*-
"""子弹/火球类"""
import pygame
from constants import *

class Projectile(pygame.sprite.Sprite):
    """子弹/火球"""
    def __init__(self, x, y, direction, projectile_type="fireball"):
        super().__init__()
        self.projectile_type = projectile_type
        self.image = self._create_sprite()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.velocity_x = PROJECTILE_SPEED * direction
        self.velocity_y = 0
        self.alive_time = 0
        self.max_alive_time = 300  # 5秒后消失
    
    def _create_sprite(self):
        """创建子弹精灵"""
        surface = pygame.Surface((PROJECTILE_SIZE, PROJECTILE_SIZE), pygame.SRCALPHA)
        
        if self.projectile_type == "fireball":
            # 火球（橙红色渐变）
            pygame.draw.circle(surface, ORANGE, (8, 8), 8)
            pygame.draw.circle(surface, YELLOW, (8, 8), 5)
            pygame.draw.circle(surface, WHITE, (8, 8), 2)
        elif self.projectile_type == "ice":
            # 冰弹（浅蓝色）
            pygame.draw.circle(surface, (173, 216, 230), (8, 8), 8)
            pygame.draw.circle(surface, WHITE, (8, 8), 4)
        elif self.projectile_type == "boss_fire":
            # Boss火球（更大更红）
            surface = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(surface, RED, (10, 10), 10)
            pygame.draw.circle(surface, ORANGE, (10, 10), 7)
            pygame.draw.circle(surface, YELLOW, (10, 10), 4)
        
        return surface
    
    def update(self, platforms=None, enemies=None):
        """更新子弹位置"""
        self.rect.x += self.velocity_x
        self.alive_time += 1
        
        # 超出屏幕移除
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        
        # 超时移除
        if self.alive_time > self.max_alive_time:
            self.kill()
        
        # 平台碰撞
        if platforms:
            hits = pygame.sprite.spritecollide(self, platforms, False)
            if hits:
                self.kill()
        
        # 敌人碰撞
        if enemies:
            hits = pygame.sprite.spritecollide(self, enemies, False)
            if hits:
                for enemy in hits:
                    enemy.take_damage()
                self.kill()

class Attack(pygame.sprite.Sprite):
    """近战攻击（剑击）"""
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.image = pygame.Surface((30, 40), pygame.SRCALPHA)
        self.image.fill((255, 255, 255, 180))
        self.rect = self.image.get_rect()
        
        if player.facing_right:
            self.rect.left = player.rect.right
        else:
            self.rect.right = player.rect.left
        self.rect.y = player.rect.y + 10
        
        self.lifetime = 10  # 攻击持续时间
    
    def update(self):
        """更新攻击"""
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()
        
        # 跟随玩家
        if self.player.facing_right:
            self.rect.left = self.player.rect.right
        else:
            self.rect.right = self.player.rect.left
        self.rect.y = self.player.rect.y + 10
        
        # 淡出效果
        if self.lifetime < 5:
            self.image.set_alpha(int(180 * self.lifetime / 5))
