import React from "react";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { type Model, modelManager } from "@/model";
import { openai, google, anthropic, qwen, deepseek, grok } from '@/components/Icon';

export default function ChatModelSelect({
    model,
}: {
    model: Model;
}) {
    const [selectedModel, setSelectedModel] = React.useState<string>(model.model);

    React.useEffect(() => {
        setSelectedModel(selectedModel);
        model.model = selectedModel;
    }, [selectedModel]);

    return (
        <Select value={selectedModel} onValueChange={setSelectedModel}>
            <SelectTrigger className="w-full h-7 text-xs font-medium font-mono">
                <SelectValue placeholder="Select model">
                    <div className="flex items-center gap-2">
                        {selectedModel.startsWith("openai") && openai("")}
                        {selectedModel.startsWith("google") && google("")}
                        {selectedModel.startsWith("anthropic") && anthropic("")}
                        {selectedModel.startsWith("qwen") && qwen("")}
                        {selectedModel.startsWith("deepseek") && deepseek("")}
                        {selectedModel.startsWith("x-ai") && grok("")}
                        <span>{selectedModel.split("/").length > 1 ? selectedModel.split("/")[1] : selectedModel}</span>
                    </div>
                </SelectValue>
            </SelectTrigger>
            <SelectContent>
                {modelManager.availableModels.map((m) => (
                    <SelectItem key={m.model} value={m.model}>
                        <div className="flex items-center gap-2">
                            {m.model.startsWith("openai") && openai("")}
                            {m.model.startsWith("google") && google("")}
                            {m.model.startsWith("anthropic") && anthropic("")}
                            {m.model.startsWith("qwen") && qwen("")}
                            {m.model.startsWith("deepseek") && deepseek("")}
                            {m.model.startsWith("x-ai") && grok("")}
                            <span>{m.model.split("/").length > 1 ? m.model.split("/")[1] : m.model}</span>
                        </div>
                    </SelectItem>
                ))}
            </SelectContent>
        </Select>
    );
}
