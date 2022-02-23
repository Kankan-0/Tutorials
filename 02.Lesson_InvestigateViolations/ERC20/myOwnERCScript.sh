
if [ "$#" -eq 3 ]
then
certoraRun "$1":ERC20 --verify ERC20:ERC20.spec \
--solc solc8.0 \
--optimistic_loop \
--msg "$2" \
--rule "$3"

elif [ "$#" -eq 2 ]
then 
certoraRun "$1":ERC20 --verify ERC20:ERC20.spec \
--solc solc8.0 \
--optimistic_loop \
--msg "$2"

fi