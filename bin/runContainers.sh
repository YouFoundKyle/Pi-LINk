for subdir in `ls /etc/pilink/services`;
do
    (sudo -u ha docker-compose -f /etc/pilink/services/$subdir/docker-compose.yml up --remove-orphans -d);
done
