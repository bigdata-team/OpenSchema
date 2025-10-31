export interface Model {
    model: string;
}

/*
export const availableModels: Model[] = [
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

export function initModels() {
    availableModels.length = 0; // Clear 
    for (const m of modelRwaData.data) {
        if (
            m.id.startsWith("openai")
            || m.id.startsWith("google")
            || m.id.startsWith("anthropic")
            || m.id.startsWith("qwen")
            || m.id.startsWith("deepseek")
            || m.id.startsWith("x-ai")
        ) {
            availableModels.push({
                model: m.id
            });
        }
    }
}
    */


export const modelRwaData = {
    "data": [
        {
            "id": "openai/gpt-oss-safeguard-20b",
            "object": "",
            "created": 1761752836,
            "ownedBy": ""
        },
        {
            "id": "nvidia/nemotron-nano-12b-v2-vl:free",
            "object": "",
            "created": 1761675565,
            "ownedBy": ""
        },
        {
            "id": "nvidia/nemotron-nano-12b-v2-vl",
            "object": "",
            "created": 1761675565,
            "ownedBy": ""
        },
        {
            "id": "minimax/minimax-m2:free",
            "object": "",
            "created": 1761252093,
            "ownedBy": ""
        },
        {
            "id": "minimax/minimax-m2",
            "object": "",
            "created": 1761252093,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen3-vl-32b-instruct",
            "object": "",
            "created": 1761231332,
            "ownedBy": ""
        },
        {
            "id": "liquid/lfm2-8b-a1b",
            "object": "",
            "created": 1760970984,
            "ownedBy": ""
        },
        {
            "id": "liquid/lfm-2.2-6b",
            "object": "",
            "created": 1760970889,
            "ownedBy": ""
        },
        {
            "id": "ibm-granite/granite-4.0-h-micro",
            "object": "",
            "created": 1760927695,
            "ownedBy": ""
        },
        {
            "id": "deepcogito/cogito-v2-preview-llama-405b",
            "object": "",
            "created": 1760709933,
            "ownedBy": ""
        },
        {
            "id": "openai/gpt-5-image-mini",
            "object": "",
            "created": 1760624583,
            "ownedBy": ""
        },
        {
            "id": "anthropic/claude-haiku-4.5",
            "object": "",
            "created": 1760547638,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen3-vl-8b-thinking",
            "object": "",
            "created": 1760463746,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen3-vl-8b-instruct",
            "object": "",
            "created": 1760463308,
            "ownedBy": ""
        },
        {
            "id": "openai/gpt-5-image",
            "object": "",
            "created": 1760447986,
            "ownedBy": ""
        },
        {
            "id": "inclusionai/ring-1t",
            "object": "",
            "created": 1760384099,
            "ownedBy": ""
        },
        {
            "id": "inclusionai/ling-1t",
            "object": "",
            "created": 1760316076,
            "ownedBy": ""
        },
        {
            "id": "openai/o3-deep-research",
            "object": "",
            "created": 1760129661,
            "ownedBy": ""
        },
        {
            "id": "openai/o4-mini-deep-research",
            "object": "",
            "created": 1760129642,
            "ownedBy": ""
        },
        {
            "id": "nvidia/llama-3.3-nemotron-super-49b-v1.5",
            "object": "",
            "created": 1760101395,
            "ownedBy": ""
        },
        {
            "id": "baidu/ernie-4.5-21b-a3b-thinking",
            "object": "",
            "created": 1760048887,
            "ownedBy": ""
        },
        {
            "id": "google/gemini-2.5-flash-image",
            "object": "",
            "created": 1759870431,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen3-vl-30b-a3b-thinking",
            "object": "",
            "created": 1759794479,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen3-vl-30b-a3b-instruct",
            "object": "",
            "created": 1759794476,
            "ownedBy": ""
        },
        {
            "id": "openai/gpt-5-pro",
            "object": "",
            "created": 1759776663,
            "ownedBy": ""
        },
        {
            "id": "z-ai/glm-4.6",
            "object": "",
            "created": 1759235576,
            "ownedBy": ""
        },
        {
            "id": "z-ai/glm-4.6:exacto",
            "object": "",
            "created": 1759235576,
            "ownedBy": ""
        },
        {
            "id": "anthropic/claude-sonnet-4.5",
            "object": "",
            "created": 1759161676,
            "ownedBy": ""
        },
        {
            "id": "deepseek/deepseek-v3.2-exp",
            "object": "",
            "created": 1759150481,
            "ownedBy": ""
        },
        {
            "id": "thedrummer/cydonia-24b-v4.1",
            "object": "",
            "created": 1758931878,
            "ownedBy": ""
        },
        {
            "id": "relace/relace-apply-3",
            "object": "",
            "created": 1758891572,
            "ownedBy": ""
        },
        {
            "id": "google/gemini-2.5-flash-preview-09-2025",
            "object": "",
            "created": 1758820178,
            "ownedBy": ""
        },
        {
            "id": "google/gemini-2.5-flash-lite-preview-09-2025",
            "object": "",
            "created": 1758819686,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen3-vl-235b-a22b-thinking",
            "object": "",
            "created": 1758668690,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen3-vl-235b-a22b-instruct",
            "object": "",
            "created": 1758668687,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen3-max",
            "object": "",
            "created": 1758662808,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen3-coder-plus",
            "object": "",
            "created": 1758662707,
            "ownedBy": ""
        },
        {
            "id": "openai/gpt-5-codex",
            "object": "",
            "created": 1758643403,
            "ownedBy": ""
        },
        {
            "id": "deepseek/deepseek-v3.1-terminus",
            "object": "",
            "created": 1758548275,
            "ownedBy": ""
        },
        {
            "id": "deepseek/deepseek-v3.1-terminus:exacto",
            "object": "",
            "created": 1758548275,
            "ownedBy": ""
        },
        {
            "id": "x-ai/grok-4-fast",
            "object": "",
            "created": 1758240090,
            "ownedBy": ""
        },
        {
            "id": "alibaba/tongyi-deepresearch-30b-a3b:free",
            "object": "",
            "created": 1758210804,
            "ownedBy": ""
        },
        {
            "id": "alibaba/tongyi-deepresearch-30b-a3b",
            "object": "",
            "created": 1758210804,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen3-coder-flash",
            "object": "",
            "created": 1758115536,
            "ownedBy": ""
        },
        {
            "id": "arcee-ai/afm-4.5b",
            "object": "",
            "created": 1758040484,
            "ownedBy": ""
        },
        {
            "id": "opengvlab/internvl3-78b",
            "object": "",
            "created": 1757962555,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen3-next-80b-a3b-thinking",
            "object": "",
            "created": 1757612284,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen3-next-80b-a3b-instruct",
            "object": "",
            "created": 1757612213,
            "ownedBy": ""
        },
        {
            "id": "meituan/longcat-flash-chat:free",
            "object": "",
            "created": 1757427658,
            "ownedBy": ""
        },
        {
            "id": "meituan/longcat-flash-chat",
            "object": "",
            "created": 1757427658,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen-plus-2025-07-28",
            "object": "",
            "created": 1757347599,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen-plus-2025-07-28:thinking",
            "object": "",
            "created": 1757347599,
            "ownedBy": ""
        },
        {
            "id": "nvidia/nemotron-nano-9b-v2:free",
            "object": "",
            "created": 1757106807,
            "ownedBy": ""
        },
        {
            "id": "nvidia/nemotron-nano-9b-v2",
            "object": "",
            "created": 1757106807,
            "ownedBy": ""
        },
        {
            "id": "moonshotai/kimi-k2-0905",
            "object": "",
            "created": 1757021147,
            "ownedBy": ""
        },
        {
            "id": "moonshotai/kimi-k2-0905:exacto",
            "object": "",
            "created": 1757021147,
            "ownedBy": ""
        },
        {
            "id": "deepcogito/cogito-v2-preview-llama-70b",
            "object": "",
            "created": 1756831784,
            "ownedBy": ""
        },
        {
            "id": "deepcogito/cogito-v2-preview-llama-109b-moe",
            "object": "",
            "created": 1756831568,
            "ownedBy": ""
        },
        {
            "id": "deepcogito/cogito-v2-preview-deepseek-671b",
            "object": "",
            "created": 1756830949,
            "ownedBy": ""
        },
        {
            "id": "stepfun-ai/step3",
            "object": "",
            "created": 1756415375,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen3-30b-a3b-thinking-2507",
            "object": "",
            "created": 1756399192,
            "ownedBy": ""
        },
        {
            "id": "x-ai/grok-code-fast-1",
            "object": "",
            "created": 1756238927,
            "ownedBy": ""
        },
        {
            "id": "nousresearch/hermes-4-70b",
            "object": "",
            "created": 1756236182,
            "ownedBy": ""
        },
        {
            "id": "nousresearch/hermes-4-405b",
            "object": "",
            "created": 1756235463,
            "ownedBy": ""
        },
        {
            "id": "google/gemini-2.5-flash-image-preview",
            "object": "",
            "created": 1756218977,
            "ownedBy": ""
        },
        {
            "id": "deepseek/deepseek-chat-v3.1:free",
            "object": "",
            "created": 1755779628,
            "ownedBy": ""
        },
        {
            "id": "deepseek/deepseek-chat-v3.1",
            "object": "",
            "created": 1755779628,
            "ownedBy": ""
        },
        {
            "id": "openai/gpt-4o-audio-preview",
            "object": "",
            "created": 1755233061,
            "ownedBy": ""
        },
        {
            "id": "mistralai/mistral-medium-3.1",
            "object": "",
            "created": 1755095639,
            "ownedBy": ""
        },
        {
            "id": "baidu/ernie-4.5-21b-a3b",
            "object": "",
            "created": 1755034167,
            "ownedBy": ""
        },
        {
            "id": "baidu/ernie-4.5-vl-28b-a3b",
            "object": "",
            "created": 1755032836,
            "ownedBy": ""
        },
        {
            "id": "z-ai/glm-4.5v",
            "object": "",
            "created": 1754922288,
            "ownedBy": ""
        },
        {
            "id": "ai21/jamba-mini-1.7",
            "object": "",
            "created": 1754670601,
            "ownedBy": ""
        },
        {
            "id": "ai21/jamba-large-1.7",
            "object": "",
            "created": 1754669020,
            "ownedBy": ""
        },
        {
            "id": "openai/gpt-5-chat",
            "object": "",
            "created": 1754587837,
            "ownedBy": ""
        },
        {
            "id": "openai/gpt-5",
            "object": "",
            "created": 1754587413,
            "ownedBy": ""
        },
        {
            "id": "openai/gpt-5-mini",
            "object": "",
            "created": 1754587407,
            "ownedBy": ""
        },
        {
            "id": "openai/gpt-5-nano",
            "object": "",
            "created": 1754587402,
            "ownedBy": ""
        },
        {
            "id": "openai/gpt-oss-120b",
            "object": "",
            "created": 1754414231,
            "ownedBy": ""
        },
        {
            "id": "openai/gpt-oss-120b:exacto",
            "object": "",
            "created": 1754414231,
            "ownedBy": ""
        },
        {
            "id": "openai/gpt-oss-20b:free",
            "object": "",
            "created": 1754414229,
            "ownedBy": ""
        },
        {
            "id": "openai/gpt-oss-20b",
            "object": "",
            "created": 1754414229,
            "ownedBy": ""
        },
        {
            "id": "anthropic/claude-opus-4.1",
            "object": "",
            "created": 1754411591,
            "ownedBy": ""
        },
        {
            "id": "mistralai/codestral-2508",
            "object": "",
            "created": 1754079630,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen3-coder-30b-a3b-instruct",
            "object": "",
            "created": 1753972379,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen3-30b-a3b-instruct-2507",
            "object": "",
            "created": 1753806965,
            "ownedBy": ""
        },
        {
            "id": "z-ai/glm-4.5",
            "object": "",
            "created": 1753471347,
            "ownedBy": ""
        },
        {
            "id": "z-ai/glm-4.5-air:free",
            "object": "",
            "created": 1753471258,
            "ownedBy": ""
        },
        {
            "id": "z-ai/glm-4.5-air",
            "object": "",
            "created": 1753471258,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen3-235b-a22b-thinking-2507",
            "object": "",
            "created": 1753449557,
            "ownedBy": ""
        },
        {
            "id": "z-ai/glm-4-32b",
            "object": "",
            "created": 1753376617,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen3-coder:free",
            "object": "",
            "created": 1753230546,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen3-coder",
            "object": "",
            "created": 1753230546,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen3-coder:exacto",
            "object": "",
            "created": 1753230546,
            "ownedBy": ""
        },
        {
            "id": "bytedance/ui-tars-1.5-7b",
            "object": "",
            "created": 1753205056,
            "ownedBy": ""
        },
        {
            "id": "google/gemini-2.5-flash-lite",
            "object": "",
            "created": 1753200276,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen3-235b-a22b-2507",
            "object": "",
            "created": 1753119555,
            "ownedBy": ""
        },
        {
            "id": "switchpoint/router",
            "object": "",
            "created": 1752272899,
            "ownedBy": ""
        },
        {
            "id": "moonshotai/kimi-k2:free",
            "object": "",
            "created": 1752263252,
            "ownedBy": ""
        },
        {
            "id": "moonshotai/kimi-k2",
            "object": "",
            "created": 1752263252,
            "ownedBy": ""
        },
        {
            "id": "thudm/glm-4.1v-9b-thinking",
            "object": "",
            "created": 1752244385,
            "ownedBy": ""
        },
        {
            "id": "mistralai/devstral-medium",
            "object": "",
            "created": 1752161321,
            "ownedBy": ""
        },
        {
            "id": "mistralai/devstral-small",
            "object": "",
            "created": 1752160751,
            "ownedBy": ""
        },
        {
            "id": "cognitivecomputations/dolphin-mistral-24b-venice-edition:free",
            "object": "",
            "created": 1752094966,
            "ownedBy": ""
        },
        {
            "id": "x-ai/grok-4",
            "object": "",
            "created": 1752087689,
            "ownedBy": ""
        },
        {
            "id": "google/gemma-3n-e2b-it:free",
            "object": "",
            "created": 1752074904,
            "ownedBy": ""
        },
        {
            "id": "tencent/hunyuan-a13b-instruct",
            "object": "",
            "created": 1751987664,
            "ownedBy": ""
        },
        {
            "id": "tngtech/deepseek-r1t2-chimera:free",
            "object": "",
            "created": 1751986985,
            "ownedBy": ""
        },
        {
            "id": "tngtech/deepseek-r1t2-chimera",
            "object": "",
            "created": 1751986985,
            "ownedBy": ""
        },
        {
            "id": "morph/morph-v3-large",
            "object": "",
            "created": 1751910858,
            "ownedBy": ""
        },
        {
            "id": "morph/morph-v3-fast",
            "object": "",
            "created": 1751910002,
            "ownedBy": ""
        },
        {
            "id": "baidu/ernie-4.5-vl-424b-a47b",
            "object": "",
            "created": 1751300903,
            "ownedBy": ""
        },
        {
            "id": "baidu/ernie-4.5-300b-a47b",
            "object": "",
            "created": 1751300139,
            "ownedBy": ""
        },
        {
            "id": "thedrummer/anubis-70b-v1.1",
            "object": "",
            "created": 1751208347,
            "ownedBy": ""
        },
        {
            "id": "inception/mercury",
            "object": "",
            "created": 1750973026,
            "ownedBy": ""
        },
        {
            "id": "mistralai/mistral-small-3.2-24b-instruct:free",
            "object": "",
            "created": 1750443016,
            "ownedBy": ""
        },
        {
            "id": "mistralai/mistral-small-3.2-24b-instruct",
            "object": "",
            "created": 1750443016,
            "ownedBy": ""
        },
        {
            "id": "minimax/minimax-m1",
            "object": "",
            "created": 1750200414,
            "ownedBy": ""
        },
        {
            "id": "google/gemini-2.5-flash-lite-preview-06-17",
            "object": "",
            "created": 1750173831,
            "ownedBy": ""
        },
        {
            "id": "google/gemini-2.5-flash",
            "object": "",
            "created": 1750172488,
            "ownedBy": ""
        },
        {
            "id": "google/gemini-2.5-pro",
            "object": "",
            "created": 1750169544,
            "ownedBy": ""
        },
        {
            "id": "moonshotai/kimi-dev-72b:free",
            "object": "",
            "created": 1750115909,
            "ownedBy": ""
        },
        {
            "id": "moonshotai/kimi-dev-72b",
            "object": "",
            "created": 1750115909,
            "ownedBy": ""
        },
        {
            "id": "openai/o3-pro",
            "object": "",
            "created": 1749598352,
            "ownedBy": ""
        },
        {
            "id": "x-ai/grok-3-mini",
            "object": "",
            "created": 1749583245,
            "ownedBy": ""
        },
        {
            "id": "x-ai/grok-3",
            "object": "",
            "created": 1749582908,
            "ownedBy": ""
        },
        {
            "id": "mistralai/magistral-small-2506",
            "object": "",
            "created": 1749569561,
            "ownedBy": ""
        },
        {
            "id": "mistralai/magistral-medium-2506:thinking",
            "object": "",
            "created": 1749354054,
            "ownedBy": ""
        },
        {
            "id": "mistralai/magistral-medium-2506",
            "object": "",
            "created": 1749354054,
            "ownedBy": ""
        },
        {
            "id": "google/gemini-2.5-pro-preview",
            "object": "",
            "created": 1749137257,
            "ownedBy": ""
        },
        {
            "id": "deepseek/deepseek-r1-0528-qwen3-8b:free",
            "object": "",
            "created": 1748538543,
            "ownedBy": ""
        },
        {
            "id": "deepseek/deepseek-r1-0528-qwen3-8b",
            "object": "",
            "created": 1748538543,
            "ownedBy": ""
        },
        {
            "id": "deepseek/deepseek-r1-0528:free",
            "object": "",
            "created": 1748455170,
            "ownedBy": ""
        },
        {
            "id": "deepseek/deepseek-r1-0528",
            "object": "",
            "created": 1748455170,
            "ownedBy": ""
        },
        {
            "id": "anthropic/claude-opus-4",
            "object": "",
            "created": 1747931245,
            "ownedBy": ""
        },
        {
            "id": "anthropic/claude-sonnet-4",
            "object": "",
            "created": 1747930371,
            "ownedBy": ""
        },
        {
            "id": "mistralai/devstral-small-2505:free",
            "object": "",
            "created": 1747837379,
            "ownedBy": ""
        },
        {
            "id": "mistralai/devstral-small-2505",
            "object": "",
            "created": 1747837379,
            "ownedBy": ""
        },
        {
            "id": "google/gemma-3n-e4b-it:free",
            "object": "",
            "created": 1747776824,
            "ownedBy": ""
        },
        {
            "id": "google/gemma-3n-e4b-it",
            "object": "",
            "created": 1747776824,
            "ownedBy": ""
        },
        {
            "id": "openai/codex-mini",
            "object": "",
            "created": 1747409761,
            "ownedBy": ""
        },
        {
            "id": "meta-llama/llama-3.3-8b-instruct:free",
            "object": "",
            "created": 1747230154,
            "ownedBy": ""
        },
        {
            "id": "nousresearch/deephermes-3-mistral-24b-preview",
            "object": "",
            "created": 1746830904,
            "ownedBy": ""
        },
        {
            "id": "mistralai/mistral-medium-3",
            "object": "",
            "created": 1746627341,
            "ownedBy": ""
        },
        {
            "id": "google/gemini-2.5-pro-preview-05-06",
            "object": "",
            "created": 1746578513,
            "ownedBy": ""
        },
        {
            "id": "arcee-ai/spotlight",
            "object": "",
            "created": 1746481552,
            "ownedBy": ""
        },
        {
            "id": "arcee-ai/maestro-reasoning",
            "object": "",
            "created": 1746481269,
            "ownedBy": ""
        },
        {
            "id": "arcee-ai/virtuoso-large",
            "object": "",
            "created": 1746478885,
            "ownedBy": ""
        },
        {
            "id": "arcee-ai/coder-large",
            "object": "",
            "created": 1746478663,
            "ownedBy": ""
        },
        {
            "id": "microsoft/phi-4-reasoning-plus",
            "object": "",
            "created": 1746130961,
            "ownedBy": ""
        },
        {
            "id": "inception/mercury-coder",
            "object": "",
            "created": 1746033880,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen3-4b:free",
            "object": "",
            "created": 1746031104,
            "ownedBy": ""
        },
        {
            "id": "deepseek/deepseek-prover-v2",
            "object": "",
            "created": 1746013094,
            "ownedBy": ""
        },
        {
            "id": "meta-llama/llama-guard-4-12b",
            "object": "",
            "created": 1745975193,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen3-30b-a3b:free",
            "object": "",
            "created": 1745878604,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen3-30b-a3b",
            "object": "",
            "created": 1745878604,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen3-8b:free",
            "object": "",
            "created": 1745876632,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen3-8b",
            "object": "",
            "created": 1745876632,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen3-14b:free",
            "object": "",
            "created": 1745876478,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen3-14b",
            "object": "",
            "created": 1745876478,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen3-32b",
            "object": "",
            "created": 1745875945,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen3-235b-a22b:free",
            "object": "",
            "created": 1745875757,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen3-235b-a22b",
            "object": "",
            "created": 1745875757,
            "ownedBy": ""
        },
        {
            "id": "tngtech/deepseek-r1t-chimera:free",
            "object": "",
            "created": 1745760875,
            "ownedBy": ""
        },
        {
            "id": "tngtech/deepseek-r1t-chimera",
            "object": "",
            "created": 1745760875,
            "ownedBy": ""
        },
        {
            "id": "microsoft/mai-ds-r1:free",
            "object": "",
            "created": 1745194100,
            "ownedBy": ""
        },
        {
            "id": "microsoft/mai-ds-r1",
            "object": "",
            "created": 1745194100,
            "ownedBy": ""
        },
        {
            "id": "thudm/glm-z1-32b",
            "object": "",
            "created": 1744924148,
            "ownedBy": ""
        },
        {
            "id": "openai/o4-mini-high",
            "object": "",
            "created": 1744824212,
            "ownedBy": ""
        },
        {
            "id": "openai/o3",
            "object": "",
            "created": 1744823457,
            "ownedBy": ""
        },
        {
            "id": "openai/o4-mini",
            "object": "",
            "created": 1744820942,
            "ownedBy": ""
        },
        {
            "id": "shisa-ai/shisa-v2-llama3.3-70b:free",
            "object": "",
            "created": 1744754858,
            "ownedBy": ""
        },
        {
            "id": "shisa-ai/shisa-v2-llama3.3-70b",
            "object": "",
            "created": 1744754858,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen2.5-coder-7b-instruct",
            "object": "",
            "created": 1744734887,
            "ownedBy": ""
        },
        {
            "id": "openai/gpt-4.1",
            "object": "",
            "created": 1744651385,
            "ownedBy": ""
        },
        {
            "id": "openai/gpt-4.1-mini",
            "object": "",
            "created": 1744651381,
            "ownedBy": ""
        },
        {
            "id": "openai/gpt-4.1-nano",
            "object": "",
            "created": 1744651369,
            "ownedBy": ""
        },
        {
            "id": "eleutherai/llemma_7b",
            "object": "",
            "created": 1744643225,
            "ownedBy": ""
        },
        {
            "id": "alfredpros/codellama-7b-instruct-solidity",
            "object": "",
            "created": 1744641874,
            "ownedBy": ""
        },
        {
            "id": "arliai/qwq-32b-arliai-rpr-v1:free",
            "object": "",
            "created": 1744555982,
            "ownedBy": ""
        },
        {
            "id": "arliai/qwq-32b-arliai-rpr-v1",
            "object": "",
            "created": 1744555982,
            "ownedBy": ""
        },
        {
            "id": "agentica-org/deepcoder-14b-preview:free",
            "object": "",
            "created": 1744555395,
            "ownedBy": ""
        },
        {
            "id": "agentica-org/deepcoder-14b-preview",
            "object": "",
            "created": 1744555395,
            "ownedBy": ""
        },
        {
            "id": "x-ai/grok-3-mini-beta",
            "object": "",
            "created": 1744240195,
            "ownedBy": ""
        },
        {
            "id": "x-ai/grok-3-beta",
            "object": "",
            "created": 1744240068,
            "ownedBy": ""
        },
        {
            "id": "nvidia/llama-3.1-nemotron-ultra-253b-v1",
            "object": "",
            "created": 1744115059,
            "ownedBy": ""
        },
        {
            "id": "meta-llama/llama-4-maverick:free",
            "object": "",
            "created": 1743881822,
            "ownedBy": ""
        },
        {
            "id": "meta-llama/llama-4-maverick",
            "object": "",
            "created": 1743881822,
            "ownedBy": ""
        },
        {
            "id": "meta-llama/llama-4-scout:free",
            "object": "",
            "created": 1743881519,
            "ownedBy": ""
        },
        {
            "id": "meta-llama/llama-4-scout",
            "object": "",
            "created": 1743881519,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen2.5-vl-32b-instruct:free",
            "object": "",
            "created": 1742839838,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen2.5-vl-32b-instruct",
            "object": "",
            "created": 1742839838,
            "ownedBy": ""
        },
        {
            "id": "deepseek/deepseek-chat-v3-0324:free",
            "object": "",
            "created": 1742824755,
            "ownedBy": ""
        },
        {
            "id": "deepseek/deepseek-chat-v3-0324",
            "object": "",
            "created": 1742824755,
            "ownedBy": ""
        },
        {
            "id": "openai/o1-pro",
            "object": "",
            "created": 1742423211,
            "ownedBy": ""
        },
        {
            "id": "mistralai/mistral-small-3.1-24b-instruct:free",
            "object": "",
            "created": 1742238937,
            "ownedBy": ""
        },
        {
            "id": "mistralai/mistral-small-3.1-24b-instruct",
            "object": "",
            "created": 1742238937,
            "ownedBy": ""
        },
        {
            "id": "allenai/olmo-2-0325-32b-instruct",
            "object": "",
            "created": 1741988556,
            "ownedBy": ""
        },
        {
            "id": "google/gemma-3-4b-it:free",
            "object": "",
            "created": 1741905510,
            "ownedBy": ""
        },
        {
            "id": "google/gemma-3-4b-it",
            "object": "",
            "created": 1741905510,
            "ownedBy": ""
        },
        {
            "id": "google/gemma-3-12b-it:free",
            "object": "",
            "created": 1741902625,
            "ownedBy": ""
        },
        {
            "id": "google/gemma-3-12b-it",
            "object": "",
            "created": 1741902625,
            "ownedBy": ""
        },
        {
            "id": "cohere/command-a",
            "object": "",
            "created": 1741894342,
            "ownedBy": ""
        },
        {
            "id": "openai/gpt-4o-mini-search-preview",
            "object": "",
            "created": 1741818122,
            "ownedBy": ""
        },
        {
            "id": "openai/gpt-4o-search-preview",
            "object": "",
            "created": 1741817949,
            "ownedBy": ""
        },
        {
            "id": "google/gemma-3-27b-it:free",
            "object": "",
            "created": 1741756359,
            "ownedBy": ""
        },
        {
            "id": "google/gemma-3-27b-it",
            "object": "",
            "created": 1741756359,
            "ownedBy": ""
        },
        {
            "id": "thedrummer/skyfall-36b-v2",
            "object": "",
            "created": 1741636566,
            "ownedBy": ""
        },
        {
            "id": "microsoft/phi-4-multimodal-instruct",
            "object": "",
            "created": 1741396284,
            "ownedBy": ""
        },
        {
            "id": "perplexity/sonar-reasoning-pro",
            "object": "",
            "created": 1741313308,
            "ownedBy": ""
        },
        {
            "id": "perplexity/sonar-pro",
            "object": "",
            "created": 1741312423,
            "ownedBy": ""
        },
        {
            "id": "perplexity/sonar-deep-research",
            "object": "",
            "created": 1741311246,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwq-32b",
            "object": "",
            "created": 1741208814,
            "ownedBy": ""
        },
        {
            "id": "nousresearch/deephermes-3-llama-3-8b-preview:free",
            "object": "",
            "created": 1740719372,
            "ownedBy": ""
        },
        {
            "id": "nousresearch/deephermes-3-llama-3-8b-preview",
            "object": "",
            "created": 1740719372,
            "ownedBy": ""
        },
        {
            "id": "google/gemini-2.0-flash-lite-001",
            "object": "",
            "created": 1740506212,
            "ownedBy": ""
        },
        {
            "id": "anthropic/claude-3.7-sonnet:thinking",
            "object": "",
            "created": 1740422110,
            "ownedBy": ""
        },
        {
            "id": "anthropic/claude-3.7-sonnet",
            "object": "",
            "created": 1740422110,
            "ownedBy": ""
        },
        {
            "id": "mistralai/mistral-saba",
            "object": "",
            "created": 1739803239,
            "ownedBy": ""
        },
        {
            "id": "cognitivecomputations/dolphin3.0-mistral-24b:free",
            "object": "",
            "created": 1739462019,
            "ownedBy": ""
        },
        {
            "id": "cognitivecomputations/dolphin3.0-mistral-24b",
            "object": "",
            "created": 1739462019,
            "ownedBy": ""
        },
        {
            "id": "meta-llama/llama-guard-3-8b",
            "object": "",
            "created": 1739401318,
            "ownedBy": ""
        },
        {
            "id": "openai/o3-mini-high",
            "object": "",
            "created": 1739372611,
            "ownedBy": ""
        },
        {
            "id": "google/gemini-2.0-flash-001",
            "object": "",
            "created": 1738769413,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen-vl-plus",
            "object": "",
            "created": 1738731255,
            "ownedBy": ""
        },
        {
            "id": "aion-labs/aion-1.0",
            "object": "",
            "created": 1738697557,
            "ownedBy": ""
        },
        {
            "id": "aion-labs/aion-1.0-mini",
            "object": "",
            "created": 1738697107,
            "ownedBy": ""
        },
        {
            "id": "aion-labs/aion-rp-llama-3.1-8b",
            "object": "",
            "created": 1738696718,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen-vl-max",
            "object": "",
            "created": 1738434304,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen-turbo",
            "object": "",
            "created": 1738410974,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen2.5-vl-72b-instruct",
            "object": "",
            "created": 1738410311,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen-plus",
            "object": "",
            "created": 1738409840,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen-max",
            "object": "",
            "created": 1738402289,
            "ownedBy": ""
        },
        {
            "id": "openai/o3-mini",
            "object": "",
            "created": 1738351721,
            "ownedBy": ""
        },
        {
            "id": "mistralai/mistral-small-24b-instruct-2501:free",
            "object": "",
            "created": 1738255409,
            "ownedBy": ""
        },
        {
            "id": "mistralai/mistral-small-24b-instruct-2501",
            "object": "",
            "created": 1738255409,
            "ownedBy": ""
        },
        {
            "id": "deepseek/deepseek-r1-distill-qwen-32b",
            "object": "",
            "created": 1738194830,
            "ownedBy": ""
        },
        {
            "id": "deepseek/deepseek-r1-distill-qwen-14b",
            "object": "",
            "created": 1738193940,
            "ownedBy": ""
        },
        {
            "id": "perplexity/sonar-reasoning",
            "object": "",
            "created": 1738131107,
            "ownedBy": ""
        },
        {
            "id": "perplexity/sonar",
            "object": "",
            "created": 1738013808,
            "ownedBy": ""
        },
        {
            "id": "deepseek/deepseek-r1-distill-llama-70b:free",
            "object": "",
            "created": 1737663169,
            "ownedBy": ""
        },
        {
            "id": "deepseek/deepseek-r1-distill-llama-70b",
            "object": "",
            "created": 1737663169,
            "ownedBy": ""
        },
        {
            "id": "deepseek/deepseek-r1:free",
            "object": "",
            "created": 1737381095,
            "ownedBy": ""
        },
        {
            "id": "deepseek/deepseek-r1",
            "object": "",
            "created": 1737381095,
            "ownedBy": ""
        },
        {
            "id": "minimax/minimax-01",
            "object": "",
            "created": 1736915462,
            "ownedBy": ""
        },
        {
            "id": "mistralai/codestral-2501",
            "object": "",
            "created": 1736895522,
            "ownedBy": ""
        },
        {
            "id": "microsoft/phi-4",
            "object": "",
            "created": 1736489872,
            "ownedBy": ""
        },
        {
            "id": "sao10k/l3.1-70b-hanami-x1",
            "object": "",
            "created": 1736302854,
            "ownedBy": ""
        },
        {
            "id": "deepseek/deepseek-chat",
            "object": "",
            "created": 1735241320,
            "ownedBy": ""
        },
        {
            "id": "sao10k/l3.3-euryale-70b",
            "object": "",
            "created": 1734535928,
            "ownedBy": ""
        },
        {
            "id": "openai/o1",
            "object": "",
            "created": 1734459999,
            "ownedBy": ""
        },
        {
            "id": "cohere/command-r7b-12-2024",
            "object": "",
            "created": 1734158152,
            "ownedBy": ""
        },
        {
            "id": "google/gemini-2.0-flash-exp:free",
            "object": "",
            "created": 1733937523,
            "ownedBy": ""
        },
        {
            "id": "meta-llama/llama-3.3-70b-instruct:free",
            "object": "",
            "created": 1733506137,
            "ownedBy": ""
        },
        {
            "id": "meta-llama/llama-3.3-70b-instruct",
            "object": "",
            "created": 1733506137,
            "ownedBy": ""
        },
        {
            "id": "amazon/nova-lite-v1",
            "object": "",
            "created": 1733437363,
            "ownedBy": ""
        },
        {
            "id": "amazon/nova-micro-v1",
            "object": "",
            "created": 1733437237,
            "ownedBy": ""
        },
        {
            "id": "amazon/nova-pro-v1",
            "object": "",
            "created": 1733436303,
            "ownedBy": ""
        },
        {
            "id": "openai/gpt-4o-2024-11-20",
            "object": "",
            "created": 1732127594,
            "ownedBy": ""
        },
        {
            "id": "mistralai/mistral-large-2411",
            "object": "",
            "created": 1731978685,
            "ownedBy": ""
        },
        {
            "id": "mistralai/mistral-large-2407",
            "object": "",
            "created": 1731978415,
            "ownedBy": ""
        },
        {
            "id": "mistralai/pixtral-large-2411",
            "object": "",
            "created": 1731977388,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen-2.5-coder-32b-instruct:free",
            "object": "",
            "created": 1731368400,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen-2.5-coder-32b-instruct",
            "object": "",
            "created": 1731368400,
            "ownedBy": ""
        },
        {
            "id": "raifle/sorcererlm-8x22b",
            "object": "",
            "created": 1731105083,
            "ownedBy": ""
        },
        {
            "id": "thedrummer/unslopnemo-12b",
            "object": "",
            "created": 1731103448,
            "ownedBy": ""
        },
        {
            "id": "anthropic/claude-3.5-haiku",
            "object": "",
            "created": 1730678400,
            "ownedBy": ""
        },
        {
            "id": "anthropic/claude-3.5-haiku-20241022",
            "object": "",
            "created": 1730678400,
            "ownedBy": ""
        },
        {
            "id": "anthracite-org/magnum-v4-72b",
            "object": "",
            "created": 1729555200,
            "ownedBy": ""
        },
        {
            "id": "anthropic/claude-3.5-sonnet",
            "object": "",
            "created": 1729555200,
            "ownedBy": ""
        },
        {
            "id": "mistralai/ministral-3b",
            "object": "",
            "created": 1729123200,
            "ownedBy": ""
        },
        {
            "id": "mistralai/ministral-8b",
            "object": "",
            "created": 1729123200,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen-2.5-7b-instruct",
            "object": "",
            "created": 1729036800,
            "ownedBy": ""
        },
        {
            "id": "nvidia/llama-3.1-nemotron-70b-instruct",
            "object": "",
            "created": 1728950400,
            "ownedBy": ""
        },
        {
            "id": "inflection/inflection-3-productivity",
            "object": "",
            "created": 1728604800,
            "ownedBy": ""
        },
        {
            "id": "inflection/inflection-3-pi",
            "object": "",
            "created": 1728604800,
            "ownedBy": ""
        },
        {
            "id": "anthracite-org/magnum-v2-72b",
            "object": "",
            "created": 1727654400,
            "ownedBy": ""
        },
        {
            "id": "thedrummer/rocinante-12b",
            "object": "",
            "created": 1727654400,
            "ownedBy": ""
        },
        {
            "id": "meta-llama/llama-3.2-1b-instruct",
            "object": "",
            "created": 1727222400,
            "ownedBy": ""
        },
        {
            "id": "meta-llama/llama-3.2-3b-instruct:free",
            "object": "",
            "created": 1727222400,
            "ownedBy": ""
        },
        {
            "id": "meta-llama/llama-3.2-3b-instruct",
            "object": "",
            "created": 1727222400,
            "ownedBy": ""
        },
        {
            "id": "meta-llama/llama-3.2-90b-vision-instruct",
            "object": "",
            "created": 1727222400,
            "ownedBy": ""
        },
        {
            "id": "meta-llama/llama-3.2-11b-vision-instruct",
            "object": "",
            "created": 1727222400,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen-2.5-72b-instruct:free",
            "object": "",
            "created": 1726704000,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen-2.5-72b-instruct",
            "object": "",
            "created": 1726704000,
            "ownedBy": ""
        },
        {
            "id": "neversleep/llama-3.1-lumimaid-8b",
            "object": "",
            "created": 1726358400,
            "ownedBy": ""
        },
        {
            "id": "mistralai/pixtral-12b",
            "object": "",
            "created": 1725926400,
            "ownedBy": ""
        },
        {
            "id": "cohere/command-r-plus-08-2024",
            "object": "",
            "created": 1724976000,
            "ownedBy": ""
        },
        {
            "id": "cohere/command-r-08-2024",
            "object": "",
            "created": 1724976000,
            "ownedBy": ""
        },
        {
            "id": "sao10k/l3.1-euryale-70b",
            "object": "",
            "created": 1724803200,
            "ownedBy": ""
        },
        {
            "id": "qwen/qwen-2.5-vl-7b-instruct",
            "object": "",
            "created": 1724803200,
            "ownedBy": ""
        },
        {
            "id": "microsoft/phi-3.5-mini-128k-instruct",
            "object": "",
            "created": 1724198400,
            "ownedBy": ""
        },
        {
            "id": "nousresearch/hermes-3-llama-3.1-70b",
            "object": "",
            "created": 1723939200,
            "ownedBy": ""
        },
        {
            "id": "nousresearch/hermes-3-llama-3.1-405b:free",
            "object": "",
            "created": 1723766400,
            "ownedBy": ""
        },
        {
            "id": "nousresearch/hermes-3-llama-3.1-405b",
            "object": "",
            "created": 1723766400,
            "ownedBy": ""
        },
        {
            "id": "openai/chatgpt-4o-latest",
            "object": "",
            "created": 1723593600,
            "ownedBy": ""
        },
        {
            "id": "sao10k/l3-lunaris-8b",
            "object": "",
            "created": 1723507200,
            "ownedBy": ""
        },
        {
            "id": "openai/gpt-4o-2024-08-06",
            "object": "",
            "created": 1722902400,
            "ownedBy": ""
        },
        {
            "id": "meta-llama/llama-3.1-405b",
            "object": "",
            "created": 1722556800,
            "ownedBy": ""
        },
        {
            "id": "meta-llama/llama-3.1-8b-instruct",
            "object": "",
            "created": 1721692800,
            "ownedBy": ""
        },
        {
            "id": "meta-llama/llama-3.1-70b-instruct",
            "object": "",
            "created": 1721692800,
            "ownedBy": ""
        },
        {
            "id": "meta-llama/llama-3.1-405b-instruct",
            "object": "",
            "created": 1721692800,
            "ownedBy": ""
        },
        {
            "id": "mistralai/mistral-nemo:free",
            "object": "",
            "created": 1721347200,
            "ownedBy": ""
        },
        {
            "id": "mistralai/mistral-nemo",
            "object": "",
            "created": 1721347200,
            "ownedBy": ""
        },
        {
            "id": "openai/gpt-4o-mini-2024-07-18",
            "object": "",
            "created": 1721260800,
            "ownedBy": ""
        },
        {
            "id": "openai/gpt-4o-mini",
            "object": "",
            "created": 1721260800,
            "ownedBy": ""
        },
        {
            "id": "google/gemma-2-27b-it",
            "object": "",
            "created": 1720828800,
            "ownedBy": ""
        },
        {
            "id": "google/gemma-2-9b-it:free",
            "object": "",
            "created": 1719532800,
            "ownedBy": ""
        },
        {
            "id": "google/gemma-2-9b-it",
            "object": "",
            "created": 1719532800,
            "ownedBy": ""
        },
        {
            "id": "anthropic/claude-3.5-sonnet-20240620",
            "object": "",
            "created": 1718841600,
            "ownedBy": ""
        },
        {
            "id": "sao10k/l3-euryale-70b",
            "object": "",
            "created": 1718668800,
            "ownedBy": ""
        },
        {
            "id": "nousresearch/hermes-2-pro-llama-3-8b",
            "object": "",
            "created": 1716768000,
            "ownedBy": ""
        },
        {
            "id": "mistralai/mistral-7b-instruct:free",
            "object": "",
            "created": 1716768000,
            "ownedBy": ""
        },
        {
            "id": "mistralai/mistral-7b-instruct",
            "object": "",
            "created": 1716768000,
            "ownedBy": ""
        },
        {
            "id": "mistralai/mistral-7b-instruct-v0.3",
            "object": "",
            "created": 1716768000,
            "ownedBy": ""
        },
        {
            "id": "microsoft/phi-3-mini-128k-instruct",
            "object": "",
            "created": 1716681600,
            "ownedBy": ""
        },
        {
            "id": "microsoft/phi-3-medium-128k-instruct",
            "object": "",
            "created": 1716508800,
            "ownedBy": ""
        },
        {
            "id": "openai/gpt-4o-2024-05-13",
            "object": "",
            "created": 1715558400,
            "ownedBy": ""
        },
        {
            "id": "openai/gpt-4o",
            "object": "",
            "created": 1715558400,
            "ownedBy": ""
        },
        {
            "id": "openai/gpt-4o:extended",
            "object": "",
            "created": 1715558400,
            "ownedBy": ""
        },
        {
            "id": "meta-llama/llama-guard-2-8b",
            "object": "",
            "created": 1715558400,
            "ownedBy": ""
        },
        {
            "id": "meta-llama/llama-3-70b-instruct",
            "object": "",
            "created": 1713398400,
            "ownedBy": ""
        },
        {
            "id": "meta-llama/llama-3-8b-instruct",
            "object": "",
            "created": 1713398400,
            "ownedBy": ""
        },
        {
            "id": "mistralai/mixtral-8x22b-instruct",
            "object": "",
            "created": 1713312000,
            "ownedBy": ""
        },
        {
            "id": "microsoft/wizardlm-2-8x22b",
            "object": "",
            "created": 1713225600,
            "ownedBy": ""
        },
        {
            "id": "openai/gpt-4-turbo",
            "object": "",
            "created": 1712620800,
            "ownedBy": ""
        },
        {
            "id": "anthropic/claude-3-haiku",
            "object": "",
            "created": 1710288000,
            "ownedBy": ""
        },
        {
            "id": "anthropic/claude-3-opus",
            "object": "",
            "created": 1709596800,
            "ownedBy": ""
        },
        {
            "id": "mistralai/mistral-large",
            "object": "",
            "created": 1708905600,
            "ownedBy": ""
        },
        {
            "id": "openai/gpt-4-turbo-preview",
            "object": "",
            "created": 1706140800,
            "ownedBy": ""
        },
        {
            "id": "openai/gpt-3.5-turbo-0613",
            "object": "",
            "created": 1706140800,
            "ownedBy": ""
        },
        {
            "id": "mistralai/mistral-small",
            "object": "",
            "created": 1704844800,
            "ownedBy": ""
        },
        {
            "id": "mistralai/mistral-tiny",
            "object": "",
            "created": 1704844800,
            "ownedBy": ""
        },
        {
            "id": "mistralai/mistral-7b-instruct-v0.2",
            "object": "",
            "created": 1703721600,
            "ownedBy": ""
        },
        {
            "id": "mistralai/mixtral-8x7b-instruct",
            "object": "",
            "created": 1702166400,
            "ownedBy": ""
        },
        {
            "id": "neversleep/noromaid-20b",
            "object": "",
            "created": 1700956800,
            "ownedBy": ""
        },
        {
            "id": "alpindale/goliath-120b",
            "object": "",
            "created": 1699574400,
            "ownedBy": ""
        },
        {
            "id": "openrouter/auto",
            "object": "",
            "created": 1699401600,
            "ownedBy": ""
        },
        {
            "id": "openai/gpt-4-1106-preview",
            "object": "",
            "created": 1699228800,
            "ownedBy": ""
        },
        {
            "id": "mistralai/mistral-7b-instruct-v0.1",
            "object": "",
            "created": 1695859200,
            "ownedBy": ""
        },
        {
            "id": "openai/gpt-3.5-turbo-instruct",
            "object": "",
            "created": 1695859200,
            "ownedBy": ""
        },
        {
            "id": "openai/gpt-3.5-turbo-16k",
            "object": "",
            "created": 1693180800,
            "ownedBy": ""
        },
        {
            "id": "mancer/weaver",
            "object": "",
            "created": 1690934400,
            "ownedBy": ""
        },
        {
            "id": "undi95/remm-slerp-l2-13b",
            "object": "",
            "created": 1689984000,
            "ownedBy": ""
        },
        {
            "id": "gryphe/mythomax-l2-13b",
            "object": "",
            "created": 1688256000,
            "ownedBy": ""
        },
        {
            "id": "openai/gpt-4-0314",
            "object": "",
            "created": 1685232000,
            "ownedBy": ""
        },
        {
            "id": "openai/gpt-3.5-turbo",
            "object": "",
            "created": 1685232000,
            "ownedBy": ""
        },
        {
            "id": "openai/gpt-4",
            "object": "",
            "created": 1685232000,
            "ownedBy": ""
        }
    ],
    "object": "list"
}