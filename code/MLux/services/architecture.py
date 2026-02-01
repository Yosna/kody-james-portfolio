"""A module for exporting model architecture modules.

Includes:
- HParams: A class to contain the hyperparameters for the model.
- Architecture: A class to export model architecture modules.
"""

import inspect
import textwrap

import torch
import torch.nn as nn


class HParams:
    """A class to contain the hyperparameters for the model."""

    pass


class Architecture:
    """A class to export model architecture modules."""

    source: str

    def __init__(self, model: str):
        """Initialize the architecture module.

        Args:
            model (str): The name of the model to export.
        """
        models = {
            "bigram": self.Bigram,
            "lstm": self.LSTM,
            "gru": self.GRU,
            "transformer": self.Transformer,
        }
        source = inspect.getsource(models.get(model, None))
        self.source = textwrap.dedent(source) if source else ""

    def __repr__(self):
        """Return the source code of the architecture module."""
        return self.source

    class Bigram(nn.Module):
        """The basic architecture for a bigram model."""

        batch_size: int
        block_size: int
        lr: float

        def __init__(self, vocab_size: int, hparams: dict):
            """Initialize the bigram model.

            Args:
                vocab_size (int): The size of the vocabulary.
                hparams (dict): The hyperparameters for the model.
            """
            super().__init__()

            for key, value in hparams.items():
                if key in HParams.__annotations__:
                    setattr(self, key, value)
                else:
                    raise ValueError(f"Invalid hyperparameter: {key}")

            self.embedding = nn.Embedding(vocab_size, vocab_size)

        def forward(self, idx: torch.Tensor) -> torch.Tensor:
            """Forward pass for the bigram model.

            Args:
                idx (torch.Tensor): The input tensor.

            Returns:
                torch.Tensor: The output tensor.
            """
            # (B, T, vocab_size): map indices to logits for next character prediction
            logits = self.embedding(idx)
            return logits

    class LSTM(nn.Module):
        """The basic architecture for an LSTM model."""

        batch_size: int
        block_size: int
        lr: float
        embedding_dim: int
        hidden_size: int
        num_layers: int

        def __init__(self, vocab_size: int, hparams: dict):
            """Initialize the LSTM model.

            Args:
                vocab_size (int): The size of the vocabulary.
                hparams (dict): The hyperparameters for the model.
            """
            super().__init__()

            for key, value in hparams.items():
                if key in HParams.__annotations__:
                    setattr(self, key, value)
                else:
                    raise ValueError(f"Invalid hyperparameter: {key}")

            self.embedding = nn.Embedding(vocab_size, self.embedding_dim)

            self.lstm = nn.LSTM(
                input_size=self.embedding_dim,
                hidden_size=self.hidden_size,
                num_layers=self.num_layers,
                batch_first=True,
            )

            self.fc = nn.Linear(self.hidden_size, vocab_size)

        def forward(self, idx: torch.Tensor) -> torch.Tensor:
            """Forward pass for the LSTM model.

            Args:
                idx (torch.Tensor): The input tensor.

            Returns:
                torch.Tensor: The output tensor.
            """
            # (B, T, embedding_dim): map indices to embeddings
            x = self.embedding(idx)
            # (B, T, hidden_size): process sequence with LSTM
            out, _ = self.lstm(x)
            # (B, T, vocab_size): project to vocabulary size
            logits = self.fc(out)
            return logits

    class GRU(nn.Module):
        """The basic architecture for a GRU model."""

        batch_size: int
        block_size: int
        lr: float
        embedding_dim: int
        hidden_size: int
        num_layers: int

        def __init__(self, vocab_size: int, hparams: dict):
            """Initialize the GRU model.

            Args:
                vocab_size (int): The size of the vocabulary.
                hparams (dict): The hyperparameters for the model.
            """
            super().__init__()

            for key, value in hparams.items():
                if key in HParams.__annotations__:
                    setattr(self, key, value)
                else:
                    raise ValueError(f"Invalid hyperparameter: {key}")

            self.embedding = nn.Embedding(vocab_size, self.embedding_dim)

            self.gru = nn.GRU(
                input_size=self.embedding_dim,
                hidden_size=self.hidden_size,
                num_layers=self.num_layers,
                batch_first=True,
            )

            self.fc = nn.Linear(self.hidden_size, vocab_size)

        def forward(self, idx: torch.Tensor) -> torch.Tensor:
            """Forward pass for the GRU model.

            Args:
                idx (torch.Tensor): The input tensor.

            Returns:
                torch.Tensor: The output tensor.
            """
            # (B, T, embedding_dim): map indices to embeddings
            x = self.embedding(idx)
            # (B, T, hidden_size): process sequence with GRU
            out, _ = self.gru(x)
            # (B, T, vocab_size): project to vocabulary size
            logits = self.fc(out)
            return logits

    class Transformer(nn.Module):
        """The basic architecture for a Transformer model."""

        batch_size: int
        block_size: int
        lr: float
        embedding_dim: int
        max_seq_len: int
        num_heads: int
        ff_dim: int
        num_layers: int

        def __init__(self, vocab_size: int, hparams: dict):
            """Initialize the Transformer model.

            Args:
                vocab_size (int): The size of the vocabulary.
                hparams (dict): The hyperparameters for the model.
            """
            super().__init__()

            for key, value in hparams.items():
                if key in HParams.__annotations__:
                    setattr(self, key, value)
                else:
                    raise ValueError(f"Invalid hyperparameter: {key}")

            self.token_embedding = nn.Embedding(vocab_size, self.embedding_dim)
            self.position_embedding = nn.Embedding(self.max_seq_len, self.embedding_dim)

            encoder_layer = nn.TransformerEncoderLayer(
                d_model=self.embedding_dim,
                nhead=self.num_heads,
                dim_feedforward=self.ff_dim,
                batch_first=True,
            )
            self.transformer = nn.TransformerEncoder(
                encoder_layer, num_layers=self.num_layers
            )

            self.fc = nn.Linear(self.embedding_dim, vocab_size)

        def forward(self, idx: torch.Tensor) -> torch.Tensor:
            """Forward pass for the Transformer model.

            Args:
                idx (torch.Tensor): The input tensor.

            Returns:
                torch.Tensor: The output tensor.
            """
            # (B, T, embedding_dim): map indices to embeddings
            x = self.token_embedding(idx)
            B, T = x.shape[:2]

            # (T, embedding_dim): position embeddings for each position in the sequence
            positions = self.position_embedding(torch.arange(T, device=x.device))
            # (B, T, embedding_dim): expand position embeddings to batch size
            positions = positions.unsqueeze(0).expand(B, -1, -1)

            # (T, T): unrestricted mask for the sequence as a matrix of ones
            full_mask = torch.ones(T, T, device=x.device)
            # (T, T): causal mask to prevent attending to future positions
            attn_mask = torch.triu(full_mask, diagonal=1).bool()

            # (B, T, embedding_dim): sum token and position embeddings
            x = x + positions
            # (B, T, embedding_dim): process sequence with transformer encoder
            x = self.transformer(x, mask=attn_mask)
            # (B, T, vocab_size): project to vocabulary size
            logits = self.fc(x)
            return logits
