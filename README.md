# FactsCheckerGPT

Perform facts checks on your conversations with LLMs to catch fake-news, misleading information, and LLMs confusion.
FactsCheckerGPT enables you to talk to ChatGPT, and to validate each response against an "army" of LLMs.
As the FactChecker Agent2, the user can choose a different LLM, such as GPT3.5 / Alpaca (more to be added soon).
Currently, there is no support for multiple FactCheckers.

<img src="docs/images/facts-checker-gpt_.drawio.png" width="850">

## 🔧 Usage

Run the `facts_checker_gpt` Python module in your terminal:
   _(Type this into your CMD window)_

```
python -m facts_checker_gpt
```

You can start asking questions:
![usage-example.png](docs%2Fimages%2Fusage-example.png)

## Enable Alpaca

To use Alpaca, follow the getting started guide of [alpaca.cpp](https://github.com/antimatter15/alpaca.cpp#get-started-7b).
After you've downloaded both files, update your `.env` file:
```env
ALPACA_MODEL_PATH=C:\alpaca.cpp\chat\ggml-alpaca-7b-q4.bin
ALPACA_EXECUTABLE_PATH=C:\alpaca.cpp\chat\chat.exe

AGENT1_MODEL=alpaca
AGENT2_MODEL=gpt-3.5-turbo-0301
```

Currently, the alpaca model doesn't perform well as a verifier (tested with the version of the 7B parameters).