#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <assert.h>

int main(int argc, char** argv) {
	char* speakers[28] = {
		"0: Hajime",
		"1: Nagito",
		"2: Byakuya",
		"3: Gundham",
		"4: Kazuichi",
		"5: Teruteru",
		"6: Nekomaru",
		"7: Fuyuhiko",
		"8: Akane",
		"9: Chiaki",
		"10: Sonia",
		"11: Hiyoko",
		"12: Mahiru",
		"13: Mikan",
		"14: Ibuki",
		"15: Peko",
		"16: Monokuma",
		"17: Monomi",
		"18: Junko",
		"19: Mechamaru",
		"20: Makoto",
		"21: Kyoko",
		"22: Byakuya (real)",
		"23: Teruteru's mom",
		"24: Alter Ego",
		"25: Minimaru",
		"26: Monokuma & Monomi",
		"27: Narrator",
	};
	char* cats[11] = {
		"0: Chapter 1",
		"1: Chapter 2",
		"2: Chapter 3",
		"3: Chapter 4",
		"4: Chapter 5",
		"5: Chapter 6",
		"6: Chapters 8/99 (from 1)",
		"7: Chapters 8/99 (from 101)",
		"8: Chapters 8/99 (from 401)",
		"9: Chapters 8/99 (from 601)",
		"10: Chapters 8/99 (from 801)",
	};

	FILE* file = fopen(argv[1], "rb");
	fseek(file, 0x26280, SEEK_SET);
	int16_t (*table)[11] = malloc(28*11*sizeof(int16_t));
	size_t count = fread(table, 2, 28*11, file);
	assert(count == 28*11);

	for(int cat = 0; cat < 10; ++cat) {
		printf(",%s", cats[cat]);
	}
	printf("\n");

	for(int speaker = 0; speaker < 28; ++speaker) {
		printf("%s", speakers[speaker]);
		for(int category = 0; category < 10; ++category) {
			printf(",%hd", table[speaker][category]);
		}
		printf("\n");
	}
}
