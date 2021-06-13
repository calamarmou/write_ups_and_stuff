#!/usr/bin/env python3

class MT19937() :
	# Source : https://en.wikipedia.org/wiki/Mersenne_Twister#Algorithmic_detail
	def __init__(self) :
		self.w, self.n, self.m, self.r = 32, 624, 397, 31
		self.MT = [0] * (self.n)
		self.f = 1812433253
		self.a = 0x9908B0DF
		self.u, self.d = 11, 0xFFFFFFFF
		self.s, self.b = 7, 0x9D2C5680
		self.t, self.c = 15, 0xEFC60000
		self.l = 18

		self.index = self.n + 1
		self.lower_mask = (1 << self.r) - 1
		self.upper_mask = self.w & ~self.lower_mask

	def seed_mt(self, seed) :
		self.index = self.n 
		self.MT[0] = seed
		for i in range(1, self.n - 1) :
			self.MT[i] = self.w & (self.f * (self.MT[i - 1] ^ (self.MT[i - 1] >> (self.w - 2))) + i)

	def extract_number(self) :
		if self.index >= self.n :
			if self.index > self.n :
				print("Generator was never seeded")
				exit()
			self.twist()

		self.y = self.MT[self.index]
		self.y ^= ((self.y >> self.u) & self.d)
		self.y ^= ((self.y << self.s) & self.b)
		self.y ^= ((self.y << self.t) & self.c)
		self.y ^= (self.y >> self.l)

		self.index += 1 
		return self.w & self.y

	def twist(self) :
		for i in range(self.n - 1) :
			x = (self.MT[i] & self.upper_mask) + (self.MT[(i + 1) % self.n] & self.lower_mask) 
			xA = x >> 1 
			if (x % 2) != 0 :
				xA = xA ^ a 
			self.MT[i] = self.MT[(i + self.m) % self.n] ^ xA 

		self.index = 0

if __name__ == "__main__" : 

	mt_gen = MT19937()
	mt_gen.seed_mt(5489)
	for i in range(30) :
		print(mt_gen.extract_number())