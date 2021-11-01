import pandas as pd
import pprint
import collections


def create_table(filename):
	df = pd.read_csv(filename, skiprows=0)
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


def compute_avg_grades(buckets):
	avg_grades = {}

	for key in buckets.keys():
		running_total = 0
		count = 0

		for tup in buckets[key]:
			running_total += tup[1]
			count += 1

		if count > 0:
			avg_grades[key] = round(running_total / count, 2)

	print('\n***** AVG GRADES *****\n')
	pprint.pprint(avg_grades)


def compute_avg_rank(buckets):
	avg_rank = {}

	for key in buckets.keys():
		running_total = 0
		count = 0

		for tup in buckets[key]:
			running_total += tup[2]
			count += 1

		if count > 0:
			avg_rank[key] = round(running_total / count, 2)

	# print('\n***** AVG RANK *****\n')
	# pprint.pprint(avg_rank)

	sorted_rank = sorted(avg_rank.items(), key=lambda item: item[1])
	sorted_rank_dict = collections.OrderedDict(sorted_rank)
	print('\n***** AVG RANK - SORTED *****\n')
	pprint.pprint(sorted_rank_dict)


def remove_duplicates(input_str):
	return "".join(set(input_str))


def sort_string(input_str):
	sorted_chars = sorted(input_str)
	result = ''.join(sorted_chars)

	return result


def group_sequences(combinations, table):
	buckets = dict()
	students_grouped = set()

	for substr in combinations:
		buckets[substr] = []
		for key in table.keys():
			seq = table[key][0]
			seq_nd = remove_duplicates(seq)
			sorted_seq = sort_string(seq_nd)

			if len(substr) == 2 and substr[1] == 'Y':
				if substr in sorted_seq and len(sorted_seq) == 2:
					buckets[substr].append((seq, table[key][1], table[key][2], key))
					students_grouped.add(key)
			elif substr in sorted_seq:
				buckets[substr].append((seq, table[key][1], table[key][2], key))
				students_grouped.add(key)

	pprint.pprint(buckets)
	compute_avg_grades(buckets)
	compute_avg_rank(buckets)
	print_legend()
	print('\nnum students grouped: ' + str(len(students_grouped)))
	print('total num buckets: ' + str(len(combinations)))
	find_empty_buckets(buckets)


def get_all_combinations(filename):
	df = pd.read_csv(filename,header=None)

	combinations = []

	for _, row in df.iterrows():
		strlen = len(row[0])
		if strlen >= 2 and row[0][strlen - 1] != 'Y':
			continue
		combinations.append(str(row[0]))

	return combinations


def find_empty_buckets(buckets):
	empty_buckets = []

	for combo in buckets.keys():
		if not buckets[combo]:
			empty_buckets.append(combo)

	buckets_filled = len(buckets) - len(empty_buckets)
	print('num buckets filled: ' + str(buckets_filled))
	print('empty buckets: ')
	print(empty_buckets)


def print_legend():
	print('\n***** LEGEND *****\n')
	print('A: CodioAssign')
	print('C: Canvas')
	print('G: Piazza')
	print('L: CodioLecture')
	print('T: OHQ')
	print('Y: No platforms used')


def main():
	table = create_table('hw7_grades-ranked.csv')
	combos = get_all_combinations('combos_ACGLTY.csv')
	group_sequences(combos, table)
	

if __name__== "__main__":
	main()

