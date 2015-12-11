import shlex
import subprocess
import shutil
import CreateSamplingFiles
import os.path
from CreateSamplingFiles import *
import Input_Helper
import sys
import time
from datetime import timedelta

start_time = time.time()
'''
Pipeline designed by me, Tiago Maie
In the future, if I have time, check other already designed libraries that would allow me to make a pipeline.
ruffus or makefile for example

This pipeline is divided into 6 steps
1 - SINS
2 - SINSSampler
3 - AggregateSins
4 - Arlequin
5 - ArlequinOutputParser
6 - ParsedOutputToGraphs

When running the pipeline one has to specify in the command line the steps that will be performed
For example to run the full pipeline one would write
>python SINSPipeline.py 1 2 3 4 5 6

To run everything but the first step, one would write
>python SINSPipeline.py 2 3 4 5 6

Please note that this pipeline needs to run sequentially that is, you cannot skip steps.
For example YOU SHOULD NOT DO THIS:
>python SINSPipeline.py 1 2 5 6
'''
print(str(sys.argv))
# Before doing anything else, checks if the paths given in the par file are in a nice format (aka finish with '/' char)
Input_Helper.main()

'''
open file sequentially and search for string in line
'''
# Parse parameter file
with open("./Input_SINS_Pipeline.par", 'r') as inF:
    for line in inF:
        if line[0] != '#':
            if 'OPTIONS' in line:
                option = int(line.split()[1])
                print option
            elif 'PROJECT_NAME' in line:
                projectName = line.split()[2]
            # sins
            elif 'PATH_TO_SINS_DIST_FOLDER' in line:
                pathToSINSdistFolder = line.split()[2]
            elif 'PATH_TO_SINS_OUTPUT_FOLDER' in line:
                outputFolderSINS = line.split()[2]
            elif 'NAME_OF_SINS_PROJECT' in line:
                nameOfSINSProject = line.split()[2]
            elif 'NUMBER_OF_SIMULATIONS' in line:
                numberOfSimulations = int(line.split()[2])
            # sins sampler
            elif 'NAME_OF_SINSSAMPLER_SIMULATION' in line:
                nameOfSINSSamplerSimulation = line.split()[2]
            elif 'PATH_TO_OUTPUT_FOLDER_SINSSAMPLER' in line:
                outputFolderSINSSampler = line.split()[2]
            elif 'PATH_TO_SINSSAMPLER_DIST_FOLDER' in line:
                pathToSINSSAMPLERdistFolder = line.split()[2]
            # aggregate sins
            elif 'PATH_TO_OUTPUT_FOLDER_AGGREGATESINS' in line:
                outputFolderAggregate = line.split()[2]
            elif 'PATH_TO_AGGREGATESINS_DIST_FOLDER' in line:
                pathToAGGREGATESINSdistFolder = line.split()[2]
            elif 'NUMBER_OF_CHROMOSOMES' in line:
                numberOfZomes = int(line.split()[2])
            # arlequin
            elif 'PATH_TO_ARLEQUIN_FOLDER' in line:
                arlequinFolder = line.split()[2]
            elif 'NAME_OF_LAUNCH_ARLECORE_SCRIPT' in line:
                launchArlecore = line.split()[2]
            elif 'NAME_OF_ARLEQUIN_SETTINGS_FILE' in line:
                arlequinSettingsFile = line.split()[2]
            elif 'NAME_OF_ARLEQUIN_EXECUTABLE_FILE' in line:
                arlequinExecutable = line.split()[2]
            # arlequin output parser
            elif 'IS_TABLE_ADAPTED_TO_R' in line:
                isTableAdaptedToR = bool(line.split()[2])
            elif 'PATH_TO_OUPUT_FOLDER_ARLEQUINOUTPUTPARSER' in line:
                ouputFolderArlequinOutputParser = line.split()[2]
            elif 'PATH_TO_ARLEQUINOUTPUTPARSER_DIST_FOLDER' in line:
                pathToARLEQOUTPUTPARSERdistFolder = line.split()[2]
            # parsed output to graphs
            elif 'PATH_TO_R_SCRIPT_FOLDER' in line:
                pathToRScriptFolder = line.split()[2]


# main project
    # projectName = "ParamPipelineTest"
# sins
    # pathToSINSdistFolder = "/home/tiago/Documents/PipelineTestFolder/SINS/dist/"
    # nameOfSINSProject = "PipelineTestSimulation"
    # numberOfSimulations = 1
