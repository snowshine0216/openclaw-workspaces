# Notion Schema

This reference defines the target Notion structure for the frontier-intel skill.

## Databases

- `AI Research Items`
- `AI Research Digests`

## Minimum viable fields

### `AI Research Items`
- `Title`
- `Type`
- `Source`
- `Published At`
- `URL`
- `PDF URL`
- `Executive Summary`
- `Highlights`
- `Suggested Actions`
- `Learning`
- `Digest Date`
- `Week`
- `Dedup Key`

### `AI Research Digests`
- `Title`
- `Period`
- `Digest Date`
- `Week`
- `Executive Summary`
- `Top Highlights`
- `Suggested Actions`
- `Learning Themes`
- `Item Count`

## Notes

- Use `Week` as text in phase one
- Keep item-level links mandatory
- For `arXiv`, store both source page and PDF URL
