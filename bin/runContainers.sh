for subdir in `ls /etc/pilink/services`;
do
    (docker-compose -f /etc/pilink/services/$subdir/docker-compose.yml up --remove-orphans -d);
done
