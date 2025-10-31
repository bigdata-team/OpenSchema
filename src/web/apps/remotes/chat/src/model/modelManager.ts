import { modelRwaData, type Model } from "./model";

class ModelManager {
    private initialized: boolean = false;
    private initPromise: Promise<void>;
    models: Model[] = [
        {
            model: "openai/gpt-5",
        },
        {
            model: "google/gemini-2.5-flash",
        },
        {
            model: "anthropic/claude-sonnet-4.5",
        }
    ];
    availableModels: Model[] = [
        {
            model: "openai/gpt-5",
        },
        {
            model: "google/gemini-2.5-flash",
        },
        {
            model: "anthropic/claude-sonnet-4.5",
        }
    ];

    constructor() {
      this.initPromise = this._initialize();
    }

     public isInitialized(): boolean {
      return this.initialized;
    }

    public async waitForInitialization(): Promise<void> {
      return this.initPromise;
    }

    private async _initialize() {
        /*
        const models = fetch('https://chat.elpai.org/v1/models');
        console.log("Fetched models:", models);
        */
        this.initModels();
    }

    initModels() {
        this.availableModels.length = 0; // Clear 
        for (const m of modelRwaData.data) {
            if (
                m.id.startsWith("openai")
                || m.id.startsWith("google")
                || m.id.startsWith("anthropic")
                || m.id.startsWith("qwen")
                || m.id.startsWith("deepseek")
                || m.id.startsWith("x-ai")
            ) {
                this.availableModels.push({
                    model: m.id
                });
            }
        }
    }
}

export const modelManager = new ModelManager();