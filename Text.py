import pygame

def text_to_screen(screen, text, x, y, size, color, font_type = 'MachineRegular.ttf'):
    try:

        text = str(text)
        font = pygame.font.Font(font_type, size)
        text = font.render(text, True, color)
        screen.blit(text, (x, y))

    except e:
        print('Font Error')
        raise e