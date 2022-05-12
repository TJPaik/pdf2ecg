# ecg_parsing_from_pdf_docker

```shell
docker save -o converter.tar converter:220216
docker load -i tar converter.tar

# "A" folder contains pdf files
docker run -it --rm -v A:/root/workspace converter:220216
```