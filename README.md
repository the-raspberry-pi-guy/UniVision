# UniVision - Hack Cambridge 4D Hackathon 2019

![alt text](https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/static/UniVision_logo.png)

# Video
https://www.youtube.com/watch?v=XtQeyhVP8pg&feature=youtu.be

# Overview
UniVision is a system that uses **cloud-based face identification** to accurately record and monitor the attendance of University students in lectures via a **video livestream**. Accessed over an easy-to-use **web interface**, our software uses a standard webcam and **Microsoft Azure web services** to determine people coming into a lecture theatre. Trained on only a small sample of images (no need for large sample sets), UniVision uses **Microsoft Azure's Face API** to quickly and efficently inform a lecturer as to whether a student is present in the class. In the background, an **SQL Azure database** stores a catalogue of students, their course information and timetables, amongst other information. Using our program, statistics like lecture attendance and other averages can be calculated and presented to the user.

# The Problem?
A fact that many students do not like to own up to is that attendance at lectures is critical to education success. In a first year "Intro to Linear Algebra" course at the University of Edinburgh, missing just 2 lectures brought an average student's final grade down by 20%. Missing more caused an even steeper decline, with students who were absent in 5-10 lectures passing at a rate of less than 50%. This is a clear problem, with much evidence elsewhere: https://scholar.google.co.uk/scholar?hl=en&as_sdt=0%2C5&q=lecture+attendance+and+exam+results&btnG=

# Our Solution
We set about trying to solve this problem by creating a much more reliable system of attendance, using cloud-based image recognition - trained on small sets of user-provided photos of students. This is faster than a Professor calling out a register, and more resilient to being "cheated". For example, using UniVision, it is not possible for one student to mark another present when they are not.

The principle behind our idea is for a camera to be mounted near the door to a lecture theatre. Before a lecture begins, the teacher can access our web interface and select which class they are about to teach. They can then press the "Start" button, which commences the video feed, and students can enter the room.

![alt text](https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/images/2.jpg)

When the web interface is started, the camera feed begins to stream information. This binary data is sent to the Microsoft Azure Face API, which we have pre-trained with a set of images for the students in a class. Due to the advanced nature of the Face API, only a small sample of user-uploaded images are required to train the database and identify people.

![alt text](https://github.com/the-raspberry-pi-guy/UniVision/blob/master/images/demo1.gif?raw=true)

We have then programmed the interface with Azure services and, after this stage, for each frame of video any identification is passed back to the program. When a student is recognised, their unique University number (Student ID) is stored in an SQL database, also hosted in the cloud using Azure web services. This data is linked to other fields and information, like student name, their prior attendance and courses they are studying.

![alt text](https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/images/database.png)

Meanwhile, at the front of the classroom, the teacher can monitor in real-time the students that are currently in their class. Before they start lecturing, they can disable the attendance by simply pressing "Stop".

We have also integrated many other advanced SQL-based features into our Python library, including providing an interface for teachers and students to see what courses they are taking, their attendance in each of the student's courses and their overall attendance.

![alt text](https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/images/1.jpg)

# Solution Details

Despite never having used it before, we were very impressed by and found the Microsoft Azure API to be highly capable, easy-to-use and reliable. All of our code can be viewed in this repository:
- The main body of code is written in Python and handles the image stream, compiling photos and training the image recognition, as well as sending data to be processed by Microsoft Azure. This code also contains methods for remote SQL database operations and attendance functions etc.
- The SQL database is hosted in the cloud using Azure services, and can be edited either directly using Microsoft's tools, or through our Python methods for adding students and other information.
- The web interface is a Python Flask app and interfaces between the main code and SQL database, triggering events and displaying information to the user.

# Ideas for Improvements

As a project developed in only 24 hours, there are many areas for improvement and further modifications. Here are some of our ideas:
- Improve the web interface to include more features, like a calendar and interactive attendance features
- Scale UniVison to be a University-wide system and incorporate other interfaces, like a library feature for taking out books, or a security system for access to restricted parts of campus and accommodation

# Ethics

As with any project using face identification, and especially with one based in education, there are obvious ethical concerns. Worries about tracking people, breaching privacy and other sensitive individual information do arise from the UniVision project.

As this was a Hackathon and not necessarily a serious project, we decided to proceed with the project and experiment with our implementation. This is by no means finished work or a product.

# Authors

This is a Hack Cambridge 4D project, completely designed, coded and implemented in 24 hours, from 12pm on January 19th - January 20th.

Developed by Matt Timmons-Brown, Neil Weidinger, and Rafael Anderka - 1st year Computer Science students at the University of Edinburgh
