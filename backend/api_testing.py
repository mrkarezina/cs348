import requests
import sys
import inspect

############ run this script in an environment containing the requests module

base_url = "http://localhost:5001/"


def test__country_rankings_by_stat__happy_path():
    stat_name = "Population"
    get_data = f"api/country_rankings_by_stat?stat_name={stat_name}"
    response = requests.get(base_url + get_data)
    top10population = [['CHN', 1410539758.0],
                       ['IND', 1389637446.0],
                       ['USA', 337341954.0],
                       ['IDN', 277329163.0],
                       ['PAK', 242923845.0],
                       ['NGA', 225082083.0],
                       ['BRA', 217240060.0],
                       ['BGD', 165650475.0],
                       ['RUS', 142021981.0],
                       ['MEX', 129150971.0]]
    assert response.status_code == 201
    assert response.json() == top10population

    stat_name = "Population"
    limit = 8
    order_by = "DESC"
    get_data = f"api/country_rankings_by_stat?stat_name={stat_name}&limit={limit}&order_by={order_by}"
    response = requests.get(base_url + get_data)
    assert response.status_code == 201
    assert response.json() == top10population[:8]

    stat_name = "area"
    limit = 3
    order_by = "ASC"
    get_data = f"api/country_rankings_by_stat?stat_name={stat_name}&limit={limit}&order_by={order_by}"
    response = requests.get(base_url + get_data)
    bottom3area = [['VAT', 0], ['MCO', 2], ['GIB', 7]]
    assert response.status_code == 201
    assert response.json() == bottom3area


def test__country_rankings_by_stat__error_check():
    stat_name = "Pop"
    limit = 10
    order_by = "ASC"
    get_data = f"api/country_rankings_by_stat?stat_name={stat_name}&limit={limit}&order_by={order_by}"
    response = requests.get(base_url + get_data)
    assert response.status_code == 400

    stat_name = "Population"
    limit = -1
    order_by = "ASC"
    get_data = f"api/country_rankings_by_stat?stat_name={stat_name}&limit={limit}&order_by={order_by}"
    response = requests.get(base_url + get_data)
    assert response.status_code == 400

    stat_name = "Population"
    limit = 10
    order_by = "lmao"
    get_data = f"api/country_rankings_by_stat?stat_name={stat_name}&limit={limit}&order_by={order_by}"
    response = requests.get(base_url + get_data)
    assert response.status_code == 400




















if __name__ == '__main__':
    all_functions = inspect.getmembers(sys.modules[__name__], inspect.isfunction)
    for key, value in all_functions:
        if str(inspect.signature(value)) == "()":
            value()
