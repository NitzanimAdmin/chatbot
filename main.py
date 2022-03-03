import pygame

from Classes.Bot import Bot
from constants import WINDOW_WIDTH, WINDOW_HEIGHT
from helpers import screen


def main():

    pygame.init()
    pygame.display.set_caption('ChatBot')
    clock = pygame.time.Clock()

    background = pygame.image.load('images/background.jpg')
    background = pygame.transform.scale(background,
                                        (WINDOW_WIDTH, WINDOW_HEIGHT))
    background_without_chat = pygame.image.load('images'
                                                '/background_without_chat.png')
    background_without_chat = pygame.transform.scale(
        background_without_chat, (WINDOW_WIDTH, WINDOW_HEIGHT))
    bot = Bot()
    running = True
    while running:
        # Grabs events such as key pressed, mouse pressed and so.
        # Going through all the events that happened in the last clock tick
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if bot.done_guessing():
                bot.next_question()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get the position (x,y) of the mouse press
                mouse_pos = event.pos
                bot.check_click(mouse_pos)

        screen.blit(background, (0, 0))
        bot.display_questions()
        screen.blit(background_without_chat, (0, 0))
        pygame.display.update()
        clock.tick(60)
    pygame.quit()
    quit()


main()
