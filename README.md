# tab-generator

I'll try to write a python program to take an audio file and transcribe it to tabs.

Notes:
I used librosa to write an audio retriever and processor, that takes an audio file, divides it into chunks and processes each chunk to get the main notes and their frequencies.

From these frequencies, I'll use an algorithm to get the midi notes, using the formula:

```
12 * log2 (f / 440) + 49
```

where f is the frequency of the note.
440 is the frequency of the A4 note.
49 is the midi note of the A4 note.
