# Démarrage rapide — de rien à une app qui tourne

*[English version](QUICKSTART.md)* · *Pourquoi tout ça existe : [README.fr.md](README.fr.md)*

Cette page suppose que tu n'as jamais utilisé ce workspace. C'est le chemin le plus court
qui soit honnête. Tout le reste du dépôt est de la documentation de référence que tu peux
ignorer aujourd'hui.

---

## Ce qu'il te faut d'abord

| | Pourquoi | Vérifier |
|---|---|---|
| **git** | Obligatoire. Rien ne marche sans. | `git --version` |
| **Un agent avec un CLI** | Claude Code, Codex, Cursor, Gemini CLI, opencode… | `claude --version` |
| **[uv](https://astral.sh/uv)** | Installe `specify`, qui échafaude chaque projet | `uv --version` |
| **Node.js** (optionnel) | Seulement pour les hooks du plugin `ponytail`. Tu peux t'en passer, dis-le. | `node --version` |

`uv` manquant ? `curl -LsSf https://astral.sh/uv/install.sh \| sh` sous macOS/Linux,
`irm https://astral.sh/uv/install.ps1 \| iex` sous PowerShell.

---

## Trois commandes

```bash
git clone https://github.com/MoradDev/skills-unified.git mon-workspace
cd mon-workspace
```

Choisis un nom de dossier qui n'existe pas déjà. Sous Windows et macOS le système de
fichiers est insensible à la casse, donc un nom générique comme `workspace` entrera en
collision avec un `Workspace` existant et le clone échouera.

Ouvre ensuite ton agent **dans ce dossier** et donne-lui une seule instruction :

> Lis SETUP.md et installe ce workspace, puis crée un projet appelé `livres`.

Il va contrôler ton système, cloner ce dont la méthode a besoin aux commits que ce dépôt
épingle, installer `specify`, échafauder `livres/`, y raccorder les skills et créer son
`STATE.md`. Il s'arrête là volontairement — il ne commence pas à construire.

Ouvre alors une **nouvelle** session, cette fois dans `mon-workspace/livres/`, et accepte le
dialogue de confiance si ton agent en affiche un. Les skills d'un projet ne se chargent que
depuis le dossier où la session a été ouverte.

---

## Un exemple complet : « une page pour suivre les livres que j'ai lus »

Tape ceci dans l'ordre, dans la session du projet. Chaque étape produit un fichier que la
suivante relit — c'est tout l'intérêt : l'agent ne peut pas oublier en silence ce que tu as
validé.

| Tu tapes | Ce que tu obtiens | Ton rôle |
|---|---|---|
| `/speckit-constitution` | `.specify/memory/constitution.md` — tes non-négociables | Réponds à ses questions. « Ça doit marcher hors ligne » et « pas de compte utilisateur » vont là. |
| `/speckit-specify` *une page où je note les livres finis, avec titre, auteur, date et une note de 1 à 5* | `spec.md` — le **quoi** et le **pourquoi**, aucune technologie | Lis-le. Il est court exprès. Corrige tout ce qui n'est pas ce que tu voulais dire. |
| `/speckit-clarify` | Les réponses intégrées à `spec.md` | Il t'interroge sur ce que tu as laissé flou. Réponds simplement. |
| `/speckit-plan` | `plan.md` — la stack et l'architecture | **C'est ici que tu dis non.** S'il propose Postgres et Docker pour une page que tu utilises seul, dis-le. |
| `/speckit-tasks` | `tasks.md` — une liste ordonnée | Parcours-la. Une tâche qui t'est obscure est obscure pour l'agent aussi. |
| `/speckit-implement` | Du vrai code | Laisse-le travailler. Fais-lui remonter les échecs avec leur sortie. |
| `/speckit-converge` | De nouvelles tâches pour les écarts entre le code et la spec | Répète implement → converge jusqu'à ce qu'il ne trouve plus rien. |

**Une idée floue plutôt que claire ?** Dis *« grille-moi sur cette idée »* avant
`/speckit-specify`. Tu te fais interroger jusqu'à ce que l'idée tienne. C'est plus rapide
que de spécifier quelque chose que tu n'as pas pensé jusqu'au bout.

**Avant de finir une session**, écris ce qui s'est passé dans `livres/STATE.md`. C'est la
seule chose qu'un autre agent — ou toi dans trois semaines — pourra lire pour reprendre le
travail. Même « essayé X, impasse, ne pas réessayer » mérite une ligne.

---

## Ce qui travaille pour toi, en silence

Tu n'invoques pas ces choses. Elles se déclenchent sur ce que tu fais.

| | Effet sur ta session |
|---|---|
| **84 skills sélectionnées** | Une question React appelle la skill React, une question Postgres celle de Postgres. Tu ne les nommes jamais. |
| **superpowers** | Pousse les tests avant le code, le débogage systématique, la vérification avant de déclarer quoi que ce soit fini. |
| **ponytail** | Plaide pour la chose la plus courte qui marche. Dis *« stop ponytail »* pour le couper sur la session. |
| **taste-skill** | Fait que les interfaces générées aient l'air dessinées, pas gabaritées. |
| **14 agents spécialistes** | Architecture, backend, frontend, revue, base de données, devops, prototypage, UI, UX, tests, accessibilité, appsec, rédaction technique. Contrairement aux skills, ceux-là s'appellent : *« utilise l'architecte backend pour ça »*. |

Elles se recoupent parfois et se concurrencent. [`AGENTS.md`](AGENTS.md) § « When two skills
compete » liste les cas connus et quoi faire pour chacun.

---

## Quand ça se passe mal

| Symptôme | Cause |
|---|---|
| Aucune skill ne se déclenche jamais | Session ouverte à la racine du workspace, pas dans le dossier du projet. Réouvre-la dans `mon-workspace/livres/`. |
| « Agent Detection Error : claude not found » | `specify` ne voit pas le CLI de ton agent. Ajoute `--ignore-agent-tools`. |
| L'agent écrit une spec de trois pages pour un truc minuscule | Dis-le. `/speckit-specify` accepte la correction, et `ponytail` existe exactement pour cette dispute. |
| Il veut t'interroger alors que tu sais déjà ce que tu veux | Deux skills se concurrencent sur le même déclencheur. Dis-lui de passer directement à `/speckit-specify`. |
| `ponytail` n'arrive pas à se charger | Node.js absent. Sans conséquence — tout le reste fonctionne. |

---

## Où aller ensuite

- [`CHEATSHEET.fr.md`](CHEATSHEET.fr.md) — toutes les commandes et toutes les skills, sur une page
- [`AGENTS.md`](AGENTS.md) — la méthode de travail en entier, et les règles que suit l'agent
- [`README.fr.md`](README.fr.md) — pourquoi cette sélection et pas une autre
