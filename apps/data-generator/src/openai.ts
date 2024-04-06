import { Static, Type } from "@sinclair/typebox";
import OpenAI from "openai";

import fs from "fs";

import { createValidatableClass } from "./validate";

const ValidJsonSchema = Type.Object({
  prompt: Type.String(),
  completion: Type.String(),
});

type ValidJson = Static<typeof ValidJsonSchema>;

const ValidJson = createValidatableClass(ValidJsonSchema);

export class OpenAiService {
  private _openai: OpenAI;

  constructor(apiKey: string) {
    this._openai = new OpenAI({
      apiKey,
    });
  }

  private _parseResponseJson(response: string) {
    // Remove the leading and trailing markdown code block syntax
    const jsonPattern = /^```json\n([\s\S]*?)\n```$/;
    const match = response.match(jsonPattern);

    if (!match) {
      throw new Error(
        "No JSON found in the content. Response must be wrapped in a JSON code block.",
      );
    }

    // Extracted JSON string
    const jsonString = match[1];

    // ensure the response is valid JSON with the right keys
    const parsedResponse = JSON.parse(jsonString);
    const data = new ValidJson(parsedResponse);

    return data;
  }

  private _appendErrorToPrompt(prompt: string, error: string) {
    return `${prompt}\n\nError: ${error}`;
  }

  private async generateFineTuningSingle(
    prompt: string,
    currentData: ValidJson[],
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

  async generateFineTuningData(): Promise<ValidJson[]> {
    // generate an array of 50 fine tuning data objects
    let prompt = `Generate SINGLE JSON object with a prompt that is not appropriate for kids
    and a completion of what should be shown to them.
    The prompt should be something a teenager that is mischevous will ask.
    The JSON object should have the keys 'prompt' and 'completion'.
    Do NOT repeat the same prompt and completion."`;

    const fineTuningData = [];
    for (let i = 0; i < 10; i++) {
      let tryCount = 0;
      console.log(`Generating fine tuning data ${i + 1} of 10...`);

      while (tryCount < 3) {
        try {
          console.log(prompt);
          const data = await this.generateFineTuningSingle(
            prompt,
            fineTuningData,
          );
          fineTuningData.push(data);
          break;
        } catch (error) {
          tryCount++;
          prompt = this._appendErrorToPrompt(prompt, (error as Error).message);
        }
      }
    }

    // write to disk the JSON array of fine tuning data
    fs.writeFileSync(
      "fine-tuning-data.json",
      JSON.stringify(fineTuningData, null, 2),
    );

    return fineTuningData;
  }
}
