# Feature Implementation Prompt Template (Angular)

You are implementing a feature in an Angular app.

Before implementing any feature, you must load and follow the corresponding instruction file(s) for each requirement section below.

## Mandatory Instruction Files
- Implementation Requirements -> `.github/instructions/angular.instructions.md`
- UI/UX Requirements -> `.github/instructions/ux-ui-glassmorphism.instructions.md`
- Security Requirements -> `.github/instructions/security.instructions.md`
- Testing Requirements -> `.github/instructions/testing.instructions.md`
- Documentation Requirements -> `.github/instructions/documentation.instructions.md`
- If additional requirement categories are added, follow their corresponding `*.instructions.md` file before implementation.

## Feature Name
{{FEATURE_NAME}}

## Business Goal
{{BUSINESS_GOAL}}

## Detailed Feature Description
{{DETAILED_DESCRIPTION}}

Include:
- User story
- Acceptance criteria
- Edge cases
- Failure states
- Permissions and roles involved

## Implementation Requirements
{{IMPLEMENTATION_REQUIREMENTS}}

Follow `.github/instructions/angular.instructions.md` for all implementation decisions.

Include:
- Routing changes
- Components/services/guards/interceptors needed
- State management approach
- API/Auth integration details (if applicable)
- Error handling and loading states

## UI/UX Requirements (if visual work is needed)
{{UI_REQUIREMENTS}}

Follow `.github/instructions/ux-ui-glassmorphism.instructions.md` for all visual and interaction decisions.

Include:
- Screen(s) affected
- Layout behavior on mobile and desktop
- Form fields and validation messages
- Empty/loading/error/success states
- Accessibility requirements (labels, keyboard navigation, focus order, contrast)

## Security Requirements (must always be enforced)
Follow `.github/instructions/security.instructions.md` and enforce it across all affected files.

- Apply least privilege and role checks for protected actions.
- Never hardcode secrets, tokens, or credentials.
- Validate and sanitize all user input.
- Prevent XSS by avoiding unsafe HTML rendering.
- Use secure auth flows and token handling best practices.
- Avoid exposing sensitive data in logs, errors, or UI.
- State server-side authorization assumptions explicitly.
- List security risks and mitigations in the final report.

## Testing Requirements
{{TESTING_SCOPE}}

Follow `.github/instructions/testing.instructions.md` when defining and implementing tests.

Must include:
- Unit tests for business logic and validation
- Component/integration tests for key user flows
- Negative tests for invalid and unauthorized scenarios
- If applicable, end-to-end coverage for critical paths
- Commands to run tests and expected results

## Documentation Requirements (after implementation is correct)
Follow `.github/instructions/documentation.instructions.md` when updating docs and TODO notes.

- Update or create documentation for:
	- Feature overview
	- Technical design decisions
	- Configuration and environment requirements
	- Test coverage summary
	- Known limitations
- Update TODO progress:
	- Mark completed items
	- Add follow-up tasks
	- Add newly discovered technical debt

## Output Format
1. Implementation plan
2. Files to change and why
3. Code changes
4. Tests added or updated
5. Security checklist with pass/fail per item
6. Documentation updates performed
7. TODO updates performed
8. Final verification summary (what works, what remains)

## Definition of Done
- Feature behavior matches acceptance criteria.
- Security checklist has no unresolved critical issues.
- Tests pass for new and changed behavior.
- Documentation is updated.
- TODO reflects the latest implementation status.

