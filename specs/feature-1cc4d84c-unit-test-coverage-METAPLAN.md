# Metaplan: Comprehensive Unit Test Coverage for Jerry

## Source
- **Issue**: GitHub #50
- **ADW ID**: 1cc4d84c
- **Spec**: specs/feature-1cc4d84c-unit-test-coverage.md
- **Worktree**: /Users/ameno/dev/tac/tac-8/trees/1cc4d84c

## Phases

| Phase | Group | Description | Depends On | Parallel | Status |
|-------|-------|-------------|------------|----------|--------|
| 1 | A | Testing Infrastructure Setup | - | false | ✅ Complete |
| 2 | B | Core Module Tests | A | true | ⏳ Pending |
| 3 | C | Platform Integration Module Tests | A | true | ⏳ Pending |
| 4 | D | Content Processing Module Tests | A | true | ⏳ Pending |
| 5 | E | ADW Workflow Tests - Core | A | true | ⏳ Pending |
| 6 | F | ADW Workflow Tests - Isolation | A | true | ⏳ Pending |
| 7 | G | ADW Workflow Tests - Composite | E, F | true | ⏳ Pending |
| 8 | H | Trigger and Integration Tests | B, C, D, E, F, G | false | ⏳ Pending |
| 9 | I | Refactoring and Consistency | H | false | ⏳ Pending |
| 10 | J | Documentation and CI/CD | I | false | ⏳ Pending |

## Execution Order

```
Phase 1 (A): Infrastructure ✅ COMPLETE
    ↓
Phases 2-6 (B, C, D, E, F): Can run in parallel
    ↓
Phase 7 (G): Depends on E, F
    ↓
Phase 8 (H): Depends on B, C, D, E, F, G
    ↓
Phase 9 (I): Depends on H
    ↓
Phase 10 (J): Depends on I
```

## Parallel Groups

- **Group 1** (after Phase 1): Phases 2, 3, 4, 5, 6 (B, C, D, E, F)
- **Group 2** (after Group 1): Phase 7 (G)
- **Sequential**: Phases 8, 9, 10 (H, I, J)

---

## Phase 2: Core Module Tests (Group B)

### Steps
- B.1: Test agent.py module
- B.2: Test agent_sdk.py module
- B.3: Test data_types.py module
- B.4: Test validation.py module
- B.5: Test state.py module
- B.6: Test workflow_ops.py module
- B.7: Test git_ops.py module
- B.8: Test worktree_ops.py module

### Build Command
```bash
# For each step, create the test file following patterns from tests/modules/test_utils.py
# B.1: tests/modules/test_agent.py
# B.2: tests/modules/test_agent_sdk.py
# etc.
```

### Test Checklist
- [ ] `uv run pytest tests/modules/test_agent.py -v` passes
- [ ] `uv run pytest tests/modules/test_agent_sdk.py -v` passes
- [ ] `uv run pytest tests/modules/test_data_types.py -v` passes
- [ ] `uv run pytest tests/modules/test_validation.py -v` passes
- [ ] `uv run pytest tests/modules/test_state.py -v` passes
- [ ] `uv run pytest tests/modules/test_workflow_ops.py -v` passes
- [ ] `uv run pytest tests/modules/test_git_ops.py -v` passes
- [ ] `uv run pytest tests/modules/test_worktree_ops.py -v` passes

### Review Criteria
- [ ] Each module has dedicated test file
- [ ] Tests mock external dependencies (subprocess, APIs)
- [ ] Tests cover happy path and error cases
- [ ] Tests are independent and can run in any order

### On Success
```
test: add core module tests (agent, data_types, state, workflow_ops, git_ops, worktree_ops)
```

---

## Phase 3: Platform Integration Module Tests (Group C)

### Steps
- C.1: Test issue_providers.py module
- C.2: Test github.py module
- C.3: Test gitlab.py module
- C.4: Test code_review_providers.py module

