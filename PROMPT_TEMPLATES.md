# Prompt Templates

Reusable prompts for common AI assistant workflows. Copy and customize these for consistent, high-quality results.

## Database & Repository Layer

- "Create a repository and service layer for X using SQLAlchemy 2.0 style; inject session; include unit tests with pytest fixtures."
- "Add a new SQLAlchemy model for [entity] with relationships to [related entities]; include Alembic migration; follow declarative base pattern."
- "Write a database query using SQLAlchemy 2.0 select() that [description]; optimize with joinedload for N+1 prevention; add type hints."

## Code Quality & Refactoring

- "Refactor this function into pure logic + adapter; add type hints and docstrings; keep under 40 lines."
- "Extract this code into a reusable utility function; add comprehensive type hints; write unit tests; document edge cases."
- "Review this module for code smells; suggest refactorings following SOLID principles; maintain backward compatibility."
- "Add comprehensive type hints to this module; ensure MyPy strict mode passes; document any type: ignore with justification."

## Testing

- "Generate behave feature and step definitions for [scenario]; keep steps reusable and domain-focused."
- "Write Playwright test for [workflow] with fixtures for auth and baseURL; record trace on failure."
- "Create pytest fixtures for [resource]; use session scope where appropriate; include cleanup; add docstrings."
- "Write unit tests for [function/class] covering happy path, edge cases, and error conditions; use pytest parametrize; aim for 100% coverage."
- "Add integration tests for [API endpoint/workflow]; mock external dependencies; verify database state; use pytest-cov."

## API Development

- "Create a FastAPI endpoint for [operation]; include request/response models with Pydantic; add OpenAPI documentation; handle errors gracefully."
- "Add input validation to [endpoint] using Pydantic; return 422 for validation errors; include helpful error messages."
- "Write API client wrapper for [service]; include retry logic; add type hints; handle rate limiting; log requests."

## Documentation

- "Add docstrings to this module following Google style; include examples; document all parameters and return values; note any side effects."
- "Create a README section explaining how to [task]; include code examples; list prerequisites; add troubleshooting tips."
- "Document this API endpoint with usage examples; include curl commands; show request/response samples; note authentication requirements."

## Error Handling & Logging

- "Add comprehensive error handling to [function]; log errors with context; raise specific exceptions; include recovery suggestions."
- "Implement structured logging for [module]; use appropriate log levels; include correlation IDs; avoid logging sensitive data."

## Performance & Optimization

- "Profile this code and identify bottlenecks; suggest optimizations; maintain readability; add benchmarks to verify improvements."
- "Add caching to [expensive operation]; use appropriate TTL; handle cache invalidation; add cache hit/miss metrics."

## Configuration & Environment

- "Extract hardcoded values to environment variables; add validation; provide sensible defaults; document in .env.example."
- "Create a configuration class for [module]; use Pydantic for validation; support multiple environments; add type hints."

## Migration & Upgrade

- "Create an Alembic migration for [schema change]; include both upgrade and downgrade; test with sample data; document any manual steps."
- "Upgrade [dependency] to version X; fix breaking changes; update tests; verify backward compatibility where needed."
