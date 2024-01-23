declare -A process_list

execute(){
    if [[ -v process_list[$1] ]] 
    then
        
	line=${process_list[$1]}
        
	cmd=$(echo $line | awk -F $separator '{print $2}') 
        t0=$(echo $line  | awk -F $separator '{print $3}') 
        t1=$(echo $line  | awk -F $separator '{print $4}') 
        table=($t0 $t1)
    
        echo -e "\n\x1b[1;32m////////////[ $1 ]///////////////\x1b[0m"
     
        echo -e "\x1b[1;35m"
        echo -e "[ $1 : START ]          : $(date "+%H:%M:%S") "
        echo -e "\x1b[0m"
       
        time0=$(date "+%s.%4N")    
        $cmd 2> return_value_buffer
        time1=$(date "+%s.%4N")    
        return_value=$(cat return_value_buffer)
        rm return_value_buffer
    
        echo -e "\x1b[1;35m"
        echo -e "[ $1 : END ]            : $(date "+%H:%M:%S") "
        echo -e "[ $1 : RETURN VALUE ]   : $return_value "
        echo -e "[ $1 : TIME ]           : $(echo $time1 - $time0 | bc) s"
        
        if [[ "$return_value" == "0" || "$return_value" == "1" ]];
        then
            next_process=${table[$return_value]}
        	echo -e "[ $1 : NEXT PROCESS ]   : $next_process"
            execute $next_process
        else
            echo -e "[ $1 : NEXT PROCESS ]   : none"
            echo -e "\x1b[1;33m"
            echo -e "[ program : STATE ]     : finish"	
            
	    signal_handler_pid=$(ps ax | grep 'python3 signalhandler.py' | grep -v grep | awk '{print $1}')
       	    kill -15 $signal_handler_pid

            echo -e "\x1b[0m"
            exit 0
        fi
    else
        echo -e "\x1b[1;33m"
        echo -e "[ program : ERROR ]     : process $1 not found in the transition table"
        echo -e "[ program : STATE ]     : finish"
	
	signal_handler_pid=$(ps ax | grep 'python3 signalhandler.py' | grep -v grep | awk '{print $1}')
       	kill -15 $signal_handler_pid
        
	echo -e "\x1b[0m"
        exit 1

    fi
}

separator=';'
nb_process=$(cat transition.csv | wc -l) 

echo "╭─╴ ╭─╮ ╭─╮ ╵ ╭─╮ ╷      ┌─╮ ╭─╴ ╭─╮ ╭─╮"
echo "├╴  ├─┤ │   │ ├─┤ │   ─  ├┬╯ ├╴  │   │ │"
echo "╵   ╵ ╵ ╰─╯ ╵ ╵ ╵ ╰─╴    ╵╵  ╰─╴ ╰─╯ ╰─╯"


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
