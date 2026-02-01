from unittest.mock import patch

import pytest
import torch
import torch.nn as nn

from services.architecture import Architecture, HParams


@pytest.fixture
def hparams_mock():
    def hparams(model):
        patcher = patch.object(
            HParams, "__annotations__", get_hparams(model), create=True
        )
        patcher.start()
        return patcher

    yield hparams


def get_hparams(model):
    hparams = {"batch_size": 16, "block_size": 32, "lr": 0.001}
    if model != "bigram":
        hparams.update({"embedding_dim": 8, "num_layers": 2})
    if model == "lstm" or model == "gru":
        hparams.update({"hidden_size": 16})
    if model == "transformer":
        hparams.update({"max_seq_len": 32, "num_heads": 2, "ff_dim": 32})
    return hparams


@pytest.mark.parametrize("model", ["bigram", "lstm", "gru", "transformer"])
def test_architecture_init(model):
    architecture = Architecture(model)
    assert architecture is not None
    assert architecture.source is not ""
    assert isinstance(architecture.source, str)
    assert str(architecture) == architecture.source


def test_bigram_init(hparams_mock):
    hparams_mock("bigram")
    hparams = get_hparams("bigram")
    model = Architecture.Bigram(10, hparams)
    assert model.batch_size == 16
    assert model.block_size == 32
    assert model.lr == 0.001
    assert isinstance(model.embedding, nn.Embedding)
    assert model.embedding.num_embeddings == 10
    assert model.embedding.embedding_dim == 10


def test_bigram_forward(hparams_mock):
    hparams_mock("bigram")
    hparams = get_hparams("bigram")
    model = Architecture.Bigram(10, hparams)
    idx = torch.tensor([[0, 1, 2, 3, 4]])
    logits = model(idx)
    assert logits.shape == torch.Size([1, 5, 10])


def test_lstm_init(hparams_mock):
    hparams_mock("lstm")
    hparams = get_hparams("lstm")
    model = Architecture.LSTM(10, hparams)
    assert model.batch_size == 16
    assert model.block_size == 32
    assert model.lr == 0.001
    assert isinstance(model.embedding, nn.Embedding)
    assert model.embedding.num_embeddings == 10
    assert model.embedding.embedding_dim == 8
    assert isinstance(model.lstm, nn.LSTM)
    assert model.lstm.input_size == 8
    assert model.lstm.hidden_size == 16
    assert model.lstm.num_layers == 2
    assert model.lstm.batch_first
    assert isinstance(model.fc, nn.Linear)
    assert model.fc.in_features == 16
    assert model.fc.out_features == 10
    assert model.fc.bias is not None


def test_lstm_forward(hparams_mock):
    hparams_mock("lstm")
    hparams = get_hparams("lstm")
    model = Architecture.LSTM(10, hparams)
    idx = torch.tensor([[0, 1, 2, 3, 4]])
    logits = model(idx)
    assert logits.shape == torch.Size([1, 5, 10])


def test_gru_init(hparams_mock):
    hparams_mock("gru")
    hparams = get_hparams("gru")
    model = Architecture.GRU(10, hparams)
    assert model.batch_size == 16
    assert model.block_size == 32
    assert model.lr == 0.001
    assert isinstance(model.embedding, nn.Embedding)
    assert model.embedding.num_embeddings == 10
    assert model.embedding.embedding_dim == 8
    assert isinstance(model.gru, nn.GRU)
    assert model.gru.input_size == 8
    assert model.gru.hidden_size == 16
    assert model.gru.num_layers == 2
    assert model.gru.batch_first
    assert isinstance(model.fc, nn.Linear)
    assert model.fc.in_features == 16
    assert model.fc.out_features == 10
    assert model.fc.bias is not None


def test_gru_forward(hparams_mock):
    hparams_mock("gru")
    hparams = get_hparams("gru")
    model = Architecture.GRU(10, hparams)
    idx = torch.tensor([[0, 1, 2, 3, 4]])
    logits = model(idx)
    assert logits.shape == torch.Size([1, 5, 10])


def test_transformer_init(hparams_mock):
    hparams_mock("transformer")
    hparams = get_hparams("transformer")
    model = Architecture.Transformer(10, hparams)
    assert model.batch_size == 16
    assert model.block_size == 32
    assert model.lr == 0.001
    assert isinstance(model.token_embedding, nn.Embedding)
    assert model.token_embedding.num_embeddings == 10
    assert model.token_embedding.embedding_dim == 8
    assert isinstance(model.position_embedding, nn.Embedding)
    assert model.position_embedding.num_embeddings == 32
    assert model.position_embedding.embedding_dim == 8
    assert isinstance(model.transformer, nn.TransformerEncoder)
    assert len(model.transformer.layers) == 2
    assert isinstance(model.transformer.layers[0], nn.TransformerEncoderLayer)
    assert isinstance(model.transformer.layers[1], nn.TransformerEncoderLayer)
    assert isinstance(model.fc, nn.Linear)
    assert model.fc.in_features == 8
    assert model.fc.out_features == 10
    assert model.fc.bias is not None


def test_transformer_forward(hparams_mock):
    hparams_mock("transformer")
    hparams = get_hparams("transformer")
    model = Architecture.Transformer(10, hparams)
    idx = torch.tensor([[0, 1, 2, 3, 4]])
    logits = model(idx)
    assert logits.shape == torch.Size([1, 5, 10])


@pytest.mark.parametrize(
    "model, architecture",
    [
        ("bigram", Architecture.Bigram),
        ("lstm", Architecture.LSTM),
        ("gru", Architecture.GRU),
        ("transformer", Architecture.Transformer),
    ],
)
def test_invalid_hyperparameter(hparams_mock, model, architecture):
    hparams_mock(model)
    hparams = get_hparams(model)
    hparams["invalid"] = "invalid"
    with pytest.raises(ValueError):
        architecture(10, hparams)
