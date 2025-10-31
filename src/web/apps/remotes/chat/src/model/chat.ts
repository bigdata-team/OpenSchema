// chat-model.ts
export class Chat {
  id: string;

  parent_id: string | null = null;
  title: string | null = null;
  index: number | null = null;

  user_id: string | null = null;
  service_id: string | null = null;
  url: string | null = null;
  user_prompt: string | null = null;
  answer: string | null = null;
  request: string | null = null;
  response: string | null = null;

  completion_id: string | null = null;
  model_name: string | null = null;
  prompt_tokens: number | null = null;
  completion_tokens: number | null = null;
  total_tokens: number | null = null;
  is_stream: boolean | null = null;
  system_prompt: string | null = null;
  parameters: string | null = null;

  children: Chat[] = [];

  /**
   * Construct from a partial Chat (plain object allowed).
   * Example: new Chat({ id: '1', user_prompt: 'hi', children: [{ user_prompt: 'reply' }] })
   */
  constructor(data?: Partial<Chat>) {
    this.id = data?.id ?? '';

    // scalar fields
    this.parent_id = data?.parent_id ?? null;
    this.title = data?.title ?? null;
    this.index = data?.index ?? null;

    this.user_id = data?.user_id ?? null;
    this.service_id = data?.service_id ?? null;
    this.url = data?.url ?? null;
    this.user_prompt = data?.user_prompt ?? null;
    this.answer = data?.answer ?? null;
    this.request = data?.request ?? null;
    this.response = data?.response ?? null;

    this.completion_id = data?.completion_id ?? null;
    this.model_name = data?.model_name ?? null;
    this.prompt_tokens = data?.prompt_tokens ?? null;
    this.completion_tokens = data?.completion_tokens ?? null;
    this.total_tokens = data?.total_tokens ?? null;
    this.is_stream = data?.is_stream ?? null;
    this.system_prompt = data?.system_prompt ?? null;
    this.parameters = data?.parameters ?? null;

    // children
    this.children =
      data?.children?.map((c) => (c instanceof Chat ? c : new Chat(c))) ?? [];
  }

  addChild(child: Partial<Chat> | Chat): Chat {
    const node = child instanceof Chat ? child : new Chat(child);
    node.parent_id = this.id;
    this.children.push(node);
    return node;
  }

  removeChildById(id: string): boolean {
    const idx = this.children.findIndex((c) => c.id === id);
    if (idx >= 0) {
      this.children.splice(idx, 1);
      return true;
    }
    for (const c of this.children) {
      if (c.removeChildById(id)) return true;
    }
    return false;
  }

  findById(id: string): Chat | null {
    if (this.id === id) return this;
    for (const c of this.children) {
      const found = c.findById(id);
      if (found) return found;
    }
    return null;
  }

  recalcTotalTokens(): number {
    const p = this.prompt_tokens ?? 0;
    const c = this.completion_tokens ?? 0;
    this.total_tokens = p + c;
    return this.total_tokens;
  }

  clone(): Chat {
    const plain = this.toPlain();
    return Chat.fromPlain(plain as Partial<Chat>);
  }

  /** Return a plain JSON-serializable object (no methods). */
  toPlain(): Record<string, any> {
    return {
      id: this.id,
      parent_id: this.parent_id,
      title: this.title,
      index: this.index,

      user_id: this.user_id,
      service_id: this.service_id,
      url: this.url,
      user_prompt: this.user_prompt,
      answer: this.answer,
      request: this.request,
      response: this.response,

      completion_id: this.completion_id,
      model_name: this.model_name,
      prompt_tokens: this.prompt_tokens,
      completion_tokens: this.completion_tokens,
      total_tokens: this.total_tokens,
      is_stream: this.is_stream,
      system_prompt: this.system_prompt,
      parameters: this.parameters,

      children: this.children.map((c) => c.toPlain()),
    };
  }

  /** Factory that accepts a plain object (same shape as toPlain) */
  static fromPlain(data?: Partial<Chat>): Chat {
    return new Chat(data);
  }

  /** JSON string (pretty optional) */
  toJSON(pretty = false): string {
    return pretty ? JSON.stringify(this.toPlain(), null, 2) : JSON.stringify(this.toPlain());
  }
}
