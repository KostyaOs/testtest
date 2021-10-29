def chrom(string):
    string = string[3:string.find(' ')]
    return string

line = "chr1    HAVANA  transcript      89295   120932  .       -       .       ID=ENST00000466430.1;Parent=ENSG00000238009.2;gene_id=ENSG00000238009.2;transcript_id=ENST00000466430.1;gene_type=lincRNA;gene_status=NOVEL;gene_name=RP11-34P13.7;transcript_type=lincRNA;transcript_status=KNOWN;transcript_name=RP11-34P13.7-001;level=2;tag=basic,not_best_in_genome_evidence;havana_gene=OTTHUMG00000001096.2;havana_transcript=OTTHUMT00000003225.1"
print(line)
print()
print(chrom(line))
print(len(chrom(line)))
print()
print(line)
