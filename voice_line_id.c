// 0x506c50
// edi: speaker
// esi: chapter
// edx: line
int16_t voice_file_id(uint8_t speaker, uint8_t chapter, int16_t line) {
	int16_t const (*table)[28][11] = 0x7a4180; // rodata 0x26280

	if (speaker >= 28) {
		return -1;
	}

	int64_t id;
	if (chapter >= 1 && chapter <= 6) {
		chapter -= 1; // make it 0-indexed

		if (line <= 0) return -1;
		line -= 1; // this as well

		// fetch base id
		id = table[speaker][chapter];
	} else if (chapter == 8 || chapter == 63) {
		if (line <= 0) {
			return -1;
		} else if (line < 0x65) {
			id = table[speaker][6];
			line -= 1;
		} else if (line < 0x191) {
			id = table[speaker][7];
			line -= 0x65;
		} else if (line < 0x259) {
			id = table[speaker][8];
			line -= 0x191;
		} else if (line < 0x321) {
			id = table[speaker][9];
			line -= 0x259;
		} else {
			id = table[speaker][10];
			line -= 0x321;
		}
	} else return -1;

	if (id == -1) return -1;
	id += line;

	if (id > 0x2305) return -1;
	return id;
}
