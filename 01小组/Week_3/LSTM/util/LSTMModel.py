import torch.nn as nn

class LSTMModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(input_size = 6, 
                            num_layers = 2,
                            hidden_size = 128,  
                            batch_first = True, 
                            bidirectional= True)
        
        self.dropout = nn.Dropout(0.2)
        self.linear1 = nn.Linear(128*2, 64) 
        self.linear2 = nn.Linear(64, 8) 
        self.output_linear = nn.Linear(8, 1)
        
        
    def forward(self, x):  
        x, _ = self.lstm(x)
        x = self.dropout(x)
        x = self.linear1(x)
        x = self.linear2(x)
        x = self.output_linear(x)
        return x