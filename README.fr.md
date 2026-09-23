# Skills Unified

**Un workspace prêt à l'emploi pour agents de code. On le clone, on dit à son agent de
lire `SETUP.md`, et il installe le reste lui-même.**

*[English version](README.md)*

Les skills d'agents sont dispersées dans des dizaines de dépôts, avec des noms qui se
recouvrent, des descriptions qui se concurrencent et une qualité très inégale. Ce dépôt
est le résultat de l'audit de 21 d'entre eux — 2808 fichiers de skills au total — dont on
a gardé les 83 qui méritent leur place, en laissant le raisonnement à découvert.

Il n'est pas lié à Claude Code. N'importe quel agent sachant lire du Markdown peut s'en
servir.

---

## Démarrage

```bash
git clone https://github.com/MoradDev/skills-unified.git workspace
cd workspace
```

Ouvre ensuite ton agent dans ce dossier et donne-lui une seule instruction :

> Lis SETUP.md et installe ce workspace.

C'est tout. L'agent détermine ton système, clone dans `mes_depots/` ce dont la méthode a
besoin, raccorde `curation/` à tes projets par le mécanisme que ton harnais supporte, et
te rend compte de ce qu'il a fait.

Rien n'est installé globalement. Rien n'est activé à ton insu.

---

## Ce que tu obtiens

**83 skills sélectionnées**, en deux familles.

*Méthode* (18) — transformer une idée floue en logiciel qui tourne : interrogatoire
structuré d'une idée avant d'écrire une spec, conception d'API, CI/CD, durcissement
sécurité, performance, observabilité, workflow git, ADR, migration, livraison
incrémentale, ingénierie de contexte, tests navigateur, et développement piloté par les
contraintes, par le doute et par les sources.

*Création d'applications* (65) — le métier proprement dit :

| Cible | Couverture |
|---|---|
| **Web — front** | React (patterns, perf, tests), Vue, Nuxt 4, Next.js/Turbopack, Angular, Vite, design systems, accessibilité WCAG 2.2, motion design |
| **Web — back** | FastAPI, Django, NestJS, Laravel, Spring Boot, Rails, Go, architecture hexagonale, contract-first, gestion d'erreurs — avec des skills sécurité dédiées pour Django, Laravel et Spring Boot |
| **Données** | PostgreSQL, MySQL, Redis, Prisma, migrations |
| **Mobile** | SwiftUI, concurrence Swift 6.2, Liquid Glass, modèles de fondation embarqués, architecture clean Android, Kotlin, Compose Multiplatform, Flutter/Dart, React Native |
| **Desktop** | .NET, Rust, C++, tests E2E Windows natif, Bun |
| **Tests & livraison** | Playwright, tests Python/Go/C#, Docker, Kubernetes, déploiement |

Plus les **rulesets par langage** pour 21 langages et frameworks, et un **catalogue** de
21 dépôts amont avec leur rôle et leur politique d'activation.

---

## Pourquoi une curation plutôt qu'un tas

Ajouter toutes les skills qu'on trouve rend un agent *moins* bon, pas meilleur.
L'auto-invocation se décide sur le champ `description` : deux skills aux descriptions
proches se concurrencent, et l'espace de noms n'y change rien. Chaque skill ajoutée est
aussi du contexte dépensé.

La sélection écarte donc plus qu'elle ne retient :

- **227 des 292 skills d'ECC** — hors sujet pour la plupart des projets (santé,
  logistique, trading, homelab) ou redondantes avec l'existant.
- **832 des 864 d'awesome-claude-skills** — des connecteurs SaaS, conservés comme simple
  annuaire de veille.
- **9 des 25 d'agent-skills** — une collision de nom exacte sur `test-driven-development`,
  plus huit doublons conceptuels.
- **Trois tentantes écartées pour chevauchement de déclencheur** : `frontend-patterns`
  (couverte par `react-patterns` + `react-performance`), `frontend-a11y` (couverte par
  `accessibility`), `browser-qa` (couverte par `browser-testing-with-devtools`).

