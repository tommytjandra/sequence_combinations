import pandas as pd
import pprint
from scipy.stats import mannwhitneyu


def create_table(filename):
	df = pd.read_csv(filename,header=None)
	char_sequence = ''
	penn_id = 0
	table = dict()

	for _, row in df.iterrows():
		grade = 0
		rank = 0
		for col in range(0, len(row)):
			if col == 0:
				penn_id = row[col]
			elif col == len(row) - 2:
				grade = row[col]
			elif col == len(row) - 1:
				rank = row[col]
			elif row[col] == 0:
				char_sequence += 'Y'
			else:
				mod = (col - 1) % 5

				if mod == 0:
					char_sequence += 'C' # Canvas
				elif mod == 1:
					char_sequence += 'A' # CodioAssign
				elif mod == 2:
					char_sequence += 'L' # CodioLecture
				elif mod == 3:
					char_sequence += 'T' # OHQ
				else: # mod == 4
					char_sequence += 'G' # Piazza
	 	
		table[int(penn_id)] = (char_sequence, grade, rank)
		char_sequence = ''

	return table


def divide_sequences(table):
	piazza_rank = []
	no_piazza_rank = []

	for key in table.keys():
		seq = table[key][0]

		if 'G' in seq:
			piazza_rank.append((table[key][2]))
		else:
			no_piazza_rank.append((table[key][2]))

	return piazza_rank, no_piazza_rank


def nonparametric_test(piazza_rank, no_piazza_rank):
	stat, p = mannwhitneyu(piazza_rank, no_piazza_rank)
	print('Piazza vs No Piazza')
	print('Statistics=%.2f, p=%.5f' % (stat, p))

	alpha = 0.05
	if p > alpha:
		print('Same distribution (fail to reject H0)')
	else:
		print('Different distribution (reject H0)')


def main():
	table = create_table('hw5_reformatted_data_grades-ranked.csv')
	piazza_rank, no_piazza_rank = divide_sequences(table)
	nonparametric_test(piazza_rank, no_piazza_rank)
	

if __name__== "__main__":
	main()
