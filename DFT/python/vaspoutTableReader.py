import pandas as pd

filename = 'testFile.txt'

df = pd.read_csv(filename, \
		names = ['MxForce','Drift','Press','TOTEN','Filename'], \
		delimiter = "\t",skiprows = 1)

with open('texOutput.tex','w') as tex_file:
	tex_file.write(str(df['Press']))

print df