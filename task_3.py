import unittest
from selenium import webdriver
from selenium.common import exceptions


class TestCitySelect(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(5)
        self.driver.get('http://2gis.ru/countries/global')

    def tearDown(self):
        self.driver.quit()

    def test_city_search_with_2_symbol(self):
        """
        Steps:
        1.Ввести в строку поиска сочетание из двух букв
        2.Проверить, у всех ли отфильтрованных городов есть это сочетание
        Expected result:
        все сочетания совпадают
        """

        search_class = "world__searchInput"
        country_closed_xpath = '//*[@class="world__section _collapsed"]'
        cities_xpath = '//*[@class="world__list"]'
        symbols = 'Во'
        symbols_eng = 'Vo'

        self.driver.find_element_by_class_name(search_class).send_keys(symbols)
        list = self.driver.find_elements_by_xpath(country_closed_xpath)
        count_countries = len(list)+1

        for j in range(count_countries):
            list = self.driver.find_elements_by_xpath(cities_xpath + '/li')
            count_cities = len(list)

            for i in range(count_cities):
                xpath = cities_xpath + '[' + str(j + 1) + ']/li[' + str(i + 1) + ']/h2/a/span'
                try:
                    text = self.driver.find_element_by_xpath(xpath).text
                except exceptions.NoSuchElementException:
                    text = ''
                if text == symbols or text == symbols.lower() or text == symbols_eng or text == symbols_eng.lower():
                    continue
                else:
                    xpath = cities_xpath + '[' + str(j + 1) + ']/li[' + str(i + 1) + ']/ul/li/span'
                    try:
                        text = self.driver.find_element_by_xpath(xpath).text
                        if text == symbols or text == symbols.lower() or text == symbols_eng or text == symbols_eng.lower():
                            continue
                        else:
                            self.fail('wrong search')
                    except exceptions.NoSuchElementException:
                        self.fail('matches not found')
        pass

    def test_city_search_with_1_symbols(self):
        """
        Steps:
        1. Ввести одну букву в строку поиска
        2. Проверить, что ничего не отфильтровалось(количество городов в странах осталось преждним)
        Expected result:
        количество городов то же
        """

        search_class = "world__searchInput"
        country_closed_xpath = '//*[@class="world__section _collapsed"]'
        country_open_xpath = '//*[@class="world__sectionHeader"]'
        symbols = 'А'
        count_massive = []
        list = self.driver.find_elements_by_xpath(country_closed_xpath)
        count_countries = len(list)

        for i in range(count_countries):
            count_xpath = country_closed_xpath + '[' + str(i + 1) + ']/header/div/span'
            count_massive.append(int(self.driver.find_element_by_xpath(count_xpath).text))

        self.driver.find_element_by_class_name(search_class).send_keys(symbols)
        self.driver.find_element_by_xpath(country_open_xpath).click()

        for i in range(count_countries):
            count_xpath = country_closed_xpath + '[' + str(i + 1) + ']/header/div/span'
            count_now = int(self.driver.find_element_by_xpath(count_xpath).text)
            self.assertEqual(count_massive[i], count_now)

    def test_search_with_500_or_more_symbols(self):
        """
        Steps:
        1. ввести в строку поиска 500 символов
        2. посмотреть, сколько символов ввелось
        3. ввести в строку поиска 501 символ
        4. посмотреть сколько символов ввелось
        Expected result:
        в обоих случаях должно быть введено 500 символов
        """

        search_element = self.driver.find_element_by_class_name("world__searchInput")
        max_symbols = 500

        symbols = 's' * max_symbols
        search_element.send_keys(symbols)
        count = len(search_element.get_attribute('value'))
        self.assertEqual(count, max_symbols)
        search_element.clear()

        symbols += 's'
        search_element.send_keys(symbols)
        count = len(search_element.get_attribute('value'))
        self.assertEqual(count, max_symbols)

    def test_choice_city_from_list(self):
        """
        Steps:
        1. раскрыть вкладку страны
        2. выбрать город
        3. проверить, что перешли к карте того города, который выбрали
        Expected result:
        перешли к ожидаемому городу
        """

        country_closed_xpath = '//*[@class="world__section _collapsed"]'
        country_open_xpath = '//*[@class="world__listItem"]'
        city_name_xpath = '//*[@class="dashboard__cityName"]/a'

        self.driver.find_element_by_xpath(country_closed_xpath).click()
        city_in_list = self.driver.find_element_by_xpath(country_open_xpath + '/h2/a').text
        self.driver.find_element_by_xpath(country_open_xpath).click()
        city_on_map = self.driver.find_element_by_xpath(city_name_xpath).text
        self.assertEqual(city_in_list, city_on_map)

    def test_choice_city_from_map(self):
        """
        Steps:
        1. нажать на значек страны на карте
        2. нажать на значек города на карте
        3. проверить, что перешли к карте того города, который выбирали
        Expected result:
        города совпадают
        """

        countries_map_xpath = '//*[@class="leaflet-pane leaflet-globalCountry-pane"]/div'
        cities_map_xpath = '//*[@class="leaflet-pane leaflet-globalCity-pane"]/div'
        city_name_xpath = '//*[@class="dashboard__cityName"]/a'

        self.driver.find_element_by_xpath(countries_map_xpath).click()
        city_name_on_cities_map = self.driver.find_element_by_xpath(cities_map_xpath + '/div').text
        self.driver.find_element_by_xpath(cities_map_xpath).click()
        city_name_on_map = self.driver.find_element_by_xpath(city_name_xpath).text
        self.assertEqual(city_name_on_cities_map, city_name_on_map)


if __name__ == "__main__":
    unittest.main()
