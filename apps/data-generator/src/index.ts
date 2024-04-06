import dotenv from "dotenv";
import "reflect-metadata";

import { OpenAiService } from "./openai";

dotenv.config();

const main = async () => {
  if (!process.env.OPENAI_API_KEY) {
    throw new Error("OPENAI_API_KEY is not set");
  }

  const openai = new OpenAiService(process.env.OPENAI_API_KEY);
  await openai.generateFineTuningData();
};

main();
