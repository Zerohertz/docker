docker build -t label-studio .
docker run \
    --name label-studio \
    -p 8080:8080 \
    -v ${root}/data:/label-studio/data \
    -v ${root}/files:/home/user \
    label-studio