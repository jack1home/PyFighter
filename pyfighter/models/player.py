"""Player object for the game."""

from pygame.sprite import Group as SpriteGroup
from pygame import Vector2
from pygame.mask import Mask
from pygame.mixer import Sound
from models.actor import Actor
from constants import (
    IMG_OFFSETS,
    BASE_LASER_SPEED,
    BASE_CANNON_COOLDOWN,
    BASE_LASER_DMG,
)


class Player(Actor):
    """Player object for the game"""

    def __init__(
        self,
        pos: Vector2,
        hp: int,
        speed: int,
        ship_img,
        ship_mask: Mask,
        offset: dict,
        laser_img,
        laser_mask: Mask,
        laser_sfx: Sound,
        laser_hit_sfx: Sound,
        explosion_sfx: Sound,
    ):
        super().__init__(pos, hp, speed, ship_img, ship_mask, offset)
        self.cooldown_threshold = BASE_CANNON_COOLDOWN
        self.cooldown_counter = 0
        self.laser_dmg = BASE_LASER_DMG
        self.missile_count = 0
        self.score = 0
        self.laser_img = laser_img
        self.lasers_fired = SpriteGroup()
        self.laser_mask = laser_mask
        self.laser_offset = IMG_OFFSETS["blueLaser"]
        self.laser_sfx = laser_sfx
        self.laser_hit_sfx = laser_hit_sfx
        self.explosion_sfx = explosion_sfx
        self.cannon_cooldown = PLAYER_BASE_CANNON_COOLDOWN  # added for powerUps by jack
        self.has_missiles = False  
        self.powerup_start_time = time.time()  

    def shoot(self):
        """Appends a new laser to the laser list if the player's cannon is not in cooldown."""
        # 0 = player is ready to fire
        if self.cooldown_counter == 0:
            laser_pos = Vector2((self.pos.x), (self.pos.y - self.offset["y"]))
            laser = Actor(
                laser_pos,
                self.laser_dmg,
                BASE_LASER_SPEED,
                self.laser_img,
                self.laser_mask,
                self.laser_offset,
            )
            self.lasers_fired.add(laser)
            self.laser_sfx.play()
            if self.has_missiles:  # added for powerUps by jack
                # Add missile shooting logic here
                pass  # Placeholder for missile logic
            # Setting to 1 starts timer (see cooldown_cannon())
            self.cooldown_counter = 1

    def resolve_hits(self, laser, objs):
        """Resolves player lasers in the game, a hit = -1 hp on target. If
        the objects hp is <= 0 then method calls kill() on the object."""

        for obj in objs:
            if Actor.resolve_collision(laser, obj):
                obj.hp -= 1
                self.laser_hit_sfx.play()
                if obj.hp <= 0:
                    obj.kill()
                    self.explosion_sfx.play()
                self.lasers_fired.remove(laser)  # Stop drawing laser that hit

    def cooldown_cannon(self):
        """Needs to be called on every frame of the game, once the threshold is
        reached the player can fire again."""

        # If threshold met, then set counter to 0 (player can fire again)
        if self.cooldown_counter >= self.cooldown_threshold:
            self.cooldown_counter = 0
        # Else increase counter (gets closer to threshold)
        elif self.cooldown_counter > 0:
            self.cooldown_counter += 1
