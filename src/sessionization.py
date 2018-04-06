import csv
import datetime
import operator
import sys
from collections import defaultdict
from collections import OrderedDict

INPUT_LOG_FILE = sys.argv[1]
INACTIVITY_PERIOD_FILE = sys.argv[2]
OUTPUT_FILE = sys.argv[3]

with open(INACTIVITY_PERIOD_FILE) as f:
    defined_inactivity_period = f.read()
    defined_inactivity_period = int(defined_inactivity_period)
f.close()

#Converts entry date time format into python datetime format
def convert_to_datetime(input_date, input_time):
    toConvert = str(input_date) + " " + str(input_time)
    datetime_output = datetime.datetime.strptime(toConvert, "%Y-%m-%d %H:%M:%S")
    return datetime_output

#Checks if session is active
def is_active(last_page_time, current_time):
    duration = (current_time - last_page_time).total_seconds()
    if duration > int(defined_inactivity_period):
        return False
    else:
        return True

#Writing inactive entries to output
def inactive_entries_to_file(oldest_entry, current_time, last_page_time_dict, ip_dict, first_page_time_dict):
    for ip_in_list in last_page_time_dict[oldest_entry]:
        try:
            output_ip = str(ip_in_list)
            output_first_page_time = str(ip_dict[ip_in_list][0])
            output_last_page_time = str(ip_dict[ip_in_list][1])
            output_duration = str(int((ip_dict[ip_in_list][1] - ip_dict[ip_in_list][0]).total_seconds()+1))
            output_count = str(ip_dict[ip_in_list][2])
            active = is_active(ip_dict[ip_in_list][1], current_time)
            if not active:
                with open('sessionization.txt', 'a') as output_file:
                    print(output_ip + "," + output_first_page_time + "," + output_last_page_time + "," +
                          output_duration + "," + output_count, file=output_file)
                    first_page_time_dict[ip_dict[ip_in_list][0]].remove(ip_in_list)
                    del ip_dict[ip_in_list]
                    del last_page_time_dict[oldest_entry][0]
        except IndexError:
            break
    del last_page_time_dict[oldest_entry]

#To write the active sessions at the end of the file to output
def write_last_bits_to_file(first_page_time_dict, ip_dict):
    o = OrderedDict(sorted(first_page_time_dict.items(), key=operator.itemgetter(0)))
    anotherList = []
    for time in o:
        for ip in o[time]:
            if ip not in anotherList:
                anotherList.append(ip)
    with open(OUTPUT_FILE, 'a') as output_file:
        for ip_in_list in anotherList:
            output_ip = str(ip_in_list)
            output_first_page_time = str(ip_dict[ip_in_list][0])
            output_last_page_time = str(ip_dict[ip_in_list][1])
            output_duration = str(int((ip_dict[ip_in_list][1] - ip_dict[ip_in_list][0]).total_seconds() + 1))
            output_count = str(ip_dict[ip_in_list][2])
            print(output_ip + "," + output_first_page_time + "," + output_last_page_time + "," +
                  output_duration + "," + output_count, file=output_file)

#main
with open(INPUT_LOG_FILE, newline='') as csvfile:
    file = csv.reader(csvfile, delimiter=' ', quotechar='|')
    header = file.__next__()[0].split(',')
    ip_col = header.index('ip')
    date_col = header.index('date')
    time_col = header.index('time')
    cik_col = header.index('cik')
    acc_col = header.index('accession')
    ext_col = header.index('extention')
    ip_dict = defaultdict(list) #key: ip, value: [first page, last page, count]
    last_page_time_dict = defaultdict(list) #key: time, value:[i1, ip2, ip3]
    first_page_time_dict = defaultdict(list)
    passed_first_line = False

    for entry in file:
        entry = entry[0].split(',')
        ip = entry[ip_col]
        date = entry[date_col]
        time = entry[time_col]
        current_time = convert_to_datetime(date, time)

        #To avoid empty lists at the very beginning
        if passed_first_line:
            try:
                oldest_entry = min(list(last_page_time_dict))
            except ValueError:
                pass
            if current_time - oldest_entry > datetime.timedelta(seconds=defined_inactivity_period):
                inactive_entries_to_file(oldest_entry, current_time, last_page_time_dict, ip_dict, first_page_time_dict)

        if ip in ip_dict:
            try:
                ip_dict[ip][2] = ip_dict[ip][2] + 1 #update count
                ip_dict[ip][1] = current_time #update last page time
                last_page_time_dict[current_time].append(ip)
            except IndexError:
                continue
        else:
            passed_first_line = True
            ip_dict[ip] = [current_time, current_time, 1] #[first page, last page, count]
            last_page_time_dict[current_time].append(ip)
            if ip not in first_page_time_dict[current_time]:
                first_page_time_dict[current_time].append(ip)

    write_last_bits_to_file(first_page_time_dict, ip_dict)
