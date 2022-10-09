import pygame


TILES = {
    "ground": {"type": "ground", "id": 313},
    "wood": {"type": "interactable", "id": 204},
    "spike": {"type": "interactable", "id": 208},
    #
    "player": {"type": "player", "id": 30},
    "weight": {"type": "weight", "id": 148},
    "box": {"type": "movable", "id": 146},
    #
    "playerEnd": {"type": "interactable", "id": 581},
    "weightEnd": {"type": "interactable", "id": 523},
    "boxEnd": {"type": "interactable", "id": 553},
    #
    "ice": {"type": "interactable", "id": 378},
    "fire": {"type": "interactable", "id": 408},
    "hole": {"type": "interactable", "id": 206},
    #
    "button": {"type": "interactable", "id": 262},
    "heavyButton": {"type": "interactable", "id": 263},
    "slime": {"type": "slime", "id": 527},
    #
    "slimeInverted": {"type": "slime", "id": 266},
}

SOUNDS = {
    "root": "sounds_effects/editor",
    "set": [
        "bloop1.ogg",
        "bloop2.ogg",
        "bloop3.ogg",
        "bloop4.ogg",
        "bloop5.ogg",
        "bloop6.ogg",
        "bloop7.ogg",
        "bloop8.ogg",
        "bloop9.ogg",
        "bloop10.ogg",
    ],
}

# It was designed for 3 columns
# If you're changing that, please, care to change this too :)
TILE_KEYS = [
    pygame.K_1,
    pygame.K_2,
    pygame.K_3,
    #
    pygame.K_q,
    pygame.K_w,
    pygame.K_e,
    #
    pygame.K_a,
    pygame.K_s,
    pygame.K_d,
    #
    pygame.K_z,
    pygame.K_x,
    pygame.K_c,
    #
    pygame.K_4,
    pygame.K_5,
    pygame.K_6,
    #
    pygame.K_r,
    pygame.K_t,
    pygame.K_y,
]

assert len(TILES) <= len(TILE_KEYS)
