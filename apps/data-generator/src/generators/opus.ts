import Anthropic from "@anthropic-ai/sdk";

import Generator from "./generator";

export class OpusGenerator extends Generator {
  private _anthropic: Anthropic;

  constructor(apiKey: string) {
    super("claude-3-opus-20240229");
    this._anthropic = new Anthropic({
      apiKey,
    });
  }

  protected regexPattern: RegExp =
    /{[\s\S]*"prompt": "[\s\S]*?",[\s\S]*"completion": "[\s\S]*?"[\s\S]*}/;
  protected matchExtractor: number = 0;

  protected async generateFineTuningSingle(
    prompt: string,
    currentData: Generator.ValidJson[],
  ) {
    const response = await this._anthropic.messages.create({
      model: "claude-3-opus-20240229",
      max_tokens: 4096,
      messages: [
        {
          role: "user",
          content: `You are a helpful assistant for generating fine tuning data for language models.
          The currently generated data is as follows: ${JSON.stringify(
            currentData,
            null,
            2,
          )}.

          This is the prompt for generating the next piece of fine tuning data: ${prompt}`,
        },
      ],
      temperature: 0.6,
      stream: false,
    });

    const content = response.content.map((v) => v.text).join("\n");
    if (!content) {
      throw new Error("No content found in the response.");
    }

    const parsedResponse = this._parseResponseJson(content);

    return parsedResponse;
  }
}
