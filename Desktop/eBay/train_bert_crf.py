# train_bert_crf.py
from collections import defaultdict
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizerFast, BertModel
from TorchCRF import CRF
import torch.nn as nn
from tqdm import tqdm
from sklearn.model_selection import train_test_split

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
LABEL_PAD = "[PAD]"
LABEL_CONT = "[CONT]"

class NERDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

class BERT_CRF_Model(nn.Module):
    def __init__(self, num_labels):
        super().__init__()
        self.bert = BertModel.from_pretrained("bert-base-multilingual-cased")
        self.dropout = nn.Dropout(0.1)
        self.classifier = nn.Linear(self.bert.config.hidden_size, num_labels)
        self.crf = CRF(num_labels=num_labels, pad_idx=None, use_gpu=torch.cuda.is_available())

    def forward(self, input_ids, attention_mask, labels=None):
        outputs = self.bert(input_ids, attention_mask=attention_mask)
        sequence_output = self.dropout(outputs.last_hidden_state)
        emissions = self.classifier(sequence_output)
        if labels is not None:
            log_likelihood = self.crf(emissions, labels, mask=attention_mask.bool())
            loss = -log_likelihood.sum()  # Make it a scalar loss for backward()
            return loss
        else:
            return self.crf.decode(emissions, mask=attention_mask.bool())

def load_data(path):
    df = pd.read_csv(path, sep='\t', dtype=str).dropna(subset=['Token'])
    grouped = defaultdict(lambda: {"tokens": [], "tags": []})
    for _, row in df.iterrows():
        rec_id = row['Record Number']
        grouped[rec_id]["tokens"].append(row['Token'])
        grouped[rec_id]["tags"].append(row['Tag'] if pd.notna(row['Tag']) else LABEL_CONT)
    return grouped

def tokenize_and_align_labels(examples, tokenizer, label2id):
    input_ids, attention_masks, aligned_labels = [], [], []
    for entry in examples.values():
        tokens, labels = entry["tokens"], entry["tags"]
        bert_tokens, label_ids = [], []
        for tok, tag in zip(tokens, labels):
            word_pieces = tokenizer.tokenize(tok)
            if not word_pieces:
                continue
            bert_tokens.extend(word_pieces)
            label_id = label2id[tag]
            label_ids.extend([label_id] + [label2id[LABEL_PAD]] * (len(word_pieces) - 1))

        encoding = tokenizer(bert_tokens, is_split_into_words=True, truncation=True, padding='max_length', max_length=128, return_tensors="pt")
        input_ids.append(encoding['input_ids'][0])
        attention_masks.append(encoding['attention_mask'][0])
        padded_labels = label_ids[:128] + [label2id[LABEL_PAD]] * (128 - len(label_ids))
        aligned_labels.append(padded_labels)
    return input_ids, attention_masks, aligned_labels

def main():
    data_path = "Tagged_Titles_Train.tsv"
    data = load_data(data_path)

    all_labels = set(tag for v in data.values() for tag in v['tags'])
    all_labels = sorted(list(all_labels | {LABEL_CONT, LABEL_PAD}))
    label2id = {label: idx for idx, label in enumerate(all_labels)}
    id2label = {idx: label for label, idx in label2id.items()}

    tokenizer = BertTokenizerFast.from_pretrained("bert-base-multilingual-cased")
    input_ids, attention_masks, labels = tokenize_and_align_labels(data, tokenizer, label2id)

    X_input_train, X_input_val, X_mask_train, X_mask_val, y_train, y_val = train_test_split(input_ids, attention_masks, labels, test_size=0.1, random_state=42)
    
    train_dataset = NERDataset(
        {"input_ids": X_input_train, "attention_mask": X_mask_train},
        y_train
    )

    val_dataset = NERDataset(
        {"input_ids": X_input_val, "attention_mask": X_mask_val},
        y_val
    )

    train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=8)

    model = BERT_CRF_Model(len(label2id)).to(DEVICE)
    optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

    for epoch in range(3):
        model.train()
        total_loss = 0
        for batch in tqdm(train_loader, desc=f"Epoch {epoch+1}"):
            input_ids = batch['input_ids'].to(DEVICE)
            attention_mask = batch['attention_mask'].to(DEVICE)
            labels = batch['labels'].to(DEVICE)

            optimizer.zero_grad()
            loss = model(input_ids, attention_mask, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        print(f"Epoch {epoch+1}, Loss: {total_loss / len(train_loader):.4f}")

    torch.save(model.state_dict(), "bert_crf_model.pt")
    print("Model saved as bert_crf_model.pt")

if __name__ == "__main__":
    main()
