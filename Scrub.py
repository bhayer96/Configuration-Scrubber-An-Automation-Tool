# User interactive program that hides sensitive material in a configuration. This
# material includes: description, IP address, key-string, password, and snmp-server.
# Scrub automates the process of manually scrubbing data, line by line, file by file.
class Scrub:

	# Class constructor that retrieves configuration text file and intializes
	# instance variables. Once this is down, the constructor calls the menu()
	# method to start the process of scrubbing.
	def __init__(self):
		valid = 0 # Variable that is used to tell the program if a valid congig
				  # file has been found. 0 means not found and 1 means found.
		while valid == 0: # Keep asking for a file name until an existing config
						  # is entered
			try:
				self.filename = self.fileName() # Gets the name for the config that
											 	# needs to have its contents hidden.
				self.filetxt = open(self.filename, 'r') # Read mode
				valid = 1 # File found
			except IOError: # File not found so restart loop
				print("\nConfiguration does not exist in current directory.")
		self.copyList = [] # Will be used to store lines and to update changes made.
						   # It is used as a sort of temporary line editor that
						   # will have its contents writtne to an output file.
		self.IPs = {} # Dictionary of IP addresses mapped to IP placeholders.
		self.ipNum = 0 # Number of distint IP addresses found so far.
		self.menu() # Start the menu.

	# Defines a user interactive menu that takes in the user's choice of scrubbable
	# data. Once a choice has been  made, it is removed from the next run
	# of the menu to provide visibility into what has been already removed. Based
	# on the user's choice, the appropriate data is removed by calling readFile().
	def menu(self):
		quit = 0
		userMenu = ["Description:		de", "IP Address:		ip",
					"Key-string:		ks", "Password:		pw",
					"Snmp-server:		ss", "Display original:	do",
					"Display scrubbed:	ds", "Quit:			qu\n"]
		while quit == 0: # Continue until user decides to quit (when quit = 1).
			print("\nType in data type to scrub or an action to complete using "
				  + "the menu below:\n")

			for data in userMenu: # Prints out the user menu to the terminal session.
				if data == "": # This means this choice was already made so skip it.
					continue
				else:
					print(data)
			choice = raw_input('>>   ') # Need to use raw_input with Python 2

			if choice == "de":
				if (userMenu[0]== ""): # Let the user know that choices aleady made
									   # cannot be remade.
					print("\nDescriptions were already removed!")
				else:
					userMenu[0] = "" # Change description's location in the menu
									 # list to empty since the choice has now been
									 # selected.
					self.readFile("description") # readFile() removes all lines
												 # with an instance of the parameter
												 # passes in.
			elif choice == "ip": # Same concept as removing description.
				if (userMenu[1]== ""):
					print("\nIP addresses were already removed!")
				else:
					userMenu[1] = ""
					self.readFile("ip address")
			elif choice == "ks":
				if (userMenu[2]== ""):
					print("\nKey-strings were already removed!")
				else:
					userMenu[2] = ""
					self.readFile("key-string")
			elif choice == "ss":
				if (userMenu[4]== ""):
					print("\nSnmp-servers were already removed!")
				else:
					userMenu[4] = ""
					self.readFile("snmp-server")
			elif choice == "pw":
				if (userMenu[3]== ""):
					print("\nPasswords were already removed!")
				else:
					userMenu[3] = ""
					self.readFile("password")
			elif choice == "do": # Display original configuration to terminal session.
				print("\nDisplaying original configuration: ")
				self.filetxt.seek(0) # Put "cursor" at first byte in file.
				print("\n" + self.filetxt.read())
				print("Configuration done.")
			elif choice == "ds": # Displays the current scrubbed file.
				try: # Check to see if a scrubbed file has been created
					hidden = open("Scrubbed_"+ self.filename, 'r')
					print("\nDisplaying scrubbed configuration: ")
					print("\n" + hidden.read())
					print("Configuration done.")
					hidden.close()
				except IOError: # Catch the raised exception and let the user know
								# of the problem.
					print("\nScrubbed configuration file has not been created "
						+ "yet so cannot display.")
			elif choice == "qu": # Quit
				if (userMenu[1]== ""):
					self.writeIP() # Map the IP placeholders to IP addresses if
								   # IP addresses have been scrubbed.
					print("\nIP mapping has been written to file with the name: " +
					  	  "IP_Mapping_" + self.filename + "\n")
				print("\nQuitting program...\n")
				self.filetxt.close()
				return
			else: # The user entered something that wasn't part of the menu.
				print("\nChoice is not a part of the menu. Try again!")

	# Retrieves the filename of the configuration and returns the string.
	def fileName(self): # Used to get config file name from user.
		print("\nPlease enter file name, including the file extension.")
		filename = raw_input(">>   ")
		return filename

	# Uses the dictionary of IP placeholders (keys)	and IP address (value) to map
	# the key-value pairs into a separate IP output file.
	def writeIP(self):
		ipFile = open("IP_Mapping_" + self.filename, 'w') # Create file with this name.
		ipFile.write("The IP address placeholders have been mapped to their " +
					 "specific IP addresses below.\n\n")

		# Before looping, sort the dictionary since Python dictionaries do not have
		# any order so entries are inserted at a certain function based on a hash.
		# Loop through the sorted result to write each pair to a file.
		for key, value in sorted(self.IPs.items()):
			ipFile.write(key + ": " + value)

	# Creates a scrubbed file that is cleared and reopened with each scrub. The
	# method accepts a word (string type) parameter. This parameter is the type
	# of data that the user wishes to remove (description, key-string, etc.). There
	# is a special case for the first call since the contents of the config file
	# need to be copied over to copyList because the original cannot be changed.
	# This method saves memory usage.
	def readFile(self, word):
		# Open or create a file to write content of config file, with hidden revisions
		hidden = open("Scrubbed_"+ self.filename, 'w')

		newLine = " "
		if not self.copyList: # If copyList is empty, that means this is the first
							  # time readFile is being called so copy contents,
							  # while making the first scrub.

			self.filetxt.seek(0) # Starts at the first byte (byte 0) in the file
			for line in (self.filetxt): # Since this is the first call, read from
										# original config file.
				if "no ip address" in line: # This line contains "ip address", but
											# it does not need to be changed.
					self.copyList.append(line)
					hidden.write(line) # Copy as in.
				elif word in line: # Check to see if key-phrase is in the line.

					# Special case for IP address since the program needs to keep
					# track of how many distinct addresses there are and store them
					# in the dictionary.
					if word == "ip address":
						value = line.split("ip address ")[1] # Retrieves the address.
						key = ""
						if value not in self.IPs.values(): # A distinct IP address found.
							self.ipNum += 1 # Icrement number of distint addresses.
							key = "IP " + str(self.ipNum) # Placeholder, or key, (i.e. IP 1)
							self.IPs[key] = value  # Add pair to the dictionary.
						else: # Not a distinct IP address.
							for k in self.IPs: # Iterate until the appropriate
											   # pair is found.
								if self.IPs[k] == value: # The pair has been found.
									key  = k
									break
						newLine = "**** " + key + " REMOVED ****\n"
					else: # Scrub data by changing the line to the string below.
						newLine = "**** " + word.upper() + " REMOVED ****\n"
					hidden.write(newLine) # Write altered line to the hidden config file.
					self.copyList.append(newLine) # Also add this line to copyList
												  # to make keeping track of which lines are
												  # changed easier in the future calls.
				else: # The line did not contain a key phrase so add as is.
					self.copyList.append(line)
					hidden.write(line)
			print("\nNAME OF NEW SCRUBBED FILE IS: " + "Scrubbed_"+ self.filename)
		else: # Not first call to readFile.

			# Iterate through copyList to copy and change lines. Works same way
			# as the first call loop does, except instead of reading line by line
			# from a file, the loop is reading element by element in the list.
			for e in range(len(self.copyList)):
				if "no ip address" in self.copyList[e]:
					hidden.write(self.copyList[e]) # No changes need to be made so use
												   # what's stored in the list.
				elif word in self.copyList[e]: # Look for key phrase in the line.
					if word == "ip address": # Special case for IP add. since counter is
											 # needed.
						value = (self.copyList[e]).split("ip address ")[1]
						key = ""
						if value not in self.IPs.values(): # A distinct IP address found
							self.ipNum += 1
							key = "IP " + str(self.ipNum)
							self.IPs[key] = value
						else:
							for k in self.IPs:
								if self.IPs[k] == value:
									key  = k
									break
						newLine = "**** " + key + " REMOVED ****\n"

					else:
						newLine = "**** " + word.upper() + " REMOVED ****\n"
					hidden.write(newLine) # Write altered line to the hidden config file.
					self.copyList[e] = newLine # Update in the list that this line has been changed
											   # so that the change is not lost in the next call.
				else:
						hidden.write(self.copyList[e]) # No changes need to be made so use
													   # what's stored in the list.

		hidden.close() # Close file before leaving method call.

hideConfig = Scrub() # Creates an instance of the class to begin the program.
