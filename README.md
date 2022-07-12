# printer-project

solution to local tech company technical interview prompt

![alt_text](https://github.com/scott-sattler/printer-project/blob/main/tech_test_printer_screen.png?raw=true)


prompt: <br>
&emsp; printer that accepts user input <br>
&emsp; instructions for compiling and executing code in chosen language <br>
&emsp; detailed code comments explaining thought process and any assumptions made <br>

imposed constraints: <br>
&emsp; print when buffer (1024 char) full <br>
&emsp; print if unprinted for 10 seconds <br>
&emsp; print method should not wait on completion <br>
&emsp; complete the project in less than two hours  <br>

## Usage:

main.py: uses console; contains app logic<br>
main_gui.py: is a functional (vs OOP) GUI

from IDE, run main_gui.py

to compile single file executable:<br>
pyinstaller -F --noconsole main_gui.py


## Comments:
the unimplemented optimization looks to be a bin packing problem <br>
evidently it was *not* intended to be an optimization problem... <br>
failed to adequately consider extensability <br>

## TODO:
~~disable debugging flags and/or<br>
add toggle for prompt constraints~~<br>
debug threading