# sinssampler
    # nameOfSINSSamplerSimulation = "PipelineTestSSampler"
    # outputFolderSINSSampler = "/home/tiago/Documents/PipelineTestFolder/SINSSampler/dist/output/PipelineTestOutputSSampler/"
    # pathToSINSSAMPLERdistFolder = "/home/tiago/Documents/PipelineTestFolder/SINSSampler/dist/"
# aggregatesins
    # outputFolderAggregate = "/home/tiago/Documents/PipelineTestFolder/AggregateSINSSamplerFiles/dist/output/AggregatedFiles_Test/"
    # pathToAGGREGATESINSdistFolder = "/home/tiago/Documents/PipelineTestFolder/AggregateSINSSamplerFiles/dist/"
    # numberOfZomes = 4
# arlequin
    # arlequinFolder = "/home/tiago/Documents/PipelineTestFolder/Arlequin/"
    # launchArlecore = "LaunchArlecore.sh"
    # arlequinSettingsFile = "arl_run.ars"
    # arlequinExecutable = "arlecore3522_64bit"
# arlequinoutputparser
    # isTableAdaptedToR = True
    # ouputFolderArlequinOutputParser = "/home/tiago/Documents/PipelineTestFolder/ArlequinOutputParser/dist/output/PipelineTest/"
    # pathToARLEQOUTPUTPARSERdistFolder = "/home/tiago/Documents/PipelineTestFolder/ArlequinOutputParser/dist/"
# parsedoutputtographs
    # pathToRScriptFolder = "/home/tiago/Documents/PipelineTestFolder/ParsedOutputToGraphs/"


'''
PipelineTestFolder
    SINS
        dist (RUN SINS HERE): java -jar SINS2.jar  -projectName "PipelineTestSimulation" -formati fZip -numberOfSimulation 1 -takeSampledParametersFromFile yes
            SINS2.jar
            lib
            input
            results
    SINSSampler
        dist (RUN SINSSampler HERE): "java -jar SinsSampler.jar -input \"/home/tiago/Documents/PipelineTestFolder/SINS/dist/results/"+nameOfSINSProject+"\" -numberOfSimulation 1 -output \"output/PipelineTestOutputSSampler\" -simulationName \""+nameOfSINSSamplerSimulationName+"\""
            SinsSampler.jar
            lib
            input
            PipelineTestOutputFolder
    AggregateSINSSamplerFiles
        dist (): java -jar AggregateSINSSamplerFiles.jar -input "/home/tiago/Documents/PipelineTestFolder/SINSSampler/dist/PipelineTestOutputFolder/ARLsimulation_1/" -output "/home/tiago/Documents/PipelineTestFolder/SINSSampler/dist/PipelineTestOutputFolder/ARLsimulation_1/AggregatedFiles_Test/" -zomeNumber 4
    Arlequin (copy content of Arlequin folder (which should only be these 3 files) into the folder with the output of AggregateSINSSamplerFiles)
        arlecore3522_64bit
        arl_run.ars
        LaunchArlecore.sh
    ArlequinOutputParser
        dist


'''

# SINS2
if sys.argv.count("1"):

    print "Step 1 - SINS - is running."

    if os.path.isdir(outputFolderSINS):
        shutil.rmtree(outputFolderSINS)

    cmdExecuteSINS = "java -jar SINS2.jar  -projectName \"" + nameOfSINSProject + \
                     "\" -formati fZip -numberOfSimulation " + str(numberOfSimulations) + " -takeSampledParametersFromFile yes"
    cmdExecuteSINS = shlex.split(cmdExecuteSINS)
    # change SINS so that maybe the file not found exception doesnt happen
    # maybe a nice way to implement it is just to assume nothing, and give the user the option to pass the parameters
    # aka the folders where the files needed are
    SINSprocess = subprocess.Popen(cmdExecuteSINS, stdout=subprocess.PIPE, cwd=pathToSINSdistFolder).stdout.read()
    print SINSprocess

    print "Step 1 has finished."


# SINSSampler

CreateSamplingFiles.main(nameOfSINSSamplerSimulation)

if sys.argv.count("2"):

    print "Step 2 - SINS Sampler - is running."

    if os.path.isdir(outputFolderSINSSampler):
        shutil.rmtree(outputFolderSINSSampler)

    cmdExecuteSinsSampler = "java -jar SinsSampler.jar -input \""+pathToSINSdistFolder+"results/" + nameOfSINSProject + "\" -numberOfSimulation 1 -output \"" + outputFolderSINSSampler + "\" -simulationName \"" + nameOfSINSSamplerSimulation + "\""
    cmdExecuteSinsSampler = shlex.split(cmdExecuteSinsSampler)

    subprocess.Popen(cmdExecuteSinsSampler, stdout=subprocess.PIPE, cwd=pathToSINSSAMPLERdistFolder).stdout.read()

    print "Step 2 has finished."


