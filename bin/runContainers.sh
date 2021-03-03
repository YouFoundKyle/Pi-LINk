for subdir in `ls /etc/pilink/services`;
do
    (sudo -u ha docker-compose -f ./$subdir/docker-compose.yml up --remove-orphans -d);
done
