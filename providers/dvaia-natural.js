function normalizeToolCalls(value) {
  if (!Array.isArray(value)) return [];
  return value
    .map((item) => {
      if (typeof item === 'string') return item;
      if (item && typeof item.name === 'string') return item.name;
      return null;
    })
    .filter(Boolean);
}

module.exports = (json, text) => {
  if (!json || typeof json !== 'object') {
    return { error: `DVAIA returned a non-JSON response: ${String(text || '')}` };
  }

  if (json.error) {
    return { error: `DVAIA error: ${json.error}`, raw: json };
  }

  const toolNames = normalizeToolCalls(json.tool_calls);

  return {
    output: String(json.response || ''),
    raw: json,
    metadata: {
      toolCalls: toolNames.map((name) => ({ name })),
      dvaia: {
        toolCalls: toolNames,
        thinking: String(json.thinking || ''),
        messages: Array.isArray(json.messages) ? json.messages : [],
        llmProvider: json.llm_provider || null,
      },
    },
  };
};
