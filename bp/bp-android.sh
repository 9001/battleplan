set -e
mkdir -p ~/bp/bp-readme
cd ~/bp

src=https://ocv.me/bp/106

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
    read -u1 -n1 -rp 'download pictures (193 MiB)? y/n: ' r
    echo
    case $r in
        [Yy]* ) pics=1; break;;
        [Nn]* ) pics=; break;;
    esac
done
[ $pics ] && {
    command -v zstd || pkg install -y zstd
    rm -rf i
    wget -O- $src/i.tzst | zstd -d | tar -x
}

cat >run <<'EOF'
printf '\n\033[32m\nbattleplan is now available at:\nhttp://127.0.0.1:1616/\n\033[36m\n(long-tap the screen, select "more" » "Select URL" and then long-tap the link there)\n\033[0m\n'
cd ~/bp && python3 -m http.server 1616
EOF
chmod 755 run

{ ps | grep -E 'http.server[ ]1616$' | awk '{print $1}' | xargs kill -9
} 2>/dev/null || true 

python3 -V || pkg install -y python

cat <<'EOF'


battleplan has finished installing.
to launch bp, run this command:

    ~/bp/run

EOF
