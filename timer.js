//Number of timers made for the unique id values of each
var count = 0
var defaultTimeInSeconds = "60"

//The + new timer button (possibly rename me)
var refNewTimer = document.getElementById("newTimer")
refNewTimer.onclick = createTimer

function createTimer()
{
    //Adds to the number of timers
    count++

    //Creates the form for a new timer
    var newForm = document.createElement("form")
    newForm.id = "timer_" + count

    //Inserts the timer before the add new timer button
    document.body.insertBefore(newForm, refNewTimer)

    //Close button
    var newCloseTimer = createInput("button", "closeTimer", "-")
    newCloseTimer.onclick = function() {closeTimer(newForm)};
    newForm.insertBefore(newCloseTimer, newFieldset)

    //Settings button
    var newCfgTimer = createInput("button", "settings", "cfg.")         //swap with img
    newForm.insertBefore(newCfgTimer, newFieldset)
    newCfgTimer.onclick = function() {openCfg(newFieldset, newFieldsetSettings)}

    // Timer Elements
    var newFieldset = document.createElement("fieldset")
    newForm.appendChild(newFieldset)
        //Title text
        //REPLACE THE LEGEND WITH THE CONFIGURATION OF TIMER
        //thus no weird number issues
    var newLegend = document.createElement("legend")
    newLegend.innerHTML = "Timer " + count
    newFieldset.appendChild(newLegend)

        //Time display
        var newP = document.createElement("p")
        newP.innerHTML = "00:00"
        newFieldset.appendChild(newP)
        //Start/Pause button
        var newToggleTimer = createInput("button", "toggleTimer", "Start")
        newFieldset.appendChild(newToggleTimer)
        newToggleTimer.onclick = function() {toggleTimer(newToggleTimer)}
        //Reset button
        var newResetTimer = createInput("button", "resetTimer", "Reset")
        newFieldset.appendChild(newResetTimer)

    //Settings Elements
    var newFieldsetSettings = document.createElement("fieldset")
    newFieldsetSettings.hidden = true //Default of settings being hidden
    newFieldsetSettings.id = "Settings"
    newForm.appendChild(newFieldsetSettings)

    var newLegendSettings = document.createElement("legend")
    newLegendSettings.innerHTML = "Settings"
    newFieldsetSettings.appendChild(newLegendSettings)

        //name
        var newNameLabel = createLabel("Name", "Name")
        newFieldsetSettings.appendChild(newNameLabel)
        var newName = createInput("text", "Name", "")
        newFieldsetSettings.appendChild(newName)

        // replace stuff to be with hour, minute, seconds all seperate boxes with
        // placeholder values

        //timer
        //timeInSeconds
        var newTimeInSecondsLabel = createLabel("TimeInSecondsLabel", "Time")
        newFieldsetSettings.appendChild(newTimeInSecondsLabel)
        var newTimeInSeconds = createInput("Input", "TimeInSeconds", defaultTimeInSeconds)
        newFieldsetSettings.appendChild(newTimeInSeconds)

        //audio file
        var newAudioFileLabel = createLabel("AudioFile", "Audio")
        newFieldsetSettings.appendChild(newAudioFileLabel)
        var newAudioFile = createInput("file", "AudioFile", "")
        newFieldsetSettings.appendChild(newAudioFile)

        //volume
        var newVolumeSliderLabel = createLabel("VolumeSlider", "Volume")
        newFieldsetSettings.appendChild(newVolumeSliderLabel)
        var newVolumeSlider = createInput("range", "VolumeSlider", "50")
        newFieldsetSettings.appendChild(newVolumeSlider)

        //test soundandvolume button
        var newTestButtonLabel = createLabel("TestButton", "Test")
        newFieldsetSettings.appendChild(newTestButtonLabel)
        var newTestButton = createInput("image", "TestButton", "")
        newTestButton.onclick = function() {testAudio(newFieldsetSettings)}
        newFieldsetSettings.appendChild(newTestButton)

        //repeat option
        var newRepeatOptionLabel = createLabel("RepeatOption", "Repeat")
        newFieldsetSettings.appendChild(newRepeatOptionLabel)
        var newRepeatOption = createInput("checkbox", "RepeatOption", "repeat")
        newFieldsetSettings.appendChild(newRepeatOption)

        //example of a good input field!
        //<input tad-va="time" placeholder="hh" onfocus="ifc(this,'h')" pattern="[0-9]*\s*([aApP][mM])?" maxlength="5" size="3" id="hour" name="hour" title="Please enter the hour of the day as a one or two-digit number, with an optional 'am' or 'pm' suffix. The valid ranges are from 00 to 23 if you choose to use the 24-hour clock format, and from 12 am to 11 pm if you choose to use the 12-hour clock format." type="text">
}

function createInput(Type,id,Value) 
{
    var newInput = document.createElement("input")
    newInput.type = Type

    if (Type === "image" && id == "settings") newInput.src="img/timer/s.png" //still need to fix the img and add it
    if (Type === "image" && id == "TestButton") newInput.src="img/timer/audioTest.png"

    if (Type === "range")
    {
        newInput.min="1"
        newInput.max="100"
    }
    newInput.id = id
    newInput.value = Value
    return newInput
}

function createLabel(id,text)
{
    var newLabel = document.createElement("label")
    newLabel.htmlFor = id
    newLabel.innerHTML= text

    var newLabelInput = createInput("form", id, "default value")
    return newLabel
}

function toggleTimer(button)
{
    button.value = button.value == "Start" ? 'Stop' : "Start"
}

function openCfg(fieldset, fieldsetSettings)
{
    fieldset.hidden = fieldset.hidden == true ? false : true
    fieldsetSettings.hidden = fieldsetSettings.hidden == true ? false : true

    //todo set the values of stuff once you click this. makes sense right?
}

function closeTimer(form)
{
    document.body.removeChild(form)
}

function testAudio(form)
{
    console.log("todo: implement me")
    return false
}

if (count == 0) createTimer()