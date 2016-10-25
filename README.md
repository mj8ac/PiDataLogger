# PiDataLogger

Use this python script and web front end to read temperature data from the MAX31850 thermocouple amplifier. The python script reads data from the W1_SLAVE file and generates JSON files and a CSV file with the temperature data. Apache reads the text file which is requested by some javascript. 

The javascript reads the data and generates two charts per thermocouple channel; one showing all recorded data from the session, and a real time chart showing the last 15 minutes. 
