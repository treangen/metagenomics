import json
import subprocess
from shutil import copyfile
import urllib.request
from urllib.parse import urlparse
import os
import sys
import argparse
import time
from socket import error as SocketError
from snakemake.io import expand

workflows=['read_filtering', 'test_files', 'assembly', 'comparison', 'sourmash', 'kaiju', 'taxonomic_classification', 'functional_inference', 'all']  #keep all at the end of the list

def reporthook(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration))
    percent = min(int(count*block_size*100/total_size),100)
    sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed" %
                    (percent, progress_size / (1024 * 1024), speed, duration))
    sys.stdout.flush()
    
def download_file(workflow, data, install_dir):
    if workflow in data.keys():
        for file_name, url_string in data[workflow].items():
            try:
                url = urlparse(url_string)
            except Exception as e:  #we don't care since some of the JSONS are not URL's
                pass
            if (file_name == 'sbttar'):     #sourmash files from the taxonomic classification workflow.
                tar_file = data[workflow]['sbttar']
                db = data[workflow]['databases']
                kv = data[workflow]['kvalue']
                sbturl = data[workflow]['sbturl']
                sourmash_files = expand(tar_file, database=db, kvalue=kv)
                for file in sourmash_files:
                    if not (os.path.isfile(install_dir+"/"+file)):
                        print("\nDownloading " + file +" from " +sbturl)
                        try:
                            urllib.request.urlretrieve("http://" +sbturl + '/' +file, install_dir +"/" +file, reporthook)
                        except SocketError as e:
                            print("Error downloading file " + file + "Retry script.")
                            print(e)
                            try:
                                os.remove(install_dir+ "/"+file)
                            except OSError:
                                pass
            elif (url.scheme == "http" or url.scheme == "https"):      #download via http
                if not (os.path.isfile(os.path.join(install_dir, file_name))):
                    print("Downloading " +file_name + " from " + url_string)
                    try:
                        urllib.request.urlretrieve(url_string, install_dir+ "/"+file_name, reporthook)
                    except SocketError as e:
                        print("Error downloading file " + file_name + " Retry script.")
                        print(e)
                        try:
                            os.remove(install_dir+ "/"+file_name)
                        except OSError:
                            pass
            elif (url.scheme == 'docker'):    #download singularity image
                if not (os.path.isfile("../container_images/"+file_name)):
                    print("Downloading singularity image " +file_name)
                    sing_command = "singularity pull "+url_string
                    subprocess.run([sing_command], shell=True)   #TODO: Error handling for sing pull
                    os.rename(file_name, "../container_images/"+file_name)  
            elif (url.scheme =="file"):         #copy file from local location
                if not (os.path.isfile(os.path.join(install_dir, file_name))):
                    print("Copying "+ file_name)
                    copyfile(".."+ url.path, install_dir+ "/"+ file_name)
                        
                         
    
def main_func(user_input, install_dir, file_list='config/offline_downloads.json'):   
    try:
        with open(file_list)as f:
            data = json.load(f)
    except IOError:
        print("Error: offline_downloads.json is missing. Exiting")
        sys.exit(1)
         
    try:
        if not os.path.isdir("data"):
            os.mkdir("data")
    except IOError:
        print("Error: can't create data directory")     
    if ('all' in user_input):
        user_input = workflows[0:-1]
        for workflow in user_input:     
            download_file(workflow, data, install_dir)
    else:
        for workflow in user_input:
            download_file(workflow, data, install_dir)
        
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script to download data required for offline processing of Dahak software. Requires config/offline_downloads.json")
    parser.add_argument("--workflow", nargs='+', help="Download databases/images for inputed workflow", choices=workflows, type=str.lower, required=True)
    parser.add_argument("--data_dir", help="directory to copy non image files to", default="data")
    args = parser.parse_args()
    install_dir = args.data_dir
    user_input = args.workflow
    main_func(user_input, install_dir)
    