### Test Checklist
- [ ] `uv run pytest tests/modules/test_issue_providers.py -v` passes
- [ ] `uv run pytest tests/modules/test_github.py -v` passes
- [ ] `uv run pytest tests/modules/test_gitlab.py -v` passes
- [ ] `uv run pytest tests/modules/test_code_review_providers.py -v` passes

### Review Criteria
- [ ] API calls are mocked (no real GitHub/GitLab calls)
- [ ] Error handling for API failures tested
- [ ] Authentication scenarios covered

### On Success
```
test: add platform integration module tests (issue_providers, github, gitlab, code_review_providers)
```

---

## Phase 4: Content Processing Module Tests (Group D)

### Steps
- D.1: Enhance test_content_extractors.py
- D.2: Test pdf_ops.py module
- D.3: Test youtube_ops.py module
- D.4: Test pattern_executor.py module
- D.5: Test web_ops.py module
- D.6: Test diff_visualizer.py module
- D.7: Test report_generator.py module

### Test Checklist
- [ ] `uv run pytest tests/modules/test_content_extractors.py -v` passes
- [ ] `uv run pytest tests/modules/test_pdf_ops.py -v` passes
- [ ] `uv run pytest tests/modules/test_youtube_ops.py -v` passes
- [ ] `uv run pytest tests/modules/test_pattern_executor.py -v` passes
- [ ] `uv run pytest tests/modules/test_web_ops.py -v` passes
- [ ] `uv run pytest tests/modules/test_diff_visualizer.py -v` passes
- [ ] `uv run pytest tests/modules/test_report_generator.py -v` passes

### Review Criteria
- [ ] External services mocked (yt-dlp, HTTP requests)
- [ ] Sample fixtures created for PDF, video metadata
- [ ] Large input handling tested

### On Success
```
test: add content processing module tests (content_extractors, pdf_ops, youtube_ops, pattern_executor, web_ops)
```

---

## Phase 5: ADW Workflow Tests - Core (Group E)

### Steps
- E.1: Test adw_prompt.py
- E.2: Test adw_sdk_prompt.py
- E.3: Test adw_slash_command.py
- E.4: Test adw_import_workflow.py

### Test Checklist
- [ ] `uv run pytest tests/adws/test_adw_prompt.py -v` passes
- [ ] `uv run pytest tests/adws/test_adw_sdk_prompt.py -v` passes
- [ ] `uv run pytest tests/adws/test_adw_slash_command.py -v` passes
- [ ] `uv run pytest tests/adws/test_adw_import_workflow.py -v` passes

### Review Criteria
- [ ] CLI argument parsing tested
- [ ] Agent execution mocked
- [ ] Output file generation validated

### On Success
```
test: add core ADW workflow tests (adw_prompt, adw_sdk_prompt, adw_slash_command, adw_import_workflow)
```

---

## Phase 6: ADW Workflow Tests - Isolation (Group F)

### Steps
- F.1: Test adw_plan_iso.py
- F.2: Test adw_build_iso.py
- F.3: Test adw_review_iso.py
- F.4: Test adw_ship_iso.py
- F.5: Test adw_review_all_iso.py

### Test Checklist
- [ ] `uv run pytest tests/adws/test_adw_plan_iso.py -v` passes
- [ ] `uv run pytest tests/adws/test_adw_build_iso.py -v` passes
- [ ] `uv run pytest tests/adws/test_adw_review_iso.py -v` passes
- [ ] `uv run pytest tests/adws/test_adw_ship_iso.py -v` passes
- [ ] `uv run pytest tests/adws/test_adw_review_all_iso.py -v` passes

### Review Criteria
- [ ] Worktree operations mocked
- [ ] State transitions validated
- [ ] Cleanup on failure tested

### On Success
```
test: add isolation ADW workflow tests (adw_plan_iso, adw_build_iso, adw_review_iso, adw_ship_iso)
```

---

## Phase 7: ADW Workflow Tests - Composite (Group G)

### Dependencies
- Phase 5 (E) complete
- Phase 6 (F) complete

