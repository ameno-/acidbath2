# Audit AI Optimization

Check all blog posts for AI optimization compliance and generate a report.

## Usage

```
Audit my blog posts for AI optimization. Check that all posts have the required
fields for llms.txt and structured data.
```

## What This Audits

### Required Frontmatter Fields

| Field | Purpose | Requirement |
|-------|---------|-------------|
| `title` | Post title | Required |
| `description` | SEO/AI summary | Required, <160 chars |
| `tldr` | AI quick answer | Required, 2-3 sentences |
| `keyTakeaways` | Structured insights | Required, 3-5 items |
| `category` | Topic grouping | Required |
| `difficulty` | Reader level | Required |
| `date` | Publication date | Required |

### Optional but Recommended

| Field | Purpose |
|-------|---------|
| `prerequisites` | Reader requirements |
| `relatedPosts` | Internal linking |
| `proficiencyLevel` | Schema.org mapping |
| `dependencies` | Technical requirements |
| `readingTime` | UX element |

### Content Structure

| Check | Description |
|-------|-------------|
| TL;DR section | Has `## TL;DR` heading |
| Heading hierarchy | No skipped levels (H2 → H3) |
| Code languages | All code blocks have language |
| Key Takeaways section | Has `## Key Takeaways` heading |

### Code Organization (POC Rule Compliance)

| Check | Description |
|-------|-------------|
| Inline code size | No inline blocks >30 lines (threshold) |
| Code references | All code refs link to valid acidbath-code paths |
| Complete examples | Long code (>40 lines) extracted to repository |
| Manifest sync | Blog post in manifest.json if has extracted code |
| POC Rule | All code is accessible (inline or linked) |

## Audit Process

1. Scan all files in `src/content/blog/`
2. Parse frontmatter from each post
3. Check required fields
4. Validate content structure
5. **Check code organization compliance**:
   - Count inline code block sizes
   - Verify code reference links are valid
   - Cross-reference with acidbath-code manifest
6. Generate report

## Audit Script

Save as `scripts/audit-ai-optimization.js`:

```javascript
import fs from 'fs/promises';
import path from 'path';
import matter from 'gray-matter';

const BLOG_DIR = 'src/content/blog';

const REQUIRED_FIELDS = [
  'title',
  'description', 
  'tldr',
  'keyTakeaways',
  'category',
  'difficulty',
  'date'
];

const RECOMMENDED_FIELDS = [
  'prerequisites',
  'relatedPosts',
  'proficiencyLevel',
  'dependencies',
  'readingTime'
];

async function auditPosts() {
  console.log('🔍 AI Optimization Audit Report');
  console.log('================================\n');
  
  const files = await fs.readdir(BLOG_DIR);
  const mdxFiles = files.filter(f => f.endsWith('.mdx') || f.endsWith('.md'));
  
  const results = {
    passed: [],
    warnings: [],
    failed: []
  };
  
  for (const file of mdxFiles) {
    const content = await fs.readFile(path.join(BLOG_DIR, file), 'utf-8');
    const { data: frontmatter, content: body } = matter(content);
    
    const issues = [];
    const warnings = [];
    
    // Check required fields
    for (const field of REQUIRED_FIELDS) {
      if (!frontmatter[field]) {
        issues.push(`Missing required field: ${field}`);
      } else if (field === 'description' && frontmatter[field].length > 160) {
        issues.push(`description exceeds 160 chars (${frontmatter[field].length})`);
      } else if (field === 'keyTakeaways') {
        if (!Array.isArray(frontmatter[field])) {
          issues.push('keyTakeaways must be an array');
        } else if (frontmatter[field].length < 3) {
          issues.push(`keyTakeaways has only ${frontmatter[field].length} items (need 3+)`);
        }
      }
    }
    
    // Check recommended fields
    for (const field of RECOMMENDED_FIELDS) {
      if (!frontmatter[field]) {
        warnings.push(`Missing recommended field: ${field}`);
      }
    }
    
    // Check content structure
    if (!body.includes('## TL;DR') && !body.includes('## TLDR')) {
      warnings.push('Missing ## TL;DR section in content');
    }
    
    // Check code blocks have language
    const codeBlocksWithoutLang = (body.match(/```\n/g) || []).length;
    if (codeBlocksWithoutLang > 0) {
      warnings.push(`${codeBlocksWithoutLang} code block(s) without language specified`);
    }
    
    // Check heading hierarchy
    const headings = body.match(/^#{1,6} /gm) || [];
    // Simple check: shouldn't have H4 without H3
    if (body.includes('#### ') && !body.includes('### ')) {
      warnings.push('Heading hierarchy issue: H4 without H3');
    }
    
    // Categorize result
    const slug = file.replace(/\.mdx?$/, '');
    
    if (issues.length === 0 && warnings.length === 0) {
      results.passed.push({ slug, frontmatter });
    } else if (issues.length === 0) {
      results.warnings.push({ slug, warnings, frontmatter });
    } else {
      results.failed.push({ slug, issues, warnings, frontmatter });
    }
  }
  
  // Print report
  console.log(`📊 Summary: ${mdxFiles.length} posts audited\n`);
  
  console.log(`✅ Fully optimized: ${results.passed.length}`);
  results.passed.forEach(p => console.log(`   - ${p.slug}`));
  
  console.log(`\n⚠️  Warnings only: ${results.warnings.length}`);
  results.warnings.forEach(p => {
    console.log(`   - ${p.slug}`);
    p.warnings.forEach(w => console.log(`     ⚠️  ${w}`));
  });
  
  console.log(`\n❌ Missing required fields: ${results.failed.length}`);
  results.failed.forEach(p => {
    console.log(`   - ${p.slug}`);
    p.issues.forEach(i => console.log(`     ❌ ${i}`));
    p.warnings.forEach(w => console.log(`     ⚠️  ${w}`));
  });
  
  // Detailed recommendations
  if (results.failed.length > 0 || results.warnings.length > 0) {
    console.log('\n📝 Recommended Actions:\n');
    
    const allIssues = [...results.failed, ...results.warnings];
    
    // Group by issue type
    const missingTldr = allIssues.filter(p => 
      p.issues?.includes('Missing required field: tldr') ||
      p.warnings?.includes('Missing ## TL;DR section in content')
    );
    
    if (missingTldr.length > 0) {
      console.log('1. Add TL;DR to these posts:');
      missingTldr.forEach(p => console.log(`   - ${p.slug}`));
      console.log('   Template: 2-3 sentences with specific insight and one concrete result.\n');
    }
    
    const missingTakeaways = allIssues.filter(p =>
      p.issues?.some(i => i.includes('keyTakeaways'))
    );
    
    if (missingTakeaways.length > 0) {
      console.log('2. Add keyTakeaways to these posts:');
      missingTakeaways.forEach(p => console.log(`   - ${p.slug}`));
      console.log('   Template: 3-5 specific, actionable insights.\n');
    }
  }
  
  // Return exit code for CI/CD
  return results.failed.length === 0 ? 0 : 1;
}

