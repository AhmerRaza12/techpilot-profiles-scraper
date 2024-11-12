with open("wasser_profile_links.txt", "r") as infile, open("wasser_cleaned_profile_links.txt", "w") as outfile:
    for line in infile:
        if "http" in line:
            cleaned_line = line[line.find("http"):] 
            outfile.write(cleaned_line)

print("Cleaning complete! Check 'wasser_cleaned_profile_links.txt' for the cleaned links.")