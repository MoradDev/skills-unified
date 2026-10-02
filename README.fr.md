# Skills Unified

**Un workspace prêt à l'emploi pour agents de code. On le clone, on dit à son agent de
lire `SETUP.md`, et il installe le reste lui-même.**

*[English version](README.md)* · *Toutes les commandes sur une page : [CHEATSHEET.fr.md](CHEATSHEET.fr.md)*

Les skills d'agents sont dispersées dans des dizaines de dépôts, avec des noms qui se
recouvrent, des descriptions qui se concurrencent et une qualité très inégale. Ce dépôt
est le résultat de l'audit de 21 d'entre eux — 2808 fichiers de skills au total — dont on
a gardé les 83 qui méritent leur place, en laissant le raisonnement à découvert.

Il n'est pas lié à Claude Code. N'importe quel agent sachant lire du Markdown peut s'en
servir.

---

## Démarrage

```bash
git clone https://github.com/MoradDev/skills-unified.git mon-workspace
cd mon-workspace
```

Le nom du dossier est libre, rien n'en dépend. Choisis-en un qui n'existe pas déjà :
sous Windows et macOS le système de fichiers est insensible à la casse, donc un nom
générique comme `workspace` entrera en collision avec un `Workspace` existant et le
clone échouera.

Ouvre ensuite ton agent dans ce dossier et donne-lui une seule instruction :

> Lis SETUP.md et installe ce workspace.

C'est tout. L'agent détermine ton système, clone dans `mes_depots/` ce dont la méthode a
besoin, raccorde `curation/` à tes projets par le mécanisme que ton harnais supporte, et
te rend compte de ce qu'il a fait.

Rien n'est installé globalement. Rien n'est activé à ton insu.

---

## Ce que tu obtiens

**83 skills sélectionnées**, en deux familles.

