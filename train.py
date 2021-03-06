from cnn import Net
import data_processing
from data_processing import process_data
import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm

train, test, val = process_data()
device = torch.device('cuda:0')
net = Net().to(device)

def train_model(net):

    X = torch.Tensor([i[0] for i in train]).view(-1, 98, 98).to(device)
    # Normalize data
    X = X / 255.0
    y = torch.Tensor([i[1] for i in train]).to(device)

    optimizer = optim.Adam(net.parameters(), lr=0.001)
    loss_function = nn.MSELoss()

    epochs = 2
    batch_size = 32

    for epoch in tqdm(range(epochs)):
        running_loss = 0.0
        for i in range(0, len(X), batch_size):
            batch_X = X[i: i+batch_size].view(-1, 1, 98, 98).to(device)
            batch_y = y[i: i+batch_size].to(device)

            optimizer.zero_grad()

            outputs = net(batch_X)
            loss = loss_function(outputs, batch_y)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            if i % 512 == 0:
                print('[%d, %5d] loss: %.3f' % (epoch + 1, i + 1, running_loss / 2000))
            running_loss = 0.0

        print('Done.')

def test_model(net):
    correct = 0
    total = 0
    X = torch.Tensor([i[0] for i in test]).view(-1, 98, 98).to(device)
    y = torch.Tensor([i[1] for i in test]).to(device)
    with torch.no_grad():
        for i in tqdm(range(len(X))):
            real_target = torch.argmax(y[i])
            output = net(X[i].view(-1, 1, 98, 98))[0]
            prediction = torch.argmax(output)

            if prediction == real_target:
                correct += 1
            total += 1
    print('Accuracy:', round(correct/total, 4) * 100)
