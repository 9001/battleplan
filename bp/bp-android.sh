set -e
mkdir -p ~/bp/bp-readme
cd ~/bp

src=https://ocv.me/bp/101

cat >files.list <<'EOF'
index.html
lz-string.min.js
lkrxy1.json
lkrxy2.json
EOF

#cat files.list | xargs rm || true
cat files.list | sed -r "s@^@$src/@" | wget -Ni-
(cd bp-readme && wget -N $src/bp-readme/index.html)

while true; do
    echo
    read -u1 -n1 -rp 'download pictures (226 MiB)? y/n: ' r
    echo
    case $r in
        [Yy]* ) pics=1; break;;
        [Nn]* ) pics=; break;;
    esac
done
[ $pics ] && {
    command -v zstd || pkg install -y zstd
    wget -O- $src/i.tzst | zstd -d | tar -x
}

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