# Aggregate

if sys.argv.count("3"):

    print "Step 3 - Aggregate SINS Sampler files - is running."

    if os.path.isdir(outputFolderAggregate):
        shutil.rmtree(outputFolderAggregate)

    cmdExecuteAggregate = "java -jar AggregateSINSSamplerFiles.jar -input \"" + outputFolderSINSSampler + "/ARLsimulation_1/\" -output \"" + outputFolderAggregate + "\" -zomeNumber "+str(numberOfZomes)

    cmdExecuteAggregate = shlex.split(cmdExecuteAggregate)
    subprocess.Popen(cmdExecuteAggregate, stdout=subprocess.PIPE, cwd=pathToAGGREGATESINSdistFolder).stdout.read()

    print "Step 3 has finished."


# Arlequin

if sys.argv.count("4"):

    print "Step 4 - Arlequin - is running."

    # checks if files exist before trying to copy them
    if os.path.isfile(arlequinFolder + launchArlecore):
        shutil.copy(arlequinFolder + launchArlecore, outputFolderAggregate)
    if os.path.isfile(arlequinFolder + arlequinSettingsFile):
        shutil.copy(arlequinFolder + arlequinSettingsFile, outputFolderAggregate)
    if os.path.isfile(arlequinFolder + arlequinExecutable):
        shutil.copy(arlequinFolder + arlequinExecutable, outputFolderAggregate)

    cmdExecuteLaunchArlequin = "./LaunchArlecore.sh " + arlequinExecutable + " " + arlequinSettingsFile
    cmdExecuteLaunchArlequin = shlex.split(cmdExecuteLaunchArlequin)

    # give the user permission to execute to the file
    cmdToGivePermission = "chmod u+x " + launchArlecore
    cmdToGivePermission = shlex.split(cmdToGivePermission)
    subprocess.Popen(cmdToGivePermission, stdout=subprocess.PIPE, cwd=outputFolderAggregate).stdout.read()

    subprocess.Popen(cmdExecuteLaunchArlequin, stdout=subprocess.PIPE, cwd=outputFolderAggregate).stdout.read()

    print "Step 4 has finished."


# ArlequinOutputParser

if sys.argv.count("5"):

    print "Step 5 - Arlequin Output Parser - is running."

    if os.path.isdir(ouputFolderArlequinOutputParser):
        shutil.rmtree(ouputFolderArlequinOutputParser)

    cmdExecuteArlequinOutputParser = "java -jar ArlequinOutputParser.jar -input \"" + outputFolderAggregate + "\" -isTableAdaptedToR " + str(
        isTableAdaptedToR).lower() + " -output " + ouputFolderArlequinOutputParser
    cmdExecuteArlequinOutputParser = shlex.split(cmdExecuteArlequinOutputParser)
    subprocess.Popen(cmdExecuteArlequinOutputParser, stdout=subprocess.PIPE, cwd=pathToARLEQOUTPUTPARSERdistFolder).stdout.read()

    print "Step 5 has finished."


# R script

if sys.argv.count("6"):

    print "Step 6 - Parsed Output to Graphs - is running."

    if isTableAdaptedToR:
        # note that the third argument stand for "initial generation"
        cmdExecuteOutputRGraphs = "Rscript arlequinOutputToGraphs.r \"" + ouputFolderArlequinOutputParser + "\" \"A1_output_Exp\" 0 " + str(CreateSamplingFiles.numberOfGenerations) + " " + str(CreateSamplingFiles.generationsSampledInterval) + " " + projectName + " " + pathToRScriptFolder
        cmdExecuteOutputRGraphs = shlex.split(cmdExecuteOutputRGraphs)
        subprocess.Popen(cmdExecuteOutputRGraphs, stdout=subprocess.PIPE, cwd=pathToRScriptFolder).stdout.read()

    print "Step 6 has finished."


print "The SINS pipeline has finished."
end_time = time.time()
elapsed_time = end_time - start_time
print "Elapsed time: " + str(timedelta(seconds=elapsed_time))
'''
commandToExecute = "some bash command -l"

return_code = subprocess.call(commandToExecute, shell=True)

splitCommand = shlex.split(commandToExecute)

print(splitCommand)

return_codePopen = subprocess.Popen(splitCommand, bufsize=0, executable=None, stdin=None, stdout=subprocess.PIPE, stderr=None, preexec_fn=None,
                 close_fds=False, shell=False, cwd=None, env=None, universal_newlines=False, startupinfo=None,
                 creationflags=0).stdout.read()

print return_codePopen
'''
