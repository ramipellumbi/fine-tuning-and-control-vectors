import dotenv from "dotenv";
import "reflect-metadata";

import { OpusGenerator, OpenAiGenerator } from "./generators";

dotenv.config();

const main = async () => {
  if (!process.env.OPENAI_API_KEY) {
    throw new Error("OPENAI_API_KEY is not set");
  }

  if (!process.env.OPUS_API_KEY) {
    throw new Error("OPUS_API_KEY is not set");
  }

  const openai = new OpenAiGenerator(process.env.OPENAI_API_KEY);
  await openai.generateFineTuningData();

  const opus = new OpusGenerator(process.env.OPUS_API_KEY);
  await opus.generateFineTuningData();
};

main();
