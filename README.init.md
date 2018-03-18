To add the private ssh key to the internal volume follow this procedure:

    docker-compose run --rm --name eeadockergithubdocs_init app tail -f /dev/null
    docker exec -it eeadockergithubdocs_init bash
    cd /root/.ssh
    cat > id_rsa
    # paste private key
    chmod 700 id_rsa
    exit
    docker stop eeadockergithubdocs_init
    # restart
    docker-compose up
