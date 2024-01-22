declare -A process_list

execute(){
    line=${process_list[$1]}
    if [ "$line" == "" ];
    then
        echo "process $1 not found in the transition table"
        echo "Program over"
        exit 1
    fi  
    cmd=$(echo $line | awk -F $separator '{print $2}') 
    t0=$(echo $line  | awk -F $separator '{print $3}') 
    t1=$(echo $line  | awk -F $separator '{print $4}') 
    table=($t0 $t1)
    echo "$1 is running ..."
    return_value=$($cmd)
    echo "$1 finish with return value $return_value"
    if [[ "$return_value" == "0" || "$return_value" == "1" ]];
    then
        next_process=${table[$return_value]}
        echo "next process : $next_process"
        execute $next_process
    else
        echo "no process, program over"
        exit 0
    fi
}

separator=';'
nb_process=$(cat transition.csv | wc -l) 


echo "Reading transition.csv file"
for ((i=2; i <= $nb_process; i++))
do  
    line=$(sed -n $i\p transition.csv)

    if [ "$line" != "" ];
    then
        echo "ligne $i : $line"

        name=$(echo $line | awk -F $separator '{print $1}') 
	process_list[$name]=$line


        if [ $i -eq 2 ];then
            process_0=$name 	    
        fi
    fi
done

execute $process_0 & python3 signalhandler.py
