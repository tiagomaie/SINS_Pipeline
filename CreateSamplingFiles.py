import os.path

'''
Automatically creates the necessary files with the necessary data for SinsSampler to run
Currently I only tested it with a single autosome and a single layer. Need to run more tests in the future
'''


def main(simulationName):

    with open("./Input_SINS_Pipeline.par", 'r') as inF:
        for line in inF:
            if 'PATH_TO_SINS_INPUT_FOLDER' in line:
                pathToSINSInputFolder = line.split()[2]
            elif 'NAME_OF_SINS_PROJECT' in line:
                nameOfSINSProject = line.split()[2]
            elif 'PATH_TO_SINSSAMPLER_INPUT_FOLDER' in line:
                addressOfInputFolder = line.split()[2]


    addressOfPrefFile = pathToSINSInputFolder + nameOfSINSProject + "/output_preferences.txt"
    addressOfWorldFile = pathToSINSInputFolder + nameOfSINSProject + "/world.txt"


    '''
    open file sequentially and search for string in line
    '''
    with open(addressOfPrefFile, 'r') as inF:
        for line in inF:
            if 'generationsIntervalgen' in line:
                global generationsSampledInterval
                generationsSampledInterval = int(line.split()[1])


    nameOfLayer = ''
    with open(addressOfWorldFile, 'r') as inF:
        for line in inF:
            if 'numberOfGenerations' in line:
                global numberOfGenerations
                numberOfGenerations = int(line.split()[1])
            elif 'layerName' in line:
                nameOfLayer += line.split()[1] + "\n"
            elif 'numberOfLayers' in line:
                numberOfLayers = line.split()[1]

    addressOfGenotypeFile = pathToSINSInputFolder + nameOfSINSProject +"/genetics/"+nameOfLayer.split("\n")[0]+"/genotype.txt"

    typeOfChromosomeA = ''
    with open(addressOfGenotypeFile, 'r') as inF:
        for line in inF:
            if 'typeX' in line:
                typeOfChromosomeX = line
            elif 'typeY' in line:
                typeOfChromosomeY = line
            elif 'typeMT' in line:
                typeOfChromosomeMT = line
            elif 'typeA' in line:
                typeOfChromosomeA += line + "\n"
            elif 'nbAutosomes' in line:
                numberOfAutosomesLine = line

    '''
    Creates sampling files necessary for SinsSampler to run
    '''
    ''''Create config.txt'''
    configFile = open(addressOfInputFolder + 'config'+simulationName+'.txt', 'w+')
    configFile.write("inputInformation\n"
                     "layerNumber " + numberOfLayers + "\n" +
                     nameOfLayer +
                     numberOfAutosomesLine +
                     typeOfChromosomeX +
                     typeOfChromosomeY +
                     typeOfChromosomeMT +
                     typeOfChromosomeA)

    '''Create generation.txt'''
    if os.path.isfile(addressOfInputFolder + 'generations.txt'):
        generationFile = open(addressOfInputFolder + 'generations.txt', 'w+')
    else:
        generationFile = open(addressOfInputFolder + 'generations.txt', 'a')

    for i in range(0, numberOfGenerations + 1, generationsSampledInterval):
        print i
        generationFile.write(str(i) + "\n")

    generationFile.close()

    '''
    Create sampling[generation].txt

    Example:
    "PopulationName DemeLine DemeColumn NumMale NumFemale\n"
    "layerOne 0 0 10 10\n"
    "layer0 0 4 10 10\n"
    "layer0 0 8 10 10\n"
    "layer0 2 2 10 10\n"
    "layer0 2 6 10 10\n"
    "layer0 4 0 10 10\n"
    "layer0 4 4 10 10\n"
    "layer0 4 8 10 10\n"
    "layer0 6 2 10 10\n"
    "layer0 6 6 10 10\n"
    "layer0 8 0 10 10\n"
    "layer0 8 4 10 10\n"
    "layer0 8 8 10 10"
    '''
    # range(initial generation, number of generations + 1, generations sampling interval)
    for i in range(0, numberOfGenerations + 1, generationsSampledInterval):
        print i
        samplingFile = open(addressOfInputFolder + 'sampling' + str(i) + '.txt', 'w+')
        samplingFile.write("PopulationName DemeLine DemeColumn NumMale NumFemale\n"
                           "layerOne 0 0 10 10\n")
        samplingFile.close()
