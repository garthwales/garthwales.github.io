var beenFocused = true
window.onblur = function ()
{
    beenFocused = false
}

window.onfocus = function () 
{
    if (!beenFocused)
    {
        beenFocused = true
        location = location
    }
}