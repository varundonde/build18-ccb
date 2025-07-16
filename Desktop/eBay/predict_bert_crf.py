import pandas as pd
import torch
from transformers import BertTokenizerFast, BertModel
from TorchCRF import CRF
import torch.nn as nn
from tqdm import tqdm
import json

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
LABEL_PAD = "[PAD]"
LABEL_CONT = "[CONT]"

class BERT_CRF_Model(nn.Module):
    def __init__(self, num_labels):
        super().__init__()
        self.bert = BertModel.from_pretrained("bert-base-multilingual-cased")
        self.dropout = nn.Dropout(0.1)
        self.classifier = nn.Linear(self.bert.config.hidden_size, num_labels)
        self.crf = CRF(num_labels=num_labels, pad_idx=None, use_gpu=torch.cuda.is_available())

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids, attention_mask=attention_mask)
        sequence_output = self.dropout(outputs.last_hidden_state)
        emissions = self.classifier(sequence_output)
        return self.crf.viterbi_decode(emissions, attention_mask.bool())

def load_model(label2id):
    model = BERT_CRF_Model(len(label2id))
    model.load_state_dict(torch.load("bert_crf_model.pt", map_location=DEVICE))
    model.to(DEVICE)
    model.eval()
    return model

def predict(model, label2id):
    id2label = {v: k for k, v in label2id.items()}
    df = pd.read_csv("Listing_Titles.tsv", sep="\t", usecols=["Record Number", "Category", "Title"])

    tokenizer = BertTokenizerFast.from_pretrained("bert-base-multilingual-cased")
    predictions = []

    for _, row in tqdm(df.iterrows(), total=len(df)):
        record_id = row['Record Number']
        category = row['Category']
        title = str(row['Title'])

        tokens = title.strip().split()
        bert_tokens = []
        token_to_word = []

        for idx, token in enumerate(tokens):
            word_pieces = tokenizer.tokenize(token)
            if not word_pieces:
                continue
            bert_tokens.extend(word_pieces)
            token_to_word.extend([idx]*len(word_pieces))

        encoding = tokenizer(bert_tokens, is_split_into_words=True, truncation=True, padding='max_length', max_length=128, return_tensors="pt")
        input_ids = encoding['input_ids'].to(DEVICE)
        attention_mask = encoding['attention_mask'].to(DEVICE)

        pred = model(input_ids, attention_mask)[0]  # batch size = 1
        pred_labels = [id2label[idx] for idx in pred]

        # Reconstruct entities from subword predictions
        current_aspect = None
        current_value = []
        used_words = set()

        for subword_idx, label in zip(token_to_word, pred_labels):
            if subword_idx in used_words:
                continue
            used_words.add(subword_idx)
            token = tokens[subword_idx]

            if label in [LABEL_PAD, "O"]:
                continue
            if label == LABEL_CONT:
                if current_aspect:
                    current_value.append(token)
                continue
            if current_aspect:
                predictions.append([record_id, category, current_aspect, " ".join(current_value)])

            current_aspect = label
            current_value = [token]

        if current_aspect:
            predictions.append([record_id, category, current_aspect, " ".join(current_value)])

    out_df = pd.DataFrame(predictions, columns=["Record Number", "Category", "Aspect Name", "Aspect Value"])
    out_df.to_csv("submission.tsv", sep="\t", index=False)
    print("Predictions saved to submission.tsv")

if __name__ == "__main__":
    with open("label2id.json", "r") as f:
        label2id = json.load(f)

        if len(label2id) <= 2:
            raise ValueError("Define your label2id dictionary with actual labels from training!")

        model = load_model(label2id)
        predict(model, label2id)
