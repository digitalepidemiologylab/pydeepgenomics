import math
import random
import time

import numpy as np
import pandas as pd

from pydeepgenomics.preprocess import usefulfunctions as uf


def compare_files(file_one, file_ten):

	data_one = np.genfromtxt(file_one, delimiter='\n')
	data_ten = np.genfromtxt(file_ten, delimiter='\n')
	# Array of boolean
	data_from_one_present_in_ten = np.in1d(data_one, data_ten)
	missing_data = np.all(data_from_one_present_in_ten)
	if missing_data:
		return missing_data
	else:
		summ = 0
		for values in data_from_one_present_in_ten:
			if values:
				summ += 1
		print("{0}/{1} correct lines in {2}".format(
			summ,
			data_from_one_present_in_ten.size,
			fileOne.split("/")[-1]))
		return None

numberOfFilesToTestPerFolder = 1
numberOfChromosomes = 22
numberOfSubsets = 3
numberOfGenerations = 2
TOTALFILESTOTEST = numberOfFilesToTestPerFolder * numberOfChromosomes * \
	numberOfSubsets * numberOfGenerations
timeBegin = time.time()
pathTenPercent = "/mount/SDF/1000genomeprocesseddata/Subsets/10_PERCENT/"
pathOnePercent = "/mount/SDF/1000genomeprocesseddata/Subsets/1_PERCENT/"
"""
pathTenPercent = "/mount/SDF/1000genomeprocesseddata/Subsets/FULL/"
pathOnePercent = "/mount/SDF/1000genomeprocesseddata/Subsets/10_PERCENT/"
"""
# uf.list_elements(pathOnePercent, _type="dir")
subsetsOne = [pathOnePercent+"Test"]
TOTALFILESTOTEST /= 3
score = 0
totalTests = 0
totalNbOfFiles = 0
incorrectFiles = []
correctFiles = []
newBatchOfErrors = True
print("\n#########################################################\n")
for sub in subsetsOne:
	subName = sub.split("/")[-1]
	generationsOne = uf.list_elements(sub+"/", _type="dir")
	for gen in generationsOne:
		genName = gen.split("/")[-1]
		chromosomes = uf.list_elements(gen+"/", _type="dir")
		for chrom in chromosomes:
			chromName = chrom.split("/")[-1]
			filesOne = uf.list_elements(chrom + "/", extension=".txt.gz")
			totalNbOfFiles += len(filesOne)
			toTest = random.sample(filesOne, numberOfFilesToTestPerFolder)
			for files in toTest:
				fileName = files.split("_")[-1]
				fileOne = files
				fileTen = pathTenPercent + subName + "/" + genName + "/" + \
					chromName + "/10PER_" + fileName
				if compare_files(fileOne, fileTen):
					score += 1
					if not newBatchOfErrors or correctFiles == []:
						correctFiles.append([])
						newBatchOfErrors = True
					correctFiles[-1].append(fileOne)
				else:
					# print("Erreur !")
					if newBatchOfErrors or incorrectFiles == []:
						incorrectFiles.append([])
						newBatchOfErrors = False
					incorrectFiles[-1].append(fileOne)
				totalTests += 1
				m, s = divmod(time.time()-timeBegin, 60)
				h, m = divmod(m, 60)
				s = int(math.floor(s))
				h, m = int(h), int(m)
				prefix = "{0}/{1} tests ({2}/{0} success) elapsed : {3}h{4}m{5}s\t".format(
					totalTests,
					TOTALFILESTOTEST,
					score,
					h,
					m,
					s)
				uf.print_progress(
					totalTests,
					TOTALFILESTOTEST,
					prefix=prefix,
					decimals=3)
pd.DataFrame(incorrectFiles).to_csv("./Incorrectfiles.csv")
print("\n\n#########################################################\n")
print("Cleaning ...")
for batch in incorrectFiles:
	for i in range(len(batch)):
		batch[i] = batch[i].split("/")
	for i in range(len(batch[0])):
		skip = 0
		toRemove = True
		folder = batch[0][skip]
		for paths in batch:
			if paths[skip] != folder:
				toRemove = False
				skip += 1
				break
		if toRemove:
			for j in range(len(batch)):
				batch[j].remove(folder)
for i in range(len(incorrectFiles)):
	print(
	"""
	##################################################################
	##################################################################

	""")
	for j in range(len(incorrectFiles[i])):
		print(incorrectFiles[i][j])
	print(2*"\n")
print("{0}/{1} files correct ({1}/{2} files tested)".format(
	score,
	totalTests,
	totalNbOfFiles))
