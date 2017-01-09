#! /usr/bin/sh
PATHOUT="./"
NUMBEROFCHROMS=3
NUMBEROFCONTROLS=25
NUMBEROFCASES=25


rm $PATHOUT*.vcf.gz

for((chr = 1; chr <= $NUMBEROFCHROMS; chr++)); do
	echo $chr
	./plink --simulate wgas.sim acgt --simulate-ncases $NUMBEROFCASES --simulate-ncontrols $NUMBEROFCONTROLS --double-id --recode vcf bgz --real-ref-alleles --out $PATHOUT$chr
done

rm *.log *.simfreq
