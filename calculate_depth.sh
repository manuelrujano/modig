#!/bin/bash

# Define the BAM/CRAM files and regions
BAM_FILES=(
    "/Users/xrujma/bin/tools/datasets/synchron_seq/2A/2A.recal.cram"
    "/Users/xrujma/bin/tools/datasets/synchron_seq/2C/2C.recal.cram"
    "/Users/xrujma/bin/tools/datasets/synchron_seq/3A/3A.recal.cram"
    "/Users/xrujma/bin/tools/datasets/synchron_seq/3C/3C.recal.cram"
    "/Users/xrujma/bin/tools/datasets/synchron_seq/9A/9A.recal.cram"
    "/Users/xrujma/bin/tools/datasets/synchron_seq/9C/9C.recal.cram"
    "/Users/xrujma/bin/tools/datasets/endo_seq/1E/1E.recal.cram"
    "/Users/xrujma/bin/tools/datasets/endo_seq/1N/1N.recal.cram"
    "/Users/xrujma/bin/tools/datasets/endo_seq/2E/2E.recal.cram"
    "/Users/xrujma/bin/tools/datasets/endo_seq/2N/2N.recal.cram"
    "/Users/xrujma/bin/tools/datasets/endo_seq/3E/3E.recal.cram"
    "/Users/xrujma/bin/tools/datasets/endo_seq/3N/3N.recal.cram"
    "/Users/xrujma/bin/tools/datasets/endo_seq/4E/4E.recal.cram"
    "/Users/xrujma/bin/tools/datasets/endo_seq/4N/4N.recal.cram"
    "/Users/xrujma/bin/tools/datasets/endo_seq/5E/5E.recal.cram"
    "/Users/xrujma/bin/tools/datasets/endo_seq/5N/5N.recal.cram"
    "/Users/xrujma/bin/tools/datasets/endo_seq/6E/6E.recal.cram"
    "/Users/xrujma/bin/tools/datasets/endo_seq/6N/6N.recal.cram"
)
REGION="chr9:4490417-4490548"
OUTPUT_DIR="depth_results"

# Create an output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Loop through each BAM/CRAM file
for BAM_FILE in "${BAM_FILES[@]}"; do
    # Extract the filename without path or extension
    FILE_NAME=$(basename "$BAM_FILE" | sed 's/\..*//')
    
    # Output file path
    OUTPUT_FILE="$OUTPUT_DIR/${FILE_NAME}_depth.txt"

    # Calculate depth for the region and save to file
    samtools depth -r "$REGION" "$BAM_FILE" > "$OUTPUT_FILE"

    echo "Depth for $BAM_FILE saved to $OUTPUT_FILE"
done
