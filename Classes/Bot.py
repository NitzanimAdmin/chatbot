import pygame

from Classes.Button import Button
from constants import START_OVER_X, START_OVER_Y, START_OVER_WIDTH, \
    START_OVER_HEIGHT, END_OF_CHAT_Y, NUM_OF_ANSWERS, START_OVER_BUTTON_COLOR, \
    QUESTION_FONT_SIZE, RESULTS_TEXT_COLOR, CHAT_BOX_WIDTH, QUESTION_X, \
    RESULTS_Y, START_OVER_TEXT_SIZE, START_OVER_TEXT_COLOR, GAP_Y
from database_functions import analyze_data
from helpers import calculate_question_answers_height, \
    mouse_in_button, \
    screen, center_text, calculate_question_box_height, \
    calculate_answers_box_height, calculate_user_guessed_answer_height


class Bot:

    def __init__(self):
        self.questions_array, self.num_of_questions = analyze_data()
        self.current_question_number = 0
        self.current_question = self.questions_array[
            self.current_question_number]
        self.start_over_button = Button(START_OVER_X, START_OVER_Y,
                                        START_OVER_WIDTH, START_OVER_HEIGHT)
        self.displayed_questions = [self.current_question]
        self.player_points = 0
        self.finish_questions = False
        self.done_guess = False

    def next_question(self):
        if self.current_question_number + 1 < self.num_of_questions:
            self.current_question_number += 1
            prev_question = self.current_question
            self.current_question = self.questions_array[
                self.current_question_number]
            if self.next_question_y_pos(
                    prev_question) + calculate_question_answers_height(
                    self.current_question) > END_OF_CHAT_Y:
                self.roll_up(prev_question)
            self.current_question.set_y_pos(self.next_question_y_pos(prev_question))
            self.displayed_questions.append(self.current_question)
            self.done_guess = False
        else:
            self.finish_questions = True

    def check_click(self, mouse_pos):
        self.check_guess(mouse_pos)
        self.start_over(mouse_pos)

    def check_guess(self, mouse_pos):
        answers_buttons = self.current_question.answers_buttons()
        for i in range(0, NUM_OF_ANSWERS):
            if mouse_in_button(answers_buttons[i], mouse_pos):
                guess = self.current_question.guess(i)
                if guess:
                    self.player_points += 1
                self.done_guess = True

    def start_over(self, mouse_pos):
        if self.finish_questions and mouse_in_button(self.start_over_button,
                                                     mouse_pos):
            self.current_question_number = 0
            self.player_points = 0
            self.finish_questions = False
            self.done_guess = False
            for quest in self.questions_array:
                quest.restart()
            self.current_question = self.questions_array[
                self.current_question_number]
            self.displayed_questions = [self.current_question]

    def display_questions(self):
        if not self.finish_questions:
            for display_question in self.displayed_questions:
                display_question.display()
        else:
            self.display_results()

    def done_guessing(self):
        return self.done_guess

    def next_question_y_pos(self, question):
        if not question.get_guess_user_answer() == -1:
            return question.get_y_pos() + \
                                  calculate_question_box_height(question) + \
                                  GAP_Y + (
                                      calculate_answers_box_height(question)) \
                                  + GAP_Y + (
                                      calculate_user_guessed_answer_height(
                                          question))
        else:
            return question.get_y_pos() + calculate_question_box_height(
                question) + \
                                  GAP_Y + calculate_answers_box_height(question)

    def calculate_pixels_to_rollup(self, prev_question):
        return -1 * (END_OF_CHAT_Y - (
                self.next_question_y_pos(
                    prev_question) + calculate_question_answers_height
                (self.current_question)))

    def roll_up(self, prev_question):
        pixel_to_roll_up = self.calculate_pixels_to_rollup(prev_question)
        for display_question in self.displayed_questions:
            display_question.set_y_pos(
                display_question.question_y_pos - pixel_to_roll_up)
            display_question.display()

    def display_results(self):
        start_over_back_rect = pygame.draw.rect(screen, START_OVER_BUTTON_COLOR,
                                                pygame.Rect(START_OVER_X,
                                                            START_OVER_Y,
                                                            START_OVER_WIDTH,
                                                            START_OVER_HEIGHT))
        results_text = pygame.font.SysFont('chalkduster.ttf',
                                           QUESTION_FONT_SIZE, bold=False)
        results_display = results_text.render(
            "You have " + str(self.player_points) + " correct answers!",
            True, RESULTS_TEXT_COLOR)
        results_text_rect = results_display.get_rect()
        width_margin = (CHAT_BOX_WIDTH - results_text_rect.width) // 2
        results_text_rect.x = QUESTION_X + width_margin
        screen.blit(results_display, (
            results_text_rect.x, RESULTS_Y))

        start_over_font = pygame.font.SysFont('chalkduster.ttf',
                                              START_OVER_TEXT_SIZE, bold=False)
        start_over_display = start_over_font.render(
            "START OVER",
            True, START_OVER_TEXT_COLOR)
        start_over_text_rect = start_over_display.get_rect()
        start_over_text_rect = center_text(start_over_back_rect,
                                           start_over_text_rect, 0, 1)
        screen.blit(start_over_display,
                    (start_over_text_rect.x, start_over_text_rect.y))
