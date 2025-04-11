import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import torch

class WeatherData:
    def __init__(self):
        self.train_df = pd.read_csv('./data/DailyDelhiClimateTrain.csv')
        self.test_df = pd.read_csv('./data/DailyDelhiClimateTest.csv')

    # 计算湿度与气压的比值
    def humidity_pressure_ratio(self, df):
        df['humidity_pressure_ratio'] = df['humidity'] / df['meanpressure']
        return df
    
    # 划分时间
    def get_date_columns(self, date):
        year, month, day = date.split('-')
        return (year, month, day)
    
    # 数据预处理
    def preprocess(self):
        self.train_df = self.humidity_pressure_ratio(self.train_df)
        self.test_df = self.humidity_pressure_ratio(self.test_df)

        tr_date_cols = self.train_df['date'].apply(self.get_date_columns)
        te_date_cols = self.test_df['date'].apply(self.get_date_columns)

        self.train_df[['year', 'month', 'day']] = pd.DataFrame(tr_date_cols.tolist(), index=self.train_df.index)
        self.test_df[['year', 'month', 'day']] = pd.DataFrame(te_date_cols.tolist(), index=self.test_df.index)

        tr_timeseries = self.train_df[['month', 'day', 'humidity', 'wind_speed', 'meanpressure', 'humidity_pressure_ratio', 'meantemp']].values.astype('float32')
        te_timeseries = self.test_df[['month', 'day',  'humidity', 'wind_speed', 'meanpressure', 'humidity_pressure_ratio', 'meantemp']].values.astype('float32')

        new = pd.concat([self.train_df, self.test_df], axis=0).reset_index().drop('index', axis=1)
        new_timeseries = new[['month', 'day',  'humidity', 'wind_speed', 'meanpressure',  'humidity_pressure_ratio', 'meantemp']].values.astype('float32')

        # 数据归一化
        scaler = MinMaxScaler()
        tr_timeseries = scaler.fit_transform(tr_timeseries)
        te_timeseries = scaler.transform(te_timeseries)

        return tr_timeseries, te_timeseries
    
    # 创建数据集
    def dataset(self):
        def create_dataset(dataset, lookback):
            X, y = [], []
            for i in range(len(dataset)-lookback):
                feature = dataset[:,:6][i:i+lookback]
                target = dataset[:, 6][i:i+lookback]
                X.append(feature)
                y.append(target)
            return torch.tensor(X), torch.tensor(y)
        
        lookback = 7
        train, test = self.preprocess()
        train_X, train_y = create_dataset(train, lookback)
        test_X, test_y = create_dataset(test, lookback)

        return train_X, train_y, test_X, test_y