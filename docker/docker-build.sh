docker build -t reco .;

id_docker=$(docker run -id -v $(pwd)/..:/facial-reco-ia reco);

docker exec -ti $id_docker bash