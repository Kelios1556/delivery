import torch
import math
import torch.nn as nn
import numpy as np

class Generator(nn.Module):
    def __init__(self, input_length):
        super().__init__()
        self.dense_layer = nn.Linear(int(input_length), int(input_length))
        self.activation = nn.Sigmoid()
    def forward(self, x):
        return self.activation(self.dense_layer(x))

class Discriminator(nn.Module):
    def __init__(self, input_length):
        super().__init__()
        self.dense = nn.Linear(int(input_length), 1)
        self.activation = nn.Sigmoid()
    def forward(self, x):
        return self.activation(self.dense(x))

device = ("cuda" if torch.cuda.is_available()
                 else "mps" if torch.backends.mps.is_available()
                 else "cpu"
          )
print(f"Using {device}")

def create_binary(number):
    return [int(x) for x in list(bin(number))[2:]]


def generate_even_data(max_int, batch_size):
    max_length = int(math.log(max_int, 2))

    sample_int = np.random.randint(0, int(max_int / 2), batch_size)

    labels = [[1]] * batch_size

    data = [create_binary(int(x * 2)) for x in sample_int]
    data = [([0] * (max_length - len(x))) + x for x in data]

    return labels, data

def train(max_int=128, batch_size=16, training_steps=500):
    input_length = int(math.log(max_int, 2))
    generator = Generator(input_length).to(device)
    discriminator = Discriminator(input_length).to(device)

    loss = nn.BCELoss()

    gen_optimizer = torch.optim.Adam(generator.parameters(), lr=0.001)
    dis_optimizer = torch.optim.Adam(discriminator.parameters(), lr=0.001)

    for i in range(training_steps):
        gen_optimizer.zero_grad()

        noise = torch.randint(0, 2, size = (batch_size, input_length)).float()
        noise = noise.to(device)
        x = generator(noise)

        real_labels, real_data = generate_even_data(max_int, batch_size)
        real_labels = torch.tensor(real_labels).float()
        real_labels = real_labels.to(device)
        real_data = torch.tensor(real_data).float()
        real_data = real_data.to(device)

        gen_out = discriminator(x)
        gen_loss = loss(gen_out, real_labels)
        gen_loss.backward()
        gen_optimizer.step()

        dis_optimizer.zero_grad()
        dis_out = discriminator(real_data)
        dis_loss = loss(dis_out, real_labels)
        
        gen_out = discriminator(x.detach())
        fake_labels =  [[0]] * batch_size
        fake_labels = torch.tensor(fake_labels).float()
        fake_labels = fake_labels.to(device)
        gen_loss = loss(gen_out, fake_labels)
        dis_loss_ = (dis_loss + gen_loss) / 2
        dis_loss_.backward()
        dis_optimizer.step()

        if(i % 100 == 0):
            print(torch.round(x))

if __name__ == '__main__':
    epochs = 5
    for i in range(epochs):
        train()

