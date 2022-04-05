import torch
#from transformers import AutoTokenizer,BertTokenizerFast, BertForQuestionAnswering
from flask import jsonify
from transformers import CamembertForQuestionAnswering
from transformers import CamembertTokenizer


###etape2

# Definire tokenizer de bert
#tokenizer = AutoTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
model_path = 'illuin/camembert-base-fquad'
tokenizer = CamembertTokenizer.from_pretrained(model_path)


# chargéé la modele bert
#model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
model = CamembertForQuestionAnswering.from_pretrained(model_path)


# etape3
class Q_R:
    def _init_(self):
        pass

    def loadModel(self):
        ###etape2

        # Definire tokenizer de bert
        # tokenizer = AutoTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
        model_path = 'illuin/camembert-base-fquad'
        tokenizer = CamembertTokenizer.from_pretrained(model_path)

        # chargéé la modele bert
        # model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
        model = CamembertForQuestionAnswering.from_pretrained(model_path)
        model.eval()


    def predict(self,context, query):
        inputs = tokenizer.encode_plus(query, context, return_tensors='pt')
        outputs = model(**inputs)
        answer_start = torch.argmax(outputs[0])  # get the most likely beginning of answer with the argmax of the score
        answer_end = torch.argmax(outputs[1]) + 1
        answer = tokenizer.convert_tokens_to_string(
            tokenizer.convert_ids_to_tokens(inputs['input_ids'][0][answer_start:answer_end]))
        return answer

    def predictjson(context, query):
        inputs = tokenizer.encode_plus(query, context, return_tensors='pt')
        outputs = model(**inputs)
        answer_start = torch.argmax(outputs[0])  # get the most likely beginning of answer with the argmax of the score
        answer_end = torch.argmax(outputs[1]) + 1
        answer = tokenizer.convert_tokens_to_string(
            tokenizer.convert_ids_to_tokens(inputs['input_ids'][0][answer_start:answer_end]))
        return answer

    def normalize_text(self,s):
        """La suppression d'articles et de ponctuation et la normalisation des espaces blancs sont toutes des étapes typiques de traitement de texte."""
        import string, re

        #methode de rien a faire
        def remove_articles(text):
            regex = re.compile(r"\b(a|an|the)\b", re.UNICODE)
            return re.sub(regex, " ", text)

        def white_space_fix(text):
            return " ".join(text.split())

        def remove_punc(text):
            exclude = set(string.punctuation)
            return "".join(ch for ch in text if ch not in exclude)

        def lower(text):
            return text.lower()

        return white_space_fix(remove_articles(remove_punc(lower(s))))



    def compute_exact_match(self,prediction, truth):
        return int(self.normalize_text(prediction) == self.normalize_text(truth))


    def compute_f1(self,prediction, truth):
        pred_tokens = self.normalize_text(prediction).split()
        truth_tokens = self.normalize_text(truth).split()

        # if either the prediction or the truth is no-answer then f1 = 1 if they agree, 0 otherwise
        if len(pred_tokens) == 0 or len(truth_tokens) == 0:
            return int(pred_tokens == truth_tokens)

        common_tokens = set(pred_tokens) & set(truth_tokens)

        # if there are no common tokens then f1 = 0
        if len(common_tokens) == 0:
            return 0

        prec = len(common_tokens) / len(pred_tokens)
        rec = len(common_tokens) / len(truth_tokens)

        return 2 * (prec * rec) / (prec + rec)



    """méthode la ou on resoudre la réponse"""


    def give_an_answer(self,context, query, answer):
        prediction = self.predict(context, query)
        em_score = self.compute_exact_match(prediction, answer)
        f1_score = self.compute_f1(prediction, answer)

        print(f"Question: {query}")
        print(f"Prediction: {prediction}")
        print(f"True Answer: {answer}")
        print(f"EM: {em_score}")
        print(f"F1: {f1_score}")
        print("\n")

    def give_an_answer1(self,context, query):
        prediction = self.predict(context, query)
        # em_score = compute_exact_match(prediction, answer)
        # f1_score = compute_f1(prediction, answer)

        print(f"Question: {query}")
        print(f"Prediction: {prediction}")
        # print(f"True Answer: {answer}")
        # print(f"EM: {em_score}")
        # print(f"F1: {f1_score}")
        print("\n")

