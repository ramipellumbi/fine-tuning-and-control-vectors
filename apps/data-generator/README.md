# Data Generator

This application generates fine tuning samples using OpenAI, Anthropic, or both.

## Getting Started

Create a `.env` file with the environment variables

```
OPENAI_API_KEY=FILL_IN
OPUS_API_KEY=FILL_IN
```

in the [`src/`](./src) directory.

Ensure you have `pnpm` installed. Install packages for the application by running

```
pnpm install
```

inside the `data-generator/` (this) directory. You can run the generation script by executing

```
ts-node index.ts
```

from the `src/` directory.

## Generators

The abstract base class [`generator`](./src/generators/generator.ts) defines a means for extracting the desired fine tuning samples from API layers of popular LLMs. The classes [`openai.ts`](./src/generators/openai.ts) and
[`opus.ts`](./src/generators/opus.ts) define the behavior for generating a fine tuning data sample from `OpenAI` and `Anthropic`, respectively.

## Validators

Data returned by the API's is not guaranteed to be in the correct format. To that end, we have adoped a custom built runtime validator to parse the JSON output and re-request data from the model if it is not in the right format.
The magic happens in [`validate.ts`](./src/validate.ts), which provides means for creating a validatable data class from a [Typebox](https://github.com/sinclairzx81/typebox) schema.

Here is example usage:

```
const ValidSampleSchema = Type.Object({
  prompt: Type.String(),
  completion: Type.String(),
})

const ValidSample = createValidatableClass(ValidSampleSchema);

const generateSample = async () => {
  // some invocation to a model that returns a response of
  // unknown type
  const response = await model.response();

  // parse out JSON from response
  // has compile time type of `any`
  const parsedResponse = parseResponse(response);

  const data = new ValidSample(parsedResponse);

  // this point onwards you can assure the data is present
  // in the right format
}
```
