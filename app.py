import random
import pygame
import sys
from pygame.locals import *

fps = 32
screen_width = 289
screen_height = 511
screen = pygame.display.set_mode((screen_width,screen_height))
ground = screen_height*0.8
game_sprites = {}
game_sounds = {}
player = 'gallery/sprites/bird.png'
background = 'gallery/sprites/background.png'
pipe = 'gallery/sprites/pipe.png'

def welcome():
    playerx = int(screen_width/5)
    playery = int((screen_height - game_sprites['player'].get_height())/2)
    messagex= int((screen_width-game_sprites['message'].get_width())/2)
    messagey = int(screen_height*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                screen.blit(game_sprites['background'],(0,0))
                screen.blit(game_sprites['player'],(playerx,playery))
                screen.blit(game_sprites['message'],(messagex,messagey))
                screen.blit(game_sprites['base'],(basex,ground))
                pygame.display.update()
                clock.tick(fps)

def main():
    score = 0
    playerx = int(screen_width/5)
    playery = int(screen_height/2)
    basex = 0
    pipe1 = getrandompipe()
    pipe2 = getrandompipe()
    upperpipes = [
        {'x': screen_width+200, 'y': pipe1[0]['y']},
        {'x': screen_width+200+(screen_width/2), 'y':pipe2[0]['y']}
    ]
    lowerpipes = [
        {'x': screen_width+200, 'y': pipe1[1]['y']},
        {'x': screen_width+200+(screen_width/2), 'y':pipe2[1]['y']}
    ]
    velx = -4
    vely = -9
    maxv = 10
    minv = -8
    accv = 1

    flapv = -8
    flapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    vely = flapv
                    flapped = True
                    game_sounds['wing'].play()

        crash = iscollide(playerx,playery,upperpipes,lowerpipes)
        if crash:
            return

        playermid = playerx + game_sprites['player'].get_width()/2
        for pipe in upperpipes:
            pipemid = pipe['x'] + game_sprites['pipe'][0].get_width()/2
            if pipemid <= playermid < pipemid+4:
                score += 1
                game_sounds['point'].play()

        if vely < maxv and not flapped:
            vely += accv

        if flapped:
            flapped = False
        playerheight = game_sprites['player'].get_height()
        playery = playery + min(vely,ground - playery - playerheight)

        for upperPipe,lowerPipe in zip(upperpipes,lowerpipes):
            upperPipe['x']+= velx
            lowerPipe['x']+= velx

        if 0<upperpipes[0]['x'] < 5:
            newpipe = getrandompipe()
            upperpipes.append(newpipe[0])
            lowerpipes.append(newpipe[1])

        if upperpipes[0]['x'] < -game_sprites['pipe'][0].get_width():
            lowerpipes.pop(0)
            upperpipes.pop(0)

        screen.blit(game_sprites['background'],( 0, 0))
        for upperPipe,lowerPipe in zip(upperpipes,lowerpipes):
            screen.blit(game_sprites['pipe'][0],(upperPipe['x'],upperPipe['y']))
            screen.blit(game_sprites['pipe'][1],(lowerPipe['x'],lowerPipe['y']))

        screen.blit(game_sprites['base'],(basex,ground))
        screen.blit(game_sprites['player'],(playerx,playery))
        digits = [int(x) for x in list(str(score))]
        width = 0
        for digit in digits:
            width += game_sprites['numbers'][digit].get_width()
        xoffset = (screen_width - width)/2

        for digit in digits:
            screen.blit(game_sprites['numbers'][digit],(xoffset,screen_width*0.12))
            xoffset += game_sprites['numbers'][digit].get_width()
        pygame.display.update()
        clock.tick(fps)

def iscollide(playerx,playery,upperpipes,lowerpipes):
    if playery > ground - 25 or playery < 0:
        game_sounds['hit'].play()
        return True

    for pipe in upperpipes:
        pipeHeight = game_sprites['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < game_sprites['pipe'][0].get_width()):
            game_sounds['hit'].play()
            return True

    for pipe in lowerpipes:
        if (playery + game_sprites['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < game_sprites['pipe'][0].get_width():
            game_sounds['hit'].play()
            return True

    return False

def getrandompipe():
    pipeheight = game_sprites['pipe'][0].get_height()
    offset = screen_height/3
    y2 = offset + random.randrange(0,int(screen_height - game_sprites['base'].get_height() - 1.2*offset))
    y1 = pipeheight - y2 + offset
    pipes = [
        {'x':screen_width+10, 'y': -y1},
        {'x':screen_width+10, 'y': y2}
    ]
    return pipes

if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')
    game_sprites['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )
    game_sprites['message'] = pygame.image.load('gallery/sprites/message.png').convert_alpha()
    game_sprites['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
    game_sprites['pipe'] = (
    pygame.transform.rotate(pygame.image.load(pipe).convert_alpha(),180),
    pygame.image.load(pipe).convert_alpha()
    )

    game_sounds['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    game_sounds['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    game_sounds['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    game_sounds['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    game_sounds['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    game_sprites['background'] = pygame.image.load(background).convert()
    game_sprites['player'] = pygame.image.load(player).convert_alpha()

    while True:
        welcome()
        main()
