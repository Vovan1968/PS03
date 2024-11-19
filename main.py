import requests
from bs4 import BeautifulSoup
from googletrans import Translator

# Создаем экземпляр переводчика
translator = Translator()


# Функция для получения информации с сайта
def get_english_words():
    url = "https://randomword.com/"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Получаем слово
        english_word = soup.find("div", id="random_word").text.strip()
        # Получаем описание слова
        word_definition = soup.find("div", id="random_word_definition").text.strip()

        # Возвращаем результат
        return {
            "english_word": english_word,
            "word_definition": word_definition
        }
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None


# Функция перевода
def translate(text, src_lang, dest_lang):
    try:
        return translator.translate(text, src=src_lang, dest=dest_lang).text
    except Exception as e:
        print(f"Ошибка перевода: {e}")
        return text


# Создаем функцию для игры
def word_game():
    print("Добро пожаловать в игру 'Угадай слово'!")

    while True:
        word_dict = get_english_words()

        if not word_dict:
            print("Не удалось получить слово. Попробуйте позже.")
            break

        english_word = word_dict.get("english_word")
        word_definition = word_dict.get("word_definition")

        # Переводим определение на русский
        russian_definition = translate(word_definition, src_lang="en", dest_lang="ru")
        russian_word = translate(english_word, src_lang="en", dest_lang="ru")

        # Начинаем игру
        print(f"Значение слова (на русском): {russian_definition}")
        user_input = input("Какое это слово? (введите ответ на русском): ").strip().lower()

        # Перевод ответа пользователя на английский для сравнения
        translated_input = translate(user_input, src_lang="ru", dest_lang="en").lower()

        if translated_input == english_word.lower():
            print("Все верно!")
        else:
            print(f"Ответ неверный. Правильное слово: {russian_word} (на английском: {english_word})")

        # Возможность закончить игру
        play_again = input("Хотите сыграть еще раз? (y/n): ").strip().lower()
        if play_again != "y":
            print("Спасибо за игру!")
            break


# Запуск игры
word_game()
