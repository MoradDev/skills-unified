# Attribution

Everything under `curation/` is redistributed from upstream projects, all of them MIT
licensed. Nothing here was written from scratch by this repository's maintainers — the
contribution is the **selection**, the **de-duplication**, the **cross-reference repair**
and the **method** around them.

The MIT licence permits redistribution provided the copyright notice and permission
notice travel with the work. That is the purpose of this file. The full licence text,
identical for all three sources, is reproduced at the end.

## Provenance of the 83 curated skills

### 65 skills from [`affaan-m/ECC`](https://github.com/affaan-m/ECC)

MIT License, Copyright (c) 2026 Affaan Mustafa.

`accessibility`, `android-clean-architecture`, `angular-developer`, `backend-patterns`, `bun-runtime`, `compose-multiplatform-patterns`, `contract-first`, `cpp-coding-standards`, `cpp-testing`, `csharp-testing`, `dart-flutter-patterns`, `database-migrations`, `deployment-patterns`, `design-system`, `django-patterns`, `django-security`, `docker-patterns`, `dotnet-patterns`, `e2e-testing`, `error-handling`, `fastapi-patterns`, `flutter-dart-code-review`, `foundation-models-on-device`, `golang-patterns`, `golang-testing`, `hexagonal-architecture`, `ios-icon-gen`, `java-coding-standards`, `kotlin-coroutines-flows`, `kotlin-patterns`, `kotlin-testing`, `kubernetes-patterns`, `laravel-patterns`, `laravel-security`, `liquid-glass-design`, `make-interfaces-feel-better`, `motion-advanced`, `motion-foundations`, `motion-patterns`, `mysql-patterns`, `nestjs-patterns`, `nextjs-turbopack`, `nuxt4-patterns`, `postgres-patterns`, `prisma-patterns`, `python-patterns`, `python-testing`, `rails-patterns`, `react-native-patterns`, `react-patterns`, `react-performance`, `react-testing`, `redis-patterns`, `rust-patterns`, `rust-testing`, `springboot-patterns`, `springboot-security`, `swift-actor-persistence`, `swift-concurrency-6-2`, `swift-protocol-di-testing`, `swiftui-patterns`, `ui-demo`, `vite-patterns`, `vue-patterns`, `windows-desktop-e2e`.

### 16 skills from [`addyosmani/agent-skills`](https://github.com/addyosmani/agent-skills)

MIT License, Copyright (c) 2025 Addy Osmani.

`api-and-interface-design`, `browser-testing-with-devtools`, `ci-cd-and-automation`, `constraint-driven-development`, `context-engineering`, `deprecation-and-migration`, `documentation-and-adrs`, `doubt-driven-development`, `git-workflow-and-versioning`, `incremental-implementation`, `observability-and-instrumentation`, `performance-optimization`, `security-and-hardening`, `shipping-and-launch`, `source-driven-development`, `using-agent-skills`.

### 2 skills from [`mattpocock/skills`](https://github.com/mattpocock/skills)

MIT License, Copyright (c) 2026 Matt Pocock.

`grill-me`, `grilling`.

## Other content

`curation/rules/` — per-language rulesets, from [`affaan-m/ECC`](https://github.com/affaan-m/ECC),
MIT License, Copyright (c) 2026 Affaan Mustafa.

`curation/references/` — checklists, from [`addyosmani/agent-skills`](https://github.com/addyosmani/agent-skills),
MIT License, Copyright (c) 2025 Addy Osmani.

`curation/skills/react-performance` derives from Vercel Engineering's React Best
Practices, as stated in the skill itself.

## Modifications made

Three cross-reference links were repaired in our copies, because they pointed at skills
deliberately left out of the selection:

| File | Original target | Now |
|---|---|---|
| `react-patterns/SKILL.md` | `../frontend-patterns/SKILL.md` | removed from the "see also" list |
| `react-performance/SKILL.md` | `../frontend-patterns/SKILL.md` | removed from the "see also" list |
| `react-testing/SKILL.md` | `../tdd-workflow/SKILL.md` | points to `test-driven-development` (superpowers) |

No other content was altered. All 18 remaining relative links resolve.

## Referenced but not redistributed

These are cloned by `SETUP.md` from their own repositories. No file of theirs is shipped
here. Listed because the method depends on them and credit is due:

| Project | Author | Licence |
|---|---|---|
| [`obra/superpowers`](https://github.com/obra/superpowers) | Jesse Vincent | MIT |
| [`Leonxlnx/taste-skill`](https://github.com/Leonxlnx/taste-skill) | Leonxlnx | MIT |
| [`DietrichGebert/ponytail`](https://github.com/DietrichGebert/ponytail) | DietrichGebert | MIT |
| [`msitarzewski/agency-agents`](https://github.com/msitarzewski/agency-agents) | AgentLand Contributors | MIT |
| [`github/spec-kit`](https://github.com/github/spec-kit) | GitHub | MIT |
| [`NVIDIA/Skillspector`](https://github.com/NVIDIA/Skillspector) | NVIDIA | Apache-2.0 |
| [`anthropics/skills`](https://github.com/anthropics/skills) | Anthropic | see repository |
| [`Graphify-Labs/graphify`](https://github.com/Graphify-Labs/graphify) | Graphify Labs | see repository |

The complete list, with roles, is in [`catalog/repos.tsv`](catalog/repos.tsv).

## If you are one of these authors

If you would prefer your work not be redistributed here, open an issue and it will be
removed promptly — replaced by a pointer to your repository.

---

## MIT License

Applies to the redistributed content above, under the respective copyright holders:
Copyright (c) 2026 Affaan Mustafa · Copyright (c) 2025 Addy Osmani · Copyright (c) 2026 Matt Pocock

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
