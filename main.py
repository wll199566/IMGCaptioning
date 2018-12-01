import torch
import torch.nn as nn
from vocabloader import vocab_loader
from torchvision import transforms
from dataloader import *
from torch.nn.utils.rnn import pack_padded_sequence
from Encoder import Encoder
from Decoder import Decoder

# hyperparameters
batch_size = 64
embedding_size = 512
vocal_size = 9957
learning_rate = 0.001
num_epochs = 5
log_step = 100
train_image_file = "???"
train_captions_json = "./annotations/captions_train2014.json"
val_image_file = "???"
val_captions_json = "./annotations/captions_val2014.json"

# Device configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


def train():
    pass


def validation():
    pass


def main():
    # Load all vocabulary in the data set
    vocab = vocab_loader("vocab.txt")

    # Transform image size to 224
    transform = transforms.Compose([
        transforms.RandomSizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406),
                             (0.229, 0.224, 0.225))
    ])

    # Load training data
    train_loader = get_train_loader(train_image_file, train_captions_json, transform, batch_size, True)

    # Load validation data
    val_loader = get_val_loader(val_image_file, val_captions_json, transform)

    # Build the models
    encoder = Encoder(embed_size=embedding_size).to(device)
    decoder = Decoder(vocal_size).to(device)

    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(
        filter(lambda p: p.requires_grad, list(encoder.parameters()) + list(decoder.parameter())), lr=learning_rate)

    # Train the models
    total_step = len(train_loader)
    for epoch in range(num_epochs):
        for i, (image, captions, lengths) in enumerate(train_loader):
            # Set mini-batch dataset
            images = images.to(device)
            captions = captions.to(device)

            # Exclude the "<start>" from loss function
            captions = captions[:, 1:]
            lengths_1 = lengths - 1

            targets = pack_padded_sequence(captions, lengths_1, batch_fisrt=True).data

            # Forward, backward and optimize
            features = encoder(images)
            outputs = decoder(features, captions, lengths)
            outputs = outputs[:, 1:, :]
            loss = criterion(outputs, targets)
            decoder.zero_grad()
            decoder.zero_grad()
            loss.backward()
            optimizer.step()

            # Print log info
            if i %


if __name__ == "__main__":
    pass