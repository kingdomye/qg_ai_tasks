from util.WeatherData import WeatherData
from util.LSTMModel import LSTMModel
import torch.utils.data as data
import torch
import torch.nn as nn
import numpy as np
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

if __name__ == '__main__':
    weather_data = WeatherData()
    train_X, train_y, test_X, test_y, test_df = weather_data.dataset()
    loader = data.DataLoader(data.TensorDataset(train_X, train_y), batch_size = 8, shuffle = True)

    model = LSTMModel()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-5)
    loss_fn = nn.MSELoss()

    epochs = 20
    for epoch in range(epochs):
        model.train()
        for X_batch, y_batch in loader:
            y_pred = model(X_batch)
            loss = loss_fn(y_pred.squeeze(), y_batch)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        model.eval()

        with torch.no_grad():
            y_pred = model(train_X)
            train_rmse = np.sqrt(loss_fn(y_pred, train_y.unsqueeze(2)))
            train_preds = y_pred.clone().detach().numpy()

            y_pred = model(test_X)
            test_rmse = np.sqrt(loss_fn(y_pred, test_y.unsqueeze(2)))
            test_preds = y_pred.clone().detach().numpy()

        print('Epoch: %d, Train RMSE: %.3f, Test RMSE: %.3f' % (epoch + 1, train_rmse, test_rmse))

    # 绘制预测曲线
    eval_df = pd.concat([test_df['meantemp'].reset_index(), pd.Series(test_preds.reshape(-1).tolist())], axis=1).drop('index', axis=1)
    eval_df.columns = ['real_temp', 'pred_temp']
    fig = px.line(eval_df, x=eval_df.index, y=['real_temp', 'pred_temp'], labels={'value': 'Temperature'})
    fig.show()

    # 保存模型
    torch.save(model.state_dict(), './model.pth')
