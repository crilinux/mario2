# -*- coding: utf-8 -*-
"""游戏主入口 - 完整版"""
import pygame
import sys
from constants import *
from player import Player
from level import LevelManager
from enemy import Enemy
from boss import Boss, BossRoom
from projectile import Projectile, Attack
from platform import Platform

# 初始化Pygame
pygame.init()

# 创建窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

class Game:
    """游戏主类"""
    def __init__(self):
        self.state = STATE_MENU
        self.level_manager = LevelManager()
        self.current_level = None
        
        # 玩家
        self.player = None
        self.player_group = pygame.sprite.Group()
        
        # 敌人
        self.enemies = pygame.sprite.Group()
        
        # Boss
        self.boss = None
        self.boss_room = None
        
        # 子弹
        self.projectiles = pygame.sprite.Group()
        # 初始化音效系统
        pygame.mixer.init()
        self.sounds = {}
        self._load_sounds()
        self.player_attacks = pygame.sprite.Group()
        
        # UI
        self.font = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # 游戏数据
        self.lives = 3
        self.score = 0
        self.game_over_reason = ""
    
    def _load_sounds(self):
        """加载音效""" 
        try:
            self.sounds["jump"] = pygame.mixer.Sound(SFX_JUMP)
            self.sounds["attack"] = pygame.mixer.Sound(SFX_ATTACK)
            self.sounds["hit"] = pygame.mixer.Sound(SFX_HIT)
            self.sounds["coin"] = pygame.mixer.Sound(SFX_COIN)
            self.sounds["boss_hit"] = pygame.mixer.Sound(SFX_BOSS_HIT)
            self.sounds["boss_defeat"] = pygame.mixer.Sound(SFX_BOSS_DEFEAT)
            self.sounds["level_complete"] = pygame.mixer.Sound(SFX_LEVEL_COMPLETE)
            self.sounds["game_over"] = pygame.mixer.Sound(SFX_GAME_OVER)
            
            # 设置音量
            for sound in self.sounds.values():
                sound.set_volume(0.5)
        except:
            # 如果音效文件不存在，创建静音音效
            self.sounds = {}
            print("Warning: Sound files not found, continuing without sound")
        
    def start_game(self):
        """开始游戏"""
        self.lives = 3
        self.score = 0
        self.level_manager.load_level(1)
        self.current_level = self.level_manager.get_current_level()
        self._spawn_player()
        self._load_enemies()
        self.state = STATE_PLAYING
    
    def _spawn_player(self):
        """生成玩家"""
        if self.current_level:
            start_pos = self.current_level.get_player_start()
            self.player = Player(start_pos[0], start_pos[1], self)
            self.player_group.empty()
            self.player_group.add(self.player)
    
    def _load_enemies(self):
        """加载敌人"""
        self.enemies.empty()
        if self.current_level:
            # 添加一些敌人
            if self.level_manager.level_id == 1:
                self.enemies.add(Enemy(300, SCREEN_HEIGHT - 80, "mushroom"))
                self.enemies.add(Enemy(500, SCREEN_HEIGHT - 80, "mushroom"))
                self.enemies.add(Enemy(200, 430, "turtle"))
            else:
                self.enemies.add(Enemy(250, SCREEN_HEIGHT - 80, "turtle"))
                self.enemies.add(Enemy(450, SCREEN_HEIGHT - 80, "mushroom"))
                self.enemies.add(Enemy(600, SCREEN_HEIGHT - 80, "turtle"))
                self.enemies.add(Enemy(350, 290, "mushroom"))
    
    def update(self):
        """更新游戏"""
        if self.state == STATE_PLAYING:
            self._update_playing()
        elif self.state == STATE_BOSS_FIGHT:
            self._update_boss_fight()
    
    def _update_playing(self):
        """更新游戏状态"""
        keys = pygame.key.get_pressed()
        
        # 玩家输入
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            pass  # 移动在player.update中处理
        
        # 更新玩家
        if self.player and self.player.is_alive:
            self.player.update(self.current_level.platforms, keys)
            
            # 跳跃
            # 攻击
            if keys[pygame.K_f]:
                if self.player.attack():
                    attack = Attack(self.player)
                    self.player_attacks.add(attack)
        elif self.player and not self.player.is_alive:
            self._player_died()
        
        # 更新敌人
        self.enemies.update(self.current_level.platforms)
        
        # 更新子弹
        self.projectiles.update(self.current_level.platforms, self.enemies)
        self.player_attacks.update()
        
        # 碰撞检测
        self._check_collisions()
        
        # 检查关卡完成
        if self.current_level:
            # 检查是否到达Boss位置
            if self.current_level.boss_pos:
                boss_dist = ((self.player.rect.centerx - self.current_level.boss_pos[0])**2 + 
                            (self.player.rect.centery - self.current_level.boss_pos[1])**2) ** 0.5
                if boss_dist < 100:
                    self._start_boss_fight()
            
            # 检查是否到达出口
            for portal in self.current_level.portals:
                if self.player and self.player.rect.colliderect(portal.rect):
                    self._next_level()
    
    def _check_collisions(self):
        """碰撞检测"""
        if not self.player:
            return
        
        # 玩家攻击敌人
        for attack in self.player_attacks:
            hits = pygame.sprite.spritecollide(attack, self.enemies, True)
            for enemy in hits:
                self.score += 100
        
        # 子弹击中敌人
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        for enemy in hits:
            if self.player.take_damage():
                pass
        
        # 敌人碰到平台底部掉落
        for enemy in self.enemies:
            if enemy.rect.top > SCREEN_HEIGHT:
                enemy.kill()
    
    def _start_boss_fight(self):
        """开始Boss战"""
        if self.current_level.boss_pos:
            boss_id = self.level_manager.level_id
            self.boss = Boss(self.current_level.boss_pos[0], self.current_level.boss_pos[1], boss_id, self)
            self.boss_room = BossRoom(self.boss)
            self.boss_room.activate()
            self.state = STATE_BOSS_FIGHT
    
    def _update_boss_fight(self):
        """更新Boss战"""
        keys = pygame.key.get_pressed()
        
        if self.player and self.player.is_alive:
            self.player.update(self.current_level.platforms, keys)
            
            if keys[pygame.K_f]:
                if self.player.attack():
                    attack = Attack(self.player)
                    self.player_attacks.add(attack)
        
        if self.boss and self.boss.is_alive:
            self.boss.update(self.current_level.platforms, self.player)
            self.boss.perform_attack(self.projectiles)
        
        # 更新子弹
        self.projectiles.update(self.current_level.platforms)
        self.player_attacks.update()
        
        # 玩家攻击Boss
        for attack in self.player_attacks:
            if self.boss and self.boss.is_alive and attack.rect.colliderect(self.boss.rect):
                if self.boss.take_damage():
                    self.score += 500
        
        # Boss攻击玩家
        if self.boss and self.boss.is_alive:
            hits = pygame.sprite.spritecollide(self.player, self.projectiles, True)
            if hits:
                self.player.take_damage()
            
            if self.player.rect.colliderect(self.boss.rect):
                self.player.take_damage()
        
        # 检查Boss死亡
        if self.boss and not self.boss.is_alive:
            self.boss_room.complete()
            # 播放Boss击败音效
            if "boss_defeat" in self.sounds:
            print("DEBUG: Playing boss defeat sound")
                self.sounds["boss_defeat"].play()
            # 播放关卡完成音效
            if "level_complete" in self.sounds:
            print("DEBUG: Playing level complete sound")
                self.sounds["level_complete"].play()
            self.score += 1000
            self._next_level()
        
        # 玩家死亡
        if self.player and not self.player.is_alive:
            self._player_died()
    
    def _player_died(self):
        """玩家死亡"""
        self.lives -= 1
        if self.lives > 0:
            # 重生
            if self.current_level:
                start_pos = self.current_level.get_player_start()
                self.player.respawn(start_pos[0], start_pos[1])
        else:
            self.state = STATE_GAME_OVER
            self.game_over_reason = "Game Over"
            # 播放游戏结束音效
            if "game_over" in self.sounds:
            print("DEBUG: Playing game over sound")
                self.sounds["game_over"].play()
    
    def _next_level(self):
        """下一关"""
        if self.level_manager.next_level():
            self.current_level = self.level_manager.get_current_level()
            self._spawn_player()
            self._load_enemies()
            self.projectiles.empty()
            self.player_attacks.empty()
            self.state = STATE_PLAYING
        else:
            # 通关
            self.state = STATE_VICTORY
    
    def draw(self, surface):
        """绘制"""
        if self.state == STATE_MENU:
            self._draw_menu(surface)
        elif self.state == STATE_PLAYING or self.state == STATE_BOSS_FIGHT:
            self._draw_game(surface)
        elif self.state == STATE_GAME_OVER:
            self._draw_game_over(surface)
        elif self.state == STATE_VICTORY:
            self._draw_victory(surface)
    
    def _draw_menu(self, surface):
        """绘制菜单"""
        surface.fill(SKY_BLUE)
        
        title = self.font.render(TITLE, True, WHITE)
        surface.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, SCREEN_HEIGHT//3))
        
        start_text = self.font.render("Press SPACE to Start", True, WHITE)
        surface.blit(start_text, (SCREEN_WIDTH//2 - start_text.get_width()//2, SCREEN_HEIGHT//2))
        
        controls = self.font_small.render("Controls: Arrow Keys=Move, Space=Jump, F=Attack", True, WHITE)
        surface.blit(controls, (SCREEN_WIDTH//2 - controls.get_width()//2, SCREEN_HEIGHT*2//3))
    
    def _draw_game(self, surface):
        """绘制游戏"""
        # 背景
        if self.level_manager.level_id == 1:
            surface.fill(SKY_BLUE)
        else:
            surface.fill(DARK_GRAY)
        
        # 平台
        if self.current_level:
            self.current_level.platforms.draw(surface)
            self.current_level.portals.draw(surface)
            self.current_level.question_blocks.draw(surface)
        
        # 敌人
        self.enemies.draw(surface)
        
        # Boss
        if self.boss and self.boss.is_alive:
            surface.blit(self.boss.image, self.boss.rect)
        
        # 玩家
        if self.player and self.player.is_alive:
            surface.blit(self.player.image, self.player.rect)
        
        # 子弹
        self.projectiles.draw(surface)
        self.player_attacks.draw(surface)
        
        # UI
        self._draw_ui(surface)
    
    def _draw_ui(self, surface):
        """绘制UI"""
        # 生命值
        lives_text = self.font_small.render(f"Lives: {self.lives}", True, WHITE)
        surface.blit(lives_text, (10, 10))
        
        # 分数
        score_text = self.font_small.render(f"Score: {self.score}", True, WHITE)
        surface.blit(score_text, (10, 35))
        
        # 关卡
        level_text = self.font_small.render(f"Level: {self.level_manager.level_id}", True, WHITE)
        surface.blit(level_text, (10, 60))
        
        # 玩家血条
        if self.player:
            health_width = 100
            health_height = 10
            health_ratio = self.player.health / self.player.max_health
            pygame.draw.rect(surface, RED, (10, 85, health_width, health_height))
            pygame.draw.rect(surface, GREEN, (10, 85, health_width * health_ratio, health_height))
        
        # Boss血条
        if self.boss and self.boss.is_alive and self.state == STATE_BOSS_FIGHT:
            boss_health_width = 200
            boss_health_height = 15
            boss_health_ratio = self.boss.health / self.boss.max_health
            pygame.draw.rect(surface, RED, (SCREEN_WIDTH//2 - 100, 10, boss_health_width, boss_health_height))
            pygame.draw.rect(surface, YELLOW, (SCREEN_WIDTH//2 - 100, 10, boss_health_width * boss_health_ratio, boss_health_height))
            boss_label = self.font_small.render("BOSS", True, RED)
            surface.blit(boss_label, (SCREEN_WIDTH//2 - 25, 30))
    
    def _draw_game_over(self, surface):
        """绘制游戏结束"""
        surface.fill(BLACK)
        
        text = self.font.render("GAME OVER", True, RED)
        surface.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - 50))
        
        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        surface.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2 + 10))
        
        restart_text = self.font_small.render("Press SPACE to Restart", True, WHITE)
        surface.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 60))
    
    def _draw_victory(self, surface):
        """绘制胜利"""
        surface.fill(GOLD)
        
        text = self.font.render("VICTORY!", True, WHITE)
        surface.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - 50))
        
        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        surface.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2 + 10))
        
        restart_text = self.font_small.render("Press SPACE to Play Again", True, WHITE)
        surface.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 60))
    
    def handle_event(self, event):
        """处理事件"""
        if event.type == pygame.QUIT:
            return False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            
            if event.key == pygame.K_SPACE:
                if self.state == STATE_MENU:
                    self.start_game()
                elif self.state == STATE_GAME_OVER or self.state == STATE_VICTORY:
                    self.start_game()
            
            if event.key == pygame.K_SPACE and self.state == STATE_PLAYING:
                if self.player and self.player.is_alive:
                    self.player.jump()
            
            if event.key == pygame.K_f and self.state == STATE_PLAYING:
                if self.player and self.player.is_alive:
                    if self.player.attack():
                        attack = Attack(self.player)
                        self.player_attacks.add(attack)
        
        return True
    
    def run(self):
        """运行游戏"""
        running = True
        
        while running:
            for event in pygame.event.get():
                result = self.handle_event(event)
                if result is False:
                    running = False
            
            self.update()
            self.draw(screen)
            
            pygame.display.flip()
            clock.tick(FPS)
        
        pygame.quit()
        sys.exit()


def main():
    """主函数"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
