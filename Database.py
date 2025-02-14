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
        #self.overwrite = False    

    def __readCSV(self, csv_reader):
        # read and parse a line of the csv file. 
        try:
            row = next(csv_reader)
            id = row[0]
            state = row[1]
            city = row[2]
            name = row[3]
        # Display the contents of each record to the screen to test that you are reading it properly.
            #print(f"ID: {id}, State: {state}, City: {city}, Name: {name}")
            return id, state, city, name
        except StopIteration:
            return None
        
    def getRecord(self):
        pass

    def find(self):
        pass
        
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
            #if self.overwrite:
                #print(f"Updated record is ID: {id}, State: {state}, City: {city}, Name: {name}")
            return True
        except IOError:
            return False
        
    # delete record method
    def deleteRecord(self):
        pass

    # create database
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

    # Open the database
    def open(self, filename):
        self.filestream = filename + ".data"
        self.configstream = filename + ".config"

        if self.openFlag == True:
            print("A database is already open")
            return

        try:
            # Open the configuration file to read numRecords and recordSize
            with open(self.configstream, "r") as config_file:
                for line in config_file:
                    if line.startswith("numRecords="):
                        self.numRecords = int(line.split("=")[1].strip())
                    elif line.startswith("recordSize="):
                        self.recordSize = int(line.split("=")[1].strip())
                print(f"Number of records: {self.numRecords}")
                print(f"Record size: {self.recordSize}")

            # Open the data file in read/write mode
            self.dataFileptr = open(self.filestream, 'r+')
            self.openFlag = True
        except FileNotFoundError:
            print(f"{self.filestream} not found")
            self.openFlag = False
        except Exception as e:
            print(f"An error occurred: {e}")
            self.openFlag = False

    # Read a record from the database
    def readRecord(self, recordNum, id, state, city, name):
        if not self.openFlag:
            print("Database is not open")
            return -1  # Data file is not open

        if recordNum < 0 or recordNum >= self.numRecords:
            print("Invalid record number")
            return -1  # other fail reasons

        try:
            self.dataFileptr.seek(recordNum * self.recordSize)
            line = self.dataFileptr.readline().rstrip('\n')
            if not line.strip():  # Check if the record is empty
                print("Record is empty")
                return 0
            id[0] = line[:10].strip()
            state[0] = line[10:30].strip()
            city[0] = line[30:50].strip()
            name[0] = line[50:100].strip()
            # print(f"ID: {id[0]}, State: {state[0]}, City: {city[0]}, Name: {name[0]}") 
            return 1
        except Exception as e:
            print(f"An error occurred: {e}")
            return -1
        

    #overwrite record method
    def overwriteRecord(self, record_num, id, state, city, name):
        try:
            # Calculate the byte offset of the record
            offset = record_num * self.recordSize

            # Move to the beginning of the specified record
            self.dataFileptr.seek(offset)

            # Call writeRecord to output the passed-in parameters
            self.writeRecord(self.dataFileptr, id, state, city, name)
            return True
        except IOError:
            return False

    # binary search that finds record based on id
    def binarySearch(self, id, state, city, name):

        low = 0
        high = self.numRecords - 1
        self.found = False
        failure = False

        target_id = id  # Do not strip leading zeros
        #print(target_id)

        while not self.found and high >= low and not failure:
            self.middle = (low + high) // 2
            try:
                temp_id = [None]  # Use a list to hold the ID read from the record
                self.readRecord(self.middle, temp_id, state, city, name)
            except Exception as e:
                failure = True
                break

            mid_id = temp_id[0]  # Do not strip leading zeros
            #print(mid_id)


            if mid_id == target_id:
                self.found = True
                # print("Record found at record number: ", self.middle)
            elif mid_id < target_id:
                low = self.middle + 1
            else:
                high = self.middle - 1

        #print(self.found)

        return self.found


    #close the database
    def close(self):
        if not self.openFlag:
            print("No database open.")
            return
        self.numRecords = 0 #reset instance vars
        self.recordSize = 0
        #self.text_filename.close() # close file
        if self.dataFileptr:
            self.dataFileptr.close()
        self.dataFileptr = None
        self.openFlag = False
        print("Database closed successfully.")

# main methods from menu: 

    def close_database(self):
        print("Closing database...")
        self.close()

    # don't need anymore, tester function 
    def read_record(self):
        #print("Reading record")
        id = [""]
        state = [""]
        city = [""]
        name = [""]
        recordNumber = input("Which record would you like to read? ") 
        recordNumber = int(recordNumber)
        tester = self.readRecord(recordNumber, id, state, city, name)
        if tester == 1:
            print(f"ID: {id[0]}, State: {state[0]}, City: {city[0]}, Name: {name[0]}")

    def display_record(self):
        print("Displaying record")
        id = input("Display complete record for which ID? ")
        state = [""]
        city = [""]
        name = [""]
        status = self.binarySearch(id, state, city, name)
        if status:
            print(f"ID: {id}, State: {state[0]}, City: {city[0]}, Name: {name[0]}")
        else:
            print("Record not found")


    def update_record(self):
        #print("Updating record")
        id = input("Enter ID of record to update: ")
        state = [""]
        city = [""]
        name = [""]
        status = self.binarySearch(id, state, city, name)
        if status:
            #self.overwrite = True
            print(f"ID: {id}, State: {state[0]}, City: {city[0]}, Name: {name[0]}")
            print(f"Do you want to change the state, city, or name of the record?")
            choice = input("Enter choice (state/city/name): ")
            if choice == "state":
                new_state = input("Enter new state: ")
                self.overwriteRecord(self.middle, id, new_state, city[0], name[0])
            elif choice == "city":
                new_city = input("Enter new city: ")
                self.overwriteRecord(self.middle, id, state[0], new_city, name[0])
            elif choice == "name":
                new_name = input("Enter new name: ")
                self.overwriteRecord(self.middle, id, state[0], city[0], new_name)
            else:
                print("Invalid choice")
        else:
            print("Record not found")
        #self.overwrite = False


    def create_report(self):
        print("Creating report...")
        id = [""]
        state = [""]
        city = [""]
        name = [""]
        for recordNumber in range(10):
            self.readRecord(recordNumber, id, state, city, name)
            print(f"ID: {id[0]}, State: {state[0]}, City: {city[0]}, Name: {name[0]}")

    #bonus
    def add_record(self):
        print("Adding record")
        print("Just kidding. This is not implemented yet.")


    def delete_record(self): 
        #print("Deleting record")
        id = input("Input record ID to delete:")
        state = [""]
        city = [""]
        name = [""]
        status = self.binarySearch(id, state, city, name)
        if status:
            state = ""
            city = ""
            name = ""
            self.overwriteRecord(self.middle, id, state, city, name)
        else:
            print("Record not found")
