# LaunchWarning
A script that sends you an email with a Rocket Launch info. It sends an email only if the launch is going to happen in the current day, with the following info: Day of the launch, Rocket name, Mission name and Launch time (EDT time).

The email format: - Aug. 7: The Rocket Falcon 9 will take Starlink 9/BlackSky Global at 1:12 a.m.

It uses data from https://spaceflightnow.com/launch-schedule/

I use it as a .bat file. I created a Task at Windows Scheduler to run the script everyday in the morning.

The .bat file is only one line: "C:\...The file directory...\main.pyw". 
