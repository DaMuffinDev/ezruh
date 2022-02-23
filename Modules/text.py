from pyautogui import typewrite, press
from time import sleep as wait
from keyboard import is_pressed
import random

inf = -1

def enter(): press("enter")

def spam_text_file_contents(text_file, delay, repeat_delay, repeat_amount=inf, hotkey="q"):
    """
    :param text - The sentence or word to repeat
    :param delay - The delay before the word spamming happens
    :param repeat_delay - The delay between each loop call
    :param repeat_amount - The amount of times before the scripts 
        (If inf it will stop when the for loop reaches the end of the file's contents)
    :param hotkey - The key to stop the script
    """
    wait(delay)
    with open(text_file, "r") as file:
        for index, word in enumerate(file):
            if is_pressed(hotkey) or index >= repeat_amount:
                break
            typewrite(word)
            enter()
            wait(repeat_delay)

def repeat_random_text_file_contents(text_file, delay, repeat_delay, repeat_amount=inf, hotkey="q"):
    """
    :param text - The sentence or word to repeat
    :param delay - The delay before the word spamming happens
    :param repeat_delay - The delay between each loop call
    :param repeat_amount - The amount of times before the scripts 
        (If inf it will stop when the for loop reaches the end of the file's contents)
    :param hotkey - The key to stop the script
    """
    with open(text_file, "r") as file:
        file_words = []
        for word in file:
            file_words.append(word)

    wait(delay)
    for index in range(0, repeat_amount, 1):
        if is_pressed(hotkey):
            break
        typewrite(random.choice(file_words))
        enter()
        wait(repeat_delay)

def repeat_sentence(text, delay, repeat_delay, repeat_amount=inf, hotkey="q"):
    """
    :param text - The sentence or word to repeat
    :param delay - The delay before the word spamming happens
    :param repeat_delay - The delay between each loop call
    :param repeat_amount - The amount of times before the scripts 
        (If inf it will stop when the for loop reaches the end of the file's contents)
    :param hotkey - The key to stop the script
    """

    wait(delay)
    for index in range(0, repeat_amount, 1):
        if is_pressed(hotkey): break
        typewrite(text)
        enter()
        wait(repeat_delay)