La sélection est **fermée sous ses propres références croisées** : chaque lien
`../skill/SKILL.md` a été suivi transitivement pour que rien ne pointe dans le vide.
Contrôle final : 18 liens relatifs, 0 cassé. 83 skills, 83 noms distincts, toutes
pourvues d'une `description`.

---

## Sur l'analyse de sécurité des skills

Tout a été scanné avec [NVIDIA SkillSpector](https://github.com/NVIDIA/Skillspector).
**Aucun code malveillant trouvé.** Mais le rapport brut disait l'inverse — 4969 findings,
157 CRITICAL — et cet écart mérite d'être publié, parce que quiconque scanne des skills
va le rencontrer.

71 % des findings portaient sur de la prose Markdown, pas sur du code. Les skills
officielles d'Anthropic (`docx`, `xlsx`, `pptx`, `skill-creator`, `mcp-builder`) sortent
toutes à **100/100 « DO NOT INSTALL »**. Une injection de prompt était détectée dans un
fichier de schéma XML de la norme ECMA Office. Une skill atteint 100/100 parce que les
mots *« Write skill »* apparaissaient dans un tableau markdown et déclenchaient un motif
« Self-Modification ». Une skill de durcissement sécurité est signalée pour SSRF parce
qu'elle contient `169.254.169.254` — l'adresse qu'elle apprend à **bloquer**. Une skill de
test navigateur est signalée pour *« Ignore previous instructions »*, l'attaque qu'elle
apprend à **tester**.

**Lis les rapports de scan avec ce filtre : seuls les findings situés dans des fichiers
exécutables (`.py`, `.sh`, `.js`, `.ts`) veulent dire quelque chose. Ignore ceux qui
portent sur un `.md`.** Et ne câble jamais un tel scan en garde-barrière automatique : il
bloquerait des skills officielles.

Une contre-vérification indépendante a été menée en parallèle : extraction manuelle de
tous les domaines sortants des scripts des nouveaux dépôts (tous légitimes) et recherche
de motifs de dropper (`curl | sh`, `base64 -d | sh`, `eval` sur réponse réseau) — seule
occurrence : l'installeur documenté d'un projet, depuis son propre domaine.

*Réserve, dite franchement :* 1517 skills ont été marquées « incomplete » par le scanner
et 165 fichiers n'ont jamais été inspectés, à cause de son plafond d'1 Mo par fichier. La
couverture n'est pas totale.

---

## Fonctionne avec n'importe quel agent

| Harnais | Comment |
|---|---|
| **Claude Code** | `curation/` embarque un `plugin.json` : il se charge tout seul comme plugin de dossier de skills. Pas de marketplace, pas d'étape d'installation. |
| **Codex** et autres agents qui lisent `AGENTS.md` | `AGENTS.md` est déjà écrit pour toi. |
| **Cursor** | Fais pointer un fichier de règles vers `curation/skills/`. |
| **Gemini CLI, opencode, Aider, Continue…** | Aucun système de plugins nécessaire — indexe les `description` du frontmatter et ouvre un `SKILL.md` quand il correspond à la tâche. |

`AGENTS.md` est neutre vis-à-vis du harnais et contient la méthode de travail.
`CLAUDE.md` n'ajoute que ce qui est propre à Claude Code. `SETUP.md` est la procédure
d'installation, écrite pour être exécutée par un agent plutôt que lue par un humain.

---

## Licence et crédit

MIT. **Aucune des skills n'a été écrite ici** — la contribution, c'est la sélection, la
déduplication, la réparation des références croisées et la méthode qui les entoure.

Elles viennent de [`affaan-m/ECC`](https://github.com/affaan-m/ECC) (65),
[`addyosmani/agent-skills`](https://github.com/addyosmani/agent-skills) (16) et
[`mattpocock/skills`](https://github.com/mattpocock/skills) (2), toutes en MIT.
Provenance complète skill par skill, les trois modifications apportées et les projets
référencés mais non redistribués : [`ATTRIBUTION.md`](ATTRIBUTION.md).

Si tu es l'un de ces auteurs et que tu préfères ne pas être redistribué ici, ouvre une
issue — ce sera retiré et remplacé par un lien vers ton dépôt.
