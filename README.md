
# Approach

### Storing entries
1. Read in csv file
2. Find headers, their indexes and store them for later used
3. Read in the first entry and store the entry information into IP, First Page Time and Last Page Time dictionaries. These are defaultdict with values initialized as lists. The IP dictionary uses IP as keys and the entry as values. Both First Page Time and Last Page Time Dictionaries store python's datetime data type as keys and IP as values.
4. If the entry already exists in the IP dictionary then the access count, which is also stored in the IP dictionary as a value, will be incremented by 1

### Looking for inactive sessions
1. The program will look for inactive sessions according to the set inactivity_period
2. When current time - oldest entry time is larger than inactivity_period then the program will use the Last Page Time dictionary to find the oldest entry time and the IPs at that time. The IPs latest entry time will be looked up in the IP dictionary and compared to the current time if it is inactive then the entry will be output onto sessionization.txt and the IP's entry will be deleted from all three dictionaries.

#### Wrapping up
1. When the end of the file is reached the program will look at what is left of the First Page Time dictionary which is ordered by which entry came first, and write the sessions that weren't expired at the end of the file to the output.

# Dependencies
No external packages were used.

# Run instructions
The program can be executed by executing run.sh. <br />
(sudo chmod 777 run.sh then ./run.sh)
