# QA Testing — PR Review Pipeline (Context Enhancement)

## Purpose

QA test suite for validating the new PR review pipeline's missing dependency
detection feature across 14 distinct test scenarios.

## Structure

- **main_branch/** — Foundation codebase (this folder). Becomes the `main` branch.
- **case1_cross_file_validation/** through **case14_validation_bypass/** — Each
  folder contains only the PR delta files. Each becomes a separate branch PR'd
  into main.

## Main Branch File Map

| File | Key Feature Tested |
|------|--------------------|
| `models/user.py` | Strict Age >= 18 validation in constructor |
| `models/base.py` | Insecure MD5 password hashing (no salt) |
| `models/order.py` | Step 2 business rule validation |
| `utils/logger.py` | `log_error()` with exactly 4 parameters |
| `utils/database.py` | Dict schema definitions for data validation |
| `utils/auth.py` | JWT token generation + password hashing |
| `services/inventory_service.py` | `_reservation_lock` for concurrency safety |
| `services/notification_service.py` | Calls `message_formatter` (circular dep test) |
| `services/message_formatter.py` | Called by `notification_service` |
| `api/checkout.py` | Step 1 input validation |
| `config/settings.py` | `TAX_RATE` and other centralized constants |

## Testing Workflow

1. Push `main_branch/` to GitHub as the `main` branch
2. For each case folder, create a branch from main and add the case files
3. Create PR: `caseN` → `main`
4. Run analysis on both test environment (new pipeline) and prod (old pipeline)
5. Compare results
