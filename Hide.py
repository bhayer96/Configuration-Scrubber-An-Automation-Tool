# User interactive program that hides sensitive material in a configuration.
class Hide:

	def __init__(self): # Constructor
		valid = 0
		while valid == 0: # Keep asking for a file name until an existing config is entered
			try:
				self.filename = self.fileName() # Gets the name for the config that needs to
											 	# have its content hidden.
				self.filetxt = open(self.filename, 'r') # Read mode
				valid = 1 # File found
			except IOError: # File not found
				print("\nConfiguration does not exist in current directory.")
		self.copyList = [] # Will be used to store lines and to update changes made.
						   # It is used as a sort of temporary line editor.
		self.menu() # Intiate user menu.

	def menu(self):
		quit = 0
		while quit == 0: # Continue until user decides to quit.
			print("\nType in data type to scrub or an action to complete using the menu below:\n\n"
				+ "Description:		de		IP Address:		ad\n"
				+ "Key-string:		ks		Password:		pw\n"
				+ "Snmp-server:		ss		Display original:	do\n"
				+ "Display scrubbed:	ds		Quit:			qu\n"
				)
			choice = raw_input('>>   ') # Need to use raw_input with Python 2

			if choice == "de":
				self.readFile("description")
			elif choice == "ad":
				self.readFile("ip address")
			elif choice == "ks":
				self.readFile("key-string")
			elif choice == "ss":
				self.readFile("snmp-server")
			elif choice == "pw":
				self.readFile("password")
			elif choice == "do":
				print("\nDisplaying original configuration: ")
				self.filetxt.seek(0)
				print("\n" + self.filetxt.read())
				print("Configuration done.")
			elif choice == "ds":
				try: # Check to see if a scrubbed file has been created
					hidden = open("Scrubbed_"+ self.filename, 'r')
					print("\nDisplaying scrubbed configuration: ")
					print("\n" + hidden.read())
					print("Configuration done.")
					hidden.close()
				except IOError:
					print("\nScrubbed configuration file has not been created yet so cannot display.")
			elif choice == "qu":
				print("\nQuitting program...\n")
				self.filetxt.close()
				return
			else:
				print("\nChoice is not a part of the menu. Try again!")

	def fileName(self): # Used to get config file name from user.
		print("\nPlease enter file name, including the file extension.")
		filename = raw_input(">>   ")
		return filename

	def readFile(self, word):
		i = 0

		# Open or create a file to write content of config file, with hidden revisions
		hidden = open("Scrubbed_"+ self.filename, 'w')

		newLine = " "
		if not self.copyList: # If copyList is empty, that means this is the first time
							  # readFile is being called and there is a special case
							  # for that.

			self.filetxt.seek(0) # Starts at the first byte (byte 0) in the file
			for line in (self.filetxt): # Since this is the first call, read from original
										# config file.
				if word in line: # Look for key phrase
					if word == "ip address": # Special case for IP add. since counter is
											 # needed.
						i += 1
						newLine = "IP " + str(i) + "\n" # Make a hidden IP address.
					else:
						newLine = "** " + word + " removed **\n" # Hide content of line.
					hidden.write(newLine) # Write altered line to the hidden config file.
					self.copyList.append(newLine) # Also add this line to the copyList list
												  # to make keeping track of which lines are
												  # changed easier in the future calls.
				else: # No changes need to be made to the line.
					self.copyList.append(line)
					hidden.write(line)
			print("\nNAME OF NEW SCRUBBED FILE IS: " + "Scrubbed_"+ self.filename)
		else: # Not first call to readFile.
			for e in range(len(self.copyList)): # Iterate through copyList to copy and
												# change lines.
				if word in self.copyList[e]:
					if word == "ip address":
						i += 1 # Keeps track of how many IP addresses have been changed.
						newLine = "IP " + str(i) + "\n"
					else:
						newLine = "** " + word + " removed **\n"
					hidden.write(newLine)
					self.copyList[e] = newLine # Update in the list that this line has been changed
											   # so that the change is not lost in the next call.
				else:
						hidden.write(self.copyList[e]) # No changes need to be made so use
													   # what's stored in the list.
		hidden.close()

hideConfig = Hide() # Creates an instance of the class to begin the program.
