# Gendemo

Minimal text generation demo using transformers

## Quickstart

First start the local text generation service:

```
python3 serve.py MODEL 8005
```

Where `MODEL` is the name or directory of a HF model.

Then, start the user-facing flask site:

```
./run.sh
```
