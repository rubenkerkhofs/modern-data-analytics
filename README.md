<h1> Modern Data Analytics </h1>
<br>
The purpose of this repository is to ensure smooth collaboration while working on the group project for the course on modern data analytics. The course is part of the curriculum for the master's program of Statistics and Data Science at the KU Leuven. Some basic information regarding the use of Git and virtual environments is included here.

<h2> Setting up the project </h2>
To set up the project on your PC, open the command prompt (or the git terminal on windows) and move to the folder you would like to save the project in.

<code> cd Documents/Projects </code>

Once you are in the folder, you can clone the Github project to your local machine

<code> git clone https://github.com/rubenkerkhofs/modern-data-analytics.git </code>

Now, it is important to create your own virtual environment named .venv. This will ensure that everyone in the project team uses the same versions of the packages. In order to create the virtual environment you run the following command:

<code> python -m venv .venv </code>

Note that on windows and linux, files that start with a . are sometimes hidden. That is okay and does not prevent us from using these files. The next step is to activate the virtual environment, this needs to be done every time you will install new packages for this project.

For windows: <code> .venv\scripts\activate.bat </code>

For Linux: <code> source .venv\bin\activate </code>

Once you are in the virtual environment, you need to pip install the packages that can be found in the *requirements.txt* file. This can be done with the following command:

<code> pip install -r requirements.txt </code>

Now you are ready to go! Note that to run the code in certain IDEs, you need to specify which python environment you choose (SPyder and VS code both require this). Because we named our virtual environment *.venv* the IDEs usually know which one to use but it might go wrong. So check this!

<h2> Pushing to the project </h2>
To ensure that the other team members can run your code without any problems, you must make sure to update the requirements file every time you push the code to the github server. Updating the requirements file can be done via the command:

<code> pip freeze > requirements.txt </code>

**Remember that you need to activate your virtual environment before doing this**. Otherwise, the requirements.txt file will contain all packages you ever installed. Also note that on windows the command above does not always work (depending on your settings). In that case, run *pip freeze* and manually copy the output of that command and put it in the requirements.txt file using notepad. 

Once you have update the requirements.txt file, you can stage the changes:

<code> git add --all </code>

You can then check which changes were added using the status command:

<code> git status </code>

If you installed new packages, check that the requirements file is updated. Note that certain files are ignored like by example the virtual environment saved in .venv. This is a best practice and is enforced by the .gitignore file. Once the changes are staged it is time to commit:

<code> git commit --all -m 'a descriptive message for the commit' </code>

Commiting is something that only happens locally, if the other team members need to access your changes, you need to push them to the github server. This is done via the push command

<code> Git push origin branch-name</code>

<h2> Pulling the project </h2>
Before making any changes, you must be certain that you have the most up-to-date version of the code. This is done by using the pull command:

<code> git pull </code>

After pulling, you probably want to activate your virtual environment and download the requirements once again:

<code> pip install -r requirements.txt </code>
