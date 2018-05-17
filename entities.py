import pygame


INVADER_SPRITE = {
    'path': "img/invader32x32x4.png",
    'width': 32,
    'height': 32,
    'how_many': 4,
    'animation_time': 60
}


EXPLOSION_SPRITE = {
    'path': "img/explode.png",
    'width': 128,
    'height': 128,
    'how_many': 16,
    'animation_time': 30
}


class AnimatedSprite(pygame.sprite.Sprite):

    def __init__(self, path, width, height, how_many, animation_time,
                 position=(0,0)):

        super(AnimatedSprite, self).__init__()

        self.sprite_sheet = pygame.image.load(path).convert_alpha()
        self.width = width
        self.height = height
        self.how_many = how_many

        self.images = []
        self._populate_images()

        self.index = 0

        # sprite.Group.draw will use this properties render to screen
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=position)

        self.animation_time = animation_time
        self.current_time = 0

    def _populate_images(self):
        x = y = 0
        for i in range(0, self.how_many):
            self.images.append(self._get_image(x, y))
            x += self.width

    def _get_image(self, x, y):
        # Create a new blank image
        image = pygame.Surface(
            (self.width, self.height), pygame.SRCALPHA).convert_alpha()

        # Copy the sprite from the large sheet onto the smaller image
        image.blit(
            self.sprite_sheet, (0, 0), (x, y, self.width, self.height))

        return image

    def update(self, dt):

        self.current_time += dt

        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]


class Alien(AnimatedSprite):

    def __init__(self, position):
        super(Alien, self).__init__(position=position, **INVADER_SPRITE)


class Explosion(AnimatedSprite):
    def __init__(self, alien):
        super(Explosion, self).__init__(**EXPLOSION_SPRITE)
        self.rect = self.image.get_rect(center=alien.rect.center)

    def update(self, dt):

        self.current_time += dt

        if self.current_time >= self.animation_time:

            self.current_time = 0
            self.index = self.index + 1

            if self.index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.index]
