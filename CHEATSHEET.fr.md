# Aide-mémoire

*[English version](CHEATSHEET.md)*

Toutes les commandes que ce workspace te donne, sur une seule page. Claude Code a droit à
une section courte ; tout ce que le workspace fournit ou installe lui-même est listé en
entier.

**La façon d'appeler une skill dépend de ton agent.** Les skills se déclenchent seules
quand leur `description` correspond à la tâche, donc tu as rarement besoin d'en appeler
une explicitement. Quand c'est le cas :

| Agent | Skill de la curation | Skill d'un plugin |
|---|---|---|
| Claude Code | `/curation:<nom>` | `/<plugin>:<nom>`, par exemple `/superpowers:writing-plans` |
| Tout autre agent | Demande-la par son nom, ou ouvre `curation/skills/<nom>/SKILL.md` | Pareil, dans `mes_depots/<plugin>/skills/` (Codex utilise `@<nom>` quand le plugin le prévoit) |

---

## Sommaire

1. [L'essentiel de Claude Code](#1-lessentiel-de-claude-code)
2. [Installer et entretenir le workspace](#2-installer-et-entretenir-le-workspace)
3. [spec-kit](#3-spec-kit)
4. [Skills de la curation (83)](#4-skills-de-la-curation-83)
5. [superpowers (15)](#5-superpowers-15)
6. [taste-skill (13)](#6-taste-skill-13)
7. [ponytail (6)](#7-ponytail-6)
8. [agency-agents](#8-agency-agents)
9. [Outils optionnels](#9-outils-optionnels)

---

## 1. L'essentiel de Claude Code

Une liste courte, exprès : Claude Code change d'une version à l'autre. Tape `/help` dans
une session pour la liste complète et à jour.

**Lancer une session** (depuis le dossier du projet, sinon ses skills ne se chargent pas)

| Commande | Effet |
|---|---|
| `claude` | Nouvelle session dans le dossier courant |
| `claude -c` | Reprendre la dernière conversation du dossier (`--continue`) |
| `claude -r` | Choisir une ancienne conversation à reprendre (`--resume`) |
| `claude --rc` | Session pilotable depuis l'application mobile Claude (`--remote-control`) |
| `claude -p "question"` | Une réponse unique, sans session interactive |

**Pendant la session**

| Commande | Effet |
|---|---|
| `/help` | Toutes les commandes disponibles |
| `/exit` | Quitter |
| `/clear` | Repartir d'une conversation vide |
| `/compact` | Résumer la conversation pour libérer du contexte |
| `/rewind` | Revenir en arrière, modifications de fichiers comprises |
| `/model` | Changer de modèle et de niveau d'effort |
| `/mcp` | Voir, activer ou désactiver les serveurs MCP |
| `/memory` | Éditer la mémoire et les fichiers `CLAUDE.md` |
| `/remote-control` | Rendre la session accessible depuis l'application mobile |

**Touches** : `Échap` interrompt, `Maj+Tab` change de mode de permissions (dont le mode
plan), `!` lance une commande shell, `@` désigne un fichier.

---

## 2. Installer et entretenir le workspace

La procédure complète est dans [`SETUP.md`](SETUP.md), écrite pour être exécutée par un
agent.

| Tâche | Commande |
|---|---|
| Cloner le workspace | `git clone https://github.com/MoradDev/skills-unified.git mon-workspace` |
| Laisser l'agent l'installer | Dis-lui : *« Lis SETUP.md et installe ce workspace. »* |
| Remplir le cache amont | `git clone --depth 1 <url> mes_depots/<nom>` pour chaque ligne `default` de `catalog/repos.tsv` |
| Mettre à jour un dépôt du cache | `git -C mes_depots/<nom> pull` (ne jamais y modifier de fichier) |
| Relier la curation à un projet (Windows) | `New-Item -ItemType Junction -Path "<projet>\.claude\skills\curation" -Target "<workspace>\curation"` |
| Relier la curation à un projet (macOS / Linux) | `ln -s "<workspace>/curation" "<projet>/.claude/skills/curation"` |
| Indexer les skills sans système de plugins | `find curation/skills -name SKILL.md` |

Remplace `.claude/skills/` par le chemin que lit ton agent. Les jonctions Windows ne
demandent pas de droits administrateur. Relie de la même façon les trois plugins
`default` (superpowers, taste-skill, ponytail).

---

## 3. spec-kit

La colonne vertébrale de la méthode : tout nouveau projet commence ici.

**Installer et créer un projet**

| Commande | Effet |
|---|---|
| `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git` | Installer le CLI `specify` (une fois) |
| `specify init <projet> --integration <agent> --non-interactive` | Créer un nouveau projet |
| `specify init … --ignore-agent-tools` | Sauter la vérification du CLI de l'agent dans le `PATH` (conteneurs, WSL, sandbox) |
| `specify init --help` | Toutes les options, dont la liste des intégrations |

Passe toujours `--integration` : sans lui et sans terminal interactif, `specify` choisit
Copilot sans prévenir.

**Le déroulé, dans l'ordre.** Chaque étape attend que la précédente soit validée.

| Étape | Skill | Ce qu'elle produit |
|---|---|---|
| 0 | `speckit-constitution` | Les principes non négociables du projet. Une fois, en premier. |
| 1 | `grill-me` / `grilling` | Une idée claire, si elle est encore floue (voir §4) |
| 2 | `speckit-specify` | La spec : le quoi et le pourquoi, jamais la stack technique |
| 3 | `speckit-clarify` | Les réponses aux zones floues de la spec |
| 4 | `speckit-plan` | La stack technique et l'architecture |
| 5 | `speckit-tasks` | Une liste de tâches ordonnée et actionnable |
| 6 | `speckit-analyze` | Une vérification croisée spec, plan et tâches (optionnel) |
| 7 | `speckit-implement` | Le code |
| 8 | `speckit-converge` | Les écarts restants entre code et spec, sous forme de nouvelles tâches. Répéter 7 et 8. |

**À tout moment**

| Skill | Effet |
|---|---|
| `speckit-checklist` | Générer une checklist sur mesure pour la fonctionnalité en cours |
| `speckit-taskstoissues` | Transformer `tasks.md` en issues GitHub |

Dans Claude Code, on les appelle `/speckit-constitution`, `/speckit-specify`, etc.

---

## 4. Skills de la curation (83)

Toutes dans `curation/skills/`. Les règles par langage sont dans `curation/rules/`.

### Méthode (18)

| Skill | Sert à |
|---|---|
| `grill-me` | Se faire interroger sur un plan ou une idée jusqu'à ce qu'elle tienne |
| `grilling` | Pareil, sous forme d'arbre de décisions parcouru par tours de questions |
| `using-agent-skills` | Choisir quelle skill s'applique à la tâche en cours |
| `context-engineering` | Mettre en place ou réparer le contexte et les fichiers de règles d'un agent |
| `constraint-driven-development` | Écrire le niveau de qualité exigé et empêcher les agents de le baisser |
| `doubt-driven-development` | Soumettre chaque décision importante à une revue contradictoire |
| `source-driven-development` | Appuyer chaque décision sur la documentation officielle |
| `incremental-implementation` | Livrer un changement en tranches fines et vérifiables |
| `api-and-interface-design` | Concevoir des API, des frontières de modules et des contrats stables |
| `git-workflow-and-versioning` | Committer, brancher, ouvrir des PR, publier des versions |
| `documentation-and-adrs` | Consigner les décisions (ADR) et leur raisonnement |
| `deprecation-and-migration` | Retirer du code, migrer des utilisateurs ou des schémas sans casse |
| `ci-cd-and-automation` | Mettre en place les pipelines de build, de test et de déploiement |
| `security-and-hardening` | Sécuriser les entrées, l'authentification, le stockage et les dépendances |
| `performance-optimization` | Trouver et corriger les problèmes de performance |
| `observability-and-instrumentation` | Ajouter logs, métriques, traces et alertes |
| `browser-testing-with-devtools` | Tester dans un vrai navigateur via le MCP Chrome DevTools |
| `shipping-and-launch` | Préparer une mise en production et son retour arrière |

### Web front-end (15)

| Skill | Pour |
|---|---|
| `react-patterns` | Composants React 18/19, hooks, frontières serveur/client |
| `react-performance` | Performance React et Next.js |
| `react-testing` | React Testing Library, Vitest/Jest, MSW |
| `nextjs-turbopack` | Next.js 16+ et Turbopack |
| `vue-patterns` | Vue 3, Composition API, Pinia |
| `nuxt4-patterns` | Nuxt 4, hydratation, chargement de données côté serveur |
| `angular-developer` | Code et architecture Angular |
| `vite-patterns` | Configuration Vite, plugins, HMR, builds |
| `design-system` | Créer ou auditer un design system |
| `make-interfaces-feel-better` | Peaufiner espacements, typographie, animations et interactions |
| `accessibility` | WCAG 2.2 AA sur le web et en natif |
| `motion-foundations` | Tokens d'animation, ressorts, mouvement réduit (requis par les deux suivantes) |
| `motion-patterns` | Animer boutons, fenêtres, notifications, transitions de page |
| `motion-advanced` | Glisser-déposer, gestes, animations de texte et de SVG |
| `ui-demo` | Enregistrer des vidéos de démo d'une application web avec Playwright |

### Web back-end (16)

| Skill | Pour |
|---|---|
| `backend-patterns` | Node.js, Express et routes API Next.js |
| `nestjs-patterns` | Modules, providers et guards NestJS |
| `fastapi-patterns` | FastAPI, Pydantic v2, handlers asynchrones |
| `django-patterns` | Django, DRF, ORM |
| `django-security` | Authentification Django, CSRF, XSS, réglages de déploiement |
| `laravel-patterns` | Laravel, Eloquent, files d'attente |
| `laravel-security` | Authentification Laravel, sûreté d'Eloquent, sécurité des API |
| `springboot-patterns` | REST, services et accès aux données avec Spring Boot |
| `springboot-security` | Spring Security, authentification et durcissement |
| `java-coding-standards` | Java dans des services Spring Boot ou Quarkus |
| `rails-patterns` | Rails 7.1+ et 8.x |
| `golang-patterns` | Go idiomatique |
| `python-patterns` | Python idiomatique, typage, PEP 8 |
| `hexagonal-architecture` | Ports et adaptateurs, frontières du domaine |
| `contract-first` | Schémas d'API ou d'événements partagés par plusieurs consommateurs |
| `error-handling` | Erreurs typées, relances, disjoncteurs (TS, Python, Go) |

### Données (5)

| Skill | Pour |
|---|---|
| `postgres-patterns` | Schémas, index, RLS et requêtes lentes PostgreSQL |
| `mysql-patterns` | MySQL et MariaDB |
| `redis-patterns` | Cache, verrous, limitation de débit, pub/sub |
| `prisma-patterns` | Schémas et requêtes Prisma, et ses pièges connus |
| `database-migrations` | Migrations de schéma et de données, sans interruption de service |

### Mobile (15)

| Skill | Pour |
|---|---|
| `react-native-patterns` | Applications React Native et Expo |
| `swiftui-patterns` | Vues SwiftUI, `@Observable`, navigation |
| `swift-concurrency-6-2` | Concurrence en Swift 6.2 |
| `swift-actor-persistence` | Persistance sûre en multithread avec des actors |
| `swift-protocol-di-testing` | Swift testable par injection via des protocoles |
| `liquid-glass-design` | Interfaces Liquid Glass d'iOS 26 |
| `foundation-models-on-device` | LLM embarqué d'Apple (iOS 26+) |
| `ios-icon-gen` | Icônes d'application iOS depuis SF Symbols ou Iconify |
| `android-clean-architecture` | Structure de modules Android et KMP |
| `kotlin-patterns` | Kotlin idiomatique |
| `kotlin-coroutines-flows` | Coroutines et Flow sur Android et KMP |
| `kotlin-testing` | Kotest, MockK, couverture |
| `compose-multiplatform-patterns` | Interfaces Jetpack Compose et Compose Multiplatform |
| `dart-flutter-patterns` | Applications Dart et Flutter |
| `flutter-dart-code-review` | Revue de code Flutter et Dart |

### Desktop et systèmes (7)

| Skill | Pour |
|---|---|
| `dotnet-patterns` | C# et .NET |
| `rust-patterns` | Rust idiomatique |
| `rust-testing` | Tests en Rust |
| `cpp-coding-standards` | C++ moderne (Core Guidelines) |
| `cpp-testing` | GoogleTest, CTest, sanitizers |
| `windows-desktop-e2e` | Tests de bout en bout d'applications Windows natives |
| `bun-runtime` | Bun comme runtime, bundler et lanceur de tests |

### Tests et livraison (7)

| Skill | Pour |
|---|---|
| `e2e-testing` | Tests E2E Playwright et tests instables en CI |
| `python-testing` | pytest |
| `golang-testing` | Tests, benchmarks et fuzzing en Go |
| `csharp-testing` | xUnit et tests .NET |
| `docker-patterns` | Dockerfiles et Compose |
| `kubernetes-patterns` | Manifestes Kubernetes et débogage |
| `deployment-patterns` | CI/CD, conteneurs, health checks, retours arrière |

---

## 5. superpowers (15)

Les méthodes de travail. Dans Claude Code : `/superpowers:<skill>`.

| Skill | Quand l'utiliser |
|---|---|
| `using-superpowers` | Au début d'une session : comment trouver et utiliser les skills |
| `brainstorming` | Avant tout travail créatif, pour explorer l'intention et la conception |
| `writing-plans` | Tu as les exigences d'une tâche en plusieurs étapes |
| `executing-plans` | Tu exécutes un plan toi-même, dans cette session |
| `subagent-driven-development` | Tu exécutes un plan aux tâches indépendantes via des sous-agents |
| `dispatching-parallel-agents` | Deux tâches indépendantes ou plus peuvent tourner en parallèle |
| `test-driven-development` | Pour toute fonctionnalité ou correction, les tests d'abord |
| `systematic-debugging` | Face à un bug, un test qui échoue ou un comportement inattendu |
| `verification-before-completion` | Juste avant d'affirmer que c'est fini, corrigé ou que ça passe |
| `requesting-code-review` | En fin de tâche ou avant de fusionner |
| `receiving-code-review` | Pour traiter les retours d'une revue |
| `using-git-worktrees` | Un travail qui a besoin d'un espace isolé |
| `finishing-a-development-branch` | Pour décider comment intégrer un travail terminé |
| `writing-skills` | Pour créer ou modifier une skill |
| `diagnosing-superpowers` | Pour comprendre pourquoi une session a mal tourné |

---

## 6. taste-skill (13)

Le design visuel. Dans Claude Code, la commande utilise le nom du **dossier** :
`/taste-skill:<dossier>`.

| Dossier | Nom de la skill | Pour |
|---|---|---|
| `taste-skill` | `design-taste-frontend` | Landing pages, portfolios, refontes : le choix par défaut |
| `taste-skill-v1` | `design-taste-frontend-v1` | La v1 d'origine, pour les projets qui en dépendent |
| `redesign-skill` | `redesign-existing-projects` | Améliorer un site ou une application existants |
| `soft-skill` | `high-end-visual-design` | Finition de niveau agence : polices, espacements, ombres |
| `minimalist-skill` | `minimalist-ui` | Interfaces éditoriales épurées |
| `brutalist-skill` | `industrial-brutalist-ui` | Interfaces brutes, style suisse et terminal |
| `gpt-tasteskill` | `gpt-taste` | Mises en page éditoriales animées avec GSAP |
| `stitch-skill` | `stitch-design-taste` | Fichiers `DESIGN.md` pour Google Stitch |
| `image-to-code-skill` | `image-to-code` | Générer une image de design, puis la coder |
| `imagegen-frontend-web` | `imagegen-frontend-web` | Références de design web sous forme d'images |
| `imagegen-frontend-mobile` | `imagegen-frontend-mobile` | Concepts d'écrans mobiles sous forme d'images |
| `brandkit` | `brandkit` | Planches de charte graphique et systèmes de logo |
| `output-skill` | `full-output-enforcement` | Forcer une sortie complète, sans code laissé en suspens |

---

## 7. ponytail (6)

Pousse l'agent vers la solution la plus simple qui marche. Actif dès le début de session.

| Commande | Effet |
|---|---|
| `/ponytail` | Mode full, par défaut : YAGNI, bibliothèque standard, natif, puis code minimal |
| `/ponytail lite` | Construit ce qui est demandé, et cite en une ligne l'alternative plus simple |
| `/ponytail ultra` | Supprimer avant d'ajouter ; remet en question la demande d'abord |
| `/ponytail off`, ou dis *« stop ponytail »* | Le désactiver pour la session |
| `/ponytail-review` | Revue du changement en cours, uniquement sur la sur-ingénierie |
| `/ponytail-audit` | Pareil, sur tout le dépôt |
| `/ponytail-debt` | Rassembler tous les commentaires `ponytail:` en un registre |
| `/ponytail-gain` | Tableau des gains mesurés |
| `/ponytail-help` | Fiche de référence |

Claude Code peut afficher les skills avec leur espace de noms (`/ponytail:ponytail-review`).
Codex utilise `@ponytail`, `@ponytail-review` et `@ponytail-help`.

**Mode par défaut** : définis `PONYTAIL_DEFAULT_MODE=lite|full|ultra|off`, ou
`{ "defaultMode": "lite" }` dans `~/.config/ponytail/config.json`
(Windows : `%APPDATA%\ponytail\config.json`).

---

## 8. agency-agents

Des personas spécialisées : ingénierie, design, marketing, sécurité, tests, produit,
jeu vidéo, SIG et d'autres (environ 300, dans `mes_depots/agency-agents/<division>/`).

| Tâche | Commande |
|---|---|
| Les ajouter à un projet Claude Code | Copier les fichiers `.md` dans `<projet>/.claude/agents/` (copier, pas relier) |
| Les installer pour un autre outil | `./scripts/install.sh --tool <outil>` depuis `mes_depots/agency-agents/` |
| En utiliser une | Demande la spécialité par son nom : *« Utilise l'agent Backend Architect pour… »* |

---

## 9. Outils optionnels

Proposés par `SETUP.md`, jamais installés sans qu'on le demande.

| Outil | Commande | Quand |
|---|---|---|
| graphify | `uv tool install graphifyy`, puis `graphify install` | Quand un projet dépasse environ 80 fichiers |
| graphify | `/graphify .` | Construire le graphe du code, puis lire `graph.html` / `GRAPH_REPORT.md` |
| Skillspector | `uv tool install git+https://github.com/NVIDIA/skillspector.git` | Avant de faire confiance à une skill de source inconnue |
| Skillspector | `skillspector scan <dossier-de-la-skill> --no-llm` | L'analyser. Seuls comptent les résultats sur des fichiers `.py`, `.sh`, `.js`, `.ts`, `.ps1`. |

---

*Les listes des plugins reflètent les dépôts amont au 25/09/2026 : superpowers `5bf4e78`,
taste-skill `c184364`, ponytail `e3ba2aa`, agency-agents `053ddbb`. Elles ont pu évoluer
depuis ; les skills de la curation (§4) ne changent qu'avec ce dépôt.*
