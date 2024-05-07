# Mistral Control Vectors

This notebook applies control vectors on Mistral-7B-Instruct-v0.1.

## Dependencies

The notebook requires the following dependencies (specified as installs
in the first cell of the notebook):

```bash
pip install repeng==0.2.0
pip install torch==2.1.2
pip install transformers==4.40.1
pip install numpy==1.26.4
pip install huggingface_hub==0.20.3
pip install requests==2.31.0
```

## Usage

NOTE: this runs best on a GPU - e.g., MPS or CUDA. Running on CPU has
a lot of issues.

Running the notebook will save a `.hf` model in the directory of the notebook.
To use this in the chat bot, you must convert the `.hf` model to a `.gguf` model per the instructions [here](https://github.com/ggerganov/llama.cpp/discussions/2948). Once you have a `.gguf` output of the model, you may load it into the chat bot by specifying the absolute location to the path of this file in the [get_model_path_from_option](./apps/chatbot/setup.py) function. We recommend applying control vectors to the fine tuned model.

This requires installing and making [llama-cpp](https://github.com/ggerganov/llama.cpp), and executing the specified script.
