# Mistral Fine-Tuning

This notebook performs fine-tuning on Mistral-7B-Instruct-v0.1 using data pulled from our github.

## Dependencies

The notebook requires the following dependencies:

- `transformers`
- `torch`
- `datasets`
- `pandas`
- `requests`
- `peft`
- `trl`

You can install the necessary packages by running:

```bash
pip install -q accelerate==0.21.0 peft==0.4.0 bitsandbytes==0.41.1 transformers==4.35.0 trl==0.4.7
```

## Usage

This notebook should be run on Colab ONLY.

1. Make sure you have the required dependencies installed and set your `HF_TOKEN` as a Colab secret.

2. Run the notebook cells in order.

3. The notebook will download the fine-tuning data from the specified GitHub repository and save it locally.

4. The notebook will perform the fine-tuning and save the updated model locally.

5. You can review the updated model in the generated files (mistral-7b-fine-tuned).

## Workflow

1. The notebook downloads fine-tuning data from a GitHub repository and saves it locally as JSON files.

2. The JSON files are loaded into a pandas DataFrame, and then into a Dataset.

3. The notebook loads a pre-trained model (`mistralai/Mistral-7B-Instruct-v0.1`) using the `AutoModelForCausalLM` and `AutoTokenizer` classes from the `transformers` library.

4. It performs the fine-tuning using the loaded data.

5. It merges the original model with the updated weights, saving the final model.
