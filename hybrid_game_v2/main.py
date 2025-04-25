import pygame
import random
import physics
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

# === Music ===
pygame.mixer.init()
try:
    normal_music = pygame.mixer.Sound("assets/normal_music.ogg")
    boss_music = pygame.mixer.Sound("assets/boss_music.ogg")
    normal_music.play(-1)
except:
    normal_music = None
    boss_music = None
    print("Music not found.")

# === Assets ===
explosion_img = pygame.Surface((32, 32))
explosion_img.fill((255, 128, 0))
spell_particle_img = pygame.Surface((16, 16))
spell_particle_img.fill((128, 0, 255))

damage_icon = pygame.Surface((20, 20))
damage_icon.fill((255, 0, 0))
speed_icon = pygame.Surface((20, 20))
spell_power_icon = pygame.Surface((20, 20))
spell_power_icon.fill((0, 0, 255))

# === Player ===
player = pygame.Rect(400, 300, 30, 30)
player_hp = 100
xp = 0
level = 1
inventory = {"damage_up": 0, "speed_up": 0, "spell_power": 0}
move_speed = 200
bullets = []
particles = []
drops = []
current_weapon = "normal"

# === Weapons ===
weapon_stats = {
    "normal": {"speed": 300, "damage": 10, "color": (255, 255, 0)},
    "fireball": {"speed": 200, "damage": 20, "color": (255, 64, 0)},
    "lightning": {"speed": 500, "damage": 5, "color": (0, 200, 255)},
    "laser": {"speed": 400, "damage": 15, "color": (0, 255, 0)},
    "heavy_cannon": {"speed": 150, "damage": 40, "color": (200, 200, 0)},
}

owned_weapons = ["normal", "fireball", "lightning"]
weapon_index = 0

# === Dash Ability ===
dash_cooldown = 0
dash_ready = True

# === Enemies ===
enemies = []
enemy_hp = {}
boss_mode = False

# === Achievements ===
achievements = {
    "first_blood": False,
    "spell_master": False,
    "boss_slayer": False,
}
achievement_queue = []
achievement_timer = 0

# === Background Stars ===
stars = [[random.randint(0, 800), random.randint(0, 600)] for _ in range(100)]

# === Helper Functions ===
def spawn_enemy(boss=False):
    size = 30 if not boss else 60
    hp = 30 if not boss else 200
    e = pygame.Rect(random.randint(0, 770), random.randint(0, 570), size, size)
    enemies.append(e)
    enemy_hp[id(e)] = hp

def unlock_achievement(name):
    if not achievements[name]:
        achievements[name] = True
        achievement_queue.append(name)

# === Main Game Loop ===
running = True
inventory_open = False
choosing_upgrade = False
available_upgrades = []

