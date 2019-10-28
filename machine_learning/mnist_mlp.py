from __future__ import print_function
import argparse
import time

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms


class MLPNet(nn.Module):
    def __init__(self):
        super(MLPNet, self).__init__()
        self.fc1 = nn.Linear(28 * 28, 500)
        self.fc2 = nn.Linear(500, 256)
        self.fc3 = nn.Linear(256, 10)

    def forward(self, x):
        x = x.view(-1, 28 * 28)
        x = F.leaky_relu(self.fc1(x))
        x = F.leaky_relu(self.fc2(x))
        x = self.fc3(x)
        return F.softmax(x, dim=1)


def train(args, model, device, train_loader, optimizer, epoch):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        #print(output, target)
        loss = F.cross_entropy(output, target)
        # loss = F.nll_loss(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % args.log_interval == 0:
            print('Train Epoch: {0} [{1}/{2} ({3:.1f}%)]\tLoss: {4:.4f}'.format(
                epoch,
                batch_idx * len(data),
                len(train_loader.dataset),
                100. * batch_idx / len(train_loader),
                loss.item()
            ))


def test(model, device, test_loader):
    start_time = time.time()

    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.cross_entropy(output, target, reduction='sum').item()  # sum up batch loss
            pred = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability
            correct += pred.eq(target.view_as(pred)).sum().item()

    end_time = time.time()
    test_milli_time_for_one_sample = (end_time - start_time) * 1000 / len(test_loader.dataset)
    test_loss /= len(test_loader.dataset)

    print('\nTest set: Average loss: {0:.4f}, Accuracy: {1}/{2} ({3:.1f}%), Test Time for One Sample: {4:.4f}ms.\n'.format(
        test_loss,
        correct,
        len(test_loader.dataset),
        100. * correct / len(test_loader.dataset),
        test_milli_time_for_one_sample
    ))


def arg_parse():
    # Training settings
    parser = argparse.ArgumentParser(description='PyTorch MNIST Example')
    parser.add_argument(
        '--batch-size', type=int, default=64,
        help='input batch size for training (default: 64)'
    )
    parser.add_argument(
        '--test-batch-size', type=int, default=1000,
        help='input batch size for testing (default: 1000)'
    )

    parser.add_argument(
        '--epochs', type=int, default=10,
        help='number of epochs to train (default: 10)'
    )

    parser.add_argument(
        '--lr', type=float, default=0.01,
        help='learning rate (default: 0.01)'
    )

    parser.add_argument(
        '--seed', type=int, default=1,
        help='random seed (default: 1)'
    )

    parser.add_argument(
        '--log-interval', type=int, default=10,
        help='how many batches to wait before logging training status'
    )

    parser.add_argument(
        '--save-model', action='store_true', default=False,
        help='For Saving the current Model'
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = arg_parse()
    use_cuda = torch.cuda.is_available()

    torch.manual_seed(args.seed)

    device = torch.device("cuda" if use_cuda else "cpu")
    kwargs = {'num_workers': 1} if use_cuda else {}

    train_loader = torch.utils.data.DataLoader(
        datasets.MNIST(
            '../static/data', train=True, download=True,
            transform=transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize((0.1307,), (0.3081,))
        ])),
        batch_size=args.batch_size, shuffle=True, **kwargs
    )

    test_loader = torch.utils.data.DataLoader(
        datasets.MNIST(
            '../static/data', train=False,
            transform=transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize((0.1307,), (0.3081,))
        ])),
        batch_size=args.test_batch_size, shuffle=True, **kwargs
    )

    model = MLPNet().to(device)
    optimizer = optim.SGD(model.parameters(), lr=args.lr, momentum=0.5)

    for epoch in range(1, args.epochs + 1):
        train(args, model, device, train_loader, optimizer, epoch)
        test(model, device, test_loader)

    if args.save_model:
        torch.save(model.state_dict(), "mnist_mlp.pt")
