from Classes.Question import Question


def analyze_data():
    file = open("data", "r")
    questions_array = []
    for line in file:
        text_array = line.split(", ")
        question_number = text_array[0]
        question_text = text_array[1]
        answers = [text_array[2], text_array[3], text_array[4], text_array[5]]
        correct_answer = int(text_array[6])
        questions_array.append(
            Question(question_number, question_text, answers, correct_answer))
    file.close()
    return questions_array, len(questions_array)
