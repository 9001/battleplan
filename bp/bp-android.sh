set -e
mkdir -p ~/bp
cd ~/bp

cat >files.list <<'EOF'
index.html
lz-string.min.js
lkrxy1.json
lkrxy2.json
lkrxy3.json
lkrxy4.json
EOF

#cat files.list | xargs rm || true
cat files.list | sed -r 's@^@https://ocv.me/bp/101/@' | wget -Ni-

cat >run <<'EOF'
printf '\n\nbp is now available at:\nhttp://127.0.0.1:1616/\n\n(long-tap the screen, select "more" » "Select URL" and then long-tap the link there)\n\n'
cd ~/bp && python3 -m http.server 1616
EOF
chmod 755 run

{ ps | grep -E 'http.server[ ]1616$' | awk '{print $1}' | xargs kill -9
} 2>/dev/null || true 

python3 -V || pkg install -y python

cat <<'EOF'


bp has finished installing.
to launch bp, run this command:

    ~/bp/run

EOF
