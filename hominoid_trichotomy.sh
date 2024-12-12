#set directory
cd Bioinfomatics/Orthologous_Genes

# everything in one file (this was computationally expensive to align)
datasets download gene gene-id --inputfile Orangutan_only_gene_list_CLIPPED.txt --ortholog hominidae --include none --filename testortholog.zip

#split each gene into a different zip
cat orangutan_only_gene_list_CLIPPED.txt | while read GENE; do
	datasets download gene gene-id "${GENE}"  --ortholog hominidae --unique-genome --include gene --filename "${GENE}".zip
done

#extract all files and remove zips
for file in *.zip; do unzip "$file" -d "${file%.zip}"; done
rm *.zip


#run mafft in desired #### gene directory, replace #### with GeneID
mafft --auto --thread 4 gene.fna > /Users/josephwon/Bioinfomatics/Orthologous_Genes/phylogenetic_analysis/####_alignment

#remove duplicates and rename the headers using a custom script
for file in *alignment; do
    ./process_fna.py "$file" "${file%.alignment}_alnp.fna"
done


#do it for all alignments
for alnp in *.fna
do
    base=$(basename "$alnp" .fna)
    mkdir "$base"
    ./raxml-ng --all \
             --msa "$alnp" \
             --model GTR+G \
             --prefix "$base"/"$base" \
             --threads 4 \
             --bs-trees 100
done
