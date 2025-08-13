from objects import Enemy, enemy_spritesheet, frame_width, frame_height, wdt
from random import randint


def CriarInimigosNormais(n):
    from objects import CriarInimigos

    return CriarInimigos(n)


def CriarInimigosColoridos(n):
    inimigos = []
    for _ in range(n):
        enemy = Enemy(
            enemy_spritesheet,
            frame_width,
            frame_height,
            randint(0, wdt - frame_width),
            randint(-100, 0),
            randint(3, 5),
        )

        inimigos.append(enemy)
    return inimigos


def CriarMiniBoss(n=1):
    inimigos = []
    for _ in range(n):
        miniboss = Enemy(
            enemy_spritesheet,
            frame_width,
            frame_height,
            wdt // 2 - frame_width // 2,
            randint(-100, 0),
            randint(4, 6),
        )
        inimigos.append(miniboss)
    return inimigos


def CriarBossFinal(n=1):
    boss = Enemy(
        enemy_spritesheet,
        frame_width,
        frame_height,
        wdt // 2 - frame_width // 2,
        -150,
        3,
    )
    return [boss]


def get_inimigos_para_fase(stage):
    if 1 <= stage <= 3:
        return CriarInimigosNormais(10)
    elif 4 <= stage <= 5:
        return CriarInimigosNormais(5) + CriarInimigosColoridos(5)
    elif 6 <= stage <= 8:
        return CriarMiniBoss(1)
    elif stage == 9:
        return CriarInimigosNormais(7) + CriarInimigosColoridos(7)
    elif stage == 10:
        return CriarBossFinal(1)
    else:
        return CriarInimigosNormais(10)
