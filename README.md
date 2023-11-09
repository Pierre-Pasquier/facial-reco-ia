# facial-reco-ia

Dépôt principal du projet avec tous les codes utilisés relatifs à l’IA et reconnaissance faciale respectant une structure classique de dossiers (source, tests, modèles...)

## Lancer le container docker

- Se placer à la racine du projet et **build** l'image avec le `dockerfile`.

```bash
docker build -t reco .
```

- Lancer le conteneur.

```bash
docker run -id reco
```

- Ouvrir le conteneur.

```bash
docker exec -ti <id_conteneur> bash
```
