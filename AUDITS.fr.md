# Journal des audits

*Version française uniquement — c'est un registre, pas de la documentation d'usage. Les
décisions qu'il justifie sont dans [`README.fr.md`](README.fr.md) et
[`AGENTS.md`](AGENTS.md).*

Ce fichier garde la trace datée de chaque audit du catalogue : ce qui a été ajouté, ce qui a
été écarté et pourquoi, ce que les scans de sécurité ont réellement montré, et les chiffres
mesurés à chaque fois. Il est en **ajout seul** : on ajoute une entrée, on ne réécrit pas une
ancienne. C'est ce qui permet de recontrôler une affirmation plus tard au lieu de la croire.

Les entrées sont dans l'ordre chronologique.

---

## 2026-09-12 — Audit

aucune collision de nom entre `taste-skill`/`ponytail`/`OmniRoute` et le reste du catalogue. Le seul doublon trouvé est interne à ces trois dépôts (la copie vendée de `ponytail` dans `OmniRoute/skills/ponytail/`) et sans conséquence car `OmniRoute` n'est jamais activé comme plugin de skills. Point de vigilance non bloquant : la philosophie "toujours active" de `ponytail` (solution la plus simple, YAGNI) peut entrer en tension avec le travail structuré spec-kit/superpowers (specs détaillées, architecture, TDD) — à surveiller à l'usage, pas à corriger a priori.

## 2026-09-12 — Sauvegarde

avant de retailler les descriptions des 280 personas copiées dans `white-mirror/.claude/agents/` (frontmatter `description:` ramenée à ~100-140 caractères, une phrase, pour alléger le contexte consommé par la liste d'agents à chaque session), une copie intégrale du dossier a été faite dans `Workspace/stock_agents/` — c'est la version originale (descriptions longues) telle que copiée depuis `mes_depots/agency-agents`. `Workspace/` n'étant pas un dépôt git, cette copie sert de filet de sécurité ; elle n'est pas maintenue à jour et peut être supprimée une fois la réécriture validée.

> *Note du 2026-10-02 :* `Workspace/` est devenu un dépôt git entre-temps, puis a été
> dissous (voir la dernière entrée). `stock_agents/` n'est plus dans l'arbre de travail ; sa
> copie se trouve dans la sauvegarde datée sur le bureau et dans l'historique du dépôt privé
> `claude-code-setup`, archivé. L'entrée ci-dessus est conservée telle qu'écrite.

## 2026-09-14 — Audit

(ajout de `agent-skills` et `code-on-incus`) :
- **`agent-skills` — 1 collision exacte et 8 doublons conceptuels sur 25 skills.** `test-driven-development` porte le même nom que celui de `superpowers` (versions différentes : 16,5 Ko contre 9 Ko). Huit autres recouvrent le stack par défaut : `spec-driven-development` (↔ spec-kit), `interview-me` et `idea-refine` (↔ grill-me/grilling), `code-simplification` (↔ ponytail), `frontend-ui-engineering` (↔ taste-skill), `debugging-and-error-recovery`, `code-review-and-quality`, `planning-and-task-breakdown` (↔ superpowers). **Ces 9 skills sont volontairement écartées.**
- **Les 16 skills restantes ont été versées dans `curation/`** (voir § « Ce que contient curation/ ») : api-and-interface-design, browser-testing-with-devtools, ci-cd-and-automation, constraint-driven-development, context-engineering, deprecation-and-migration, documentation-and-adrs, doubt-driven-development, git-workflow-and-versioning, incremental-implementation, observability-and-instrumentation, performance-optimization, security-and-hardening, shipping-and-launch, source-driven-development, using-agent-skills. Sept d'entre elles pointent vers `../../references/`, d’où la copie du dossier `references/` à la racine de `curation/` : la profondeur relative étant identique, tous les liens résolvent. Aucune collision de nom avec les 16 skills déjà présentes.
- **`code-on-incus` : documenté, non installé.** Linux uniquement, et architecturalement il enveloppe Claude Code de l'extérieur (`coi shell` puis lancement de l'agent dedans) — ce n'est pas un mécanisme invocable au moment de déléguer à un sous-agent, ceux-ci s'exécutant dans la session de l'agent principal.
- **Réorganisation du 2026-09-14 (suite)** : ces 16 skills, ainsi que `grill-me`/`grilling`, ont d’abord été copiées dans `mes_depots/superpowers`, puis sorties dans `curation/` lors de la mise sous git du Workspace. `superpowers` est redevenu vierge (0 modification locale), et la dette de maintenance liée à ces copies a disparu : `curation/` est versionné.

