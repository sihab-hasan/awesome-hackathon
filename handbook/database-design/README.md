# Database Design

Start with the user journey and identify the minimum persistent entities.

- Give each table or collection a clear owner.
- Use stable IDs, timestamps, and explicit relationships.
- Add uniqueness and foreign-key constraints where supported.
- Store secrets outside the database unless encrypted and required.
- Create deterministic seed data for the demo.
- Document destructive reset and migration commands.

Prefer one primary database during the event.
