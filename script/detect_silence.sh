IN=$1

ffmpeg -hide_banner -vn -i $IN -af "silencedetect=n=-35dB:d=0.1" -f null - 2>&1 | grep "silencedetect" | awk '{print $NF}'