# -*- coding: utf-8 -*-
"""游戏常量定义"""

# 屏幕设置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Mario-style Game"

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
BROWN = (139, 69, 19)
SKY_BLUE = (135, 206, 235)
GRASS_GREEN = (34, 139, 34)
BRICK_RED = (178, 34, 34)
GRAY = (128, 128, 128)
GOLD = (255, 215, 0)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)

# 玩家物理参数
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_SPEED = 5
JUMP_STRENGTH = -15
GRAVITY = 0.8
MAX_FALL_SPEED = 15
DOUBLE_JUMP_AVAILABLE = True

# 平台参数
PLATFORM_HEIGHT = 20
BRICK_SIZE = 40

# 敌人参数
ENEMY_WIDTH = 40
ENEMY_HEIGHT = 40
ENEMY_SPEED = 2

# Boss参数
BOSS1_WIDTH = 80
BOSS1_HEIGHT = 80
BOSS1_HEALTH = 5
BOSS1_SPEED = 3

BOSS2_WIDTH = 100
BOSS2_HEIGHT = 100
BOSS2_HEALTH = 8
BOSS2_SPEED = 4

# 子弹/火球参数
PROJECTILE_SPEED = 8
PROJECTILE_SIZE = 16
MAX_PROJECTILES = 3

# 游戏状态
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_PAUSED = "paused"
STATE_GAME_OVER = "game_over"
STATE_VICTORY = "victory"
STATE_BOSS_FIGHT = "boss_fight"

# 关卡配置
LEVEL_1_THEME = "grass"
LEVEL_2_THEME = "castle"

# UI参数
UI_FONT_SIZE = 24
UI_HEALTH_BAR_WIDTH = 200
UI_HEALTH_BAR_HEIGHT = 20

# 音效通道
SFX_CHANNEL_JUMP = 0
SFX_CHANNEL_ATTACK = 1
SFX_CHANNEL_HIT = 2
SFX_CHANNEL_COIN = 3
SFX_CHANNEL_BOSS_HIT = 4

# 音效文件路径 (需要在assets/sounds目录下放置对应文件)
SFX_JUMP = "assets/sounds/jump.wav"
SFX_ATTACK = "assets/sounds/attack.wav"
SFX_HIT = "assets/sounds/hit.wav"
SFX_COIN = "assets/sounds/coin.wav"
SFX_BOSS_HIT = "assets/sounds/boss_hit.wav"
SFX_BOSS_DEFEAT = "assets/sounds/boss_defeat.wav"
SFX_LEVEL_COMPLETE = "assets/sounds/level_complete.wav"
SFX_GAME_OVER = "assets/sounds/game_over.wav"
