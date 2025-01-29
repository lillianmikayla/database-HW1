import csv
import os.path


class DB:

    #default constructor
    def __init__(self):
        self.filestream = None
        self.numRecords = 0
        self.recordSize = 0
        self.dataFileptr = None
        self.openFlag = False       

    def __readCSV(self, csv_reader):
        # read and parse a line of the csv file. 
        try:
            row = next(csv_reader)
            id = row[0]
            state = row[1]
            city = row[2]
            name = row[3]
        # Display the contents of each record to the screen to test that you are reading it properly.
            print(f"ID: {id}, State: {state}, City: {city}, Name: {name}")
            return id, state, city, name
        except StopIteration:
            return None
        
    # Formatting files with spaces so each field is fixed length, i.e. ID field has a fixed length of 10
    def writeRecord(self, filestream, id, state, city, name):
        try:
            self.recordSize = 101 # 10 + 20 + 20 + 50 + 1 (1 is for the new line character)

            filestream.write("{:10.10}".format(id))
            filestream.write("{:20.20}".format(state))
            filestream.write("{:20.20}".format(city))
            filestream.write("{:50.50}".format(name))
          # filestream.write("{:30.30}".format(industry))
            filestream.write("\n")
            return True
        except IOError:
            return False
        
    #create database
    def createDB(self,filename):
        #Generate file names
        csv_filename = filename + ".csv"
        text_filename = filename + ".data"
        config_filename = filename + ".config"
             
        # Read the CSV file line by line and write into data file
        with open(csv_filename, "r") as csv_file, open(text_filename, "w") as outfile:
            csv_reader = csv.reader(csv_file)
            numRecords = 0

            for line in csv_file:
                # Read and write each record
                csv_reader = csv.reader([line])
                id, state, city, name = self.__readCSV(csv_reader)
                self.writeRecord(outfile, id, state, city, name)
                numRecords += 1

        # Store the number of records
        self.numRecords = numRecords

        # Write the configuration file
        with open(config_filename, "w") as config_file:
            config_file.write(f"numRecords={self.numRecords}\n")
            config_file.write(f"recordSize={self.recordSize}\n")
            config_file.write("fields=ID:10,State:20,City:20,Name:50\n")

    # #read the database
    def open(self, filename):
        self.filestream = filename + ".data"
        
        if not os.path.isfile(self.filestream):
            print(str(self.filestream)+" not found")
        else:
            self.text_filename = open(self.filestream, 'r+')
            self.numRecords = 10
            self.recordSize = 71

    def readRecord(self, recordNum, id, experience, marriage, wage, industry):
        status = False

        if 0 <= recordNum < self.numRecords:
            self.text_filename.seek(recordNum * self.recordSize)
            line = self.text_filename.readline().rstrip('\n')
            id[0] = line[:10].strip()
            experience[0] = line[10:15].strip()
            marriage[0] = line[15:20].strip()
            wage[0] = line[20:40].strip()
            industry[0] = line[40:70].strip()
            status = True
            
        return status

    #overwrite record method
    def overwriteRecord(self, record_num, record_id, experience, married, wage, industry):
        try:
            # Calculate the byte offset of the record
            offset = record_num * self.recordSize

            # Move to the beginning of the specified record
            self.text_filename.seek(offset)

            # Call writeRecord to output the passed-in parameters
            self.writeRecord(self.text_filename, record_id, experience, married, wage, industry)
            return True
        except IOError:
            return False


    def binarySearch(self, id, experience, marriage, wage, industry):

        low = 0
        high = self.numRecords - 1
        self.found = False
        failure = False

        target_id = id[0]  # Do not strip leading zeros

        while not self.found and high >= low and not failure:
            self.middle = (low + high) // 2
            try:
                temp_id = [None]  # Use a list to hold the ID read from the record
                self.readRecord(self.middle, temp_id, experience, marriage, wage, industry)
            except Exception as e:
                failure = True
                break

            mid_id = temp_id[0]  # Do not strip leading zeros


            if mid_id == target_id:
                self.found = True
                # print("Record found at record number: ", self.middle)
            elif mid_id < target_id:
                low = self.middle + 1
            else:
                high = self.middle - 1

        return self.found


    #close the database
    def close(self):
        self.text_filename.close()

# main methods from menu: 

    def open_database(self):
        print("Opening database")

    def close_database(self):
        print("Closing database")

    def display_record(self):
        print("Displaying record")

    def update_record(self):
        print("Updating record")

    def create_report(self):
        print("Creating report")

    def add_record(self):
        print("Adding record")

    def delete_record(self): 
        print("Deleting record")

