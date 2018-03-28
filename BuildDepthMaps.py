import PhotoScan, glob, sys, time

# BuildDepthMaps.py
# Justin Dowd, Clemson Center for Geospatial Technologies, www.clemsongis.org
# March 2018 
# Email: jmdowd@g.clemson.edu
# Scripts submits a task that builds the depth maps in our previously created project

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

# Skips over the next three lines of arguments.txt as they are not needed for this script
blank1 = argumentFile.readline()
blank2 = argumentFile.readline()
blank3 = argumentFile.readline()
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
# Open the document that was previously created by MatchPhotos.py using the filePath variable we created
doc.open(filePath)
# Set the read only variable to false in order to enable editing
doc.read_only = False

# Task 3 or Build Depth Maps Task
# Create a PhotoScan Network Task object called 'task3'    
task3 = PhotoScan.NetworkTask()
# Add all the chunks and frames(if applicable) to the network task so it has access to them
for c in doc.chunks:
        task3.chunks.append(c.key)
        task3.frames.append((c.key,0))
# Names the task
task3.name = "BuildDepthMaps"
# Applies the task to the chunks we added to the task  
task3.params['apply'] = task3.chunks
# Set the processing quality to Ultra, which is the highest quality for PhotoScan
task3.params['downscale'] = int(PhotoScan.UltraQuality)
# Set filtering to not filter 
task3.params['filter'] = int(PhotoScan.FilterMode.NoFiltering)
# Tells the task not to look for previously created depth maps since this task is creating the first one for the project
task3.params['reuse_depth'] = False
# Grants the task permission to distribute the processing onto our client
task3.params['network_distribute'] = True

# Connect to the IP Address of the PhotoScan server node we read in from address.txt
client.connect(addr_str)
# Create a batch to submit to the server node
batch_id3 = client.createBatch(filePath, [task3])

# Send the batch to the server node for processing
client.resumeBatch(batch_id3)
print("Job started...")
print("Building Depth Maps...")

# Get the current status dictionary of the batch
stat = client.batchStatus(batch_id3)
# Print the status from the dictionary
print("Status: " + stat['status'])
# Continue to the run the script until the processing step has finished
while(stat['status'] == "inprogress" or stat['status'] == "working"):
        stat = client.batchStatus(batch_id3)
		# Makes the loop sleep for 5 minutes before checking the status again
		# This is done to conserve memory as this step can take up large amounts of time and if
		# the loop is constantly checking for the status and assigning the status to a variable
		# the job on the Palmetto Cluster will eventually run out of memory and corrupt the project
        time.sleep(500)
		
# Disconnect from the client and Save the project (Save is equivalent to a 'Save As' on windows
client.disconnect()
print("Depth Maps Built")

doc.save(filePath)

