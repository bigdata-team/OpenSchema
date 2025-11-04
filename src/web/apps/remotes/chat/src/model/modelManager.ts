import { modelRwaData, type Model } from "./model";

class ModelManager {
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
                // 159
            } else {
                /*
                this.availableModels.push({
                    model: m.id
                });
                */
                // 348
            }
        }

        // Sort by provider first (anthropic, google, openai, etc), then by model name
        this.availableModels.sort((a, b) => {
            const providerA = a.model.split('/')[0];
            const providerB = b.model.split('/')[0];

            if (providerA !== providerB) {
                return providerA.localeCompare(providerB);
            }
            return a.model.localeCompare(b.model);
        });

        console.log("Initialized availableModels:", this.availableModels.length);
    }
}

export const modelManager = new ModelManager();