while running:
    dt = clock.tick(60) / 1000.0
    screen.fill((10, 10, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # === Dashing ===
    if dash_cooldown > 0:
        dash_cooldown -= dt
    else:
        dash_ready = True

    if keys[pygame.K_LSHIFT] and dash_ready:
        player.move_ip(0, -300 * dt)
        dash_cooldown = 2.0
        dash_ready = False
        particles.append({'pos': list(player.center), 'timer': 0.5})

    # === Move Player ===
    if keys[pygame.K_w]: player.move_ip(0, -(move_speed + inventory["speed_up"] * 20) * dt)
    if keys[pygame.K_s]: player.move_ip(0, (move_speed + inventory["speed_up"] * 20) * dt)
    if keys[pygame.K_a]: player.move_ip(-(move_speed + inventory["speed_up"] * 20) * dt, 0)
    if keys[pygame.K_d]: player.move_ip((move_speed + inventory["speed_up"] * 20) * dt, 0)

    if keys[pygame.K_q]:
        weapon_index = (weapon_index - 1) % len(owned_weapons)
        current_weapon = owned_weapons[weapon_index]
    if keys[pygame.K_e]:
        weapon_index = (weapon_index + 1) % len(owned_weapons)
        current_weapon = owned_weapons[weapon_index]

    # === Shooting ===
    if keys[pygame.K_SPACE]:
        bullets.append({
            "rect": pygame.Rect(player.centerx, player.centery, 5, 5),
            "weapon": current_weapon
        })

    # === Spawn Boss ===
    if not boss_mode and level % 3 == 0:
        boss_mode = True
        spawn_enemy(boss=True)
        if boss_music:
            normal_music.stop()
            boss_music.play(-1)

    # === Enemy Movement (Chase Player) ===
    for enemy in enemies:
        dx = player.centerx - enemy.centerx
        dy = player.centery - enemy.centery
        dist = math.hypot(dx, dy)
        if dist != 0:
            enemy.move_ip((dx/dist)*60*dt, (dy/dist)*60*dt)

    # === Bullets ===
    for bullet in bullets[:]:
        stats = weapon_stats[bullet["weapon"]]
        bullet["rect"].move_ip(0, -(stats["speed"] + inventory["spell_power"] * 50) * dt)
        pygame.draw.rect(screen, stats["color"], bullet["rect"])

        for enemy in enemies[:]:
            if physics.check_collision(bullet["rect"].centerx, bullet["rect"].centery, 2,
                                        enemy.centerx, enemy.centery, enemy.width // 2):
                bullets.remove(bullet)
                damage = stats["damage"] + inventory["damage_up"] * 5 + (level - 1) * 5
                enemy_hp[id(enemy)] -= damage
                particles.append({'pos': list(enemy.center), 'timer': 0.5})
                if enemy_hp[id(enemy)] <= 0:
                    if not achievements["first_blood"]:
                        unlock_achievement("first_blood")
                    enemies.remove(enemy)
                    xp += 10 if enemy.width == 30 else 50
                    if random.random() < 0.5:
                        if random.random() < 0.3:
                            new_weapon = random.choice(["laser", "heavy_cannon"])
                            if new_weapon not in owned_weapons:
                                owned_weapons.append(new_weapon)
                        else:
                            drops.append({
                                "rect": pygame.Rect(enemy.centerx, enemy.centery, 20, 20),
                                "type": random.choice(["damage_up", "speed_up", "spell_power"])
                            })
                    if enemy.width == 60:  # Boss killed
                        unlock_achievement("boss_slayer")
                        boss_mode = False
                        if normal_music:
                            boss_music.stop()
                            normal_music.play(-1)
                break

    # === Drawing Background Stars ===
    for star in stars:
        pygame.draw.circle(screen, (255, 255, 255), (star[0], star[1]), 1)
        star[1] += 40 * dt
        if star[1] > 600:
            star[1] = 0
            star[0] = random.randint(0, 800)

    # === Draw Player ===
    pygame.draw.ellipse(screen, (0, 255, 0), player)

    # === Health, XP, Level Display ===
    pygame.draw.rect(screen, (255, 0, 0), (10, 10, 100, 10))
    pygame.draw.rect(screen, (0, 255, 0), (10, 10, player_hp, 10))
    xp_text = font.render(f"XP: {xp}  Level: {level}", True, (255, 255, 255))
    screen.blit(xp_text, (10, 30))

    # === Draw Enemies ===
    for enemy in enemies:
        color = (255, 0, 0) if enemy.width == 30 else (128, 0, 128)
        pygame.draw.ellipse(screen, color, enemy)

    # === Draw Particles ===
    for p in particles[:]:
        p['timer'] -= dt
        if p['timer'] <= 0:
            particles.remove(p)
        else:
            screen.blit(explosion_img, (p['pos'][0] - 16, p['pos'][1] - 16))

    # === Draw Drops ===
    for drop in drops[:]:
        if drop["type"] == "damage_up":
            screen.blit(damage_icon, drop["rect"])
        elif drop["type"] == "speed_up":
            screen.blit(speed_icon, drop["rect"])
        elif drop["type"] == "spell_power":
            screen.blit(spell_power_icon, drop["rect"])

        if player.colliderect(drop["rect"]):
            inventory[drop["type"]] += 1
            drops.remove(drop)

    # === Level Up ===
    if xp >= level * 30:
        level += 1
        xp = 0

    # === Achievement Popup ===
    if achievement_queue:
        achievement_timer += dt
        if achievement_timer < 2:
            text = font.render(f"🏆 Achievement Unlocked: {achievement_queue[0]}", True, (255, 215, 0))
            screen.blit(text, (200, 50))
        else:
            achievement_queue.pop(0)
            achievement_timer = 0

    pygame.display.flip()

pygame.quit()
