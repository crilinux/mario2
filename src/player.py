# -*- coding: utf-8 -*-
"""玩家角色类"""
import pygame
from constants import *

class Player(pygame.sprite.Sprite):
    """玩家角色"""
    def __init__(self, x, y, game=None):
        super().__init__()
        self.game = game
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.image = self._create_sprite()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # 物理属性
        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = False
        self.can_double_jump = DOUBLE_JUMP_AVAILABLE
        self.has_double_jumped = False
        
        # 状态
        self.facing_right = True
        self.is_attacking = False
        self.attack_cooldown = 0
        
        # 生命值
        self.health = 3
        self.max_health = 3
        self.invincible = False
        self.invincible_timer = 0
        self.is_alive = True
        
        # 分数
        self.score = 0
        
        # 动画状态
        self.anim_state = "idle"
        self.anim_frame = 0
        self.anim_timer = 0
    
    def _create_sprite(self):
        """创建玩家精灵（像素风卡通小人）"""
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # 身体（蓝色）
        pygame.draw.rect(surface, BLUE, (8, 20, 24, 30))
        
        # 头
        pygame.draw.circle(surface, (255, 200, 150), (20, 12), 12)
        
        # 眼睛
        pygame.draw.circle(surface, BLACK, (24, 10), 3)
        pygame.draw.circle(surface, BLACK, (16, 10), 3)
        
        # 帽子（红色马里奥风格）
        pygame.draw.rect(surface, RED, (8, 0, 24, 8))
        pygame.draw.rect(surface, RED, (4, 4, 32, 4))
        
        # 背带裤
        pygame.draw.rect(surface, BLUE, (10, 35, 20, 15))
        pygame.draw.rect(surface, YELLOW, (12, 38, 6, 9))
        pygame.draw.rect(surface, YELLOW, (22, 38, 6, 9))
        
        # 鞋
        pygame.draw.rect(surface, BROWN, (8, 50, 14, 10))
        pygame.draw.rect(surface, BROWN, (18, 50, 14, 10))
        
        return surface
    
    def update(self, platforms, keys=None):
        """更新玩家状态"""
        if not self.is_alive:
            return
        
        if keys is None:
            keys = pygame.key.get_pressed()
        
        # 处理无敌时间
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False
        
        # 处理攻击冷却
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        # 应用重力
        self.velocity.y += GRAVITY
        if self.velocity.y > MAX_FALL_SPEED:
            self.velocity.y = MAX_FALL_SPEED
        
        # 水平移动
        self.velocity.x = 0
        if keys[pygame.K_LEFT]:
            self.velocity.x = -PLAYER_SPEED
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.velocity.x = PLAYER_SPEED
            self.facing_right = True
        
        # 更新动画状态
        if self.velocity.x != 0:
            self.anim_state = "run"
        elif self.velocity.y != 0:
            self.anim_state = "jump"
        else:
            self.anim_state = "idle"
        
        # 移动和碰撞检测
        self._move_and_collide(platforms)
        
        # 边界约束
        self._constrain_to_screen()
    
    def _move_and_collide(self, platforms):
        """移动并检测碰撞"""
        # 水平移动
        self.rect.x += self.velocity.x
        hits = pygame.sprite.spritecollide(self, platforms, False)
        for platform in hits:
            if self.velocity.x > 0:
                self.rect.right = platform.rect.left
            elif self.velocity.x < 0:
                self.rect.left = platform.rect.right
        
        # 垂直移动
        self.rect.y += self.velocity.y
        self.on_ground = False
        hits = pygame.sprite.spritecollide(self, platforms, False)
        for platform in hits:
            if self.velocity.y > 0:
                self.rect.bottom = platform.rect.top
                self.velocity.y = 0
                self.on_ground = True
                self.has_double_jumped = False
            elif self.velocity.y < 0:
                self.rect.top = platform.rect.bottom
                # 播放撞击问号箱音效
                if self.game and "coin" in self.game.sounds:
                print("DEBUG: Playing coin sound")
                    self.game.sounds["coin"].play()
                self.velocity.y = 0
    
    def _constrain_to_screen(self):
        """限制在屏幕范围内"""
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity.y = 0
            self.on_ground = True
            self.has_double_jumped = False
        
        # 掉出屏幕底部死亡
        if self.rect.top > SCREEN_HEIGHT:
            self.die()
    
    def jump(self):
        """跳跃"""
        if self.on_ground:
            self.velocity.y = JUMP_STRENGTH
            # 播放跳跃音效
            if self.game and "jump" in self.game.sounds:
                print("DEBUG: Playing jump sound")
                self.game.sounds["jump"].play()
            self.on_ground = False
        elif self.can_double_jump and not self.has_double_jumped:
            self.velocity.y = JUMP_STRENGTH
            # 播放跳跃音效
            if self.game and "jump" in self.game.sounds:
                print("DEBUG: Playing jump sound")
                self.game.sounds["jump"].play()
            self.has_double_jumped = True
    
    def attack(self):
        """攻击"""
        if self.attack_cooldown == 0:
            self.is_attacking = True
            self.attack_cooldown = 30
            # 播放攻击音效
            if "attack" in self.game.sounds:
                print("DEBUG: Playing attack sound")
                self.game.sounds["attack"].play()
            return True
        return False
    
    def take_damage(self):
        """受到伤害"""
        if not self.invincible:
            self.health -= 1
            # 播放受击音效
            if self.game and "hit" in self.game.sounds:
                print("DEBUG: Playing hit sound")
                self.game.sounds["hit"].play()
            self.invincible = True
            self.invincible_timer = 60  # 1秒无敌
            if self.health <= 0:
                self.die()
            return True
        return False
    
    def die(self):
        """死亡"""
        self.is_alive = False
        self.health = 0
    
    def add_score(self, points):
        """加分"""
        self.score += points
    
    def heal(self):
        """回血"""
        if self.health < self.max_health:
            self.health += 1
    
    def respawn(self, x, y):
        """重生"""
        self.rect.x = x
        self.rect.y = y
        self.velocity = pygame.math.Vector2(0, 0)
        self.is_alive = True
        self.health = self.max_health
        self.invincible = True
        self.invincible_timer = 120  # 2秒重生无敌
