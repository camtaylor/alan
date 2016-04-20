
WORD=""
echo ":speak:This is a letter plugin"
while [ "$WORD" !=  "exit" ]
do
echo ":speak: $WORD "
echo ":listen:"
read WORD

done
