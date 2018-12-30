import numpy as np
#import matplotlib.pyplot as plt
#from scipy.optimize import curve_fit
#import matplotlib.gridspec as gridspec
import sys
#sys.path.append("/Users/Mmac/Documents/toba")
#import auxfunc as afn
import random
import copy
import time
import argparse


##================
##variables
#N_try = 100
##----------------

def print_tehai(tehai, N_pai=14):
	lst_manzu_uni = np.array([['11',b'\\u4e00'],['12',b'\\u4e8c'],['13',b'\\u4e09'],['14',b'\\u56db'],\
	['15',b'\\u4e94'],['16',b'\\u516d'],['17',b'\\u4e03'],['18',b'\\u516b'],['19',b'\\u4e5d']])
	lst_souzu_uni = np.array([['21',b'\\uff11'],['22',b'\\uff12'],['23',b'\\uff13'],['24',b'\\uff14'],\
	['25',b'\\uff15'],['26',b'\\uff16'],['27',b'\\uff17'],['28',b'\\uff18'],['29',b'\\uff19']])
	lst_pinzu_uni = np.array([['31',b'\\u2460 '],['32',b'\\u2461 '],['33',b'\\u2462 '],['34',b'\\u2463 '],\
	['35',b'\\u2464 '],['36',b'\\u2465 '],['37',b'\\u2466 '],['38',b'\\u2467 '],['39',b'\\u2468 ']])
	lst_zihai_uni = np.array([['41',b'\\u6771'],['42',b'\\u5357'],['43',b'\\u897f'],['44',b'\\u5317'],\
	['45',b'\\u767d'],['46',b'\\u767c'],['47',b'\\u4e2d']])
	lst_uni = np.vstack((lst_manzu_uni,lst_souzu_uni,lst_pinzu_uni,lst_zihai_uni))
	str = [lst_uni[i,1].decode('unicode-escape') for pai in tehai for i in range(len(lst_uni)) if (pai == lst_uni[i,0])]
	if N_pai==14:
		print str[0],str[1],str[2],str[3],str[4],str[5],str[6],str[7],str[8],str[9],str[10],str[11],str[12],str[13]
	else:
		for i in range(N_pai):
			print(str[i])
	return 1

def deal_haipai():
	lst_pai_all = np.hstack((lst_pai,lst_pai,lst_pai,lst_pai))
	#random.seed(0)
	return sorted(random.sample(lst_pai_all, 14))

def deal_chinitsu():
	lst_chinitsu_all = lst_manzu*4
	return sorted(random.sample(lst_chinitsu_all, 14))

def deal_honitsu():
	lst_honitsu = np.hstack((lst_manzu,lst_zihai))
	lst_honitsu_all = np.hstack((lst_honitsu,lst_honitsu,lst_honitsu,lst_honitsu))
	return sorted(random.sample(lst_honitsu_all, 14))

def deal_sanma():
	lst_sanma = np.hstack((['11','19'],lst_souzu,lst_pinzu,lst_zihai))
	lst_sanma_all = np.hstack((lst_sanma,lst_sanma,lst_sanma,lst_sanma))
	return sorted(random.sample(lst_sanma_all, 14))

def is_kokushi(tehai):
	thirteen_men = ['11','19','21','29','31','39','41','42','43','44','45','46','47']
	return (sorted(list(set(tehai))) == thirteen_men)

def is_chitoi(tehai):
	toitsu = []
	for i in range(7):
		if (tehai[2*i]==tehai[2*i+1])&(tehai[2*i] not in toitsu):
			toitsu.append(tehai[2*i])
		else:
			return False
	return True

def tehai2cnt(tehai):
	lst_cnt = [tehai.count(lst_pai[i]) for i in range(len(lst_pai))]
	cnt_manzu = [0]+lst_cnt[0:9]+[0]
	cnt_souzu = [0]+lst_cnt[9:18]+[0]
	cnt_pinzu = [0]+lst_cnt[18:27]+[0]
	cnt_zihai = [0]+lst_cnt[27:36]+[0]
	return cnt_manzu, cnt_souzu, cnt_pinzu, cnt_zihai

def is_mentsu_suhai(cnt):
	if not any(cnt):
		return True
	for i in range(1,10):
		if cnt[i]>=3:
			new_cnt = copy.deepcopy(cnt)
			new_cnt[i] -= 3
			if is_mentsu_suhai(new_cnt):
				return True
		if cnt[i-1]*cnt[i]*cnt[i+1]>=1:
			new_cnt = copy.deepcopy(cnt)
			new_cnt[i-1] -= 1
			new_cnt[i] -= 1
			new_cnt[i+1] -= 1
			if is_mentsu_suhai(new_cnt):
				return True
	return False

#def is_mentsu_zihai(cnt):
#	num_mentsu = sum(cnt)//3
#	if set(cnt)==set([3]*num_mentsu+[0]*(9-num_mentsu)):
#		return True
#	return False

