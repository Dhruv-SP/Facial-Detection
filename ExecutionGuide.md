# Execution guide to the Project.
## This guide contains the explanation of the logic/code(Backend and frontend).

**Before we start getting deep into the project, let’s have a brief overview to the Project.**
As you may have known about the basich of the project, we begin with discussing the Libraries being used.

We’ve used **PyQt5** for the GUI as it’s the most convenient and appropriate as per the requirements.

For the Image processing or say Computer Vision, We’ve used the popular **cv2** to have input, perform basic operation such as color image to Black and white and output the processed image.

In the project we have also used the **Face_utils** from **imutils**, the **face_utils** contains the mapping of human face encoded inside it.

Th another main library is **dlib**. **dlib** is mainly used during the Separate parts detection to work with the facial parts.

These where the main libraries used in the project, and few other essentials such as datetime, copy, etc… .

Lets begin break down the code as per the execution.

When you run the code (Before this, make sure the path are well placed as per your PC. Check line 284 (shape predictor) and line296 (haarcascade) and also provide new path for file at line42, 262, the first window to appear is the Main Window with only have one button **“Start”**. As the buttons are GUI.PyQt5 components, they can be disabled or even hidden when required. All the buttons are first hidden using **‘.hide()’** method (#51 onwards)during the constructor call to initUI where they are also initialization.

#69  The **“Start”** is connected to method **‘showfrm’** using **‘.clicked.connect( )’** method. The **‘clicked’** in the beginning is a user event over the button such as ‘hover’ and is connected to method **‘showfrm’** using the following command **‘.connect(‘method’)’** .
What is method says is, when the user clicks on the button **“Start”**, it will call the function **‘showfrm’**.

#260  Now lets come to **‘showfrm’**, in the very start of the method, we have declared a file variable with mode ‘a’, this is used to maintain the log of the project. Then we have declared the datetime component also for log file, this method also contains an infinite loop, on to that later on.

#276  Then there is the method **‘AllShow’**. This method makes all the GUI component visible and also enables 3 important buttons to be clickable: **“Detect Face”**, **“Detect Separately”**, **“End”**. As you know what these buttons does, if not refer the ‘User Guide’ as we are not covering event and action part in this file, we will proceed to main part.

Now here the main program takes place.
When both the buttons are not clicked, two variables **‘showsq’** and **‘showdot’** are set to 0 as default.
The **‘showfrm’** checks for that value of this variables and if the both zero condition satisfies, the raw Webcam footage is being displayed using **cv2.Imshow(‘window_name’, frame)**

The Webcam footage input is taken before the condition operation happens using the **‘.read()’** method that takes the footage from the webcam. **‘cv2.VideoCapture(‘port no.’)’** method gives the access to program to use the Webcam. The port number defines which port to use for the webcam, if you are running the inbuild one, then the default for that is 0 or else 1.

Back to flow, 
When you click any button, their responding variable value is being changed from 0 to 1.
Also that button gets invisible and another button **“STOP Facial Detection”** or **"STOP part detection"** takes its place, basically the programs first hides the first button using **‘.hide()’** and the second button **“End”** is being shown using **‘.show()’** method. And both the buttons have same geometry and coordinates, so it appears that the button have changed the property but is a whole new button
When the variable value is being changed, the looping execution in ‘showfrm’ checks for the 1’s in the variables and act accordingly that weather to display the final result or not. We’ll understand that in the following block.


## How actually is the program executing?
 Let’s say when you click the button **“Detect Face”**, it calls the method **‘enableSQ’**. The method first makes an entry into log file, then changes the variable **‘showsq’** to 1, hides the button **“Detect Face”**, make visible the **“STOP Facial Detection”**  button that replaces it, and make enable the **“End”** button. You may say there is just a variable change and nothing about execution or calling to other methods to detection, how is that going to affect?
Well, the execution code is already inside the ‘showfrm’ method, which is endlessly looping, we just have to change the variable so that the condition satisfies, and the desired code executes.

## Let’s jump deep inside ‘showfrm’ now as I said before.
Back to method ‘showfrm’, we covered first few basic codes, 
#285  now we have the string holding the path to **‘shape_predictor_68_face_landmarks.dat’** file, this external file will help to detect the separate parts of face. Then we have a dlib method **‘get_frontal_face_detector’** which is a regular face detector, assign that to var **‘detector’**. 
Now we have the method to determine the point location (coordinates) of the parts in the image that defines the using the .dat file, **‘shape_predictor’** assigning to **‘predictor’**.
#294  To get the frames from Webcam we used **cv2.videoCapture** we discussed that earlier on.
The last thing before getting into the Endless Loop, we have the haarcascade.xml file, this file contains all the features of face, this will be used to detect face.

## Now we are inside the in Endless loop where the main codes are.

#300  At first we have the **‘.read()’** that will read the frame from the Webcam and store into **‘freeframe’**, also if no footage is received, the false value is being assigned to **‘check’** var.
We are using the **‘.copy()’** to create an exact copy of the **‘freeframe’**. The reason not to use the ‘=’ is because we want these frames to be independent from each other.

#307  The **‘cv2.cvtColor’** will change the color image from the **‘frame’** to black and white and save to **‘gray’**.
#310  The detector is a variable to whom we have assigned with the d lib method **‘get_frontal_face_detector’**. This will return the rectangle coordinates as (a,b)(c,d).
The a is the left wall of the rectangle, same as b is the top one, c is the right, and d is the bottom wall
Again we create a copy of frame

#316  Now using the haar cascade file, the program will search for the presence of features of human face in the **‘frame’** and will return **x-axis, y-axis, length, width** of the frame where the conditions are being satisfied.
And we draw a rectangle around the face using the return value. But before this, there are two strange things in the method ‘.detectMultiscale()’, **scaleFactor** and **minNeighbors**.

Well the **scaleFactor** is the passing criteria, you can say if the number is near 2.0, the criteria are higher, means half face, tilted face, or smaller in the frame are not going to be recognized.
The **minNeighbors** will resist the image to ‘defined’ units smaller for batter accuracy. ‘0’ will return more errors, so I recoment to keep between 3-5.

Now you may ask that, **‘face_cascade.detectMultiscale’** and **‘recognize’** are doing the same thing, why keep both?
In simple terms, just keep the code separate. The **‘face_cascade.detectMultiscale’** will be used in **“Detect Face”** and **‘recognize’** is being used for **“Detect Separately”** and the codes will be clean.

Back to the code, 
#322  now we are inside another loop, here we are taking the coordinates we get from the **‘detector’** and we are now passing that whole set of four values to the **‘predictor’**, **‘predictor’** will return the 68 defined points faces that detect the separate parts
In the next line we converted the **‘shape’** dataset to N-dimensional array which would be [68][2].
Again another loop, yes the Big(O) would be more then n^2, but execution time is not a criteria here.

##329  In the loop we are going through all that 68 points and creating a small circle or say dot at the respective coordinate


Here is some more interesting part, **‘startind’**, **‘endind’**
To explain this we have to focus outside the loop or even say the whole method **‘showfrm’**.
The 68 coordinates are not random but are in a well sorted way
  •	Mouth  [48, 68].
  •	Eyebrow [17, 27].
  •	Eye   [35, 48].
  •	Nose  [27, 35].
  •	And Jaw [0, 17].
  
As per the desired part, the user will click the button present on the right side in **“Facial Workshop”**
Those buttons are to change the focus from part to part, what they actually do is, when clicked they call a function #497 and in the function the var **‘startind’** and **‘endind’** are being altered.
Back to the **‘showfrm’** inside the for loop to draw the circle, this **‘startind’** and **‘endind’** controls which of this 68 points will be executed so only those points/circle gets drawn that are surrounding the desired part.

#344  For the following code you have to get back to the point from where this all description begin, the point where you asked **“how is that going to affect?”** here, let me explain.

Now we have a condition check in which are the variables that hold the value that weather the buttons are clicked or not, again we have done all the execution, the dots and squares are drown, now is the point where the output is being displayed.

If non of the buttons are clicked, then the **‘showsq’** and **‘showdot’** are set to 0.

#344  The outer condition check is satisfied and displays the raw Webcam footage stored in **‘freeframe’** in a new window **“WebCam”**.

There are also two more lines, on to that in a quick while.

Now, Lets say that **“Detect Face”** is being clicked, the var **‘showsq’** is set to 1.

So the outer **if** condition is now failed and destroyed the window showing **“WebCam”** (raw footage), now we are into the inner if #350  where the condition for **‘showdot’** also fails, jumps to the next if #377 where the condition is now satisfied, and the frame surrounding the face is being displayed inside a new window **“Detection”** also we saved the frame to **‘captureframesq’**, that is to save the frame, more on to that after this block. Alter displaying the frame detecting the face, the next code enables 3 scrollbars respectively for Red, Blue, Green. Moving the scrollbar will change the color of square in the frame.

And that’s how the program displays the output as per the button clicks.

Also when you press the **“STOP Facial detection”** button that replaced the **“Detect face”** button is also used to stop the displaying of output, when you click the **“STOP Facial detection”** the respective variable is set to 0 and the if conditions fails.

Lets say you started and then again stopped both the outputs, the variables are again set to 0 and the outer if is satisfied. Now back to those two commands#346,347. Those commands are to destroy the windows which were showing the output for **“Detect face”** and **“Setact Separately”**.

and all the magic of disabling and enabling, hiding and showing you may see on the main window, is also controlled by these two variables and all the following If conditions between #355 to #401. That is very lengthy and very easy portion so we're skipping on that.

#352, 379 As said earlier to explain it later, these code is to saves the copy of output frame to **‘captureframe’**.
You may see the button **“capture”** in the left side, above the scrollbar. That button is to save the most recent output frame to your pc. 
#475  The connected method first have a variable **option** for QfileDialog,
This variable holds the style properties of the file dialogue box to be displayed.
#479  The next code saves the filename returned from the dialogue box, and adds extension for two different outputs  as we may have any of them active during the process.
#486  In the outer if it checks whether the name Is being provided or not, if not provided then the files would not be saved.
inside the if we check again those variables, whoever is 1, only that frame has to be saved, that’s very obvious.

That’s all about the execution process, you may contact me for any query
