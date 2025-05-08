import fitz 

filename = 'Term 1 - Lecture 1'
doc = fitz.open(filename+'.pdf')
out = open(filename, "wb") 
content = ''
for page in doc: 
	text = page.get_text().encode("utf8") 
	content += page.get_text()
	out.write(text) 
	out.write(bytes((12,))) 
print(content)   
out.close()
