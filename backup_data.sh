DATE=`date +%d-%m-%Y`
BACKUP=backup-$DATE
mkdir $BACKUP
mv img*.png $BACKUP
mv history.out $BACKUP
