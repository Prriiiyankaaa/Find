# TestSprite Tests

This folder stores the committed TestSprite smoke-test plan used by the
`TestSprite PR Tests` GitHub Actions workflow.

The workflow runs against the light Docker Compose stack in mock ML mode, so it
can validate core upload, gallery, search, and clustering surfaces without
requiring GPU model downloads.

Keep this suite small and high-signal. Broader exploratory tests should be run
manually from the TestSprite dashboard or through `workflow_dispatch`.
