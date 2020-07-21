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
	} else if (chapter == 8 || chapter == 99) {
		if (line <= 0) {
			return -1;
		} else if (line < 101) {
			id = table[speaker][6];
			line -= 1;
		} else if (line < 401) {
			id = table[speaker][7];
			line -= 101;
		} else if (line < 601) {
			id = table[speaker][8];
			line -= 401;
		} else if (line < 801) {
			id = table[speaker][9];
			line -= 601;
		} else {
			id = table[speaker][10];
			line -= 801;
		}
	} else return -1;

	if (id == -1) return -1;
	id += line;

	if (id > 8965) return -1;
	return id;
}
