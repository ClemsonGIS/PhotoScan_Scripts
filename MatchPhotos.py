import PhotoScan, glob, sys, time

# MatchPhotos.py
# Justin Dowd, Clemson Center for Geospatial Technologies, www.clemsongis.org
# March 2018 
# Email: jmdowd@g.clemson.edu
# Scripts creates the project and submits a task that matches all photos

#Create Command Line Argument Variable that reads arguments from the run command in submitAlignCameras.sh
args = sys.argv
# Open the argument file (arguments.txt)
argumentFile =open(args[1])

# Create a variable to hold the path to where the project will be saved and assign the first line
# of arguments.txt to this variable
path = argumentFile.readline()
# Strips the new line character at the end of the path name
path = path.strip('\n')
# Get the length of the path name 
pathLen = len(path)
# Checks to see if a forward slash is at the end of the path name, if not one is added
if(path[pathLen-1] != '/'):
        path = path + '/'

# Create a variable to hold the name of the project and assigns the second line of 
# arguments.txt to this variable
docName = argumentFile.readline()
# Strips the new line character at the end of the path name
docName = docName.strip('\n')
# Get the length of the path name 
docNameLen = len(docName)
# Removes the .psx extension from the project name if it exists
if('.psx' in docName):
    docName = docName.replace('.psx', '')
# Adds the .psx extension to the end of the project name to ensure it is in the right place
if('.psx' not in docName):
        docName = docName + '.psx'

# Creates a variable to store the name of the folder where the photos to be processed are and assigns the name to this variable
sourceFolder = argumentFile.readline()
# Strips the new line character at the end of the folder name
sourceFolder = sourceFolder.strip('\n')
# Creates a variable to hold the path to where the photos folder is located and assigns the path to this variable
sourceFolderPath = argumentFile.readline()
# Strips the new line character at the end of the folder name 
sourceFolderPath = sourceFolderPath.strip('\n')
# Gets the length of the path
sourceFolderPathLen = len(sourceFolderPath)
# Checks to see if a forward slash is at the end of the path name, if it isn't not one is added
if(sourceFolderPath[sourceFolderPathLen-1] != '/'):
    sourceFolderPath = sourceFolderPath + '/'
	# Combines the path currently stored in 'sourceFolderPath' with the name of the photos folder stored in 'sourceFolder'
	# the '*' character at the end will allow the later function to access all contents of the folder.
    sourceFolderPath = sourceFolderPath + sourceFolder + "/*"
else:
    sourceFolderPath = sourceFolderPath + sourceFolder + "/*"

# Skips over one line of the argument file because it is not needed for the script
blank = argumentFile.readline()
# Create a variable to store the path to where the address.txt file (file containing IP Address of server node) is stored.
addrDir = argumentFile.readline()
# Close the argument file
argumentFile.close()

# Strip new line character at the end of the path name
addrDir = addrDir.strip('\n')
# Combine the path with the name of the address folder containing the IP Address (address.txt) and store it in the variable (addrDir)
# It will always be named address.txt becuase that is the name designated in initServerNode2.sh
addrDir = (addrDir + "/address.txt")

# Opens the address file
addr_file = open(addrDir, "r")
# Reads the IP Address and stores it in a variable
addr_str = addr_file.readline()
# Closes the address file
addr_file.close()
# Create a PhotoScan Network Client object named 'client'
client = PhotoScan.NetworkClient()

# Combines the path to where the project is to be saved with the name of the project in order to save, open, and access the project in the script
filePath = (path + docName)
# Create a PhotoScan Document object and name it 'doc'
doc = PhotoScan.app.document
# Set the read only variable to false in order to enable editing
doc.read_only = False
# Creates the project because this is the first processing task to be done
doc.save(filePath)
# Add a chunk to the project
chunk = doc.addChunk()
# Create a list to store our photos
photos = []
# Using glob, grab all the photos from the photos folder and add them to the list
for photo in glob.glob(sourceFolderPath):
    photos.append(photo)

# Add all the photos from the list to the chunk
chunk.addPhotos(photos)

# Set the read only variable to false in order to enable editing
doc.read_only = False
# Saves the current state of the project
doc.save()


# Task 1 or Match Photos Task
# Create a PhotoScan Network Task object called 'task1'  
task1 = PhotoScan.NetworkTask()
# Add all the chunks and frames(if applicable) to the network task so it has access to them
for c in doc.chunks:
        task1.frames.append((c.key,0))
        task1.chunks.append(c.key)
        print(c)
        print("Added Chunk and Frame")
# Names the task
task1.name = "MatchPhotos"
# Sets the matching accuracy to the highest accuracy possible 
task1.params['downscale'] = int(PhotoScan.HighestAccuracy)
# Grants the task permission to distribute the processing onto our client
task1.params['network_distribute'] = True

# Connect to the IP Address of the PhotoScan server node we read in from address.txt
client.connect(addr_str)
# Create a batch to submit to the server node
batch_id1 = client.createBatch(filePath, [task1])

# Send the batch to the server node for processing
client.resumeBatch(batch_id1)
print("Job started...")
print("Matching Photos...")

# Get the current status dictionary of the batch
stat = client.batchStatus(batch_id1)
# Print the status from the dictionary
print("Status: " + stat['status'])
# Continue to the run the script until the processing step has finished
while(stat['status'] == "inprogress" or stat['status'] == "working" or stat['status'] == 'pending'):
        stat = client.batchStatus(batch_id1)
		# Makes the loop sleep for 5 minutes before checking the status again
		# This is done to conserve memory as this step can take up large amounts of time and if
		# the loop is constantly checking for the status and assigning the status to a variable
		# the job on the Palmetto Cluster will eventually run out of memory and corrupt the project
        time.sleep(180)

# Disconnect from the client and Save the project (Save is equivalent to a 'Save As' on windows
client.disconnect()
print("Photos Matched")

doc.save(filePath)

