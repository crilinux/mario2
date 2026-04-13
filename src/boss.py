# -*- coding: utf-8 -*-
"""Boss类"""
import pygame
import random
from constants import *

class Boss(pygame.sprite.Sprite):
    """Boss基类"""
    def __init__(self, x, y, boss_id=1):
        super().__init__()
        self.boss_id = boss_id
        self.width = BOSS1_WIDTH if boss_id == 1 else BOSS2_WIDTH
        self.height = BOSS1_HEIGHT if boss_id == 1 else BOSS2_HEIGHT
        self.image = self._create_sprite()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.health = BOSS1_HEALTH if boss_id == 1 else BOSS2_HEALTH
        self.max_health = self.health
        self.speed = BOSS1_SPEED if boss_id == 1 else BOSS2_SPEED
        
        self.velocity = pygame.math.Vector2(0, 0)
        self.direction = -1
        self.on_ground = False
        
        self.is_alive = True
        self.attack_cooldown = 0
        self.current_attack = 0
        self.attack_timer = 0
        
        # 狂暴模式（Boss2）
        self.enraged = False
        self.enrage_threshold = self.max_health // 2
    
    def _create_sprite(self):
        """创建Boss精灵"""
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        if self.boss_id == 1:
            # Boss1 - 红色大怪物
            pygame.draw.rect(surface, RED, (10, 20, 60, 50))  # 身体
            pygame.draw.circle(surface, (255, 200, 150), (25, 15), 12)  # 头
            pygame.draw.circle(surface, (255, 200, 150), (55, 15), 12)
            pygame.draw.circle(surface, BLACK, (25, 15), 4)  # 眼睛
            pygame.draw.circle(surface, BLACK, (55, 15), 4)
            pygame.draw.rect(surface, WHITE, (20, 10, 40, 8))  # 牙齿
            pygame.draw.rect(surface, YELLOW, (15, 70, 15, 10))  # 脚
            pygame.draw.rect(surface, YELLOW, (50, 70, 15, 10))
        else:
            # Boss2 - 更大的黑色盔甲怪
            pygame.draw.rect(surface, PURPLE, (10, 10, 80, 80))  # 身体
            pygame.draw.rect(surface, DARK_GRAY, (15, 15, 70, 70), 3)  # 盔甲
            pygame.draw.circle(surface, RED, (30, 25), 10)  # 眼睛（发光）
            pygame.draw.circle(surface, RED, (70, 25), 10)
            pygame.draw.rect(surface, BLACK, (25, 50, 50, 15))  # 嘴
            pygame.draw.rect(surface, WHITE, (30, 55, 10, 8))  # 牙
            pygame.draw.rect(surface, WHITE, (60, 55, 10, 8))
        
        return surface
    
    def update(self, platforms=None, player=None):
        """更新Boss"""
        if not self.is_alive:
            return
        
        # 检查狂暴
        if self.boss_id == 2 and self.health <= self.enrage_threshold and not self.enraged:
            self.enraged = True
            self.speed *= 1.5
            self.image = self._create_enraged_sprite()
        
        # 攻击冷却
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        # 攻击计时
        if self.attack_timer > 0:
            self.attack_timer -= 1
        
        # 移动
        self._move(platforms, player)
        
        # AI行为
        if self.attack_cooldown == 0:
            self._ai_behavior(player)
    
    def _move(self, platforms, player):
        """Boss移动"""
        if player:
            # 向玩家方向移动
            if self.rect.centerx > player.rect.centerx:
                self.direction = -1
            else:
                self.direction = 1
        
        self.rect.x += self.speed * self.direction
        
        # 边界约束
        if self.rect.left < 0:
            self.rect.left = 0
            self.direction *= -1
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.direction *= -1
    
    def _ai_behavior(self, player):
        """AI行为"""
        if not player:
            return
        
        # 随机选择攻击模式
        if self.boss_id == 1:
            # Boss1: 3种攻击模式
            attack_types = ["jump", "fireball", "charge"]
            self.current_attack = random.choice(attack_types)
        else:
            # Boss2: 5种攻击模式+狂暴
            if self.enraged:
                attack_types = ["jump", "fireball", "charge", "spin", "beam", "rage"]
            else:
                attack_types = ["jump", "fireball", "charge", "spin", "beam"]
            self.current_attack = random.choice(attack_types)
        
        self.attack_cooldown = 120  # 2秒冷却
        self.attack_timer = 60  # 攻击持续1秒
    
    def _create_enraged_sprite(self):
        """创建狂暴状态精灵"""
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # 更恐怖的外观
        pygame.draw.rect(surface, (100, 0, 0), (10, 10, 80, 80))
        pygame.draw.rect(surface, RED, (15, 15, 70, 70), 3)
        pygame.draw.circle(surface, (255, 0, 0), (30, 25), 12)
        pygame.draw.circle(surface, (255, 0, 0), (70, 25), 12)
        pygame.draw.circle(surface, YELLOW, (30, 25), 6)
        pygame.draw.circle(surface, YELLOW, (70, 25), 6)
        pygame.draw.rect(surface, BLACK, (20, 50, 60, 20))
        for i in range(5):
            pygame.draw.rect(surface, WHITE, (25 + i*12, 55, 8, 10))
        return surface
    
    def perform_attack(self, projectiles_group):
        """执行攻击"""
        if self.current_attack == "fireball":
            # 发射火球
            direction = -1 if self.direction > 0 else 1
            from projectile import Projectile
            fireball = Projectile(self.rect.centerx, self.rect.centery, direction, "boss_fire")
            projectiles_group.add(fireball)
        elif self.current_attack == "charge":
            # 冲锋
            self.rect.x += self.direction * 50
    
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
    
    def get_attack_pattern(self):
        """获取攻击模式名称"""
        return self.current_attack


class BossRoom:
    """Boss房间"""
    def __init__(self, boss):
        self.boss = boss
        self.is_active = False
        self.is_completed = False
        self.entrance = None
    
    def activate(self):
        """激活Boss战"""
        self.is_active = True
    
    def complete(self):
        """完成Boss战"""
        self.is_completed = True
        self.is_active = False
    
    def reset(self):
        """重置"""
        self.is_active = False
        self.is_completed = False
