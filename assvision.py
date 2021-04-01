
"""
    Title:   ASS Video Generator
    File:    assvision.py (py3)
    Author:  9volt
    Created: 2021-03-19
    Updated: 2021-04-01
    Version: 0.1
"""

from PIL import Image
import os

def load():
    # Get user input
    print("Parameter input: Leave blank for (default_value).")
    i_out_filename = input("Output filename (output.ass): ")
    i_framerate    = input("Framerate (4): ")
    i_frame_width  = input("Frame width (426): ")
    i_frame_height = input("Frame height (240): ")
    i_sample_rate  = input("Sample rate (2): ")
    i_src_dir      = input("Relative frame source directory (frames): ")
    i_restrictor   = input("Restriction (0): ")
    i_styles       = input("Additional Styles () : ")
    i_lines        = input("Additional lines (be careful with encoding!) (): ")

    # Sanitize to defaults
    if i_out_filename == "":    i_out_filename  = "output.ass"
    if i_src_dir      == "":    i_src_dir       = "frames"
    i_restrictor       = -1  if i_restrictor   == "" else int(i_restrictor)
    i_sample_rate      = 2   if i_sample_rate  == "" else int(i_sample_rate)
    i_framerate        = 4   if i_framerate    == "" else int(i_framerate)
    i_frame_width      = 426 if i_frame_width  == "" else int(i_frame_width)
    i_frame_height     = 240 if i_frame_height == "" else int(i_frame_height)
    
    # Load
    scale_factor = 1.1875
    out_file = open(i_out_filename, "a")       # Create file
    write_header(out_file, i_styles, i_lines)  # Write ASS header
    size = i_sample_rate * scale_factor        # vector size

    run(out_file, i_src_dir, i_sample_rate, i_framerate, size, 
        i_frame_width, i_frame_height, i_restrictor, os.listdir(i_src_dir), scale_factor)


def run(out_file, src_dir, sample_rate, framerate, size, 
        width, height, restrictor, filelist, scale_factor):
    ms_counter = 0.00
    ms_per_frame = 1.0 / framerate * 1000

    for filename in filelist: # for each file
        if restrictor == 0: break
        restrictor -= 1
        print(f'Reading {src_dir}/{filename}...')
        img = Image.open(f'{src_dir}/{filename}')
        pix = img.load()

        start_t = convert_ms(ms_counter)  # Each frame lasts ms_per_frame
        ms_counter += ms_per_frame
        end_t = convert_ms(ms_counter)

        for y in range(1, height, sample_rate):  # every [SIZE] pixel to be more efficient. Squares are [SIXE]x[SIZE] to compensate. (+ scale factor)    
            out_file.write(
                f"Dialogue: 0,{int(start_t[0])}:{int(start_t[1])}:{start_t[2]}," +  # Start timestamp
                f"{int(end_t[0])}:{int(end_t[1])}:{end_t[2]}," +                    # End timestamp
                "IMAGE_GEN,,0,0,0,,{"                                               # Style (static)
                f"\\pos(0,{y * scale_factor})"                                      # position
                "}"
            )        
            current_line = ""
            for x in range(1, width, sample_rate):
                rgb_color = pix[x, y]
                hex_color = "&H{0:02x}{1:02x}{2:02x}&".format(rgb_color[2], rgb_color[1], rgb_color[0])
                
                current_line += (
                    "{"
                    f"\\c{hex_color}\\p1"                   # Color
                    "}m 0 0 l "+
                    f"0 0 0 {size} {size} {size} {size} 0"  # Vector square
                    "{\p0}"
                )
            current_line += '\n'
            out_file.write(current_line)

    print("Done!")

def convert_ms(milliseconds): 
	seconds, milliseconds = divmod(milliseconds,1000) 
	minutes, seconds = divmod(seconds, 60) 
	hours, minutes = divmod(minutes, 60) 
	seconds = seconds + milliseconds/1000 
	return hours, minutes, seconds


def write_header(out_file, styles, lines):
    additional_styles = (open(styles, "r", encoding='utf-8-sig', errors="ignore")).read() + '\n' if styles != "" else ""
    additional_lines  = (open(lines, "r", encoding='utf-8-sig', errors="ignore")).read()  + '\n' if lines  != "" else ""

    out_file.write(
        "[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, " # no \n, continues on next line
        "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
        "Style: IMAGE_GEN,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,10,10,10,1\n"
    )
    out_file.write(additional_styles)
    out_file.write(
        "[Events]\n"
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
        "Dialogue: 0,0:00:00.00,0:00:05.00,Default,,0,test2.assss0,0,,\n"
    )
    out_file.write(additional_lines)

print("ASSVISION ASS Subtitle Video Generator 0.1")
print("By 9volt")
print()

load()