def is_mentsu_zihai(cnt):
	if not any(cnt):
		return True
	for i in range(1,8):
		if cnt[i]==3:
			new_cnt = copy.deepcopy(cnt)
			new_cnt[i] -= 3
			if is_mentsu_zihai(new_cnt):
				return True
	return False

def is_mentsu_head_suhai(cnt):
	if sum(cnt)%3 == 0:
		return is_mentsu_suhai(cnt)
	elif sum(cnt)%3 == 2:
		for i in range(1,10):
			if cnt[i]>=2:
				new_cnt = copy.deepcopy(cnt)
				new_cnt[i] -= 2
				if is_mentsu_suhai(new_cnt):
					return True
	else:
		return False

#def is_mentsu_head_zihai(cnt):
#	num_mentsu = sum(cnt)//3
#	if (set(cnt)==set([3]*num_mentsu+[0]*(11-num_mentsu)))or(set(cnt)==set([3]*num_mentsu+[0]*(10-num_mentsu)+[2])):
#		return True
#	return False

def is_mentsu_head_zihai(cnt):
	if sum(cnt)%3 == 0:
		return is_mentsu_zihai(cnt)
	elif sum(cnt)%3 == 2:
		for i in range(1,8):
			if cnt[i]==2:
				new_cnt = copy.deepcopy(cnt)
				new_cnt[i] -= 2
				if is_mentsu_zihai(new_cnt):
					return True
	else:
		return False	

def cnt2mod3(cnt):
	lst_multi = np.array([0,1,2,0,1,2,0,1,2,0,0])
	return sum(np.array(cnt)*lst_multi)%3

def is_mentsu_houla(tehai):
	cnt_manzu, cnt_souzu, cnt_pinzu, cnt_zihai = tehai2cnt(tehai)
	if set([sum(cnt_manzu)%3,sum(cnt_souzu)%3,sum(cnt_pinzu)%3,sum(cnt_zihai)%3])!=set([0,0,0,2]):
		return False
	#if set([cnt2mod3(cnt_manzu),cnt2mod3(cnt_souzu),cnt2mod3(cnt_pinzu)]) not in [set([0,0,0]),set([0,0,1]),set([0,0,2])]:
	#	return False
	if all([is_mentsu_head_suhai(cnt_manzu),is_mentsu_head_suhai(cnt_souzu),is_mentsu_head_suhai(cnt_pinzu),is_mentsu_head_zihai(cnt_zihai)]):
		return True
	return False


##================
lst_manzu = ['11','12','13','14','15','16','17','18','19']
lst_souzu = ['21','22','23','24','25','26','27','28','29']
lst_pinzu = ['31','32','33','34','35','36','37','38','39']
lst_zihai = ['41','42','43','44','45','46','47']
lst_pai = np.hstack((lst_manzu,lst_souzu,lst_pinzu,lst_zihai))
##----------------


#tehai = deal_haipai()
#tehai_kokushi = ['11','19','21','29','31','31','39','41','42','43','44','45','46','47']
#tehai_chitoi = ['11','11','21','21','33','33','34','34','42','42','43','43','47','47']


def main():
	time_start = time.time()
	parser = argparse.ArgumentParser()
	parser.add_argument('--ntry', type=int, default=100)
	parser.add_argument('--write',action='store_true')
	args = parser.parse_args()
	N_try = args.ntry
	fname = "./result_tenhou_prob.txt"
	past_result = np.loadtxt(fname, skiprows=1)
	cnt_houla = 0
	i = 0
	while i < N_try:
		i += 1
		tehai = deal_haipai()
		#tehai = deal_chinitsu()
		#tehai = deal_honitsu()
		#tehai = deal_sanma()
		if is_kokushi(tehai):
			#print("kokushi")
			print_tehai(tehai)
			cnt_houla += 1
		elif is_chitoi(tehai):
			#print("chitoi")
			print_tehai(tehai)
			cnt_houla += 1
		elif is_mentsu_houla(tehai):
			#print("mentsu")
			print_tehai(tehai)
			cnt_houla += 1
		else:
			#print_tehai(tehai)
			continue
	print("RESULT_this")
	print(b'\u548c\u4e86'.decode('unicode-escape'))
	print(cnt_houla, "out of", N_try)
	print("PROB =", float(cnt_houla)/N_try)
	print("RESULT_ever")
	cnt_houla_ever = cnt_houla+int(past_result[0])
	N_try_ever = N_try+int(past_result[1])
	if args.write:
		np.savetxt(fname,[[cnt_houla_ever,N_try_ever]],delimiter='\t',header="##num_houla	num_try")
	print(cnt_houla_ever, "out of", N_try_ever)
	print("PROB =", float(cnt_houla_ever)/N_try_ever)
	time_finish = time.time()
	print('elapsed time =', time_finish-time_start)


if __name__ == '__main__':
	main()


##previous research (wiki): prob=3.0e-6
##RESULT: prob=2.98(17)e-6
