Started by researching about postcodes in the United Kingdom, 
since I lived for a year in Manchester and family in UK, I have an idea on the concept.


Postcode

	- Outward Code (between 2 and four chars long)
		- Area
			- 1 or 2 chars (alphabetic, 121 areas)
		- District
			- 1 digit, 2 digits or a digit followed by a letter

	- Inward Code (after the single space, 3 chars long)
		- Sector
			- 1 single digit 0-9
		- Unit
			- 2 chars


Some rules for validation:

London:

- A9A 9AA (postcode districts E1, N1, W1)
  - e.g: W1A 0AX, lets stay the user input "w1a0ax", I should:
    - Since the inward code mandatory have 3 chars, divide the string 3 chars from the end to the beginning
    - Verify if starts with W1;
	- AA9A 9AA (WC postcode area and districts EC1–EC4, NW1W, SE1P, SW1)



References:
https://stackoverflow.com/questions/164979/regex-for-matching-uk-postcodes

https://en.wikipedia.org/wiki/Postcodes_in_the_United_Kingdom#Formatting
The wikipedia rules seem not updated and inconsistent. Ex SR43 4AE, it should be invalid since it mentions:
"Areas with only single-digit districts: 
BL, BR, FY, HA, HD, HG, HR, HS, HX, JE, LD, SM, SR, WC, WN, ZE (although WC is always subdivided by a further letter, e.g. WC1A)
"

https://tech.marksblogg.com/uk-postcodes.html
https://github.com/simonhayward/ukpostcodeparser/blob/master/ukpostcodeparser/parser.py
https://www.mrs.org.uk/pdf/postcodeformat.pdf

https://ideal-postcodes.co.uk/guides/uk-postcode-format
https://github.com/ideal-postcodes/postcode/blob/master/lib/index.ts

