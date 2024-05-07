# Domain-Specific Value Alignment

The project has the following applications located in the [`apps/`](./apps) directory:

- [Chat Bot](./apps/chatbot): A [streamlit](https://streamlit.io/) application to interact with [Mistral 7B](https://huggingface.co/TheBloke/Mistral-7B-v0.1-GGUF) and [Llama 3 8B](https://huggingface.co/lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF). The alignment is done on Mistral's 7B instruct model, and the process for generating the non-base models is below.
- [Control Vector](./apps/control-vectors): A jupyter notebook to apply control vectors to a huggingface model. The output of the notebook will be a `hf` model with control vectors applied -- which will need to be converted to `gguf` for interaction with the `Chat Bot`.
- [Data Generator](./apps/data-generator): A collection of [Typescript](https://www.typescriptlang.org/) modules running on [NodeJS](https://nodejs.org/en) to generate fine tuning data with runtime guarantees on formatting.
- [Evaluation](./apps/evaluation): A jupyter notebook to evaluate the safety of generated fine-tuning data or model-generated completions. The output of the notebook will be csv files containing the evaluated responses, marked as safe or unsafe, and with explanations for each.
- [Fine Tuning](./apps/fine-tuning): A jupyter notebook to fine-tune Mistral-7B. The output of the notebook will be a fine-tuned `hf` model -- which will need to be converted to `gguf` for interaction with the `Chat Bot`.

# Project High Level Overview

## Dependencies

### Python

Dependencies for all **Python** applications are encapsulated in [spec-file.yml](./spec-file.yml). Each individual Python application README.md file also specifies the subset of dependencies necessary for just that application. When the application is a notebook, the necessary install commands are included at the top of the notebook for completion.

### Typescript

The **Typescript** application has its dependencies specified in the application's [package.json](./apps/data-generator/package.json).

## Setup

We recommend creating a virtual environment for the application. We personally recommend using [conda](https://docs.conda.io/en/latest/) for this purpose. The following commands will create a new conda environment and install the necessary packages:

```bash
conda env create -f spec-file.yml
```

This will create an environment called `nlp` with all the necessary packages. To activate the environment, run:

```bash
conda activate nlp
```

### Base Model

To simply run the base model, one can install the [Python packages necessary for the Chat Bot](./apps/chatbot/requirements.txt) (unnecessary if the above environment was created). We make use of [llama-cpp](https://github.com/ggerganov/llama.cpp), and particularly, [llama-cpp-python](https://github.com/abetlen/llama-cpp-python), to load `.gguf` models. To run the chat bot, one can execute

```bash
streamlit run main.py
```

from the command line when in the [`apps/chatbot/`](./apps/chatbot) directory. When the fine tuning and control vector steps have not been executed, all model selection choices in the UI correspond to the base model.

## Fine Tuned Model

To fine tune a model, one must first generate the fine tuning data. This can be done by running the [Data Generator](./apps/data-generator) application. The data generator will output a `.json` file that can be used to fine tune a model. We provide the fine tuning data we used for fine tuning [here](./apps/data-generator/src/output-data/). The fine tuning process is done in the [Fine Tuning](./apps/fine-tuning) application. The fine tuning application will output a `.hf` model. However, this can NOT be used in the [Chat Bot](./apps/chatbot) application, since this loads `.gguf` files.

To use the output fine tuned model in the chat bot, one must convert the `.hf` model to a `.gguf` model per the instructions [here](https://github.com/ggerganov/llama.cpp/discussions/2948). Once you have a `.gguf` output of the model, you may load it into the chat bot by specifying the absolute location to the path of this file in the [get_model_path_from_option](./apps/chatbot/setup.py) function.

## Control Vector Model

To apply control vector to a model, one must =run the [Control Vector](./apps/control-vectors) application. The output of this application will be a `.hf` model. However, this can NOT be used in the [Chat Bot](./apps/chatbot) application, since this loads `.gguf` files.

Similar to above, to use the output fine tuned model in the chat bot, one must convert the `.hf` model to a `.gguf` model per the instructions [here](https://github.com/ggerganov/llama.cpp/discussions/2948). Once you have a `.gguf` output of the model, you may load it into the chat bot by specifying the absolute location to the path of this file in the [get_model_path_from_option](./apps/chatbot/setup.py) function. We recommend applying control vectors to the fine tuned model.
