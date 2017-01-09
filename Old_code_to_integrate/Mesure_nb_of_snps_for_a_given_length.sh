#!/usr/bin/sh

_chrom=$1

for ((_chrom=1; _chrom<=22; _chrom++)); do

	echo "Processing chrom $_chrom :"
	_file="../1000genomeprocesseddata/$_chrom/_meta.txt.gz"
	#_file="../fakedataset/2/_meta.txt.gz"
	sizegrp=500000
	#sizegrp=1100
	onecentimorgan=1000000
	margin=$((4*$onecentimorgan))
	#onecentimorgan=1000
	startline=8
	nboflines=$(($(zcat $_file | wc -l) -$startline))
	nboftests=$(($nboflines/$sizegrp))
	unsufficientfragmentsize=0
	toobig=0
	lasttoobig=0
	lasttoosmall=0
	for ((i=$startline; i<$nboflines ; i=i+$sizegrp)); do
		begin=$i
		echo -ne "$i/$nboflines\tToo small: $unsufficientfragmentsize,last diff = $lasttoosmall\tToo big: $toobig, last diff = $lasttoobig"\\r
		posbeg=$(zcat $_file | head -$begin | tail -n1 | awk '{print $2}')
		end=$(($begin+$sizegrp))
		posend=$(zcat $_file | head -$end | tail -n1 | awk '{print $2}')
		difference=$((posend-posbeg))
	
		if [ $difference -lt $((onecentimorgan+margin)) ]; then
			unsufficientfragmentsize=$((unsufficientfragmentsize+1))
			lasttoosmall=$difference
		fi
		if [ $difference -ge $((onecentimorgan*100)) ]; then
			toobig=$((toobig+1))
			lasttoobig=$difference
		fi

	done
	echo ""
	echo "$nboftests tests"
	echo "$unsufficientfragmentsize unsufficent fragment size"
	echo "$toobig too big fragment size"
	echo "########################################################################"
done
