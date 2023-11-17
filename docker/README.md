# Launch docker container

- Be at the root of the repository project and **build** image with `dockerfile`.

```bash
docker build -t reco .
```

- Run the container.

```bash
docker run -id -v $(pwd):/facial-reco-ia reco
```

- Execute and open the container.

```bash
docker exec -ti <id_conteneur> bash
```