auditPosts()
  .then(code => process.exit(code))
  .catch(err => {
    console.error('Audit failed:', err);
    process.exit(1);
  });
```

## Example Output

```
🔍 AI Optimization Audit Report
================================

📊 Summary: 3 posts audited

✅ Fully optimized: 1
   - context-engineering

⚠️  Warnings only: 1
   - workflow-prompts
     ⚠️  Missing recommended field: prerequisites
     ⚠️  Missing ## TL;DR section in content

❌ Missing required fields: 1
   - document-generation-skills
     ❌ Missing required field: tldr
     ❌ keyTakeaways has only 2 items (need 3+)
     ⚠️  Missing recommended field: readingTime

📝 Recommended Actions:

1. Add TL;DR to these posts:
   - document-generation-skills
   - workflow-prompts
   Template: 2-3 sentences with specific insight and one concrete result.

2. Add keyTakeaways to these posts:
   - document-generation-skills
   Template: 3-5 specific, actionable insights.
```

## CI/CD Integration

Add to your build process:

```yaml
# .github/workflows/build.yml
jobs:
  build:
    steps:
      - name: Audit AI optimization
        run: node scripts/audit-ai-optimization.js
```

The script returns exit code 1 if any posts fail required field checks, which will fail the build and prevent publishing poorly optimized content.

## Fixing Common Issues

### Missing tldr

Add to frontmatter:
```yaml
tldr: "Progressive disclosure reduces LLM token consumption by 90%. Instead of loading all context upfront, inject information only when the agent needs it for the current decision."
```

### Insufficient keyTakeaways

Add 3-5 specific items:
```yaml
keyTakeaways:
  - "Progressive disclosure reduces context consumption by 90%"
  - "File-based context survives agent restarts and enables debugging"
  - "Semantic search beats keyword matching for codebases over 10K lines"
  - "Inject context at decision points, not upfront"
  - "Measure tokens per successful task completion, not just total tokens"
```

### Missing TL;DR section

Add near the top of your post:
```markdown
## TL;DR

Context engineering is about providing the right information at the right time.
Progressive disclosure—injecting context only when the agent needs it—reduces
token consumption by 90% compared to naive approaches. This post shows you how.
```

### Code blocks without language

Change:
```
```
code here
```
```

To:
```
```python
code here
```
```

## Notes

- Run this audit before every deploy
- Posts with warnings can still be published but won't be optimally indexed by AI
- Posts with failures should be fixed before publishing
- The audit is intentionally strict—AI systems need structured data
