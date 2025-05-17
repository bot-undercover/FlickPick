import requests

# response = requests.get('https://api.ipify.org?format=json')
# print(response.json()) проверка проходит ли запрос с новым IP

API_KEY = '8de5148e9e940c3c46b688eaf62b6bfe'
BASE_URL = 'https://api.themoviedb.org/3'


def search_movie_by_title(title):
    endpoint = f"{BASE_URL}/search/movie"
    params = {
        'api_key': API_KEY,
        'query': title,
        'language': 'ru-RU'
    }
    try:
        response = requests.get(endpoint, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Ошибка: {response.status_code}")
            return None
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None


def get_movie_details(movie_id):
    endpoint = f"{BASE_URL}/movie/{movie_id}"
    params = {
        'api_key': API_KEY,
        'language': 'ru-RU'
    }
    try:
        response = requests.get(endpoint, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Ошибка: {response.status_code}")
            return None
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None


def get_movie_credits(movie_id):
    endpoint = f"{BASE_URL}/movie/{movie_id}/credits"
    params = {
        'api_key': API_KEY
    }
    try:
        response = requests.get(endpoint, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Ошибка: {response.status_code}")
            return None
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None


if __name__ == "__main__":
    movie_title = "Интерстеллар"
    movies = search_movie_by_title(movie_title)

    if movies and movies.get('results'):
        first_movie = movies['results'][0]
        print(f"Найден фильм: {first_movie['title']} ({first_movie['release_date']})")

        # Получение детальной информации
        movie_id = first_movie['id']
        details = get_movie_details(movie_id)
        if details:
            print("\nДетальная информация:")
            print(f"Описание: {details['overview']}")
            print(f"Рейтинг: {details['vote_average']}")

        credits_data = get_movie_credits(movie_id)
        if credits_data and credits_data.get('crew'):
            director = next((person for person in credits_data['crew'] if person['job'] == 'Director'), None)
            if director:
                print(f"Режиссер: {director['name']}")
            else:
                print("Режиссер не найден.")
        else:
            print("Информация о съемочной группе недоступна.")
    else:
        print("Фильмы не найдены.")