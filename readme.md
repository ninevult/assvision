# ASSVISION

Generate vector Advanced SubStation Alpha (*.ass) subtitles to use as video frames.

## Usage

ASSVISION takes no command-line arguments. All parameters are entered after opening the script. The following parameters are available:

1. **Output Filename** (default: `output.ass`)
2. **Framerate** (default: `4`)
3. **Frame Width** (default: `426`)
4. **Frame Height** (default: `240`)
5. **Sample Rate** (default: `2`): Size of pixels generated. A sample rate of 2 will effectively halve the frame size. Smaller values will result in more detail at the expense of file size and amount of processing power required to load the generated file.
6. **Frame Source Directory** (default: `frames`): Relative directory to read video frames from. It is recommended that frames have an incremental filename such as `frame_%05d.png`.
7. **Restrictor** (default: `0`): Number of frames to stop processing after. A value of 0 will read all frames in the frames directory. Useful for testing.
8. **External Styles** (default: empty): Filename to add style information from. See below for an example.
9. **External Lines** (default: empty): Filename to add lines from. See below for an example.

## Requirements

1. Python 3
2. PIL

## Examples

*External Styles:* Extract the `Style:` lines from the sub file you want to add.
```
Style: Default,Corinthian Medium,17,&H00FAFAFA,&H000019FF,&H00190607,&HC40D0D0D,-1,0,0,0,100,100,0,0,1,0.833333,0.4,2,33,33,14,1
Style: Sign - Chat,Noto Sans Med,9,&H00FAFAFA,&H000019FF,&H00190607,&HC40D0D0D,0,0,0,0,100,100,0,0,1,0.355556,0.222222,2,33,33,14,1
Style: Sign - OP1 Title,Falena Heavy,18,&H00000000,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0.44375,0,1,0,0,5,0,0,0,1
```

*External Lines:* Extract the `Dialogue:` lines from the sub file you want to add. You will want to increase the Layer from the default 0 so they appear above the video lines.
```
Dialogue: 100,0:03:01.03,0:03:02.49,Default,,0,0,0,,A-Are you okay?!
Dialogue: 100,0:03:02.49,0:03:03.77,Default,,0,0,0,,Where does it hurt?
Dialogue: 100,0:03:05.19,0:03:07.24,Default,,0,0,0,,M-My ribs hurt.
Dialogue: 100,0:03:07.24,0:03:08.90,Default,,0,0,0,,I think they're broken.
Dialogue: 100,0:03:08.90,0:03:09.53,Default,,0,0,0,,A doctor should—
```

Warning: As of now, the script will break if you try to load in any fancy Unicode characters, such as kanji, triangles, music notes, etc. 