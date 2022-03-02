import pygame

from Classes.Button import Button
from constants import QUESTION_X, \
    QUESTION_Y, QUESTION_FONT_SIZE, ANSWER_BOX_WIDTH, ANSWER_BOX_X, GAP_X, GAP_Y, QUESTION_WIDTH, \
    ANSWER_FONT_SIZE, USER_ANSWER_X, ANSWER_COLOR, BLACK, BOX_MARGIN
from helpers import from_text_to_array, screen, center_text, \
    calculate_sentence_height, get_text_rect


class Question:

    def __init__(self, num_of_question, question_text, answers, correct_answer):
        self.question_text_array = from_text_to_array(question_text,
                                                      QUESTION_WIDTH,
                                                      QUESTION_FONT_SIZE)
        self.answers = answers
        for i in range(0, len(self.answers)):
            answers[i] = from_text_to_array(answers[i], ANSWER_BOX_WIDTH,
                                            ANSWER_FONT_SIZE)
        self.num_of_question = num_of_question
        self.correct_answer = correct_answer
        self.guess_answer_number = -1
        self.question_y_pos = QUESTION_Y

    def display(self):
        self.display_question()
        self.display_answers()
        self.display_user_answer()

    def display_question(self):
        text_rect = get_text_rect(QUESTION_FONT_SIZE,
                                  self.question_text_array[0], BLACK)
        text_height = text_rect.height
        pygame.draw.rect(screen, (255, 255, 255),
                         pygame.Rect(QUESTION_X,
                                     self.question_y_pos,
                                     QUESTION_WIDTH,
                                     self.question_height() + BOX_MARGIN))
        for i in range(0, len(self.question_text_array)):
            text_font = pygame.font.SysFont('chalkduster.ttf',
                                            QUESTION_FONT_SIZE, bold=False)
            text_to_display = text_font.render(self.question_text_array[i],
                                               True, (0, 0, 0))
            screen.blit(text_to_display, (
                QUESTION_X + 5, self.question_y_pos + 5 + (text_height * i)))

    def display_answers(self):
        first_answer_y = self.question_y_pos + self.question_height() + GAP_Y
        answer_box_height = self.calculate_answer_box_height()
        for i in range(0, len(self.answers)):
            color = (255, 255, 255)
            if self.guess_answer_number > -1 and self.guess_answer_number == i:
                if self.guess_answer_number == self.correct_answer:
                    color = (0, 255, 0)
                else:
                    color = (255, 0, 0)
            rect = pygame.draw.rect(screen, color,
                                    pygame.Rect(ANSWER_BOX_X + ((i % 2) * (
                                            ANSWER_BOX_WIDTH + GAP_X)),
                                                first_answer_y + ((i // 2) * (
                                                        answer_box_height + (
                                                        GAP_Y // 2))),
                                                ANSWER_BOX_WIDTH,
                                                answer_box_height))
            for j in range(0, len(self.answers[i])):
                text_font = pygame.font.SysFont('chalkduster.ttf',
                                                QUESTION_FONT_SIZE, bold=False)
                text_to_display = text_font.render(self.answers[i][j],
                                                   True, BLACK)
                text_rect = text_to_display.get_rect()

                text_rect = center_text(rect, text_rect, j,
                                        len(self.answers[i]))
                screen.blit(text_to_display, (text_rect.x, text_rect.y))

    def display_user_answer(self):
        if not self.guess_answer_number == -1:
            rect = pygame.draw.rect(screen, ANSWER_COLOR,
                                    pygame.Rect(USER_ANSWER_X,
                                                self.answers_y_pos()
                                                + (GAP_Y // 2),
                                                ANSWER_BOX_WIDTH,
                                                self.calculate_answer_box_height()))
            for i in range(0, len(self.answers[self.guess_answer_number])):
                text_font = pygame.font.SysFont('chalkduster.ttf',
                                                QUESTION_FONT_SIZE, bold=False)
                text_to_display = text_font.render(
                    self.answers[self.guess_answer_number][i],
                    True, (0, 0, 0))
                text_rect = text_to_display.get_rect()

                text_rect = center_text(rect, text_rect, i,
                                        len(self.answers[i]))
                screen.blit(text_to_display, (text_rect.x, text_rect.y))

    def answers_buttons(self):
        answers_buttons = []
        for i in range(0, len(self.answers)):
            answers_buttons.append(
                Button(ANSWER_BOX_X + ((i % 2) * (
                        ANSWER_BOX_WIDTH + GAP_X)),
                       self.question_y_pos + self.question_height() + GAP_Y + (
                               (i // 2) * (
                               self.calculate_answer_box_height() + (
                               GAP_Y // 2))),
                       ANSWER_BOX_WIDTH,
                       self.calculate_answer_box_height()))
        return answers_buttons

    def guess(self, num_of_answer):
        self.guess_answer_number = num_of_answer
        if self.correct_answer == num_of_answer:
            return True
        else:
            return False

    def restart(self):
        self.guess_answer_number = -1
        self.question_y_pos = QUESTION_Y

    def set_y_pos(self, y_pos):
        self.question_y_pos = y_pos

    def get_y_pos(self):
        return self.question_y_pos

    def answers_y_pos(self):
        return self.question_y_pos + self.question_height() + (
                1.5 * GAP_Y) + 2 * self.calculate_answer_box_height()

    def get_guess_user_answer(self):
        return self.guess_answer_number

    def question_height(self):
        return calculate_sentence_height() * len(self.question_text_array)

    def get_question_text_array(self):
        return self.question_text_array

    def calculate_answer_box_height(self):
        max_height = 0
        for i in range(0, len(self.answers)):
            height = calculate_sentence_height() * len(self.answers[i])
            if height > max_height:
                max_height = height
        return max_height + 5

    def get_answers(self):
        return self.answers
