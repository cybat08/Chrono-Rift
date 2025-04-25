import pygame
import random
import physics

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

# Music
pygame.mixer.init()
normal_music = None
boss_music = None
try:
    normal_music = pygame.mixer.Sound("assets/normal_music.ogg")
    boss_music = pygame.mixer.Sound("assets/boss_music.ogg")
    normal_music.play(-1)
except:
    print("Music files missing. Skipping music...")

# Load assets
explosion_img = pygame.Surface((32, 32))
explosion_img.fill((255, 128, 0))
spell_particle = pygame.Surface((16, 16))
spell_particle.fill((128, 0, 255))

# Inventory item icons (placeholder squares)
damage_icon = pygame.Surface((20, 20))
damage_icon.fill((255, 0, 0))
speed_icon = pygame.Surface((20, 20))
speed_icon.fill((0, 255, 0))
spell_power_icon = pygame.Surface((20, 20))
spell_power_icon.fill((0, 0, 255))

# Player
player = pygame.Rect(400, 300, 30, 30)
player_radius = 15
player_hp = 100
xp = 0
level = 1
inventory = {
    "damage_up": 0,
    "speed_up": 0,
    "spell_power": 0,
}

# Settings
move_speed = 200
bullets = []
particles = []
drops = []

current_spell = "normal"
spell_data = {
    "normal": {"speed": 300, "damage": 10, "color": (255, 255, 0)},
    "fireball": {"speed": 200, "damage": 20, "color": (255, 0, 0)},
    "lightning": {"speed": 500, "damage": 5, "color": (0, 200, 255)}
}

# Enemies
enemies = []
enemy_hp = {}
boss_mode = False

def spawn_enemy(boss=False):
    size = 30 if not boss else 60
    hp = 30 if not boss else 200
    e = pygame.Rect(random.randint(0, 770), random.randint(0, 570), size, size)
    enemies.append(e)
    enemy_hp[id(e)] = hp

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

    if choosing_upgrade:
        if keys[pygame.K_1]:
            inventory[available_upgrades[0]] += 1
            choosing_upgrade = False
        if keys[pygame.K_2]:
            inventory[available_upgrades[1]] += 1
            choosing_upgrade = False
        if keys[pygame.K_3]:
            inventory[available_upgrades[2]] += 1
            choosing_upgrade = False
        pygame.display.flip()
        continue

    if keys[pygame.K_i]:
        inventory_open = not inventory_open

    if keys[pygame.K_w]: player.move_ip(0, -(move_speed + inventory["speed_up"] * 20) * dt)
    if keys[pygame.K_s]: player.move_ip(0, (move_speed + inventory["speed_up"] * 20) * dt)
    if keys[pygame.K_a]: player.move_ip(-(move_speed + inventory["speed_up"] * 20) * dt, 0)
    if keys[pygame.K_d]: player.move_ip((move_speed + inventory["speed_up"] * 20) * dt, 0)

    if keys[pygame.K_1]: current_spell = "normal"
    if keys[pygame.K_2]: current_spell = "fireball"
    if keys[pygame.K_3]: current_spell = "lightning"

    if keys[pygame.K_SPACE]:
        bullets.append({
            "rect": pygame.Rect(player.centerx, player.centery, 5, 5),
            "spell": current_spell
        })

    if not boss_mode and level % 3 == 0:
        boss_mode = True
        spawn_enemy(boss=True)
        if boss_music:
            normal_music.stop()
            boss_music.play(-1)

    if len(enemies) < 10 and not boss_mode:
        spawn_enemy()

    # Update enemies
    for enemy in enemies:
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        enemy.move_ip(dx * 60 * dt, dy * 60 * dt)

    # Draw player
    pygame.draw.ellipse(screen, (0, 255, 0), player)

    # Draw health bar
    pygame.draw.rect(screen, (255, 0, 0), (10, 10, 100, 10))
    pygame.draw.rect(screen, (0, 255, 0), (10, 10, player_hp, 10))

    # XP + Level
    xp_text = font.render(f"XP: {xp}  Level: {level}", True, (255, 255, 255))
    screen.blit(xp_text, (10, 30))

    # Bullets
    for bullet in bullets[:]:
        spell = spell_data[bullet["spell"]]
        bullet["rect"].move_ip(0, -(spell["speed"] + inventory["spell_power"] * 50) * dt)
        pygame.draw.rect(screen, spell["color"], bullet["rect"])

        for enemy in enemies[:]:
            if physics.check_collision(bullet["rect"].centerx, bullet["rect"].centery, 2,
                                        enemy.centerx, enemy.centery, enemy.width // 2):
                bullets.remove(bullet)
                damage = spell["damage"] + inventory["damage_up"] * 5 + (level - 1) * 5
                enemy_hp[id(enemy)] -= damage
                particles.append({'pos': list(enemy.center), 'timer': 0.5})
                if enemy_hp[id(enemy)] <= 0:
                    enemies.remove(enemy)
                    xp += 10 if enemy.width == 30 else 50
                    if random.random() < 0.5:
                        drops.append({
                            "rect": pygame.Rect(enemy.centerx, enemy.centery, 20, 20),
                            "type": random.choice(["damage_up", "speed_up", "spell_power"])
                        })
                    if enemy.width == 60:  # Boss died
                        boss_mode = False
                        if normal_music:
                            boss_music.stop()
                            normal_music.play(-1)
                break

    # Draw enemies
    for enemy in enemies:
        color = (255, 0, 0) if enemy.width == 30 else (128, 0, 128)
        pygame.draw.ellipse(screen, color, enemy)

    # Particles
    for p in particles[:]:
        p['timer'] -= dt
        if p['timer'] <= 0:
            particles.remove(p)
        else:
            screen.blit(explosion_img, (p['pos'][0] - 16, p['pos'][1] - 16))

    # Drops
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

    # Level up
    if xp >= level * 30:
        level += 1
        xp = 0
        choosing_upgrade = True
        available_upgrades = random.sample(["damage_up", "speed_up", "spell_power"], 3)

    # Inventory Screen
    if inventory_open:
        pygame.draw.rect(screen, (30, 30, 30), (600, 50, 180, 180))
        y = 70
        for item, amount in inventory.items():
            text = font.render(f"{item}: {amount}", True, (255, 255, 255))
            screen.blit(text, (610, y))
            y += 30

    # Upgrade choice screen
    if choosing_upgrade:
        screen.fill((0, 0, 0))
        screen.blit(font.render("LEVEL UP! Choose an upgrade:", True, (255, 255, 255)), (200, 200))
        for i, upg in enumerate(available_upgrades):
            screen.blit(font.render(f"{i+1}. {upg}", True, (255, 255, 0)), (200, 250 + i*40))

    pygame.display.flip()

pygame.quit()
