from util.WeatherData import WeatherData

if __name__ == '__main__':
    weather_data = WeatherData()
    train_X, train_y, test_X, test_y = weather_data.dataset()
    print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)