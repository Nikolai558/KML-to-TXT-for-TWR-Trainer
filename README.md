# KML-to-TXT-for-TWR-Trainer
Convert KML file from Google Earth Pro to a text file for VATSIM Tower Trainer. Note this only does the lines you draw inside of Google Earth. Additional manual input into the txt file is required to use Tower Trainer.

## Using:
  - Download main.exe
  - Place main.exe anywhere you want on your computer
    - AV might not like this file and will either delete it, or ask you if you want to keep it.
  - Open CMD or Powershell
  - Inside CMD or Powershell type the following (replace everything inside of {} with your specific information)
    - {location of exe} {.kml file path}
    - Example: "C:\Users\nikol\Downloads\main.exe" "C:\Users\nikol\Downloads\KSLC.kml"
    - NOTE: You do not need the full file paths if the .exe and the .kml file are in the same folder (i.e. main.exe KSLC.kml )
  - OPTIONAL Argument:
    - At the very end you can add "Y" or "N" to round the cordinates to the 5th decimal place. DEFAULT IS ROUND 5 Decimal Places! 
