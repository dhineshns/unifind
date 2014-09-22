import os
import paramiko
from os.path import basename
log_file = open("./log.txt",'a+')

def get_file_paths():
	try:
		file_name = "./today.txt"
		path_file = open(file_name, 'w+')
		os.system("mdfind -onlyin ~/.  'kMDItemLastUsedDate >= $time.today()' >> {}".format(file_name))
		paths = path_file.readlines()
		log_file.write("Paths found at " + __name__) 
	except Exception as e:
		log(e)
	finally:
		path_file.close()
	return paths


def copy_files(username, password, ip, port, dest_path, recent_files):
	try:
		t = paramiko.Transport((ip, port))
		t.start_client()
		t.auth_password(username=username, password=password)
		sftp = paramiko.SFTPClient.from_transport(t)
		for source_path in recent_files:
			sftp.put(source_path, dest_path+basename(source_path))
			print source_path + " copied"
		log_file.write("Files copied to remote at :" + __name__)
		return True
	except Exception as e:
		log(e)
	return False
def log(e):
		log_file.write("Exception caught at : " + str(e)+"\n")
		print ("Exception caught at : " + str(e))

def main():
	username = "root"
	password = "admin"
	ip = "192.168.0.8"
	port = 2222
	dest_path = "/sdcard/unifind/"
	recent_files = get_file_paths()
	for i in range(0,len(recent_files)):
		recent_files[i] = recent_files[i].rstrip()
	just_files = [source_path for source_path in recent_files if os.path.isfile(source_path)]
	success = copy_files(username, password, ip, port, dest_path, just_files)
	if success: print "All files copied"
	else: print "Error in copying"
if __name__=="__main__":
	main()

log_file.close()