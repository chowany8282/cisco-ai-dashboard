# COST_GUARDRAILS

## Model policy
- Default: `gemini-2.5-flash-lite`
- Use larger models only when answer quality is insufficient

## Prompt policy
- Keep prompts task-focused and short
- Avoid repeating long static instruction blocks inside runtime text
- Reuse prompt templates from `prompts/`

## Operational limits
- If error rate spikes, reduce retries temporarily
- For expensive tabs, test with minimal input first
- Track rough daily call count from provider dashboard

## Budget alerts (manual)
- Daily: check provider usage page once
- Weekly: compare previous week and flag >30% increase

## Incident response
- If cost anomaly appears:
  1. Identify high-volume tab/model
  2. Force default to flash-lite
  3. Announce temporary limitations
  4. Review logs and adjust prompt/retry behavior
