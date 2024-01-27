### This script run the automaton described in the CSV transition file by executing one after the other the different blocks according to there transition table

execute(){	

    ### Recursive function that execute a block and call itself recursivly on the next block according to the transition table 
    ### Usage : execute <block_name> 

    block_name=$1

    ### Check if the block appears in the transition table
    if [[ -v Blocks_data[$block_name-name] ]] 	
    then
      	
	### Get data of the current block
	 
	cmd=${Blocks_data[$block_name-cmd]}
	t0=${Blocks_data[$block_name-0]}
	t1=${Blocks_data[$block_name-1]}
        
	table=($t0 $t1) 				# Transition table for the current block
	
	if [ "$verbose" = true ];
	then 
		cmd="$cmd -v"
	fi

	### Print starting block informations			

        echo -e "\n\x1b[1;32m////////////[ $1 ]///////////////\x1b[0m"
     
        echo -e "\x1b[1;35m"
        echo -e "[ $1 : START ]          : $(date "+%H:%M:%S") "
        echo -e "\x1b[0m"
     
				### BLOCK EXECUTION ###

        time0=$(date "+%s.%4N")    			# Get time before the block execution
        
	$cmd 2> return_value_buffer &			# Execute the block in background and redirect the stderr output into a buffer file
	current_block_pid="$!"				# Store the PID of the block execution in case of sigINT
	wait $current_block_pid 			# Wait the end of the block execution
       
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
        echo -e "[ program : INFO ]      : block $1 not found in the transition table"
	echo -e "[ program : END ]       : $(date "+%H:%M:%S")"
	echo -e "\x1b[0m"
        exit 1

    fi
}



# Function that stop the current block properly
onINT() { 
	
	if ps -p $current_block_pid > /dev/null
	then
		echo -e "\x1b[1;33m[ program : INFO ]       : killing block $block_name"
		kill -15 $current_block_pid 
	else
		# End of the programm
	
	        echo -e "\x1b[1;33m"
	        echo -e "[ program : INFO ]      : programm get kill"
	        echo -e "[ program : END ]       : $(date "+%H:%M:%S")"
	        echo -e "\x1b[0m"
	        exit 0
	fi
}

trap onINT SIGINT			      	# Link onINT function to SIGINT trap



verbose=false					# verbose booleen for block
logfile_name=					# log file
duration=					# programm duration in s
separator=';'					# Separator symbol for the csv file
transitionfile_name=transition.csv		# CSV transition file

usage() {
	echo "Usage: $0 [OPTIONS]"
	echo "Options:"
	echo " -h, --help			Display this help message"
	echo " -v, --verbose			Enable verbose mode"
	echo " -f, --file <FILE> 		Specify an output log file"
	echo " -t, --transition <FILE>		Specify an input csv transition file, default 'transition.csv'"
	echo " -s, --sep <SEPARATOR>		Specify the separator of the csv transition file, default ';'"
	echo " -d, --duration  hh:mm:ss 	Set a timesout"
}

has_argument() {
	[[ ("$1" == *=* && -n ${1#*=}) || ( ! -z "$2" && "$2" != -*)  ]];
}

extract_argument() {
	echo "${2:-${1#*=}}"
}

is_correct_duration_format() {
	[[ "$1" =~ [0-9]+:[0-9]+:[0-9]+ ]];		
}	

### Function to handle options and arguments
handle_options() {
	while [ $# -gt 0 ]; do
		case $1 in
			-h | --help)
        			usage
        			exit 0
        			;;

      			-v | --verbose)
        			verbose=true
        			;;

      			-f | --file*)
        			if ! has_argument $@; 
				then
          				echo "File not specified." >&2
          				usage
          				exit 1
        			fi
        			logfile_name=$(extract_argument $@)
        			shift
        			;;

			-t | --transition*)
        			if ! has_argument $@; 
				then
          				echo "Transition file not specified." >&2
          				usage
          				exit 1
        			fi
        			transitionfile_name=$(extract_argument $@)
        			shift
        			;;


      			-s | --sep*)
        			if ! has_argument $@; 
				then
          				echo "Separator not specified." >&2
          				usage
          				exit 1
        			fi
        			separator=$(extract_argument $@)
        			shift
        			;;

			-d | --duration*)
        			if ! has_argument $@; 
				then
          				echo "Duration not specified." >&2
          				usage
          				exit 1
        			fi
        			
				duration=$(extract_argument $@)
        			
				if ! is_correct_duration_format $duration;
				then
          				echo "Bad duration format." >&2
          				usage
          				exit 1
				fi
				shift
        			;;


      			*)
        			echo "Invalid option: $1" >&2
        			usage
        			exit 1
        			;;
    		esac
    		shift
  	done
}

			### MAIN ###

handle_options "$@"

nb_process=$(cat $transitionfile_name | wc -l) 	# number of line in the CSV transition file

### Associativ array that store the data of blocks contained in the csv transition file 
declare -A Blocks_data
declare -a Block_list


### LOGFILE REDIRECTION
if [ "$logfile_name" != "" ];
then
	exec &> $logfile_name
fi


### TIMEOUT DEAMON
if [ "$duration" != "" ];
then
	PID=$$
	
	h=$(echo $duration | awk -F ':' '{print $1}')
	m=$(echo $duration | awk -F ':' '{print $2}')
	s=$(echo $duration | awk -F ':' '{print $3}')

	# (sleep $h\h $m\m $s\s && echo -e "\x1b[1;33m[ program : INFO ]	: timeout\x1b[0m" && kill -INT "$PID") &
	(sleep $h\h $m\m $s\s && kill -INT "$PID") &
	timeout_deamon_pid="$!"
fi



echo "╭─╴ ╭─╮ ╭─╮ ╵ ╭─╮ ╷      ┌─╮ ╭─╴ ╭─╮ ╭─╮"
echo "├╴  ├─┤ │   │ ├─┤ │   ─  ├┬╯ ├╴  │   │ │"
echo "╵   ╵ ╵ ╰─╯ ╵ ╵ ╵ ╰─╴    ╵╵  ╰─╴ ╰─╯ ╰─╯"

echo -e "\x1b[1;33m"
echo -e "[ program : START ]     : $(date "+%H:%M:%S")"
echo -e "\x1b[0m"
	

echo "Reading $transitionfile_name file"
for ((i=2; i <= $nb_process; i++))
do  
    line=$(sed -n $i\p $transitionfile_name)

    if [ "$line" != "" ];
    then
        echo "ligne $i : $line"

	### Parse the line in csv format : 
	### <block_name>,<command>,<transition_0>,<transition_1> 
	
        name=$(echo $line | awk -F $separator '{print $1}') 
        cmd=$(echo $line | awk -F $separator '{print $2}') 
        t0=$(echo $line | awk -F $separator '{print $3}') 
        t1=$(echo $line | awk -F $separator '{print $4}') 

	Block_list[$(( $i -1 ))]=$name
	
	Blocks_data["$name-name"]=$name
	Blocks_data["$name-cmd"]=$cmd
	Blocks_data["$name-0"]=$t0
	Blocks_data["$name-1"]=$t1

        if [ $i -eq 2 ];then
            process_0=$name 	    
        fi
    fi
done

echo -e "\n$(($nb_process - 1)) blocks fund in the transition table : "

python3 aff_process.py ${Block_list[@]}

execute $process_0 
