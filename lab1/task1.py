"""
Робота з текстом. Напишіть функцію, яка приймає рядок як вхідні дані та повертає словник, 
де ключі - це унікальні слова в рядку, а значення - кількість їх появ. 
Створіть та виведіть на екран список, де зберігаються слова, що зустрічаються більше 3 разів.
"""


def input_text():
    text = input("Enter your string: ")

    words = text.lower().split()

    word_count = {}
    for word in words:
        word = word.strip('.,!?:;"')
        if word:
            word_count[word] = word_count.get(word, 0) + 1
    
    frequent_words = []
    for word, count in word_count.items():
        if count > 3:
            frequent_words.append(word)
    
    print("Words that appear more than 3 times: ", frequent_words)

input_text()