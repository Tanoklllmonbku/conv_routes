import requests


# Ваш API ключ (убедитесь, что он скрыт!)
API_KEY = "c0fd1940-e227-4799-b78b-aa800fed6d53"


# Функция для получения кода города по его названию
def get_city_code(city_name):
    url = f"https://suggests.rasp.yandex.net/all_suggests?format=old&part={city_name}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        try:
            if data and data[1]:
                return data[1][0][0]
            else:
                raise ValueError("Не удалось найти код города.")
        except (ValueError, IndexError) as e:
            print(f"Не удалось найти код города: {e}")
    else:
        print(f"Произошла ошибка. Код состояния: {response.status_code}")


# Основной блок программы
def process_cities(city1, city2,t1, t2):
    # Получаем коды городов
    code1 = get_city_code(city1)
    code2 = get_city_code(city2)
    time1 = t1
    time2 = t2
    sp1 = time1.split("-")
    sp2 = time2.split("-")


    if code1 is not None and code2 is not None:
        # Дата поездки
        DATE = time1

        # Типы транспорта
        TRANSPORT_TYPES = ["train", "plane", "bus"]

        results = []

        for transport_type in TRANSPORT_TYPES:
            # Параметры запроса
            PARAMS = {
                "apikey": API_KEY,
                "format": "json",
                "from": code1,
                "to": code2,
                "transport_types": transport_type,
                # Фильтрация по типу транспорта
                "lang": "ru_RU",
                "page": 1,
                "date": DATE
            }

            # URL для запроса
            URL = "https://api.rasp.yandex.net/v3.0/search/"

            def get_route_data(params):
                response = requests.get(URL, params=params)
                if response.status_code == 200:
                    return response.json()
                else:
                    print(
                        f"Произошла ошибка. Код состояния: {response.status_code}")
                    return None

            route_data = get_route_data(PARAMS)

            if route_data:
                segments = route_data.get("segments", [])
                if segments:
                    for segment in segments:
                        departure_time = segment["departure"]
                        arrival_time = segment["arrival"]
                        from_title = segment["from"]["title"]
                        to_title = segment["to"]["title"]
                        thread_number = segment["thread"].get("number")
                        transport_type = segment["thread"].get(
                            "transport_type")
                        duration_seconds = int(segment["duration"])
                        tt1 = departure_time[:departure_time.find('T')]
                        tt2 = arrival_time[:arrival_time.find('T')]

                        p1 = tt1.split("-")
                        p2 = tt2.split("-")


                        # Преобразование секунд в часы и минуты
                        hours = duration_seconds // 3600
                        minutes = (duration_seconds % 3600) // 60
                        time_in_travel = f"{hours} ч {minutes} мин"
                        if p1[0] <= p2[0] and p1[0] <= sp2[0]:
                            if p1[0] >= sp1[0] and p1[1] >= sp1[1] and p1[2] >= sp1[2]:
                                if p2[0] <= sp2[0] and p2[1] <= sp2[1] and p2[2] <= sp2[2]:
                                    results.append({
                                        "type": transport_type,
                                        "from": from_title,
                                        "to": to_title,
                                        "departure": departure_time,
                                        "arrival": arrival_time,
                                        "travel_time": time_in_travel,
                                        "route_number": thread_number
                                    })
                else:
                    # Сообщение об отсутствии маршрутов для данного типа транспорта
                    results.append({"type": transport_type,
                                    "message": f"{transport_type.capitalize()} маршрутов не найдено"})
            else:
                # Сообщение об отсутствии маршрутов для данного типа транспорта
                results.append({"type": transport_type,
                                "message": f"{transport_type.capitalize()} маршрутов не найдено"})

        return results
    else:
        return None