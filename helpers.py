from math import ceil

import pygame

from constants import WINDOW_WIDTH, WINDOW_HEIGHT, QUESTION_FONT_SIZE, \
    BOX_MARGIN, GAP_Y

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


def from_text_to_array(text, text_box_width, text_font_size):
    text_array = []
    text_to_edit = text
    text_font = pygame.font.SysFont('chalkduster.ttf',
                                    text_font_size, bold=False)
    text_to_display = text_font.render(text,
                                       True, (0, 0, 0))
    text_rect = text_to_display.get_rect()
    if text_rect.width > text_box_width:
        num_of_rows = ceil(text_rect.width / text_box_width)
        line_max_length = int(len(text) / num_of_rows)
        while not (len(text_to_edit) <= 0):
            if len(text_to_edit) <= line_max_length:
                text_to_edit = remove_space_from_start(text_to_edit)
                text_array.append(text_to_edit)
                text_to_edit = ""
            else:
                temp = text_to_edit[0: line_max_length]
                text_to_edit = text_to_edit[line_max_length:]
                if not (temp[-1] == " " or temp[-1] == ","):
                    if not (text_to_edit[0] == ' ' or text_to_edit[0] == ','):
                        while not (temp[-1] == ' ') and not (temp[-1] == ','):
                            text_to_edit = temp[-1] + text_to_edit
                            temp_len = int(len(temp))
                            temp = temp[0: temp_len - 1]
                temp = remove_space_from_start(temp)
                text_array.append(temp)
    else:
        text_array.append(text)
    return text_array


def remove_space_from_start(text):
    new_text = text
    if text[0] == " ":
        new_text = text[1:]
    if text[-1] == " ":
        new_text = text[:-1]
    return new_text


def center_text(rect, text_rect, row_number, num_of_rows):
    horizontal_margin = \
        (rect.height - num_of_rows * text_rect.height) // 2
    width_margin = (rect.width - text_rect.width) // 2
    text_rect.x = rect.x + width_margin
    # Center the text to the center of the post on Y axis
    text_rect.y = (rect.y + horizontal_margin +
                   row_number * text_rect.height)
    return text_rect


def mouse_in_button(button, mouse_pos):
    if button.x_pos + button.width > mouse_pos[0] > button.x_pos and \
            button.y_pos < mouse_pos[1] < button.y_pos + button.height:
        return True


def calculate_sentence_height():
    text_font = pygame.font.SysFont('chalkduster.ttf',
                                    QUESTION_FONT_SIZE, bold=False)
    text_to_display = text_font.render("hello",
                                       True, (0, 0, 0))
    text_rect = text_to_display.get_rect()
    return text_rect.height


def get_text_rect(font_size, text, text_color):
    text_font = pygame.font.SysFont('chalkduster.ttf',
                                    font_size, bold=False)
    text_to_display = text_font.render(
        text,
        True, text_color)
    return text_to_display.get_rect()


def calculate_question_answers_height(question):
    return calculate_question_box_height(
        question) + calculate_answers_box_height(question) + (
                   2 * GAP_Y)


def calculate_question_box_height(question):
    return (calculate_sentence_height() * len(
        question.get_question_text_array())) + BOX_MARGIN


def calculate_answers_box_height(question):
    return 2 * question.calculate_answer_box_height()


def calculate_user_guessed_answer_height(question):
    return calculate_sentence_height() * len(
        question.get_answers()[question.get_guess_user_answer()])

# def load_result_pic():
#     begginer = pygame.image.load('images/begginer 1.jpg')
#     begginer = pygame.transform.scale(begginer,
#                                       (QUESTION_WIDTH, QUESTION_HEIGHT))
#
#     proficient = pygame.image.load('images/proficient.jpg')
#     proficient = pygame.transform.scale(begginer,
#                                         (QUESTION_WIDTH, QUESTION_HEIGHT))
#     expert = pygame.image.load('images/expert.jpg')
#     expert = pygame.transform.scale(begginer,
#                                     (QUESTION_WIDTH, QUESTION_HEIGHT))
#     master = pygame.image.load('images/master.jpg')
#     master = pygame.transform.scale(begginer,
#                                     (QUESTION_WIDTH, QUESTION_HEIGHT))
