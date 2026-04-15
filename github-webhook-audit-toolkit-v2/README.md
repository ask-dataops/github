# GitHub Webhook Audit Toolkit (Org-wide)

Filters repos containing "ABC" anywhere (case-insensitive) and audits webhooks.

## Scripts

### 1. list_never_fired.sh
Lists webhooks that have never received any deliveries.

### 2. disable_inactive_hooks.sh
Disables webhooks with zero deliveries.

### 3. delete_disabled_hooks.sh
Deletes already disabled webhooks.

### 4. report_webhooks.sh
Generates CSV + JSON audit report.

---

## Requirements
- curl
- jq
- bash
- GitHub PAT with:
  - repo
  - admin:repo_hook

---

## Usage

```bash
chmod +x *.sh

./list_never_fired.sh
./disable_inactive_hooks.sh
./delete_disabled_hooks.sh
./report_webhooks.sh
```

---

## Safety Flow
1. Audit
2. Disable
3. Validate
4. Delete

---

⚠️ Be careful with Jira/Jenkins/Harness integrations—they may recreate hooks automatically.
