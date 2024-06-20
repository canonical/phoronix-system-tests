#!/bin/sh
# FFmpeg install to demux AV1 WebM to IVF that can then be consumed by dav1d...

tar -xf ffmpeg-6.1.1.tar.xz
echo $? > ~/install-exit-status
cd ~/
/usr/bin/ffmpeg -i Stream2_AV1_HD_6.8mbps.webm -vcodec copy -an -f ivf summer_nature_1080p.ivf
/usr/bin/ffmpeg -i Stream2_AV1_4K_22.7mbps.webm -vcodec copy -an -f ivf summer_nature_4k.ivf
/usr/bin/ffmpeg -i Chimera-AV1-8bit-1920x1080-6736kbps.mp4 -vcodec copy -an -f ivf chimera_8b_1080p.ivf
/usr/bin/ffmpeg -i Chimera-AV1-10bit-1920x1080-6191kbps.mp4 -vcodec copy -an -f ivf chimera_10b_1080p.ivf
echo $? > ~/install-exit-status
cd ~
echo "#!/bin/sh
/usr/bin/dav1d \$@ --muxer null --threads \$NUM_CPU_CORES --filmgrain 0 > \$LOG_FILE 2>&1
echo \$? > ~/test-exit-status" > dav1d
chmod +x dav1d
