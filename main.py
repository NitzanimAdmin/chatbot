import pygame

from Classes.Button import Button
from constants import WINDOW_WIDTH, WINDOW_HEIGHT,\
    START_OVER_X, START_OVER_Y, START_OVER_WIDTH, START_OVER_HEIGHT, \
    NUM_OF_ANSWERS, END_OF_CHAT_Y
from database_functions import analyze_data
from helpers import screen, mouse_in_button, display_results, roll_up, \
    next_question_y_pos, calculate_question_answers_height, \
    calculate_pixels_to_rollup


def main():

    pygame.init()
    pygame.display.set_caption('Future teller')
    clock = pygame.time.Clock()

    background = pygame.image.load('images/background.jpg')
    background = pygame.transform.scale(background,
                                        (WINDOW_WIDTH, WINDOW_HEIGHT))
    background_without_chat = pygame.image.load('images'
                                                '/background_without_chat.png')
    background_without_chat = pygame.transform.scale(
        background_without_chat, (WINDOW_WIDTH, WINDOW_HEIGHT))
    questions_array, num_of_question = analyze_data()
    current_question_number = 0
    current_question = questions_array[current_question_number]
    start_over_button = Button(START_OVER_X, START_OVER_Y, START_OVER_WIDTH,
                               START_OVER_HEIGHT)
    displayed_questions = [current_question]
    player_points = 0
    running = True
    finish_questions = False
    done_guess = False
    while running:
        # Grabs events such as key pressed, mouse pressed and so.
        # Going through all the events that happened in the last clock tick
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if done_guess:
                if current_question_number + 1 < num_of_question:
                    current_question_number += 1
                    prev_question = current_question
                    current_question = questions_array[current_question_number]
                    if next_question_y_pos(prev_question) + calculate_question_answers_height(current_question) > END_OF_CHAT_Y:
                        pixel_to_roll_up = calculate_pixels_to_rollup(prev_question, current_question)
                        roll_up(pixel_to_roll_up, displayed_questions)
                    current_question.set_y_pos(next_question_y_pos(prev_question))
                    displayed_questions.append(current_question)
                    done_guess = False
                else:
                    finish_questions = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get the position (x,y) of the mouse press
                mouse_pos = event.pos
                answers_buttons = current_question.answers_buttons()
                for i in range(0, NUM_OF_ANSWERS):
                    if mouse_in_button(answers_buttons[i], mouse_pos):
                        guess = current_question.guess(i)
                        if guess:
                            player_points += 1
                        done_guess = True
                if finish_questions and mouse_in_button(start_over_button,
                                                        mouse_pos):
                    current_question_number = 0
                    player_points = 0
                    finish_questions = False
                    done_guess = False
                    for quest in questions_array:
                        quest.restart()
                    current_question = questions_array[current_question_number]
                    displayed_questions = [current_question]

        screen.blit(background, (0, 0))
        if not finish_questions:
            for display_question in displayed_questions:
                display_question.display()
        else:
            display_results(player_points)
        screen.blit(background_without_chat, (0, 0))
        pygame.display.update()
        clock.tick(60)
    pygame.quit()
    quit()


main()
