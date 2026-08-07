# Security Incident Playbook

## Trigger

Use this playbook for exposed credentials, unauthorized access, malicious dependency behavior, data leakage, unsafe model output, suspicious uploads, or compromised accounts.

## Immediate actions

1. Stop the affected workflow and isolate the component.
2. Revoke or rotate exposed credentials.
3. Preserve logs and evidence without spreading secrets.
4. Notify the event security contact and project owner.
5. Determine whether user or organizer data is affected.

## Recovery

Remove the vulnerable path, restore from a known-good state, reduce privileges, rerun secret and dependency scans, and test the core workflow with replacement credentials.

## Demo decision

If safety cannot be restored, switch to seeded or prerecorded evidence and disclose the limitation. Do not reactivate a risky integration merely to preserve presentation quality.

## Exit criteria

The exposure is contained, credentials are replaced, affected data is understood, the safe demo path is verified, and follow-up ownership is recorded.
