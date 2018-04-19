DATE=`date +%d-%m-%Y-%H:%M:%S`
BACKUP=backup-$DATE
mkdir $BACKUP
mv img*.png $BACKUP
mv history.out $BACKUP