## 2026-09-23 — Audit

(ajout de 7 dépôts et scan de sécurité intégral) :
- **Scan Skillspector sur la totalité du catalogue** : 2790 `SKILL.md` dans `mes_depots/` plus 18 dans `curation/`. **Aucun code malveillant trouvé.** Le rapport brut annonce pourtant 4969 findings dont 157 CRITICAL — il est inexploitable tel quel.
- **Comment lire un rapport Skillspector.** 71 % des findings portent sur des fichiers markdown, pas sur du code. Les skills **officielles Anthropic** (`docx`, `xlsx`, `pptx`, `skill-creator`, `mcp-builder`, `claude-api`) sortent toutes à 100/100 « DO NOT INSTALL » ; une injection de prompt est détectée dans `opc-contentTypes.xsd`, un schéma de la norme ECMA Office. `superpowers/writing-skills` atteint 100/100 parce que les mots « Write skill » dans un tableau markdown déclenchent le motif « Self-Modification ». Notre `security-and-hardening` sort à 76/100 pour SSRF parce qu'il contient `169.254.169.254` — l'adresse qu'il apprend à **bloquer** ; `browser-testing-with-devtools` à 65/100 pour « Ignore previous instructions », l'attaque qu'il apprend à **tester**. `graphify` à 100/100 parce que ses regex `id_rsa`/`.netrc` sont les signatures de son détecteur de secrets. **Règle : ne lire que les findings situés dans des fichiers exécutables (`.py`, `.sh`, `.js`, `.ts`…), ignorer ceux des `.md`.**
- **Contre-vérification indépendante du scanner** : extraction manuelle de tous les domaines sortants des scripts des nouveaux dépôts (uniquement `schemas.openxmlformats.org`, `example.com`, `fal.ai`, `github.com`, `w3.org`) et recherche de motifs de dropper (`curl | sh`, `base64 -d | sh`, `eval` sur réponse réseau) : une seule occurrence, l'installeur documenté de VoiceStudio depuis son propre domaine. Rien de suspect.
- **Réserve de couverture** : 1517 skills marquées « incomplete », 459 fichiers partiellement inspectés et 165 jamais inspectés (plafond de 1 Mo par fichier). La couverture n'est pas totale.
- **Skillspector n'est pas câblé comme garde-barrière automatique** au démarrage d'un projet : avec ce taux de faux positifs il bloquerait des skills officielles Anthropic. Usage ponctuel et manuel uniquement.
- **65 skills d'ECC versées dans `curation/`** (voir § « Création d'applications »). Sélection fermée sous ses références croisées ; les 18 liens relatifs résolvent tous. Trois liens pointant vers des skills écartées ont été réparés dans nos copies (`react-patterns` et `react-performance` renvoyaient à `frontend-patterns`, `react-testing` à `tdd-workflow` — désormais redirigé vers `test-driven-development` du plugin superpowers).
- **Skills écartées pour chevauchement de déclencheur** : `frontend-patterns` (↔ `react-patterns` + `react-performance`), `frontend-a11y` (↔ `accessibility`), `browser-qa` (↔ `browser-testing-with-devtools` déjà présent), plus `api-design`, `architecture-decision-records`, `git-workflow`, `tdd-workflow`, `security-review`, `security-scan`, `taste*` et `frontend-design-direction`, tous en doublon conceptuel avec le stack existant.
- **Aucune collision de nom** entre les 65 nouvelles skills et les 18 existantes, `superpowers`, `taste-skill` ou `ponytail`. Vérifié aussi au niveau du `name:` de frontmatter : 83 skills, 83 noms distincts, toutes pourvues d'une `description:`.
- **`mes_depots/` change de rôle** : ce n'est plus seulement la matière première de la curation, c'est aussi le stock d'outils pour les applications à construire. VoiceStudio, voicebox et SCAIL-2 y sont conservés à ce titre, sans aucun `SKILL.md` exploitable.
- **Volume** : `mes_depots/` passe à ~1,7 Go pour 21 dépôts. `curation/` passe de 29 à 253 fichiers.