### Steps
- G.1: Test adw_plan_build_iso.py
- G.2: Test adw_patch_iso.py
- G.3: Test adw_chore_implement.py

### Test Checklist
- [ ] `uv run pytest tests/adws/test_adw_plan_build_iso.py -v` passes
- [ ] `uv run pytest tests/adws/test_adw_patch_iso.py -v` passes
- [ ] `uv run pytest tests/adws/test_adw_chore_implement.py -v` passes

### Review Criteria
- [ ] Workflow composition validated
- [ ] State transitions between phases tested
- [ ] Error propagation tested

### On Success
```
test: add composite ADW workflow tests (adw_plan_build_iso, adw_patch_iso, adw_chore_implement)
```

---

## Phase 8: Trigger and Integration Tests (Group H)

### Dependencies
- Phases 2-7 complete

### Steps
- H.1: Test trigger modules
- H.2: Create integration tests
- H.3: Migrate existing tests

### Test Checklist
- [ ] `uv run pytest tests/triggers/ -v` passes
- [ ] `uv run pytest tests/integration/ -v` passes
- [ ] Existing tests migrated and passing

### Review Criteria
- [ ] Webhook payloads mocked
- [ ] End-to-end flows validated
- [ ] Test isolation verified

### On Success
```
test: add trigger and integration tests
```

---

## Phase 9: Refactoring and Consistency (Group I)

### Dependencies
- Phase 8 complete

### Steps
- I.1: Identify refactoring opportunities
- I.2: Extract common validation logic
- I.3: Standardize error handling
- I.4: Improve module boundaries

### Test Checklist
- [ ] All existing tests still pass after refactoring
- [ ] New validator tests pass
- [ ] Error handling tests pass

### Review Criteria
- [ ] No circular dependencies
- [ ] Consistent error types
- [ ] Clean module interfaces

### On Success
```
refactor: extract common validation and standardize error handling
```

---

## Phase 10: Documentation and CI/CD (Group J)

### Dependencies
- Phase 9 complete

### Steps
- J.1: Document testing approach
- J.2: Setup coverage reporting
- J.3: Create test running scripts
- J.4: Add CI/CD integration

### Test Checklist
- [ ] `docs/TESTING.md` exists and is complete
- [ ] `uv run pytest --cov=adws --cov-fail-under=70` passes
- [ ] `scripts/run_tests.sh` works
- [ ] `.github/workflows/tests.yml` valid

### Review Criteria
- [ ] Documentation complete
- [ ] Coverage thresholds met
- [ ] CI/CD pipeline functional

### On Success
```
docs: add testing documentation and CI/CD pipeline
```

---

## Final Validation

After all phases complete:

```bash
# Run full test suite
uv run pytest tests/ -v

# Check coverage
uv run pytest tests/ --cov=adws/adw_modules --cov=adws --cov-report=term-missing

# Verify test count
find tests -name "test_*.py" | wc -l  # Expected: ≥30

# Run with random order
uv run pytest tests/ --random-order
```

## Execution Status

| Phase | Group | Build | Test | Review | Merged |
|-------|-------|-------|------|--------|--------|
| 1 | A | ✅ | ✅ | ✅ | ✅ |
| 2 | B | 🔄 | 🔄 | ⏳ | ⏳ |
| 3 | C | ⏳ | ⏳ | ⏳ | ⏳ |
| 4 | D | ⏳ | ⏳ | ⏳ | ⏳ |
| 5 | E | ⏳ | ⏳ | ⏳ | ⏳ |
| 6 | F | ⏳ | ⏳ | ⏳ | ⏳ |
| 7 | G | ⏳ | ⏳ | ⏳ | ⏳ |
| 8 | H | ⏳ | ⏳ | ⏳ | ⏳ |
| 9 | I | ⏳ | ⏳ | ⏳ | ⏳ |
| 10 | J | ⏳ | ⏳ | ⏳ | ⏳ |
