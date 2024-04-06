import OpenAI from "openai";

import Generator from "./generator";

export class OpenAiGenerator extends Generator {
  private _openai: OpenAI;

  constructor(apiKey: string) {
    super("gpt-4-turbo-preview");
    this._openai = new OpenAI({
      apiKey,
    });
  }

  protected regexPattern: RegExp = /^```json\n([\s\S]*?)\n```$/;
  protected matchExtractor: number = 1;

  protected async generateFineTuningSingle(
    prompt: string,
    currentData: Generator.ValidJson[],
  ) {
    const response = await this._openai.chat.completions.create({
      model: "gpt-4-turbo-preview",
      messages: [
        {
          role: "system",
          content:
            "You are a helpful assistant for generating fine tuning data for language models.",
        },
        {
          role: "user",
          content: `The currently generated data is as follows: ${JSON.stringify(
            currentData,
            null,
            2,
          )}`,
        },
        {
          role: "user",
          content: prompt,
        },
      ],
      temperature: 0.6,
      stream: false,
    });

    const content = response.choices[0].message.content;

    if (!content) {
      throw new Error("No content found in the response.");
    }

    const parsedResponse = this._parseResponseJson(content);

    return parsedResponse;
  }
}
