"""
Provides utility functions for handler/taskrunner level code to provide consistent
behavior across different taskrunners and reduce code repetition of similar tasks.
"""

import sys
import os
import shutil
import subprocess
import base64
import simplejson


def cleanup(logger=None, directory=None):
    """
    Clean up after the job.  At the moment this just means removing the working
    directory, but later could mean other things.
    """
    
    try:
        shutil.rmtree(directory, ignore_errors=True) # it would not delete if fold is not empty
        # need to iterate each entry
    except IOError, e:
        logger.error("Unable to remove working directory {0}".format(directory))
        raise


def setupWorkingDir(logger=None,directory=None):
    """
	Clean up an existing workingdir and create a new one
    """
    try:
    	if os.path.exists(directory): cleanup(logger,directory)
	os.makedirs(directory)
    except IOError, e:
	logger.error("Unable to setup working dir {0}".format(directory))
	raise

def gen_recursive_filelist(d):
    """
    Generate a list of all files present below a given directory.
    """
    
    for root, directories, files in os.walk(d):
        for file in files:
            yield os.path.join(root, file)

def get_dir(d):
    """
    Generate a list of all files present below a given directory.
    """
    
    dirs = [os.path.join(d,o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
    if len(dirs) > 1:
    	return dirs[0]
    else:
	return None
    #for directories, files in os.walk(d):
    #    return os.path(directories)

def get_file_with_suffix(d,suffix):
    """
    Generate a list of all files present below a given directory.
    """

    items = os.listdir(d)
    for file in items:
            if file.endswith(suffix):
		return file.split(suffix)[0]
    return None

def optimize_parallel_run(num_samples,num_threads,num_cores):
    """
    Optimizes the pool_size and the number of threads for any parallel operation
    """
    if num_samples * num_threads < num_cores:
	while num_samples * num_threads < num_cores:
		num_threads = num_threads + 1
      		continue 
	pool_size = num_samples
	return (pool_size , num_samples)
    elif num_samples * num_threads == num_cores:
	if num_threads == 1:
 	   num_threads = 2 
           pool_size = round(num_samples/num_threads)
	return (pool_size, num_threads)
    elif num_samples * num_threads > num_cores:		   
    	while num_samples * num_threads > num_cores:
		num_threads = 2
		num_samples = num_samples - 1 
		continue
	pool_size = num_samples
	return (pool_size, num_threads)

