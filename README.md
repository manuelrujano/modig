

# modig


![image](https://github.com/user-attachments/assets/db1c5215-395a-4dc4-9362-ec818cd3b336)

Here are the scripts used in the ongoing SLC1A1 study

Please note: the data was normalized by calculating the total mapped reads for each sample, dividing raw counts by this value, and scaling to reads per million (RPM).

These steps were the following:

  samtools idxstats 3A.recal.cram > 3A_stats.txt           
  
  TOTAL_READS=$(awk '{sum += $3} END {print sum}' 3A_stats.txt)
  
  samtools depth -r chr9:4490518-4490548 3A.recal.cram | \  
  awk -v total_reads=$TOTAL_READS '{print $1, $2, $3 / total_reads * 1000000}' > 3A_normalized_depth.txt

After this, a boxplot and a Wilcoxon Signed Rank test were used to assess the data.