Plus la méthode de travail elle-même, bâtie sur [spec-kit](https://github.com/github/spec-kit) :
tout projet démarre par `specify init`, puis enchaîne constitution → specify → clarify →
plan → tasks → analyze → implement. Chaque étape produit un artefact que la suivante
consomme — c'est ce qui empêche un agent d'inventer des exigences en cours de route.

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

## Les quatre dépôts activés par défaut

Quatre dépôts amont sont raccordés à chaque nouveau projet sans passer par la curation
ci-dessus : `superpowers`, `taste-skill`, `ponytail` et `agency-agents`. C'est une exception
assumée, et la raison est simple — **c'est pour moi le minimum requis pour bien coder avec un
harnais IA.** Pas une sélection triée : un plancher.

Ce que chacun apporte réellement, d'après son propre README et ses propres skills :

- **[`obra/superpowers`](https://github.com/obra/superpowers)** (15 skills) — une méthode de
  développement complète plutôt qu'un paquet de skills : elle fait extraire une spec de la
  conversation par l'agent, écrire un plan qu'un junior pourrait suivre, puis l'exécuter via
  des sous-agents en TDD rouge/vert, avec revue de code et étape de vérification avant que
  quoi que ce soit ne soit déclaré fini.
- **[`Leonxlnx/taste-skill`](https://github.com/Leonxlnx/taste-skill)** (13 skills) — le
  jugement visuel. Il porte une direction artistique concrète par style (minimalisme
  éditorial, brutalisme suisse, finition d'agence) avec les polices, espacements et règles
  d'ombre exacts, pour qu'une interface générée cesse d'avoir l'air d'un gabarit.
- **[`DietrichGebert/ponytail`](https://github.com/DietrichGebert/ponytail)** (6 skills) — un
  mode YAGNI permanent, actif dès le début de session, qui pousse l'agent vers la solution la
  plus courte qui marche et relit un diff ou un dépôt entier à la recherche de
  sur-ingénierie. Son propre benchmark annonce ~54 % de code en moins sur 12 tâches, face au
  même agent sans lui.
- **[`msitarzewski/agency-agents`](https://github.com/msitarzewski/agency-agents)** (297
  personas) — des sous-agents spécialistes à qui déléguer : ingénierie, design, sécurité,
  tests, produit et bien d'autres, pour qu'une tâche étroite aille à quelque chose écrit pour
  elle plutôt qu'au généraliste.

**Les recoupements ont été vérifiés, et aucun n'a été résolu en silence.** Les champs
`description` de leurs skills et agents ont été comparés à ceux de `curation/skills/`, parce
que l'auto-invocation se décide sur la correspondance des descriptions et que l'espace de noms
n'empêche pas la concurrence. Plusieurs recoupements réels existent :
`superpowers:test-driven-development` face aux skills de test par langage (`react-testing`
pointe déjà vers lui nommément), `superpowers:using-superpowers` face à `using-agent-skills`,
`superpowers:brainstorming` face à `grill-me` et à l'étape specify de spec-kit,
`taste-skill:high-end-visual-design` face à `make-interfaces-feel-better`, et une poignée de
personas d'`agency-agents` face aux skills couvrant le même stack. Ils sont listés en entier
dans la pull request qui a ajouté cette section. Aucun n'a été retiré : le plancher reste
entier, et savoir où deux déclencheurs se concurrencent est plus utile que de faire comme si
ce n'était pas le cas.

## Pourquoi VoiceStudio, voicebox et SCAIL-2 sont au catalogue

Ils ne sont jamais activés — leur `activation` vaut `stock` : ils sont au catalogue comme des
pièces, pas comme des skills, et aucun agent ne les charge de lui-même. Ils y figurent parce
que les applications qu'on amorce ici embarquent souvent de l'IA, et que lorsqu'il faut de la
parole ou un modèle vision-langage, mieux vaut prendre un projet connu et déjà inspecté que
d'improviser. À proposer comme briques de l'application construite, jamais comme partie de la
méthode.

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

## Dépôts amont épinglés, et comment en mettre un à jour

`catalog/repos.tsv` porte une colonne `commit` et une date `scanned` pour chaque dépôt amont.
`SETUP.md` clone **ce commit**, pas la pointe de la branche : ce que tu installes est donc
l'état réellement inspecté. Sans l'épinglage, le scan décrit plus haut porte sur un état passé
d'une branche qui bouge, et ne dit rien du code posé sur ton disque.

Un épinglage se déplace à la main, délibérément. La procédure :

1. **Lis le diff.** `git -C mes_depots/<nom> fetch origin && git -C mes_depots/<nom> diff
   <ancien-sha>..origin/HEAD --stat`, ou `https://github.com/<owner>/<repo>/compare/<ancien-sha>...<nouveau-sha>`
   dans un navigateur.
2. **Ne scanne que les fichiers exécutables touchés par le diff.** `git diff --name-only
   <ancien-sha>..<nouveau-sha> -- '*.py' '*.sh' '*.js' '*.ts' '*.ps1'` en donne la liste.
   Extrais les domaines sortants, et cherche `curl | sh`, `base64 -d | sh` et `eval` sur une
   réponse réseau. Les changements Markdown sont de la prose : lis-les si tu veux, mais un
   finding de scanner sur un `.md` ne veut rien dire (voir plus haut).
3. **Relis-le toi-même.** Un humain regarde chaque changement exécutable avant que
   l'épinglage ne bouge. Le scanner aide cette lecture, il ne la remplace jamais — et **ne le
   câble jamais en garde-barrière automatique** : il classe les skills officielles d'Anthropic
   en « DO NOT INSTALL », donc une barrière bâtie dessus bloquerait du code correct et
   apprendrait à tout le monde à la contourner.
4. **Déplace l'épinglage.** Écris le nouveau SHA dans la colonne `commit` et la date
   d'inspection dans `scanned`. Committe la modification du TSV seule, avec le lien de
   comparaison dans le message.
5. **Re-clone.** Supprime `mes_depots/<nom>` et rejoue l'étape 2 de `SETUP.md`. Ne fais jamais
   `git pull` dans un clone épinglé — c'est comme ça qu'un cache dérive en silence loin de ce
   qui est écrit.

Une GitHub Action mensuelle ([`.github/workflows/upstream-watch.yml`](.github/workflows/upstream-watch.yml))
compare chaque épinglage à la pointe de sa branche et tient à jour une issue unique listant ce
qui a bougé. Elle se contente de signaler. Elle ne change rien et ne bloque rien.

## Un projet, plusieurs agents

Chaque harnais garde sa mémoire privée, et aucun ne sait lire celle d'un autre. Tu démarres
un projet sous Claude Code, tu le reprends la semaine suivante sous Cursor, et le second
agent arrive à l'aveugle — la spec est sur le disque, mais tout ce qui s'est décidé en
conversation a disparu.

L'état partagé vit donc dans le dépôt, dans **`STATE.md` à la racine du projet** : étape en
cours, dernière et prochaine action, décisions prises en conversation *avec leur
justification*, blocages, et pièges découverts à la dure. Du Markdown, rien d'autre.

`AGENTS.md` rend la règle contraignante — le lire en arrivant, le mettre à jour en partant,
même après une session qui n'a rien produit (« exploré X, impasse, ne pas réessayer » mérite
d'être écrit). La section `Journal` est en ajout seul, donc deux agents ne peuvent pas
s'écraser mutuellement, et une table « notes propres au harnais » sert à recopier ce que la
mémoire privée d'un agent contient et que les autres devraient savoir.

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
