import argparse
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from pathlib import Path

# Add the project root to the Python path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from trading_agent_ai.src.core.logger import setup_logging

log = setup_logging("train_prediction")

# --- Model Definition ---
# This is a placeholder for a hybrid LSTM-Transformer model.
# A full implementation would be more complex, involving separate Transformer and LSTM layers.
class HybridModel(nn.Module):
    def __init__(self, input_dim, hidden_dim=64, num_layers=2, dropout=0.2):
        super(HybridModel, self).__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True, dropout=dropout)
        self.fc = nn.Linear(hidden_dim, 1)
        log.info(f"Initialized HybridModel with input_dim={input_dim}, hidden_dim={hidden_dim}")

    def forward(self, x):
        # x shape: (batch_size, seq_len, features)
        lstm_out, _ = self.lstm(x)
        # We only use the output of the last time step
        last_time_step_out = lstm_out[:, -1, :]
        out = self.fc(last_time_step_out)
        return out

# --- Data Preparation ---
def create_sequences(data, target_col, sequence_length):
    sequences = []
    labels = []
    for i in range(len(data) - sequence_length):
        seq = data[i:i+sequence_length]
        label = data[i+sequence_length:i+sequence_length+1][target_col].values[0]
        sequences.append(seq.values)
        labels.append(label)
    return np.array(sequences), np.array(labels)

# --- Training Loop ---
def train_prediction_model(
    input_path: Path,
    model_save_path: Path,
    sequence_length: int = 60,
    epochs: int = 50,
    batch_size: int = 32,
    lr: float = 0.001
):
    if not input_path.exists():
        log.error(f"Input data file not found: {input_path}")
        return

    log.info("Loading and preparing data...")
    df = pd.read_csv(input_path, index_col='date', parse_dates=True)
    
    # For simplicity, we'll predict the next day's 'close' price.
    # In a real scenario, you might predict returns or direction.
    target_column = 'close'
    features = [col for col in df.columns if col != target_column] # Use all other columns as features

    # Scale features
    scaler = MinMaxScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=df.columns, index=df.index)

    X, y = create_sequences(df_scaled, target_column, sequence_length)
    
    # Split data
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create PyTorch datasets
    train_data = TensorDataset(torch.from_numpy(X_train).float(), torch.from_numpy(y_train).float())
    val_data = TensorDataset(torch.from_numpy(X_val).float(), torch.from_numpy(y_val).float())

    train_loader = DataLoader(train_data, shuffle=True, batch_size=batch_size)
    val_loader = DataLoader(val_data, shuffle=False, batch_size=batch_size)

    log.info(f"Data prepared: {len(X_train)} train samples, {len(X_val)} validation samples.")

    # --- Model, Loss, Optimizer ---
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    log.info(f"Using device: {device}")

    input_dim = X_train.shape[2]
    model = HybridModel(input_dim=input_dim).to(device)
    criterion = nn.MSELoss() # Mean Squared Error for regression
    optimizer = optim.Adam(model.parameters(), lr=lr)

    # --- Training ---
    log.info("Starting model training...")
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for seq, labels in train_loader:
            seq, labels = seq.to(device), labels.to(device)
            optimizer.zero_grad()
            y_pred = model(seq)
            loss = criterion(y_pred, labels.unsqueeze(1))
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        
        avg_train_loss = total_loss / len(train_loader)

        # Validation
        model.eval()
        total_val_loss = 0
        with torch.no_grad():
            for seq, labels in val_loader:
                seq, labels = seq.to(device), labels.to(device)
                y_pred = model(seq)
                val_loss = criterion(y_pred, labels.unsqueeze(1))
                total_val_loss += val_loss.item()
        avg_val_loss = total_val_loss / len(val_loader)

        log.info(f"Epoch {epoch+1}/{epochs} | Train Loss: {avg_train_loss:.4f} | Val Loss: {avg_val_loss:.4f}")

    # --- Save Model ---
    log.info("Training finished. Saving model...")
    model_save_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), model_save_path)
    log.info(f"Model saved to {model_save_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a time-series prediction model.")
    parser.add_argument("--input", type=str, default="data/processed/feature_rich_data.csv", help="Path to the feature-rich input data file.")
    parser.add_argument("--output", type=str, default="models/prediction/lstm_transformer.pt", help="Path to save the trained model.")
    parser.add_argument("--epochs", type=int, default=50, help="Number of training epochs.")
    parser.add_argument("--lr", type=float, default=0.001, help="Learning rate.")

    args = parser.parse_args()

    project_root = Path(__file__).parent.parent
    input_file_path = project_root / args.input
    output_file_path = project_root / args.output

    train_prediction_model(
        input_path=input_file_path,
        model_save_path=output_file_path,
        epochs=args.epochs,
        lr=args.lr
    )
