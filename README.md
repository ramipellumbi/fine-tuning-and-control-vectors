# Domain-Specific Value Alignment

The project has the following applications located in the [`apps/`](./apps) directory:

- [Chat Bot](./apps/chatbot): A [streamlit](https://streamlit.io/) application to interact with [Mistral 7B](https://huggingface.co/TheBloke/Mistral-7B-v0.1-GGUF) and [Llama 3 8B](https://huggingface.co/lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF). The alignment is done on Mistral's 7B instruct model, and the process for generating the non-base models is below.
- [Control Vector](./apps/control-vectors): A jupyter notebook to apply control vectors to a huggingface model. The output of the notebook will be a `hf` model with control vectors applied -- which will need to be converted to `gguf` for interaction with the `Chat Bot`.
- [Data Generator](./apps/data-generator): A collection of [Typescript](https://www.typescriptlang.org/) modules running on [NodeJS](https://nodejs.org/en) to generate fine tuning data with runtime guarantees on formatting.
- [Evaluation](./apps/evaluation):
- [Fine Tuning](./apps/fine-tuning):
