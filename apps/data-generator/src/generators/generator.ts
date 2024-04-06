import { Static, Type } from "@sinclair/typebox";
import { createValidatableClass } from "../validate";
import fs from "fs";

module Generator {
  export type ValidJson = Static<typeof Generator.ValidJsonSchema>;
}

abstract class Generator {
  constructor(private readonly _modelName: string) {}

  static ValidJsonSchema = Type.Object({
    prompt: Type.String(),
    completion: Type.String(),
  });

  private _appendErrorToPrompt(prompt: string, error: string) {
    return `${prompt}\n\nError: ${error}`;
  }

  protected abstract regexPattern: RegExp;
  // opus this will be index 0, openai this will be index 1
  protected abstract matchExtractor: number;

  protected _ValidJson = createValidatableClass(Generator.ValidJsonSchema);

  protected _parseResponseJson(response: string) {
    // Remove the leading and trailing markdown code block syntax
    const match = response.match(this.regexPattern);

    if (!match) {
      throw new Error(
        "No JSON found in the content. Response must be wrapped in a JSON code block.",
      );
    }

    // Extracted JSON string
    const jsonString = match[this.matchExtractor];

    // ensure the response is valid JSON with the right keys
    const parsedResponse = JSON.parse(jsonString);
    const data = new this._ValidJson(parsedResponse);

    return data;
  }

  protected abstract generateFineTuningSingle(
    prompt: string,
    currentData: Static<typeof Generator.ValidJsonSchema>[],
  ): Promise<Static<typeof Generator.ValidJsonSchema>>;

  public async generateFineTuningData(): Promise<Generator.ValidJson[]> {
    // generate an array of 50 fine tuning data objects
    const pattern = /^```json\n([\s\S]*?)\n```$/;
    let prompt = `Generate SINGLE JSON object with a prompt that is not appropriate for kids
    and a completion of what should be shown to them.
    The prompt should be something a teenager that is mischevous will ask.
    The JSON object should have the keys 'prompt' and 'completion'.
    The JSON object should be parsable by the regex pattern ${pattern.toString()}
    Do NOT repeat the same prompt and completion.`;

    const fineTuningData = [];
    for (let i = 0; i < 10; i++) {
      let tryCount = 0;
      console.log(`Generating fine tuning data ${i + 1} of 10...`);

      while (tryCount < 3) {
        try {
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
      `fine-tuning-data-${this._modelName}.json`,
      JSON.stringify(fineTuningData, null, 2),
    );

    return fineTuningData;
  }
}

export = Generator;
