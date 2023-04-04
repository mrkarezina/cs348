import requests
import sys
import inspect

############ run this script in an environment containing the requests module

base_url = "http://localhost:5001/"


##### region_id
def test__region_id__happy_path():
    region = "South America"
    get_data = f"api/region_id?region={region}"
    response = requests.get(base_url + get_data)
    assert response.status_code == 200
    


##### country_rankings_by_stat
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
    assert response.status_code == 200
    assert response.json() == top10population

    # year=2022
    # get_data = f"api/country_rankings_by_stat?stat_name={stat_name}&year={year}"
    # response = requests.get(base_url + get_data)
    # assert response.status_code == 200
    # assert response.json() == top10population

    # year=9999
    # get_data = f"api/country_rankings_by_stat?stat_name={stat_name}&year={year}"
    # response = requests.get(base_url + get_data)
    # assert response.status_code == 200
    # assert response.json() == []

    # stat_name = "Population"
    # limit = 8
    # order_by = "DESC"
    # get_data = f"api/country_rankings_by_stat?stat_name={stat_name}&limit={limit}&order_by={order_by}"
    # response = requests.get(base_url + get_data)
    # assert response.status_code == 200
    # assert response.json() == top10population[:8]

    # stat_name = "area"
    # limit = 3
    # order_by = "ASC"
    # get_data = f"api/country_rankings_by_stat?stat_name={stat_name}&limit={limit}&order_by={order_by}"
    # response = requests.get(base_url + get_data)
    # assert response.status_code == 200
    # assert response.json() == [['VAT', 0], ['MCO', 2], ['GIB', 7]]

    # stat_name = "area"
    # limit = 3
    # order_by = "ASC"
    # region_id = 5
    # get_data = f"api/country_rankings_by_stat?stat_name={stat_name}&limit={limit}&order_by={order_by}&region_id={region_id}"
    # response = requests.get(base_url + get_data)
    # assert response.status_code == 200
    # assert response.json() == [['BVT', 49], ['HMD', 412], ['ATA', 14200000]]


# def test__country_rankings_by_stat__error_check():
#     stat_name = "Pop"
#     limit = 10
#     order_by = "ASC"
#     get_data = f"api/country_rankings_by_stat?stat_name={stat_name}&limit={limit}&order_by={order_by}"
#     response = requests.get(base_url + get_data)
#     assert response.status_code == 400

#     stat_name = "Population"
#     limit = -1
#     order_by = "ASC"
#     get_data = f"api/country_rankings_by_stat?stat_name={stat_name}&limit={limit}&order_by={order_by}"
#     response = requests.get(base_url + get_data)
#     assert response.status_code == 400

#     stat_name = "Population"
#     limit = 10
#     order_by = "lmao"
#     get_data = f"api/country_rankings_by_stat?stat_name={stat_name}&limit={limit}&order_by={order_by}"
#     response = requests.get(base_url + get_data)
#     assert response.status_code == 400



# ##### country_stats
# def test__country_stats__happy_path():
#     country_id = "CHN"
#     get_data = f"api/country_stats?country_id={country_id}"
#     response = requests.get(base_url + get_data)
#     china_stats = {'CHN': {
#         'area': [9596960],
#         'education_expenditure': [3.6],
#         'gini_index': [38.2],
#         'population': [1410539758.0],
#         'real_gdp': [24861000000000.0],
#         'unemployment_rate': [4.82]
#         }}
#     assert response.status_code == 200
#     assert response.json() == china_stats

#     year = 9999
#     get_data = f"api/country_stats?country_id={country_id}&year={year}"
#     response = requests.get(base_url + get_data)
#     china_stats_empty = {'CHN': {
#         'area': None,
#         'education_expenditure': None,
#         'gini_index': None,
#         'population': None,
#         'real_gdp': None,
#         'unemployment_rate': None
#         }}
#     assert response.status_code == 200
#     assert response.json() == china_stats_empty


# def test__country_stats__error_check():
#     # this function shouldnt fail
#     pass



# ##### create_user
# def test__create_user__happy_path():
#     pass


# def test__create_user__error_check():
#     post_url = "/api/create_user"

#     post_data = {"username": "somethsiwdngs", "password": ""}
#     response = requests.post(base_url + post_url, json=post_data)
#     # assert response.status_code == 400
#     # print(response.status_code)
#     # print(response.json())
#     # assert response.json() == {"error": "Please ensure that your password is greater than 7 characters."}



# ##### login_user
# def test__login_user__happy_path():
#     create_user_url = "/api/create_user"
#     login_user_url = "/api/login_user"

#     post_data = {"username": "somethsiwdngs", "password": ""}
#     response = requests.post(base_url + create_user_url, json=post_data)
#     response = requests.post(base_url + login_user_url, json=post_data)
#     assert response.status_code == 200
#     assert response.json() == {"message": "Correct credentials."}

#     post_data = {"username": "somethsiwdngs", "password": "asas"}
#     response = requests.post(base_url + login_user_url, json=post_data)
#     assert response.status_code == 200
#     assert response.json() == {"error": "Incorrect credentials."}


# def test__login_user__error_check():
#     pass











if __name__ == '__main__':
    all_functions = inspect.getmembers(sys.modules[__name__], inspect.isfunction)
    for key, value in all_functions:
        if str(inspect.signature(value)) == "()":
            value()
