# -*- coding: utf-8 -*-
"""关卡管理"""
import pygame
from constants import *
from platform import Platform, Portal, QuestionBlock

class Level:
    """关卡类"""
    def __init__(self, level_id, theme="grass"):
        self.level_id = level_id
        self.theme = theme
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.portals = pygame.sprite.Group()
        self.question_blocks = pygame.sprite.Group()
        
        self.player_start_pos = (50, SCREEN_HEIGHT - 150)
        self.boss_pos = None
        self.exit_pos = None
        
        self.load_level()
    
    def load_level(self):
        """加载关卡数据"""
        if self.level_id == 1:
            self._create_level_1()
        elif self.level_id == 2:
            self._create_level_2()
    
    def _create_level_1(self):
        """创建关卡1 - 草地主题"""
        # 地面
        self.platforms.add(Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40, "ground"))
        
        # 各层平台
        # 第1层
        self.platforms.add(Platform(150, 480, 200, 20, "grass"))
        self.platforms.add(Platform(450, 480, 150, 20, "grass"))
        
        # 第2层
        self.platforms.add(Platform(50, 380, 150, 20, "grass"))
        self.platforms.add(Platform(300, 350, 200, 20, "grass"))
        self.platforms.add(Platform(600, 380, 150, 20, "grass"))
        
        # 第3层
        self.platforms.add(Platform(200, 250, 180, 20, "grass"))
        self.platforms.add(Platform(500, 220, 150, 20, "grass"))
        
        # 第4层
        self.platforms.add(Platform(100, 150, 150, 20, "grass"))
        self.platforms.add(Platform(400, 120, 200, 20, "grass"))
        
        # 问号箱
        for x in [220, 320, 420]:
            self.question_blocks.add(QuestionBlock(x, 210))
        
        # Boss位置（关卡末尾）
        self.boss_pos = (700, SCREEN_HEIGHT - 160)
        
        # 出口/传送门
        self.exit_pos = (750, SCREEN_HEIGHT - 120)
        self.portals.add(Portal(750, SCREEN_HEIGHT - 120))
        
        self.player_start_pos = (50, SCREEN_HEIGHT - 100)
    
    def _create_level_2(self):
        """创建关卡2 - 城堡主题"""
        # 地面
        self.platforms.add(Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40, "castle"))
        
        # 城堡关卡更复杂的地形
        # 第1层
        self.platforms.add(Platform(100, 500, 120, 20, "brick"))
        self.platforms.add(Platform(300, 480, 180, 20, "castle"))
        self.platforms.add(Platform(550, 500, 150, 20, "brick"))
        
        # 第2层 - 阶梯
        self.platforms.add(Platform(50, 420, 80, 20, "brick"))
        self.platforms.add(Platform(150, 380, 80, 20, "brick"))
        self.platforms.add(Platform(250, 340, 80, 20, "brick"))
        
        # 中间平台区
        self.platforms.add(Platform(350, 320, 200, 20, "castle"))
        
        # 上层
        self.platforms.add(Platform(100, 250, 150, 20, "brick"))
        self.platforms.add(Platform(350, 200, 150, 20, "castle"))
        self.platforms.add(Platform(580, 250, 150, 20, "brick"))
        
        # 顶部
        self.platforms.add(Platform(200, 120, 180, 20, "castle"))
        self.platforms.add(Platform(500, 100, 150, 20, "brick"))
        
        # 问号箱
        for x in [380, 420]:
            self.question_blocks.add(QuestionBlock(x, 280))
        
        # Boss位置
        self.boss_pos = (700, SCREEN_HEIGHT - 160)
        
        # 出口 - 通关点
        self.exit_pos = (750, SCREEN_HEIGHT - 120)
        self.portals.add(Portal(750, SCREEN_HEIGHT - 120))
        
        self.player_start_pos = (50, SCREEN_HEIGHT - 100)
    
    def update(self):
        """更新关卡"""
        self.platforms.update()
        self.portals.update()
    
    def get_player_start(self):
        """获取玩家初始位置"""
        return self.player_start_pos
    
    def get_boss_position(self):
        """获取Boss位置"""
        return self.boss_pos

class LevelManager:
    """关卡管理器"""
    def __init__(self):
        self.current_level = None
        self.level_id = 1
        self.max_levels = 2
        self.levels = {}
        
        # 预加载所有关卡
        for i in range(1, self.max_levels + 1):
            theme = LEVEL_1_THEME if i == 1 else LEVEL_2_THEME
            self.levels[i] = Level(i, theme)
    
    def load_level(self, level_id):
        """加载指定关卡"""
        if level_id in self.levels:
            self.level_id = level_id
            self.current_level = self.levels[level_id]
            return True
        return False
    
    def next_level(self):
        """进入下一关"""
        if self.level_id < self.max_levels:
            return self.load_level(self.level_id + 1)
        return False
    
    def get_current_level(self):
        """获取当前关卡"""
        return self.current_level
    
    def reset(self):
        """重置到第一关"""
        return self.load_level(1)