## 2026-10-02 — Audit

(épinglage des dépôts amont, Jev remplacé par Laya) :
- **Chaque dépôt amont est désormais épinglé.** `skills-unified/catalog/repos.tsv` gagne deux colonnes, `commit` et `scanned`. Les 22 lignes portent un SHA 40-hex vérifié et la date `2026-10-02`. Le problème qu'on corrige : `SETUP.md` clonait la pointe de branche alors que le scan de sécurité portait sur un état passé — ce qu'un utilisateur installait n'était donc pas ce qui avait été vérifié. Procédure de clonage épinglé testée sur `taste-skill` et `ponytail`, les deux atterrissent exactement sur le SHA attendu.
- **Rescan complet aux commits épinglés.** La méthode manuelle (extraction des domaines sortants, motifs `curl | sh`, `base64 -d | sh`, `eval` sur réponse réseau, `Invoke-Expression` sur requête web, `pickle.loads` sur réponse réseau) a tourné sur les 22 dépôts ; Skillspector v2.11.2 sur les 12 qui apportent du contenu dans un projet. **Aucun code malveillant.** Chaque occurrence relève d'un de ces quatre cas : fixture de test d'un détecteur, installeur documenté d'un projet depuis son propre domaine, installeur amont officiel cité dans un script de build, ou faux positif de regex (`ECC/scripts/build-pi-core.js` matche sur ses *propres* chaînes de liste noire `"curl|sh"` ; `VoiceStudio/electron/src/main/updater.ts:70` matche `exec(await response.text())`, qui est `RegExp.prototype.exec` sur un flux YAML de version).
- **La grille de lecture de 2026-09-23 tient sans exception.** 11 des 12 dépôts scannés sortent à 100/100 « DO NOT INSTALL », dont `claude-code-security-review` — l'outil de sécurité d'Anthropic, signalé CRITICAL pour les appels `requests.get` à l'API GitHub qui sont sa raison d'être — et `taste-skill`, qui compte 5 fichiers exécutables et **zéro** finding dedans. Les dix findings exécutables d'`anthropics-skills` sont tous dans des skills officielles : `os.environ.copy()` dans le `soffice.py` de `docx`/`pptx`/`xlsx` lu comme « Data Exfiltration », la chaîne littérale `~/.ssh/id_rsa` dans un échafaudage d'évals `claude-api` comme « Privilege Escalation ». Le seul score sous 100 du lot est `andrej-karpathy-skills` à 33 « CAUTION », et uniquement parce qu'il ne contient aucun fichier exécutable.
- **Un seul fichier exécutable dans tout `curation/`.** `curation/` ne contient **qu'un seul** fichier exécutable sur ses 254 fichiers : `skills/ios-icon-gen/scripts/iconify_gen.sh`, relu ligne à ligne — `set -euo pipefail`, un seul domaine sortant (`api.iconify.design`), les SVG téléchargés vers des fichiers avec `curl --fail -o` et jamais tubés vers un shell, aucun `eval` ni `base64 -d`. Tout le reste est du Markdown. ⚠️ Un premier comptage avait annoncé zéro : il reposait sur un `find curation -type f` lancé depuis `skills-unified/`, où `curation` est une **jonction** que `find` ne traverse pas sans `-L`. Le vrai chiffre est 1, obtenu en parcourant le dossier réel. Et zéro finding HIGH ou CRITICAL dans un fichier exécutable à l'intérieur des 65 skills d'ECC, 16 d'`agent-skills` ou 2 de `mattpocock` qu'on redistribue — vérifié en croisant les chemins des findings avec la liste d'`ATTRIBUTION.md`.
- **`jev-mcp` retiré, remplacé par `laya`.** Il était payant à l'appel. Laya (Apache 2.0, confirmée depuis son `LICENSE` et depuis PyPI) répond à la même forme de question et tourne en local, sans clé API. Son serveur MCP vient de **son propre dépôt** — aucun wrapper tiers. Scanné propre au commit `4aa6761`. `structured-decisions` est devenue neutre vis-à-vis des fournisseurs.
- **Chiffres recomptés sur les fichiers réels**, plusieurs avaient dérivé : 83 → **84 skills** (`structured-decisions` était dans l'arbre mais dans aucun cheatsheet), 65 → **66** pour la famille applicative, 21 → **22** rulesets, 21 → **22** lignes au catalogue, 227/292 → **228/293** pour ECC qui a gagné une skill depuis. Le chiffre de « 2808 fichiers de skills » n'a pu être reproduit à aucun commit épinglé : le vrai total sur les 22 clones est **2920**, et il est désormais énoncé contre l'épinglage pour être recontrôlable.
- **Veille automatisée.** `skills-unified/.github/workflows/upstream-watch.yml`, mensuelle et déclenchable à la main, compare chaque épinglage à la pointe de sa branche et tient une issue unique avec les liens de comparaison. Permissions minimales (`contents: read`, `issues: write`), aucun clonage (`git ls-remote <url> HEAD`, ce qui gère les branches par défaut qui ne s'appellent pas `main` : `SCAIL-2` est sur `wan-scail2`, `OmniRoute` sur `release/v3.8.52`, `graphify` sur `v8`). Elle signale, elle ne change rien.
- **Recoupements d'auto-invocation relevés, volontairement non résolus** (les résoudre voudrait dire modifier un dépôt de `mes_depots/`, ce que la méthode interdit) : `superpowers:test-driven-development` face aux skills de test par langage, `superpowers:using-superpowers` face à `using-agent-skills` (quasi-doublon), `superpowers:brainstorming` — dont la description commence par « You MUST use this before any creative work » — face à `grill-me` et à l'étape `specify` de spec-kit, et `taste-skill:high-end-visual-design` face à `make-interfaces-feel-better`. Liste complète dans la PR #1 du miroir public.
- **Cache local réaligné le même jour.** Les 21 clones de `mes_depots/` ont été amenés au commit épinglé par `git fetch --depth 1 origin <sha>` puis `git checkout --force FETCH_HEAD`, dans le dossier existant plutôt que par suppression/reclonage. Avant : 6 dépôts sur 21 au bon SHA. Après : 21 sur 21, vérifiés par `rev-parse HEAD`. Vingt des 21 sont vierges de toute modification locale ; `Anthropic-Cybersecurity-Skills` a un `SKILL.md` supprimé dans son arbre de travail, laissé en place faute de savoir si c'était volontaire. Recomptages consécutifs : `superpowers` passe de 14 à 15 skills, `agency-agents` de 294 à 297 personas, `ECC/skills` de 292 à 293.
- **Personas : un noyau de 14 par défaut, le reste par division (PR #2).** `agency-agents` était en activation `default` : le dépôt public faisait cloner ses 7,5 Mo puis disait de les lier comme un plugin de skills — or il n'a ni `plugin.json` ni dossier `skills/`, donc le lien ne pouvait rien produire, et la vraie procédure de copie n'existait que dans ce `CLAUDE.md` privé. Passé en activation `core-set`, avec une étape 4b dans `SETUP.md`. Un noyau de 14 est copié d'office — architecture, backend, frontend, revue, base de données, devops, prototypage, UI, UX, tests, accessibilité, appsec, rédaction technique — pour ~600 tokens par session mesurés, et le reste se demande par division. Les 297 coûteraient ~15 800 tokens à chaque session pour trois ou quatre utilisées. Dans le même mouvement : le seuil des 80 fichiers de graphify devient actionnable (une commande de comptage à lancer avant tout changement structurel, au lieu d'une ligne que personne ne relit), et l'offre de Laya devient obligatoire et chiffrée (torch ~1 Go, checkpoint 322–421 M paramètres au premier appel) plutôt que silencieusement passable.
- **Chiffres désormais vérifiés par un script (PR #2).** `skills-unified/scripts/check.py` (bibliothèque standard, ~1 s, en CI sur chaque push) recompte les skills, les familles, chaque catégorie des deux cheatsheets, le frontmatter de chaque skill, les rulesets, l'arité et le format de `repos.tsv`, tous les liens relatifs et ancres, l'accord anglais/français, et la liste nominative des fichiers exécutables livrés. C'est ce qui manquait : les chiffres avaient dérivé parce que rien ne les recomptait. Prouvé en cassant le dépôt sept fois exprès.
- **Détail complet** : https://github.com/MoradDev/skills-unified/pull/1 et https://github.com/MoradDev/skills-unified/pull/2

## 2026-10-02 — Consolidation : un seul dépôt

Le workspace et ce dépôt faisaient la même chose, et ça coûtait à chaque modification.

**Le constat.** Les 254 fichiers de `curation/` étaient versionnés dans **deux** dépôts git :
`claude-code-setup` (privé) et `skills-unified` (public), avec la même liste et la même
empreinte. `Workspace/curation` était le vrai dossier, `skills-unified/curation` une jonction
pointant dedans. Toute modification demandait deux commits — constaté le jour même sur
`structured-decisions`. La documentation doublait aussi : 350 lignes de `Workspace/README.md`
recouvraient `README.fr.md` + `CHEATSHEET.fr.md` + `AGENTS.md`, et la même modification a dû
être écrite deux à quatre fois pendant toute la session (Laya, épinglage, personas, noyau
de 14). La règle « mets à jour les deux ensemble » n'était pas une discipline mais une taxe.

**L'argument décisif :** `SETUP.md` dit déjà que « la racine du dépôt **est** la racine du
workspace ». `Workspace/` était une coquille extérieure qui réimplémentait ce dépôt.

**Ce qui a été fait**, dans cet ordre, avec vérification entre chaque étape :

1. Sauvegarde datée de `curation/` et `stock_agents/` sur le bureau, contrôlée par empreinte
   SHA-256 normalisée (fins de ligne ignorées) : identique au bit près.
2. `skills-unified/` déplacé à la racine du bureau.
3. `curation/` est devenu un **vrai dossier** au lieu d'une jonction. Fait en renommant
   d'abord le lien, en copiant le contenu réel, en vérifiant l'empreinte, puis en supprimant le
   lien avec `rmdir` **sans `/s`** — `Remove-Item -Recurse` sur une jonction Windows efface sa
   cible, c'est le piège classique. Cible vérifiée intacte avant et après.
4. `mes_depots/` (21 clones) et le projet `prompt-eng-interactive-tutorial` déplacés dans la
   nouvelle racine. Les 21 clones sont toujours à leur SHA épinglé, vérifié.
5. `scripts/check.py` cherche désormais `mes_depots/` dans la racine du dépôt **ou** à côté,
   pour que les deux dispositions fonctionnent. 30 contrôles, 0 échec.
6. Historique d'audit sorti de `Workspace/README.md` vers ce fichier, et procédure propre à la
   machine vers `~/.claude/CLAUDE.md`.
7. `claude-code-setup` **archivé**, pas supprimé : c'était la seule copie de `stock_agents`.
   Archiver est réversible.

**Ce qui disparaît avec la fusion**, et c'est le gain : la double écriture de `curation/`, la
règle de synchronisation des deux documentations, et la section « miroir public » — il n'y a
plus de miroir, il n'y a qu'un dépôt.

## 2026-10-03 — Vérification d'intégrité et de cohérence

**Intégrité, sans écart dans le dépôt.** `git fsck --full` propre ; `main` local et distant
identiques (`5534e6e`) ; `check.py` 30/30 ; CI verte sur les cinq derniers passages.

**Cache `mes_depots/`, comparé ligne à ligne à `catalog/repos.tsv`** (`HEAD`, URL d'origine,
`git status --porcelain` pour chaque clone) : 20 des 22 à leur SHA épinglé, propres.
Deux écarts, laissés tels quels :
- `Anthropic-Cybersecurity-Skills` : un fichier absent de l'arbre de travail,
  `skills/detecting-fileless-malware-techniques/SKILL.md`. `Get-MpThreatDetection` montre que
  Defender a mis ce même fichier en quarantaine le 02/10 dans un autre clone : c'est
  l'antivirus, pas une modification. Un `git checkout` serait de nouveau effacé ; la décision
  d'une exclusion revient à l'humain.
- `laya` non cloné. Activation `opt-in`, cache reconstructible : pas une erreur.

**Cohérence, deux contradictions que `check.py` ne pouvait pas voir**, parce que chaque
nombre était juste et que seule leur somme était fausse :
1. Les deux README créditaient 65 + 16 + 2 = 83 skills et affirmaient qu'aucune n'avait été
   écrite ici, alors que le disque en compte 84 et qu'`ATTRIBUTION.md` déclare
   `structured-decisions` originale. Corrigé dans les deux README. **Nouveau contrôle**
   `check_provenance` : chaque skill du disque attribuée une seule fois dans
   `ATTRIBUTION.md`, chaque titre de section égal au nombre de noms listés, et les deux README
   créditant les mêmes nombres et nommant chaque skill originale. Vérifié en remettant les
   anciens README : 2 échecs, comme attendu. 38 contrôles, 0 échec.
2. L'enchaînement spec-kit s'arrêtait à `implement` dans les README et dans `AGENTS.md`, sans
   la boucle `converge` que les `CHEATSHEET`, `SETUP.md` et le `QUICKSTART` décrivent — et que
   le `spec-kit` épinglé fournit bien (`templates/commands/converge.md`). Ajoutée.

**Accord EN/FR des README** : relus en entier côte à côte, et contre-vérifiés par une
comparaison Jev (`jev_compare`, six aspects — nombres de skills, rejets, chiffres du scan,
personas, provenance, procédure d'épinglage) : `same_fact` sur les six, confiance 1,0. Jev
reste retiré du dépôt (voir l'entrée du 2026-10-02) ; l'appel a été fait à la demande, depuis
la session.

**Rangement** : les branches fusionnées `maintenance/pinning-and-laya` et
`maintenance/onboarding-and-checks` supprimées du dépôt distant.

---

## Avant de modifier ce fichier

Ajoute une entrée datée en bas, ne touche pas aux précédentes. Une entrée dit ce qui a
changé, **comment ça a été mesuré**, et ce qui a été décidé de ne pas faire. Un chiffre sans
sa méthode ne vaut rien six mois plus tard : c'est précisément pour ça que « 2808 fichiers de
skills » n'a jamais pu être reproduit.

Pour les contrôles automatiques qui remplacent désormais les recomptages à la main, voir
`python scripts/check.py` et [`AGENTS.md`](AGENTS.md) § « Checking the repository against
itself ».
