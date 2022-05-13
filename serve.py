import os
import sys
import unicodedata

from argparse import ArgumentParser

from transformers import AutoTokenizer, AutoModelForCausalLM
from flask import Flask, request


DEFAULT_MODEL_DIR = 'ner-model'


app = Flask(__name__)


def load_tokenizer_and_model(directory):
    print('loading tokenizer...', end='', file=sys.stderr, flush=True)
    tokenizer = AutoTokenizer.from_pretrained(directory)
    print('done.', file=sys.stderr, flush=True)
    print('loading model...', end='', file=sys.stderr, flush=True)
    model = AutoModelForCausalLM.from_pretrained(directory)
    print('done.', file=sys.stderr, flush=True)
    return tokenizer, model


@app.route('/')
def generate():
    text = request.values['text']
    max_length = request.values.get('max_length', 128)
    temperature = request.values.get('temperature', 1.0)

    try:
        temperature = min(max(float(temperature), 0), 1)
    except:
        temperature = 1.0
    try:
        max_length = min(max(max_length, 16), 512)
    except:
        max_length = 128

    generated = app.generator.generate(text, max_length, temperature)
    print(f'got prompt "{text}", max_length {max_length}, temperature {temperature}, generated "{generated}"', file=sys.stderr,
          flush=True)
    return generated


class Generator(object):
    def __init__(self, tokenizer, model):
        self.tokenizer = tokenizer
        self.model = model

    def generate(self, prompt, max_length, temperature):
        encode = lambda s: self.tokenizer.encode(s, return_tensors='pt')
        decode = lambda v: self.tokenizer.decode(v)

        prompt = prompt.rstrip('\n')
        generated = self.model.generate(
            encode(prompt),
            do_sample=True,
            max_length=max_length,
            top_k=5,
            top_p=0.95,
            temperature=temperature,
            no_repeat_ngram_size=2,
            num_return_sequences=1,
            repetition_penalty=0.9,
            bad_words_ids=[[self.tokenizer.eos_token_id]]
        )
        for g in generated:
            decoded = decode(g)
            decoded = decoded.replace(prompt, '', 1)
            return decoded

    @classmethod
    def load(cls, model_dir):
        # session/graph for multithreading, see https://stackoverflow.com/a/54783311
        model, tokenizer = load_tokenizer_and_model(model_dir)
        return cls(model, tokenizer)


def main(argv):
    ap = ArgumentParser()
    ap.add_argument('model')
    ap.add_argument('port')
    args = ap.parse_args(argv[1:])
    app.generator = Generator.load(args.model)
    app.run(port=args.port)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
