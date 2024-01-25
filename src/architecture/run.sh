execute(){	

    ### Recursive function that execute a block and call itself recursivly on the next block according to the transition table 
    ### Usage : execute <block_name> 

    block_name=$1

    ### Check if the process appears in the transition table
    if [[ -v process_list[$block_name] ]] 	
    then
	line=${process_list[$block_name]}		# Get the line in the transition table corresponding to the current block
        
	### Parse the line in csv format : 
	### <block_name>,<command>,<transition_0>,<transition_1> 
	
	cmd=$(echo $line | awk -F $separator '{print $2}') 
        t0=$(echo $line | awk -F $separator '{print $3}') 
        t1=$(echo $line | awk -F $separator '{print $4}') 
        
	table=($t0 $t1) 				# Transition table for the current block
	
	### Print starting block informations			

        echo -e "\n\x1b[1;32m////////////[ $1 ]///////////////\x1b[0m"
     
        echo -e "\x1b[1;35m"
        echo -e "[ $1 : START ]          : $(date "+%H:%M:%S") "
        echo -e "\x1b[0m"
      
				### BLOCK EXECUTION ###

        time0=$(date "+%s.%4N")    			# Get time before the block execution
        
	$cmd -v 2> return_value_buffer &		# Execute the block in background and redirect the stderr output into a buffer file
	current_block_pid="$!"				# Store the PID of the block execution in case of sigINT
	wait 						# Wait the end of the block execution

        time1=$(date "+%s.%4N")    			# Get time after the block execution
        
	return_value=$(cat return_value_buffer) 	# Get from the buffer file the return value of the block execution
        rm return_value_buffer				# Delete the buffer file
    
	### Print ending block informations			

        echo -e "\x1b[1;35m"
        echo -e "[ $1 : END ]            : $(date "+%H:%M:%S") "
        echo -e "[ $1 : RETURN VALUE ]   : $return_value "
        echo -e "[ $1 : TIME ]           : $(echo $time1 - $time0 | bc) s"
        

				### TRANSITION ###  

	### Check in the table if there is a transition corresponding to this return value for the current block
        
	if [[ -v table[$return_value] ]];		
	then	
		# Get the next block in the table and call execute on it
            
	    next_process=${table[$return_value]}
            echo -e "[ $1 : NEXT PROCESS ]   : $next_process"
            execute $next_process
        
        else  	
		# End of the programm
	    
	    echo -e "[ $1 : NEXT PROCESS ]   : none"
            echo -e "\x1b[1;33m"
	    echo -e "[ program : END ]       : $(date "+%H:%M:%S")"
            echo -e "\x1b[0m"
            exit 0
        fi


    else	
	    # End of the programm
        
	echo -e "\x1b[1;33m"
        echo -e "[ program : INFO ]      : process $1 not found in the transition table"
	echo -e "[ program : END ]       : $(date "+%H:%M:%S")"
	
	echo -e "\x1b[0m"
        exit 1

    fi
}

onINT() { 

	### Function to call when the shell get an INT signal 
	### Stop the current block properly

	kill -15 $current_block_pid 
}

trap onINT SIGINT				# Link onINT function to SIGINT trap

separator=';'					# Separator symbol for the csv file
nb_process=$(cat transition.csv | wc -l) 	# number of line in the transition.csv file

### Associativ array that store the csv lines in association with there block's name
declare -A process_list


echo "╭─╴ ╭─╮ ╭─╮ ╵ ╭─╮ ╷      ┌─╮ ╭─╴ ╭─╮ ╭─╮"
echo "├╴  ├─┤ │   │ ├─┤ │   ─  ├┬╯ ├╴  │   │ │"
echo "╵   ╵ ╵ ╰─╯ ╵ ╵ ╵ ╰─╴    ╵╵  ╰─╴ ╰─╯ ╰─╯"

echo -e "\x1b[1;33m"
echo -e "[ program : START ]     : $(date "+%H:%M:%S")"
echo -e "\x1b[0m"
	

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

echo -e "\n$(($nb_process - 1)) blocks fund in the transition table : "

python3 aff_process.py ${!process_list[@]}

execute $process_0 
