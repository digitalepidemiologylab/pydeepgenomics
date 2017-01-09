# -*- coding: utf-8 -*-
import datetime
import os
import random
import sys

import pandas as pd


try:
	import pydeepgenomics
	from pydeepgenomics.tools import generaltools as gt
	from pydeepgenomics.preprocess import settings
except ImportError:
	cmd_dir = os.path.abspath(os.path.dirname(__file__)).split("alltests")[0]
	if cmd_dir not in sys.path:
		sys.path.append(cmd_dir)
	import pydeepgenomics
	from pydeepgenomics.tools import generaltools as gt
	from pydeepgenomics.preprocess.settings import settings


def verify_filtering(path_filtered_data, chrom_to_be_tested):
	if settings.LOGGING:
		old_stdout = sys.stdout
		log_file = open(
			os.path.join(
				path_filtered_data,
				"logtestdecode{}.log".format(chrom_to_be_tested)),
			"w")
		sys.stdout = log_file

	print("Program started at {}".format(str(datetime.datetime.now())))
	errors_file = []
	errors_sup_pos = []
	errors_real_pos = []
	errors_type = []
	errors_prev_pos = []
	errors_next_pos = []
	_meta = pd.read_csv(
		os.path.join(settings.PATHORIGIN, chrom_to_be_tested, "_meta.txt.gz"),
		sep="\t",
		index_col=False).drop(
		["#CHROM", "ID", "QUAL", "FILTER", "INFO", "FORMAT"],
		1)
	files = gt.list_elements(
		os.path.join(settings.PATHENCODED, chrom_to_be_tested), extension=".txt.gz")
	for j in range(min(nbfilesmax, len(files))) :
		random.seed()
		testfile = random.choice(files)
		name = testfile.split("/")[-1].split(".")[0]
		_meta["originaldata"] = pd.read_csv(
			os.path.join(PATHORIGIN, chrom_to_be_tested, name+"_"+name+".txt.gz"),
			index_col=None,
			header=None)
		_meta["totest"] = pd.read_csv(testfile,  index_col = None, header = None)
		for i in range(nbtests):
			totest = random.choice(_meta.totest.tolist())
			A1, A2, position = uf.decode_position(totest, LN)
			if position == -1:
				index = _meta.loc[(_meta.totest == totest),:].index.tolist()[0]
				errors_file.append(testfile)
				errors_sup_pos.append(position)
				errors_real_pos.append(_meta.iloc[max(index,0), 0])
				errors_type.append("Impossible to decode")
				errors_prev_pos.append(_meta.iloc[max(index-1,0), 0])
				errors_next_pos.append(_meta.iloc[min(index+1, _meta.shape[0]), 0])
				if not settings.LOGGING:
					uf.print_progress(j*nbtests+i,nbtests*min(nbfilesmax, len(files))-1, decimals = 3)
				if VERBOSE:
					print("{0}/{1} files tested. Date : {2}".format(i, nbtests, str(datetime.datetime.now())))
				continue
			originalalleles = _meta.loc[(_meta.totest == totest), :]["originaldata"].tolist()[0].split("/")
			originalpos = _meta.loc[(_meta.totest == totest), :]["POS"].tolist()[0]
			ref =  _meta.loc[(_meta.totest == totest), :]["REF"].tolist()[0]
			alt =  _meta.loc[(_meta.totest == totest), :]["ALT"].tolist()[0]
			if position != originalpos:
				index = _meta.loc[(_meta.totest == totest),:].index.tolist()[0]
				errors_file.append(testfile)
				errors_sup_pos.append(position)
				errors_real_pos.append(_meta.iloc[max(index,0), 0])
				errors_type.append("Position")
				errors_prev_pos.append(_meta.iloc[max(index-1,0), 0])
				errors_next_pos.append(_meta.iloc[min(index+1, _meta.shape[0]), 0])
			if ((originalalleles[0] == 0) and (A1 != ref)) or ((originalalleles[0] == 1) and (A1 != alt)) :
				index = _meta.loc[(_meta.totest == totest),:].index.tolist()[0]
				errors_file.append(testfile)
				errors_sup_pos.append(position)
				errors_real_pos.append(_meta.iloc[max(index,0), 0])
				errors_type.append("Allele 1")
				errors_prev_pos.append(_meta.iloc[max(index-1,0), 0])
				errors_next_pos.append(_meta.iloc[min(index+1, _meta.shape[0]), 0])
			if ((originalalleles[-1] == 0) and (A1 != alt)) or ((originalalleles[-1] == 1) and (A1 != alt)) :
				index = _meta.loc[(_meta.totest == totest),:].index.tolist()[0]
				errors_file.append(testfile)
				errors_sup_pos.append(position)
				errors_real_pos.append(_meta.iloc[max(index,0), 0])
				errors_type.append("Allele 2")
				errors_prev_pos.append(_meta.iloc[max(index-1,0), 0])
				errors_next_pos.append(_meta.iloc[min(index+1, _meta.shape[0]), 0])
			if not settings.LOGGING:
				uf.print_progress(j*nbtests+i,nbtests*min(nbfilesmax, len(files))-1, decimals = 3)
			if VERBOSE:
				print("{0}/{1} files tested. Date : {2}".format(i, nbtests, str(datetime.datetime.now())))
	errors = pd.DataFrame({"File" : errors_file,
		"Supposed_position" : errors_sup_pos,
		"Real_position" : errors_real_pos,
		"Error_type" : errors_type,
		"Previous_positions" : errors_prev_pos,
		"Next_position" : errors_next_pos})
	if not errors.empty :
		errorsal1 = errors.loc[(errors.Error_type == "Allele 1"), :].shape[0]
		errorsal2 = errors.loc[(errors.Error_type == "Allele 2"), :].shape[0]
		errorspos = errors.loc[(errors.Error_type == "Position"), :].shape[0]
		Impossibletodecode = errors.loc[(errors.Error_type == "Impossible to decode"),:].shape[0]
		totalerror = errors.shape[0]
		print("\nAllele 1 errors : {0}\nAllele 2 errors : {1}\nPosition errors : {2}\nImpossible to decode : {3}\nTotal errors : {4}".format(errorsal1, errorsal2, errorspos, Impossibletodecode, totalerror))
		print("In total : {}% errors !\n".format(100*totalerror/(nbtests*min(nbfilesmax, len(files)))))
		print("Date : {}".format(str(datetime.datetime.now())))
		errors.to_csv("Errorsfoundin{}.csv".format(chrom_to_be_tested), sep ="\t")
	else :
		print("No error found !")
	if settings.LOGGING:
		sys.stdout = old_stdout
		log_file.close()
