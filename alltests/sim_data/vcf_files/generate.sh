#! /usr/bin/env bash
PATHOUT="./"
NUMBEROFCHROMS=3
NUMBEROFCASES=20
NUMBEROFCONTROLS=20
NUMBEROFSAMPLES=10

rm $PATHOUT*.vcf.gz $PATHOUT*.vcf

# generate dataset with plink
for((chr = 1; chr <= $NUMBEROFCHROMS; chr++)); do
	#./plink --simulate wgas.sim acgt --simulate-ncases $NUMBEROFCASES --simulate-ncontrols $NUMBEROFCONTROLS --double-id --recode vcf bgz --real-ref-alleles --out $PATHOUT$chr
	./plink --simulate-qt wgas_qt.sim acgt --simulate-n $NUMBEROFSAMPLES --double-id --recode vcf --real-ref-alleles --out $PATHOUT$chr
done

# change the values for the positions in bp (o)


rm *.log *.simfreq
