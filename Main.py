import asyncio
import sys
import pygame

pygame.init()
WIDTH, HEIGHT = 900, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mobile Stick Fight")
clock = pygame.time.Clock()

FLOOR_Y = 400
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
RED = (220, 50, 50)
BLUE = (50, 100, 220)
GRAY = (180, 180, 180)


class MobileStickman:

  def __init__(self, x, color):
    self.x = x
    self.y = FLOOR_Y
    self.color = color
    self.vx = 0
    self.vy = 0
    self.is_grounded = True
    self.facing_right = True
    self.attacking = False
    self.attack_timer = 0

  def update(self):
    self.vy += 0.8
    self.x += self.vx
    self.y += self.vy

    if self.y >= FLOOR_Y:
      self.y = FLOOR_Y
      self.vy = 0
      self.is_grounded = True

    self.x = max(20, min(WIDTH - 20, self.x))

    if self.attacking:
      self.attack_timer -= 1
      if self.attack_timer <= 0:
        self.attacking = False

  def draw(self, surface):
    x, y = int(self.x), int(self.y)
    pygame.draw.circle(surface, self.color, (x, y - 60), 12, 3)
    pygame.draw.line(surface, self.color, (x, y - 48), (x, y - 25), 3)
    pygame.draw.line(surface, self.color, (x, y - 25), (x - 8, y), 3)
    pygame.draw.line(surface, self.color, (x, y - 25), (x + 8, y), 3)

    arm_dir = 1 if self.facing_right else -1
    if self.attacking:
      pygame.draw.line(
          surface,
          self.color,
          (x, y - 45),
          (x + arm_dir * 35, y - 45),
          4,
      )
    else:
      pygame.draw.line(
          surface,
          self.color,
          (x, y - 45),
          (x + arm_dir * 15, y - 30),
          3,
      )


async def main():
  player = MobileStickman(150, BLUE)

  btn_left = pygame.Rect(30, 380, 80, 80)
  btn_right = pygame.Rect(130, 380, 80, 80)
  btn_jump = pygame.Rect(670, 380, 80, 80)
  btn_attack = pygame.Rect(770, 380, 80, 80)

  running = True
  while running:
    clock.tick(60)
    screen.fill(WHITE)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False

    mouse_pressed = pygame.mouse.get_pressed()[0]
    touch_pos = pygame.mouse.get_pos()

    player.vx = 0
    if mouse_pressed:
      if btn_left.collidepoint(touch_pos):
        player.vx = -5
        player.facing_right = False
      elif btn_right.collidepoint(touch_pos):
        player.vx = 5
        player.facing_right = True

      if btn_jump.collidepoint(touch_pos) and player.is_grounded:
        player.vy = -14
        player.is_grounded = False

      if btn_attack.collidepoint(touch_pos) and not player.attacking:
        player.attacking = True
        player.attack_timer = 10

    player.update()

    pygame.draw.line(screen, BLACK, (0, FLOOR_Y), (WIDTH, FLOOR_Y), 4)
    player.draw(screen)

    pygame.draw.rect(screen, GRAY, btn_left, border_radius=10)
    pygame.draw.rect(screen, GRAY, btn_right, border_radius=10)
    pygame.draw.rect(screen, RED, btn_jump, border_radius=10)
    pygame.draw.rect(screen, BLUE, btn_attack, border_radius=10)

    font = pygame.font.SysFont(None, 36)
    screen.blit(font.render("<", True, BLACK), (60, 405))
    screen.blit(font.render(">", True, BLACK), (160, 405))
    screen.blit(font.render("JUMP", True, WHITE), (680, 405))
    screen.blit(font.render("HIT", True, WHITE), (790, 405))

    pygame.display.flip()
    await asyncio.sleep(0)

  pygame.quit()
  sys.exit()


if __name__ == "__main__":
  asyncio.run(main())
