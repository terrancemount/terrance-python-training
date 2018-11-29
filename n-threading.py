#!/usr/bin/env python3

'''
Topic Title: Threads

**John**
Concept: A thread, similar to Java, is a separate line of execution that runs 
at the same time as the main thread and any other currently running threads.

In Python, threading is useful to run programs concurrently, especially when you need 
to run IO tasks in parallel.  Multithreading has the benefits of sharing the 
same memory space and therefore can communicate and share info with each other 
unlike processes. For the most part, threading in Python is similar to threading 
in Java. A difference is Python will only use one core of a CPU, Java will use 
multiple cores. This means Python will only run one one thread's code at a time 
(Python is effectively single threaded). To get around this, you will want to 
use fork(), which creates a new process instead of a new thread.


Notes (Some details)

****************************************************************************

**Terrance**
_thread Module

- Simplest way to start a thread is to use _thread module.  This module is a
lightweight and fast way to start a thread with just a function definition.
You do not need a class to use _thread.

In a try / except block then call 
	_thread.start_new_thread( function, (args))

*function is the function you have and args is the args for that function.

Functionality of this is very limited compared to the threading module.
You can't control the thread once created.  You can't stop the calling
thread and wait until called thread has finished i.e. join() funciton in
Threading module. 

*****************************************************************************
**All**
- Threading Module Functions (modules are like libraries in java)

	- active_count(): returns the number of threads currently alive
        - current_thread(): returns the current Thread object
       
	 - get_ident(): return the 'thread identifier' of the current thread,
		 	which is a non-zero integer
        
		-"Its value has no direct meaning: it is intended as a magic 
			cookie to be used to index a dictionary
                	of thread-specific data" -Python documentation
        
	- enumerate(): Return a list of all Thread objects currently alive 
		(like active_count(), but returns the actual objects)
        
	- main_thread(): return the main Thread object
        
	- settrace(function): set a trace function for all threads spawned from the threading module
		- *A trace function is used for Logging*
        
	- setprofile(): set a profile function for all threads spawned from the threading module
        	- Gives information about the thread (e.g. how long it has been running)
       
	 - stack_size([size]): set how much space the thread will take on the stack
        	- [size] is optional. If not included, defaults to 0. 
			If included, must be either 0, or >32,768
                
		- size should be a multiple of the page size for the system (commonly 4KiB)
                        
        ----------------------------------------------------------------------------------
        
	**Terrance**
	Synchronization functions
	- threading.Lock() gets a reference to the locking primative.  Call normally in global
		scope and stored in a reference.  The referecne is then used to aquire and 
		release functions listed below.

        - aquire() aquires a lock on the code until it is ether released or until the 
        	end of the function.
        - release() release the aquire lock on the function.
	
	
**Avery**   
- Thread Object 
	- start(): Same as Java's start(), splits execution and starts the thread
        - run(): define what the thread is going to do once it's started
        - join(): A thread calls another thread's join(), which stops the calling thread 
		until the called thread terminates. Once the called thread terminates, 
		the calling thread continues. Useful to stop the main thread from terminating 
		while other threads are still executing (call join on each thread in main)
        
	- getName() and setName()
        	- Threads are not unique, initial name is set in the constructor
        
	- is_alive(): return True if the thread is alive, False if it's not
        	- Mostly used from another thread, since a dead thread can't call is_alive()
        
	- isDaemon() and setDaemon(): isDaemon() returns True if the thread is a daemon, 
		False if not setDaemon() sets whether a thread is a daemon or not
        	
		*** getters and setters for name and daemon are deprecated, 
		can just use name and daemon directly
============================================================================================                        
Use case (Why would you use it):
  
  **Examples:
  	Client / Server tasks.  Create a new thread for each client connected to the
        server for proccessing.
        
        IO tasks -
		-make mulitple SQl requests and receive responses
		-reads from the harddrive.  
	
	Theroetical example:
		
		-> 10 second server request latency.(takes 10 seconds to get a response)
		
		-> 1 second to process the response

		-> 10 requests are made then how long, sequential vs  paralell?

			-> sequential (no threading)
				-> 10 requests * 10 seconds latency + 10 seconds processing
					= 110 seconds.
			
			-> paralell (using threads, single core)
				-> 10 second latency + 10 second proccessing
					= 20 seconds.
  
		-> Paralell has a massive decrease in time over sequential because the 
			process is not waiting for the response.
  	
============================================================================================	
Online Resources (URLs):

Offical thread documentation (difficult to start learning)
https://docs.python.org/3.6/library/threading.html

Tutorialspoint has good starting examples
https://www.tutorialspoint.com/python3/python_multithreading.htm



Authors:
- Avery Ehnis
- John Steele
- Terrance Mount

'''

import _thread
import threading
import time
import random
def main():
	setup = None
#==================================================================================
	print('Starting simple _thread example')
	#Create a thread using _thread
	try:
		_thread.start_new_thread( print_simple_time, ("Simple-Thread-1", 2, ) )
		_thread.start_new_thread( print_simple_time, ("Simple-Thread-2", 4, ) )
	except:
		print("Error: unable to start thread")
#=================================================================================
	print('Start Thread module Async threads')

	#Example of asynchronous threads (starts 10 threads that sleep for a 
	##random amount of time between 1-10 seconds)
	threads = []
	for x in range(5):
		#Set the name for each thread to make it easier to distinguish
		myThread = MyThread(name = 'Thread-{}'.format(x+1))
		myThread.start()
		threads.append(myThread)
		time.sleep(.5)
        
	#Joins the main thread with all of the asynchronous threads, 
	##pauses main until all threads are finished
	for t in threads:
		t.join()

	print('All Async threads have ended')
#===============================================================================
	print('Create sync threads')

	#clears out all the previous threads
	threads.clear()

	index = 0
	for x in range(5):
		index += 1
		myThread = SynchroThread(index, "Thread-" + str(index), 1)
		myThread.start()
		threads.append(myThread)

	for t in threads:
		t.join()

threadLock = threading.Lock()
#==============================================================================
#Class that extends the Thread class in the threading module
class MyThread(threading.Thread):
	#When the thread starts, it runs automatically
	#This run method overrides the run in Thread, threads just sleep
	def run(self):
		print('{} started'.format(self.getName()))
		time.sleep(random.randint(1,11))
		print('{} ended'.format(self.getName()))

#=============================================================================
#define a simple function to use with the _thread example
def print_simple_time( threadName, delay):
	count = 0
	while count < 3:
		time.sleep(delay)
		count += 1
		print ("%s: %s" % ( threadName, time.ctime(time.time()) ))
#=============================================================================
class SynchroThread (threading.Thread):
	def __init__(self, threadID, name, counter):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
	def run(self):
		print ("Starting " + self.name)
      		# Get lock to synchronize threads
		threadLock.acquire()
		print_synchro_time(self.name, self.counter, 3)
		# Free lock to release next thread
		threadLock.release()

def print_synchro_time(threadName, delay, counter):
	while counter:
		time.sleep(delay)
		print ("%s: %s" % (threadName, time.ctime(time.time())))
		counter -= 1
#==================================================================================
if __name__ == '__main__':
	main()
