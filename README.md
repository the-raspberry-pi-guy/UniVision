# UniVision - Hack Cambridge 4D Hackathon 2019

![alt text](https://raw.githubusercontent.com/the-raspberry-pi-guy/UniVision/master/Logo/UniVision_logo.png)

# Overview
UniVision is a system that uses cloud-based video recognition to accurately record and monitor the attendance of University students in lectures. Accessed over an easy-to-use web interface, our software uses a standard webcam and Microsoft Azure web services to determine people coming into a lecture theatre. Trained using machine-learning algorithms on only a small sample of images, UniVision uses a REST API with a high level of accuracy to quickly and efficently inform a lecturer as to whether a student is present in the class. In the background, an SQL Azure database stores a catalogue of students, their course information and timetables, amongst other information. Using our code, statistics like lecture attendance and other averages can be calculated and presented to the user.

# The Problem?
A fact that many students do not like to own up to is that attendance at lectures is critical to education success. In a first year "Intro to Linear Algebra" course at the Univeristy of Edinburgh, missing just 2 lectures brought an average student's final grade down by 20%. Missing more caused an even steeper decline, with students who were absent in 5-10 lectures passing at a rate of less than 50%. This is a clear problem, with much evidence elsewhere: https://www.google.com/search?client=safari&rls=en&q=lecture+attendance+and+exam+results&ie=UTF-8&oe=UTF-8

# Our Solution
We set about trying to solve this problem by creating a much more reliable system of attendance, using cloud-based image recognition - trained on small sets of user-provided photos of students. This is faster than a Professor calling out a register, and more resilient to being "cheated". For example, using UniVision, it is not possible for one student to mark another present when they are not.

The idea behind our principle is for a camera to be mounted near the door to a lecture theatre. Before a lecture begins, the teacher can access our web interface and select which class they are about to teach. They can then press the "Start" button, which commences the video feed, and students can enter the room.

IMAGE OF WEB INTERFACE



Edinburgh University - Matt Timmons-Brown, Neil Weidinger, Rafael Anderka
